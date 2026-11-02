# Inspect feature classes, geometry, counts, CRS and fields.
import arcpy

INPUT_GDB = r"C:\GIS\Environmental_Project\Input.gdb"

if not arcpy.Exists(INPUT_GDB):
    raise FileNotFoundError(f"Geodatabase not found: {INPUT_GDB}")

arcpy.env.workspace = INPUT_GDB
feature_classes = arcpy.ListFeatureClasses() or []

if not feature_classes:
    print("No feature classes found at the geodatabase root.")

for i, fc in enumerate(feature_classes, start=1):
    desc = arcpy.Describe(fc)
    count = int(arcpy.management.GetCount(fc)[0])
    sr = desc.spatialReference
    print(f"\n{i}. {fc}")
    print(f"   Geometry: {desc.shapeType}")
    print(f"   Count: {count}")
    print(f"   CRS: {sr.name} | WKID: {sr.factoryCode}")
    print(f"   Linear unit: {getattr(sr, 'linearUnitName', 'Not applicable')}")
    for field in arcpy.ListFields(fc):
        print(f"   Field: {field.name} | {field.type}")
print("\nInspection complete.")
