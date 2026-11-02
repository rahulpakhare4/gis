
import arcpy
import pandas as pd
import os

# ============================================================
# 1. INPUT SETTINGS
# ============================================================

excel_file = r"E:\Stantec Practical exam\Stantec_Principal_GIS_Practical_Practice.xlsx"

output_gdb = r"E:\Stantec Practical exam\Practice.gdb"

feature_name = "Rivers"
excel_sheet_name = "Rivers"

spatial_reference = 32643

# ============================================================
# 2. ATTRIBUTE FIELD SETTINGS
# ============================================================

attribute_fields = [
    "River_ID",
    "Watercourse_Name",
    "Flow_Type",
    "Sensitivity"
]

# ============================================================
# 3. OUTPUT FEATURE CLASS PATH
# ============================================================

output_fc = os.path.join(output_gdb, feature_name)

# ============================================================
# 4. READ EXCEL WORKSHEET
# ============================================================

df = pd.read_excel(
    excel_file,
    sheet_name=excel_sheet_name
)

print("Total Excel records:", len(df))

# ============================================================
# 5. VALIDATE REQUIRED EXCEL COLUMNS
# ============================================================

required_columns = ["WKT"] + attribute_fields

missing_columns = [
    field for field in required_columns
    if field not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing Excel columns: {missing_columns}"
    )

# ============================================================
# 6. CREATE GEODATABASE IF IT DOES NOT EXIST
# ============================================================

if not arcpy.Exists(output_gdb):

    arcpy.management.CreateFileGDB(
        os.path.dirname(output_gdb),
        os.path.basename(output_gdb)
    )

    print("Geodatabase created:", output_gdb)

# ============================================================
# 7. DELETE EXISTING FEATURE CLASS
# ============================================================

if arcpy.Exists(output_fc):

    arcpy.management.Delete(output_fc)

    print("Existing feature class deleted.")

# ============================================================
# 8. CREATE POLYLINE FEATURE CLASS
# ============================================================

sr = arcpy.SpatialReference(spatial_reference)

arcpy.management.CreateFeatureclass(
    out_path=output_gdb,
    out_name=feature_name,
    geometry_type="POLYLINE",
    spatial_reference=sr
)

print("Polyline feature class created.")

# ============================================================
# 9. ADD ATTRIBUTE FIELDS DYNAMICALLY
# ============================================================

field_names = attribute_fields.copy()

existing_fields = [
    field.name for field in arcpy.ListFields(output_fc)
]

for field_name in field_names:

    if field_name not in existing_fields:

        arcpy.management.AddField(
            output_fc,
            field_name,
            "TEXT"
        )

        print("Field created:", field_name)

# ============================================================
# 10. INSERT POLYLINE GEOMETRY AND ATTRIBUTES
# ============================================================

cursor_fields = ["SHAPE@"] + attribute_fields

inserted_count = 0
skipped_count = 0

with arcpy.da.InsertCursor(
    output_fc,
    cursor_fields
) as cursor:

    for index, row in df.iterrows():

        try:

            # Check missing WKT
            if pd.isna(row["WKT"]):
                skipped_count += 1
                print(f"Skipped row {index}: Missing WKT")
                continue

            # Convert WKT into polyline geometry
            polyline = arcpy.FromWKT(
                row["WKT"],
                sr
            )

            # Check empty geometry
            if polyline is None or polyline.pointCount == 0:
                skipped_count += 1
                print(f"Skipped row {index}: Empty geometry")
                continue

            # Collect attribute values dynamically
            attribute_values = [
                None if pd.isna(row[field_name])
                else str(row[field_name])
                for field_name in attribute_fields
            ]

            # Insert geometry and attributes
            cursor.insertRow(
                [polyline] + attribute_values
            )

            inserted_count += 1

        except Exception as e:

            skipped_count += 1

            print(
                f"Error processing row {index}: {e}"
            )

# ============================================================
# 11. FINAL OUTPUT AND SUMMARY
# ============================================================

total_features = int(
    arcpy.management.GetCount(output_fc)[0]
)

print("\n================================")
print("RIVER POLYLINE CONVERSION COMPLETED")
print("================================")

print("Worksheet:", excel_sheet_name)
print("Feature class:", feature_name)
print("Geometry type: POLYLINE")
print("Coordinate system:", sr.name)
print("Inserted features:", inserted_count)
print("Skipped records:", skipped_count)
print("Total river features:", total_features)
print("Output:", output_fc)

print("================================")
