# GIS Project Delivery, QA/QC and ArcPy Practical Portfolio

**Scenario:** Environmental constraints mapping for preliminary infrastructure planning  
**Platform:** ArcGIS Pro, ArcPy and ModelBuilder  
**Sample CRS:** WGS 1984 UTM Zone 43N (EPSG:32643)  
**Status:** Fictional demonstration project

## What this demonstrates
- GIS data QA/QC and issue tracking
- Project scoping, effort estimation and delivery planning
- Technical troubleshooting and decision logging
- ArcPy inspection, attribute checks and geometry validation
- Buffer, Merge, Dissolve, Erase, Intersect and geometry calculations

## Repository structure
- `01_QAQC/`: checklist and issue register
- `02_Project_Management/`: delivery plan and effort estimate
- `03_Technical_Documentation/`: error handling and decision log
- `04_ArcPy_Scripts/`: three commented ArcPy scripts
- `05_Examples/`: sample feature-class schema

## Recommended run order
1. Read `05_Examples/Sample_Data_Schema.md`.
2. Create a training file geodatabase and load the required feature classes.
3. Run `01_Inspect_Geodatabase.py`.
4. Run `02_QAQC_Checks.py`.
5. Review and resolve issues against source data.
6. Configure and run `03_Environmental_Constraints_Workflow.py`.
7. Validate outputs and complete the issue register before delivery.

## ArcPy setup
Run scripts using the Python environment installed with ArcGIS Pro. ArcPy is supplied with ArcGIS Pro; do not assume it can be installed with ordinary `pip`.

Update paths and feature-class names in each script. The workflow expects inputs in an approved projected CRS with metre units. It checks the CRS and does not silently assign or reproject data.

## Workflow
```text
River_Network ── Buffer 100 m ──┐
Road_Network ─── Buffer 250 m ──┼─ Merge ─ Dissolve ─ Restricted_Areas
Residential_Areas Buffer 500 m ─┘                         │
Protected_Sites ──────────────────────────────────────────┘
Project_Area ───────── Erase Restricted_Areas ─ Available_Land
Available_Land + optional Suitable_Slope_Polygon ─ Intersect
```

**Important:** Erase availability depends on ArcGIS licensing. The script checks for the tool and provides a clear message if unavailable. Review buffer assumptions and all outputs before use.
