# GIS QA/QC Checklist

**Project:** Environmental Constraints Mapping

## Source data
| Check | Method | Acceptance / action |
|---|---|---|
| Source and date | Metadata review | Traceable and current |
| Coordinate system | Layer Properties / Describe | Approved CRS |
| Geometry type | Describe | Expected point, line or polygon |
| Feature count | Get Count | Record and compare with source |
| Required fields | ListFields | Mandatory fields present |
| Null attributes | SQL / SearchCursor | Missing values investigated |
| Duplicate IDs | Find Identical / Python | Potential duplicates reviewed, not auto-deleted |
| Geometry validity | Check Geometry | Errors reviewed |
| Extent | Map inspection | Features in expected area |

## Processing and outputs
- [ ] Buffer distances, units and method confirmed.
- [ ] Dissolve setting matches analysis requirement.
- [ ] Overlay inputs and active selections checked.
- [ ] Empty outputs investigated using counts, extents and overlap.
- [ ] Area and length calculated in a suitable projected CRS.
- [ ] Slivers inspected; no arbitrary deletion threshold applied.
- [ ] Output feature counts and representative geometries checked.
- [ ] Map title, legend, scale bar, north arrow and CRS reviewed.
- [ ] PDF export opens and is legible.
- [ ] Final geodatabase, metadata and processing notes included.
- [ ] Independent technical review completed.

## Sign-off
| Stage | Role | Name / initials | Date | Status |
|---|---|---|---|---|
| Data preparation | GIS Analyst | | | |
| Spatial analysis | GIS Analyst | | | |
| Technical review | Senior GIS Analyst / GIS Lead | | | |
| Project approval | Project Manager | | | |
| Client issue | Authorised lead | | | |

**Acceptance:** Resolve critical issues or obtain formal acceptance from the authorised project lead. Preserve original source data.
