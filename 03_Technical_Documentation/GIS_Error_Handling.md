# GIS Error Handling and Technical Decisions

## Troubleshooting sequence
1. Read the full geoprocessing error.
2. Confirm input datasets exist and contain features.
3. Check geometry, CRS and spatial extent.
4. Check fields, nulls, schema locks and selections.
5. Review parameters, units, environments and output path.
6. Check licensing and tool availability.
7. Isolate the issue with a small test where practical.
8. Correct the root cause, rerun and validate.
9. Record issue, decision, action and result.

## Examples
### Incorrect area
**Cause:** Planar area calculated in a geographic CRS or wrong units.  
**Action:** Confirm measurement method; use an appropriate projected CRS where required; recalculate.  
**Validation:** Check linear units and sample polygons. Convert m² to hectares by dividing by 10,000.

### Empty Intersect
**Cause:** Inputs do not overlap, wrong layers, active selections or inconsistent spatial locations.  
**Action:** Check counts, extents, selections, CRS and actual spatial relationship.  
**Validation:** Confirm overlap visually and compare output count with expectation.

### Topology errors
**Cause:** Overlap, gap, dangle, self-intersection or pseudo-node.  
**Action:** Review Error Inspector and source data. Correct genuine errors only. A dead-end road or natural river endpoint may be valid. Revalidate.

### Buffer failure
**Cause:** Invalid geometry, invalid distance syntax, output path, lock or licensing issue.  
**Action:** Check geometry, distance and units, workspace and tool availability. Inspect output extent and count.

### Publishing failure
**Cause:** Unsupported fields, service definition, permissions, server connectivity or publishing privileges.  
**Action:** Review ArcGIS Pro messages, analyse map, check schema and sharing permissions. Test the published service.

## Technical decision principles
- Preserve original source data.
- Use a CRS and measurement method appropriate to the task.
- Record assumptions, distances and processing parameters.
- Do not delete suspected duplicates without verification.
- Do not treat every topology error as a real-world defect.
- Keep workflows repeatable and outputs traceable.
- Escalate decisions affecting environmental interpretation or client commitments.
