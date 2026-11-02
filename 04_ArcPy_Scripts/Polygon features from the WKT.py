
import arcpy
import pandas as pd
import os

# 1. Input Excel file
excel_file = r"E:\Stantec Practical exam\Stantec_Principal_GIS_Practical_Practice.xlsx"

# 2. Output geodatabase
output_gdb = r"E:\Stantec Practical exam\Practice.gdb"

# 3. Output feature class
output_fc = os.path.join(output_gdb, "Protected_Sites")

# 4. Read Excel worksheet
df = pd.read_excel(
    excel_file,
    sheet_name="Protected_Sites"
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

# 7. Create polygon feature class
arcpy.management.CreateFeatureclass(
    output_gdb,
    "Protected_Sites",
    "POLYGON",
    spatial_reference=arcpy.SpatialReference(4326)
)

# 8. Add attribute fields
arcpy.management.AddField(output_fc, "Site_ID", "TEXT")
arcpy.management.AddField(output_fc, "Site_Type", "TEXT")
arcpy.management.AddField(output_fc, "Sensitivity", "TEXT")

# 9. Insert polygon geometry and attributes
with arcpy.da.InsertCursor(
    output_fc,
    ["SHAPE@", "Site_ID", "Site_Type", "Sensitivity"]
) as cursor:

    for _, row in df.iterrows():

        polygon = arcpy.FromWKT(
            row["WKT"],
            arcpy.SpatialReference(4326)
        )

        cursor.insertRow([
            polygon,
            row["Site_ID"],
            row["Site_Type"],
            row["Sensitivity"]
        ])

# 10. Display output
print("Polygon conversion completed!")

print("Total polygons:", arcpy.management.GetCount(output_fc)[0])

print("Output:", output_fc)
