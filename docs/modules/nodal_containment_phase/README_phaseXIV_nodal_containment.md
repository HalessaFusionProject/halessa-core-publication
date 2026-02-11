# Phase XIV: Nodal Cascade Containment

**Overview**
This phase defines the containment threshold for cascading nodal energy within the recursive harmonic structure.
The field stability metrics are represented as a 2D heightmap, with a 3D mesh derived from that field to preserve
recursion integrity under thermal and rotational duress.

**Files Included**
- `Q_nodal_containment_field.npy` - Numerical representation of the nodal energy shell.
- `Q_nodal_containment_preview.png` - Preview visualization of field topology.
- `QESR_nodal_containment.obj` - Phase XIV mesh geometry (generated from the field).
- `README_phaseXIV_nodal_containment.md` - This document.

**Vector Stability**
Field range remains within 0.0 to 1.0, with no NaN or Inf values detected. Gradient continuity is smooth, and edge
mean is aligned with the interior mean, indicating no boundary leakage or clipping.

**Anchor Alignment (Phase XIII)**
Phase XIII uses a 400x400 field grid while Phase XIV uses 256x256. Phase XIV was resampled to 400x400 for alignment
validation. Correlation to Phase XIII is low and negative (-0.0717), so anchor alignment is not confirmed and requires
explicit Phase XV resolution.

**Next Step**
Proceed to triangulation convergence threading for Phase XV after anchor alignment decision.
