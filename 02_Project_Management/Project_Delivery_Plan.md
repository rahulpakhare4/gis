# Project Delivery Plan

## Project brief
**Project:** Environmental Constraints Mapping  
**Objective:** Prepare traceable GIS datasets and constraint mapping for preliminary infrastructure route-planning support.

**Assumed inputs:** Project_Area, Protected_Sites, River_Network, Road_Network, Residential_Areas, Land_Use and optional slope data.

**Deliverables:** cleaned GIS data, constraint buffers, Restricted_Areas, Available_Land, optional suitability overlay, final file geodatabase, PDF map, QA/QC checklist and methodology notes.

## Delivery stages
| Stage | Activity | Hold point |
|---|---|---|
| 1 | Confirm scope, inputs, CRS and assumptions | Approved data inventory |
| 2 | Inspect, clean and standardise data | Data QA/QC review |
| 3 | Run buffers and overlay analysis | Processing outputs checked |
| 4 | Calculate area / length and summaries | Measurement review |
| 5 | Prepare map and metadata | Draft deliverables |
| 6 | Independent technical review | Review comments / approval |
| 7 | Resolve comments and package | Final issue package |

## Roles
| Role | Responsibility |
|---|---|
| GIS Lead | Scope, estimate, resource coordination, escalations and technical approval |
| Senior GIS Analyst | Workflow design, complex analysis review and mentoring |
| GIS Analyst | Data preparation, processing, cartography and documentation |
| Project Manager | Scope, schedule, budget, client communication and approvals |
| Discipline specialist | Confirm environmental interpretation and constraints |

## Risks and mitigation
| Risk | Impact | Mitigation |
|---|---|---|
| Incomplete source data | Rework / delay | Early inventory and query log |
| CRS mismatch | Incorrect overlay / measurement | CRS checks and approved transformations |
| Invalid geometry | Tool failure / inaccurate result | Geometry checks and controlled repair |
| Unclear constraint criteria | Incorrect interpretation | Obtain discipline lead approval |
| Late design change | Additional effort | Change control and re-estimation |
| Staff availability | Delivery delay | Resource plan and backup reviewer |

Estimate by data volume, complexity, automation, review cycles and deliverables. Include data queries, peer review, corrections and coordination, not just geoprocessing runtime.
