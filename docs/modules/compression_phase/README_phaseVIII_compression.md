
# Phase VIII – Compression Shell Envelope

This phase defines the outer containment structure for the QESR harmonic ignition zone. The compression shell balances radial bloom pressure with axial convergence harmonics. This boundary phase is critical for maintaining phase integrity across curl and tunnel-thread transitions.

## Artifacts

- `Q_compression_shell_field.npy`  
  ⤷ Scalar pressure modulation map for envelope shaping  
  _Location_: `/data/fields/`

- `Q_compression_shell_preview.png`  
  ⤷ Visual density modulation map  
  _Location_: `/docs/modules/compression_phase/`

- `QESR_compression_shell.obj`  
  ⤷ Polygonal surface mesh representing shell enclosure  
  _Location_: `/prototypes/Nivalis_Node_Phase_I/modules/`

## Purpose

- Provide harmonic field limits during peak ignition  
- Modulate pressure gradients around convergence path  
- Serve as outermost coherence envelope before ignition sustain

## Notes

- Generated from peak compression potential zones across Z-layer sweep  
- Mesh is optimized for low-poly surface preview and Unity injection  
- Phase IX will continue from this boundary via symmetry-phase curl foldback
