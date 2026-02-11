# Phase VII – Corridor Convergence Slice

This module represents the harmonic corridor convergence analysis linking Phase VI (Curl Threading) to the initiation point of Phase VIII (Envelope Compression Shell). It captures the moment where tunnel-borne field vectors align toward axial ignition coherence.

## Files and Artifacts

- `Q_corridor_convergence_field.npy`  
  ⤷ Harmonic field scalar map (3D, float32)  
  _Location_: `/data/fields/`

- `Q_corridor_convergence_preview.png`  
  ⤷ Grayscale field preview for quick reference  
  _Location_: `/docs/modules/corridor_phase/`

- `QESR_corridor_convergence_mesh.obj`  
  ⤷ Extracted vector potential surface in OBJ format  
  _Location_: `/prototypes/Nivalis_Node_Phase_I/modules/`

## Purpose

- Analyze compression geometry near tunnel coherence regions
- Visualize outer-wall modulations and pressure trough locking
- Provide transitional handoff to Phase VIII: Shell Bloom Compression

## Notes

- Mesh generated from high-frequency Z-layer curl resonance
- PNG preview auto-scales from normalized ∇Q magnitude
- All values interpolated from the `Q_corridor_convergence_field` array
