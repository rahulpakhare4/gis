# Demonstration workflow: buffers -> merge -> dissolve -> erase -> area.
# All inputs remain unchanged. Outputs are written to a separate geodatabase.
import arcpy
import os
import traceback

INPUT_GDB = r"C:\GIS\Environmental_Project\Input.gdb"
OUTPUT_GDB = r"C:\GIS\Environmental_Project\Output.gdb"
LOG_FOLDER = r"C:\GIS\Environmental_Project\Logs"

RIVER_BUFFER = "100 Meters"
ROAD_BUFFER = "250 Meters"
RESIDENTIAL_BUFFER = "500 Meters"
EXPECTED_WKID = 32643
SUITABLE_SLOPE_POLYGON = None  # e.g. "Suitable_Slope_Polygon"

def log(message, log_file):
    print(message)
    with open(log_file, "a", encoding="utf-8") as stream:
        stream.write(message + "\n")

def require_input(name):
    path = os.path.join(INPUT_GDB, name)
    if not arcpy.Exists(path):
        raise FileNotFoundError(f"Required input missing: {path}")
    if int(arcpy.management.GetCount(path)[0]) == 0:
        raise ValueError(f"Input has no features: {path}")
    return path

def check_crs(paths):
    for path in paths:
        sr = arcpy.Describe(path).spatialReference
        if sr.type != "Projected" or sr.factoryCode != EXPECTED_WKID:
            raise ValueError(
                f"{path}: found {sr.name} (WKID {sr.factoryCode}); "
                f"expected projected WKID {EXPECTED_WKID}. "
                "Confirm CRS and project using an approved transformation."
            )
        if "meter" not in sr.linearUnitName.lower():
            raise ValueError(f"{path} does not use metres: {sr.linearUnitName}")

def add_area_fields(fc):
    names = {f.name for f in arcpy.ListFields(fc)}
    if "Area_SqM" not in names:
        arcpy.management.AddField(fc, "Area_SqM", "DOUBLE")
    if "Area_Ha" not in names:
        arcpy.management.AddField(fc, "Area_Ha", "DOUBLE")
    arcpy.management.CalculateGeometryAttributes(
        fc, [["Area_SqM", "AREA"]], area_unit="SQUARE_METERS"
    )
    arcpy.management.CalculateField(
        fc, "Area_Ha", "!Area_SqM! / 10000.0", "PYTHON3"
    )

def main():
    os.makedirs(LOG_FOLDER, exist_ok=True)
    log_file = os.path.join(LOG_FOLDER, "workflow.log")
    arcpy.env.overwriteOutput = True

    try:
        if not arcpy.Exists(INPUT_GDB):
            raise FileNotFoundError(f"Input geodatabase not found: {INPUT_GDB}")

        project = require_input("Project_Area")
        protected = require_input("Protected_Sites")
        rivers = require_input("River_Network")
        roads = require_input("Road_Network")
        residential = require_input("Residential_Areas")
        check_crs([project, protected, rivers, roads, residential])

        out_folder = os.path.dirname(OUTPUT_GDB)
        os.makedirs(out_folder, exist_ok=True)
        if not arcpy.Exists(OUTPUT_GDB):
            arcpy.management.CreateFileGDB(out_folder, os.path.basename(OUTPUT_GDB))

        river_buf = os.path.join(OUTPUT_GDB, "River_Buffer_100m")
        road_buf = os.path.join(OUTPUT_GDB, "Road_Buffer_250m")
        res_buf = os.path.join(OUTPUT_GDB, "Residential_Buffer_500m")
        merged = os.path.join(OUTPUT_GDB, "Merged_Constraints")
        restricted = os.path.join(OUTPUT_GDB, "Restricted_Areas")
        available = os.path.join(OUTPUT_GDB, "Available_Land")

        log("1. Buffer rivers", log_file)
        arcpy.analysis.Buffer(rivers, river_buf, RIVER_BUFFER, dissolve_option="ALL")
        log("2. Buffer roads", log_file)
        arcpy.analysis.Buffer(roads, road_buf, ROAD_BUFFER, dissolve_option="ALL")
        log("3. Buffer residential areas", log_file)
        arcpy.analysis.Buffer(residential, res_buf, RESIDENTIAL_BUFFER,
                              dissolve_option="ALL")

        log("4. Merge buffers and protected sites", log_file)
        arcpy.management.Merge([river_buf, road_buf, res_buf, protected], merged)
        log("5. Dissolve merged constraints", log_file)
        arcpy.management.Dissolve(merged, restricted)

        log("6. Erase constraints from project area", log_file)
        if hasattr(arcpy.analysis, "Erase"):
            arcpy.analysis.Erase(project, restricted, available)
        elif hasattr(arcpy.analysis, "PairwiseErase"):
            log("Erase unavailable; using Pairwise Erase.", log_file)
            arcpy.analysis.PairwiseErase(project, restricted, available)
        else:
            raise RuntimeError(
                "Erase / Pairwise Erase is unavailable. Check ArcGIS Pro licensing "
                "and tool availability, or use an approved alternative."
            )

        log("7. Calculate available-land area", log_file)
        add_area_fields(available)

        if SUITABLE_SLOPE_POLYGON:
            slope = require_input(SUITABLE_SLOPE_POLYGON)
            check_crs([slope])
            suitable = os.path.join(OUTPUT_GDB, "Suitable_Land")
            log("8. Intersect available land with suitable slope", log_file)
            arcpy.analysis.Intersect([available, slope], suitable)
            add_area_fields(suitable)

        log("Output summary:", log_file)
        outputs = [river_buf, road_buf, res_buf, restricted, available]
        if SUITABLE_SLOPE_POLYGON:
            outputs.append(os.path.join(OUTPUT_GDB, "Suitable_Land"))
        for output in outputs:
            count = int(arcpy.management.GetCount(output)[0])
            sr = arcpy.Describe(output).spatialReference
            log(f"{os.path.basename(output)}: {count} feature(s); CRS={sr.name}", log_file)

        log("Workflow completed. Review and QA/QC all outputs before delivery.", log_file)

    except Exception as exc:
        log(f"ERROR: {exc}", log_file)
        log(traceback.format_exc(), log_file)
        raise

if __name__ == "__main__":
    main()
