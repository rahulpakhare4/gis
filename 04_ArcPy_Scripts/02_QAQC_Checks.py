# Report missing attributes, duplicate IDs and geometry errors.
# This script does not delete records or repair geometry.
import arcpy
import os
from collections import Counter

INPUT_GDB = r"C:\GIS\Environmental_Project\Input.gdb"
REPORT_FOLDER = r"C:\GIS\Environmental_Project\QAQC_Reports"
CHECKS = {
    "Survey_Observations": {
        "mandatory_fields": ["Site_ID", "Survey_Status", "Confidence"],
        "duplicate_id_field": "Site_ID"
    },
    "Protected_Sites": {
        "mandatory_fields": ["Site_ID"],
        "duplicate_id_field": "Site_ID"
    }
}

os.makedirs(REPORT_FOLDER, exist_ok=True)
report_path = os.path.join(REPORT_FOLDER, "qaqc_report.txt")

def write(message):
    print(message)
    with open(report_path, "a", encoding="utf-8") as log:
        log.write(message + "\n")

with open(report_path, "w", encoding="utf-8") as log:
    log.write("GIS QA/QC report\n")

for fc, config in CHECKS.items():
    path = os.path.join(INPUT_GDB, fc)
    if not arcpy.Exists(path):
        write(f"[SKIP] Dataset not found: {fc}")
        continue

    desc = arcpy.Describe(path)
    count = int(arcpy.management.GetCount(path)[0])
    write(f"\n{fc}: geometry={desc.shapeType}; count={count}")
    fields = {f.name for f in arcpy.ListFields(path)}

    for field_name in config["mandatory_fields"]:
        if field_name not in fields:
            write(f"[WARNING] Required field missing: {field_name}")
            continue
        missing = 0
        with arcpy.da.SearchCursor(path, [field_name]) as rows:
            for (value,) in rows:
                if value is None or (isinstance(value, str) and not value.strip()):
                    missing += 1
        write(f"[ATTRIBUTE] {field_name}: {missing} null/blank value(s)")

    id_field = config.get("duplicate_id_field")
    if id_field and id_field in fields:
        values = []
        with arcpy.da.SearchCursor(path, [id_field]) as rows:
            for (value,) in rows:
                if value not in (None, ""):
                    values.append(value)
        duplicates = [v for v, n in Counter(values).items() if n > 1]
        write(f"[DUPLICATES] {id_field}: {len(duplicates)} repeated value(s)")
        for value in duplicates:
            write(f"   Review: {value}")

    geometry_table = os.path.join(REPORT_FOLDER, f"{fc}_geometry_errors.dbf")
    try:
        arcpy.management.CheckGeometry(path, geometry_table)
        error_count = int(arcpy.management.GetCount(geometry_table)[0])
        write(f"[GEOMETRY] CheckGeometry errors: {error_count}")
        write(f"   Review table: {geometry_table}")
    except arcpy.ExecuteError:
        write(f"[WARNING] CheckGeometry failed: {arcpy.GetMessages(2)}")

print(f"\nReport saved: {report_path}")
