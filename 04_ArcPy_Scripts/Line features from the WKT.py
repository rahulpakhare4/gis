
import arcpy
import pandas as pd
import os

# 1. Input Excel file
excel_file = r"E:\Stantec Practical exam\Stantec_Principal_GIS_Practical_Practice.xlsx"

# 2. Output geodatabase
output_gdb = r"E:\Stantec Practical exam\Practice.gdb"

# 3. Output feature class
output_fc = os.path.join(output_gdb, "Rivers")

# 4. Read Excel worksheet
df = pd.read_excel(
    excel_file,
    sheet_name="Rivers"
)

# 5. Check whether geodatabase exists
if not arcpy.Exists(output_gdb):
    arcpy.management.CreateFileGDB(
        os.path.dirname(output_gdb),
        os.path.basename(output_gdb)
    )

# 6. Delete existing output if present
if arcpy.Exists(output_fc):
    arcpy.management.Delete(output_fc)

# 7. Create Polyline feature class
arcpy.management.CreateFeatureclass(
    output_gdb,
    "Rivers",
    "POLYLINE",
    spatial_reference=arcpy.SpatialReference(4326)
)

# 8. Add attribute fields
arcpy.management.AddField(output_fc, "River_ID", "TEXT")
arcpy.management.AddField(output_fc, "Watercourse_Name", "TEXT")
arcpy.management.AddField(output_fc, "Flow_Type", "TEXT")
arcpy.management.AddField(output_fc, "Sensitivity", "TEXT")

# 9. Insert line geometry and attributes
with arcpy.da.InsertCursor(
    output_fc,
    ["SHAPE@", "River_ID", "Watercourse_Name",
     "Flow_Type", "Sensitivity"]
) as cursor:

    for _, row in df.iterrows():

        polyline = arcpy.FromWKT(
            row["WKT"],
            arcpy.SpatialReference(4326)
        )

        cursor.insertRow([
            polyline,
            row["River_ID"],
            row["Watercourse_Name"],
            row["Flow_Type"],
            row["Sensitivity"]
        ])

# 10. Display output
print("River Polyline conversion completed!")

print("Total river features:",
      arcpy.management.GetCount(output_fc)[0])

print("Output:", output_fc)
