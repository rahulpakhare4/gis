
import arcpy
import os

# --------------------------------------------------
# 1. INPUT SETTINGS
# --------------------------------------------------

input_gdb = r"E:\Stantec Practical exam\Practice.gdb"

# Add existing UTM projected feature classes here
input_layers = [
    "Project_OutDataset_Clip_Protected_Sites",
    "Project_OutDataset_Clip_Rivers",
    "Project_OutDataset_Clip_Land_Use"
]


arcpy.env.workspace = input_gdb

# --------------------------------------------------
# 2. PROCESS EACH LAYER
# --------------------------------------------------

for layer in input_layers:

    input_fc = os.path.join(input_gdb, layer)

    print("\n-----------------------------------")
    print("Processing:", layer)
    print("-----------------------------------")

    if not arcpy.Exists(input_fc):
        print("Layer not found. Skipping:", layer)
        continue

    # Get geometry and coordinate system
    desc = arcpy.Describe(input_fc)

    geometry_type = desc.shapeType
    spatial_ref = desc.spatialReference

    print("Geometry:", geometry_type)
    print("Coordinate System:", spatial_ref.name)

    # --------------------------------------------------
    # 3. CHECK PROJECTED COORDINATE SYSTEM
    # --------------------------------------------------

    if spatial_ref.type != "Projected":
        print("ERROR: Layer is not projected. Skipping.")
        continue

    if spatial_ref.linearUnitName.lower() not in [
        "meter", "metre", "meters", "metres"
    ]:
        print("ERROR: Coordinate system is not in metres.")
        continue

    # Get existing fields
    existing_fields = [
        field.name.lower()
        for field in arcpy.ListFields(input_fc)
    ]

    # --------------------------------------------------
    # 4. POLYGON AREA CALCULATION
    # --------------------------------------------------

    if geometry_type == "Polygon":

        # Add Area_SqM field
        if "area_sqm" not in existing_fields:
            arcpy.management.AddField(
                input_fc, "Area_SqM", "DOUBLE"
            )
            print("Area_SqM field created.")

        # Add Area_Ha field
        if "area_ha" not in existing_fields:
            arcpy.management.AddField(
                input_fc, "Area_Ha", "DOUBLE"
            )
            print("Area_Ha field created.")

        # Calculate area
        with arcpy.da.UpdateCursor(
            input_fc,
            ["SHAPE@", "Area_SqM", "Area_Ha"]
        ) as cursor:

            for row in cursor:

                if row[0] is not None and row[0].pointCount > 0:

                    area_sqm = row[0].getArea(
                        "PLANAR", "SQUAREMETERS"
                    )

                    area_ha = area_sqm / 10000

                    row[1] = area_sqm
                    row[2] = area_ha

                else:
                    row[1] = None
                    row[2] = None

                cursor.updateRow(row)

        print("Area calculation completed.")

    # --------------------------------------------------
    # 5. POLYLINE LENGTH CALCULATION
    # --------------------------------------------------

    elif geometry_type == "Polyline":

        # Add Length_M field
        if "length_m" not in existing_fields:
            arcpy.management.AddField(
                input_fc, "Length_M", "DOUBLE"
            )
            print("Length_M field created.")

        # Add Length_Km field
        if "length_km" not in existing_fields:
            arcpy.management.AddField(
                input_fc, "Length_Km", "DOUBLE"
            )
            print("Length_Km field created.")

        # Calculate length
        with arcpy.da.UpdateCursor(
            input_fc,
            ["SHAPE@", "Length_M", "Length_Km"]
        ) as cursor:

            for row in cursor:

                if row[0] is not None and row[0].pointCount > 0:

                    length_m = row[0].getLength(
                        "PLANAR", "METERS"
                    )

                    length_km = length_m / 1000

                    row[1] = length_m
                    row[2] = length_km

                else:
                    row[1] = None
                    row[2] = None

                cursor.updateRow(row)

        print("Length calculation completed.")

    else:
        print("Unsupported geometry type.")

    print("Completed:", layer)

# --------------------------------------------------
# 6. FINAL MESSAGE
# --------------------------------------------------

print("\n===================================")
print("ALL INPUT LAYERS PROCESSED")
print("===================================")
