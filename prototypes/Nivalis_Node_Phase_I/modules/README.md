# QESR Phase Mesh Modules

This folder collects OBJ meshes generated from QESR phase field outputs. Use the registry and build pipeline to regenerate meshes from `.npy` fields as needed.

## Registry

- Mesh registry: `data/config/phase_mesh_registry.json`
- Build command: `python scripts/build_phase_meshes.py --registry data/config/phase_mesh_registry.json`

## Mesh Inventory

| Phase | Mesh | Source Field |
| --- | --- | --- |
| Phase V | `QESR_echo_spiral_reinforcement.obj` | `data/fields/Q_echo_harmonic_spiral.npy` |
| Phase VI | `QESR_curl_threading_structure.obj` | `data/fields/Q_curl_threading_field.npy` |
| Phase VII | `QESR_corridor_convergence_mesh.obj` | `data/fields/Q_corridor_convergence_field.npy` |
| Phase VIII | `QESR_compression_shell.obj` | `data/fields/Q_compression_shell_field.npy` |
| Phase IX | `QESR_foldback_retention.obj` | `data/fields/Q_foldback_resonance_field.npy` |
| Phase X | `QESR_modulation_braid.obj` | `data/fields/Q_modulation_banding_field.npy` |
| Phase XI | `QESR_ignition_threshold_shell.obj` | `data/fields/Q_ignition_weave_field.npy` |
| Phase XII | `QESR_harmonic_resonance_shell.obj` | `data/fields/Q_harmonic_resonance_field.npy` |
| Phase XIII | `QESR_confinement_lens.obj` | `data/fields/Q_confinement_lens_field.npy` |
| Phase II | `PhaseII_Parametric_Bloom.obj` | Authored mesh (no field input) |
| Phase X | `QESR_charge_braid.obj` | Authored mesh (no field input) |
| Phase VII | `QESR_corridor_mesh_link.obj` | Authored mesh (no field input) |

## Notes

- Authored meshes live alongside generated meshes; see their companion `.md` files for context.
