# Sample Data Schema

| Feature class | Geometry | Suggested fields |
|---|---|---|
| Project_Area | Polygon | Project_ID (Text), Project_Name (Text) |
| Protected_Sites | Polygon | Site_ID (Text), Site_Name (Text), Sensitivity (Text) |
| River_Network | Polyline | River_ID (Text), River_Name (Text) |
| Road_Network | Polyline | Road_ID (Text), Road_Class (Text) |
| Residential_Areas | Polygon | Area_ID (Text), Area_Name (Text) |
| Survey_Observations | Point | Site_ID (Text), Survey_Status (Text), Confidence (Text), Survey_Date (Date) |
| Suitable_Slope_Polygon | Polygon | Slope_Class (Text), Suitability (Short Integer) |

## Coordinate system
The sample script expects WGS 1984 UTM Zone 43N (EPSG:32643), with metres as linear units. This is only an example CRS. Confirm the correct project CRS for real work.

## Suggested synthetic QA/QC test cases
- One observation with missing Confidence.
- Two records with repeated Site_ID values.
- Two polygons with a small overlap.
- One line with a dangling endpoint.
- One feature class with an intentionally incorrect CRS.

Use a separate training geodatabase and preserve a clean copy of source data.
