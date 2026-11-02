# ArcPy scripts: setup and run order

Run these scripts using the Python environment installed with ArcGIS Pro. ArcPy is supplied with ArcGIS Pro; do not assume ordinary `pip install arcpy` is supported.

Update paths and feature-class names in each script. Use a separate output geodatabase. Inputs must use the approved projected CRS with metre units for this sample workflow.

## Expected feature classes
| Name | Geometry | Use |
|---|---|---|
| Project_Area | Polygon | Available land |
| Protected_Sites | Polygon | Restricted areas |
| River_Network | Polyline | 100 m buffer |
| Road_Network | Polyline | 250 m buffer |
| Residential_Areas | Polygon | 500 m buffer |
| Survey_Observations | Point | QA/QC example |
| Suitable_Slope_Polygon | Polygon | Optional suitability overlay |

Run in order: inspect geodatabase, run QA/QC checks, then run the environmental workflow.

`CheckGeometry` reports errors; it does not repair them. The QA/QC script flags duplicates but does not delete records. The workflow checks the expected WKID. Erase availability depends on licensing; the script checks for Erase / Pairwise Erase and stops if neither is available. Confirm buffer distances and analysis assumptions before real use.
