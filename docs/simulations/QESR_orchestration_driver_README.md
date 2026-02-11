# QESR Orchestration Driver

This note describes the master orchestration driver that runs end-to-end generation and
visualization of each harmonic simulation phase using existing `.npy` and `.obj` assets.

Script:
- `src/QESR_orchestration_driver.py`

---

## CLI Usage

```bash
python src/QESR_orchestration_driver.py --all
python src/QESR_orchestration_driver.py --phase ignition_core --phase bloom_compression
python src/QESR_orchestration_driver.py --out results/orchestration_previews
```

---

## Phases

1) **Ignition Core**
   - `data/fields/Q_total_field_sweep.npy`
   - `data/fields/Q_output_field_trace.csv`

2) **Bloom Compression**
   - `models/PhaseII_Parametric_Bloom.obj`
   - Optional: `images/QESR_simulation_field_evolution.mp4`

3) **Ignition Threshold and Containment Shell**
   - `data/fields/Q_harmonic_feedback_map.npy`
   - `prototypes/Nivalis_Node_Phase_I/modules/QESR_ignition_threshold_shell.obj`

4) **Feedback Echo & Mesh Coupling**
   - `data/fields/Q_harmonic_feedback_map.npy`
   - `prototypes/Nivalis_Node_Phase_I/modules/QESR_corridor_mesh_link.obj`

5) **Echo Spiral Reinforcement**
   - `data/fields/Q_echo_harmonic_spiral.npy`
   - `prototypes/Nivalis_Node_Phase_I/modules/QESR_echo_spiral_reinforcement.obj`

6) **Curl Harmonic Threading**
   - `data/fields/Q_curl_threading_field.npy`
   - `prototypes/Nivalis_Node_Phase_I/modules/QESR_curl_threading_structure.obj`

---

## Outputs

- Preview plots: `results/orchestration_previews/`
- Metadata log: `results/orchestration_previews/orchestration_log.csv`

---

## Notes

- Mesh viewing is optional and attempts to use `trimesh` if installed.
- Phase outputs are logged even when assets are missing.
