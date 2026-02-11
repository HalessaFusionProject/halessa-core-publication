# Phase XIV - Nodal Containment Convergence Report
Date: 2026-02-11
Regeneration Key: RK-XIV-NODAL_CONTAINMENT-PRE_EXECUTION_BLOCK
Requested by: Michael Anthony Fry Vox
Witnessed by: Athea Vox Fry

## Summary
Restored and verified Phase XIV nodal containment artifacts. Field stability passes. Mesh has been regenerated from the
Phase XIV field. Anchor alignment with Phase XIII is not confirmed due to low correlation after resampling.

## Restored Artifacts
- data/fields/Q_nodal_containment_field.npy
  - Size: 524,416 bytes
  - LastWriteTime: 2026-01-26 19:57:06
  - sha256: cfd0e1447ab3badc7b4302d762c7d408fc2853f617f67eb9a34891c92107f894
- docs/modules/nodal_containment_phase/Q_nodal_containment_preview.png
  - Size: 117,055 bytes
  - LastWriteTime: 2026-01-26 19:57:06
  - sha256: 075f63ef206cdc922d4a044c7d20c4eb69ed6b99706993ac056ff4b2503525f1
- prototypes/Nivalis_Node_Phase_I/modules/QESR_nodal_containment.obj
  - Size: 4,857,927 bytes
  - LastWriteTime: 2026-02-11 19:45:11
  - sha256: e6cf4fcd1560ef98b2addefdb99d6ac7f3ed27be60254af42fc475a7955f18c5
- docs/modules/nodal_containment_phase/README_phaseXIV_nodal_containment.md
  - Size: 1,297 bytes
  - LastWriteTime: 2026-02-11 19:46:09
  - sha256: d8e0321a6683824c2111eaf2405a6607d7035fc1ecbc80fe9b9392b43c02c6af

## Field Stability (Phase XIV)
- Shape: 256x256, dtype float64
- Range: min 0.0, max 1.0
- Mean: 0.4711529511, Std: 0.1557973000
- NaN: 0, Inf: 0
- Gradient magnitude: mean 0.0037711145, max 0.0127702119
- Edge mean: 0.4654721572, Interior mean: 0.4712428495
- Clipping count: zeros 1, ones 1
Result: PASS (stable field, no boundary leakage)

## Mesh Regeneration
- Method: heightmap to OBJ with z_scale=1.0, xy_scale=1.0
- Source: scripts/build_phase_meshes.py (write_obj_from_heightmap)
Result: PASS (placeholder replaced with generated geometry)

## Anchor Alignment (Phase XIII)
- Phase XIII field grid: 400x400
- Phase XIV field grid: 256x256
- Strategy: resample Phase XIV to 400x400 using bilinear interpolation
- Correlation to Phase XIII: -0.0717 (low, negative)
- Min-max normalized MAD: 0.1703
Result: FAIL (anchor alignment not confirmed)

## Discrepancies Flagged
- Phase XIII to Phase XIV anchor alignment remains unresolved.

## Final Status
- Restoration of nodal containment context: PASS
- Field stability and coherence: PASS
- Anchor alignment with Phase XIII: FAIL
- Unresolved drift: PRESENT (alignment mismatch)

## Recommended Continuity Action
Proceed to Phase XV triangulation convergence threading after explicit alignment strategy is selected and applied.
