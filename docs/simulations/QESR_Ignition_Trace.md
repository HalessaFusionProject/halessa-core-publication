# QESR Ignition Trace

This document formalizes the ignition sequence and simulation pathway for the Halessa Fusion Model,
linking the divergence threshold field, curl modulation, and ignition envelope into a canonical,
phase-by-phase trace.

---

## Reference Assets

**Ignition threshold animation**:
- `images/QESR_ignition_threshold_evolution.mp4`
- `images/QESR_ignition_threshold_evolution.gif`

**Ignition shell mesh**:
- `prototypes/Nivalis_Node_Phase_I/modules/QESR_ignition_threshold_shell.obj`

**Related docs**:
- `images/README_images_QESR_Ignition.md`
- `images/README_dynamic_visuals.md`

**Notes (source)**:
- `_notes/Simulations/Harmonic Fusion Energy Simulation (HFE).txt`
- `_notes/Simulations/Simulation Of The Halessa Fusion Energy Output Q(x, y) at t = 0.txt`
- `_notes/Simulations/‼️⛓️‍💥Dynamic Harmonic Fusion Energy Field Animation.txt`
- `_notes/Simulations/‼️⛓️‍💥time-evolving harmonic fusion energy field simulation.txt`

---

## Canonical Simulation Phases

### 1) Field Initiation

Defines the initial energy output field from charge density, rotational potential, and harmonic
feedback.

Field construction (static + time-evolving):

Q(x, y, t) = σ · ρ(x, y) · Φ(x, y) · ψ(x, y, t)

ρ(x, y) = exp(-(x² + y²) / (2 σ_ρ²))

Φ(x, y) = sin(πx) · cos(πy)

ψ(x, y, t) = cos(2πx + t) · sin(2πy + t)

σ = 0.8, σ_ρ = 0.8

---

### 2) Curl Convergence & Thread Alignment

Curl modulation establishes the harmonic corridor and prepares the field for divergence routing.

curl_t(R, θ) = exp(-R²) · sin(6θ + φ_t) · (1 + 0.4 · sin(4R - φ_t))

φ_t = 2πt / 24

This curl field is used to detect alignment corridors and seed the later ignition envelope.

---

### 3) Tunnel Compression & Divergence Threshold

Divergence pressure index (conceptual form):

D(P) = α · |∇×Q(P)| + β · |∂(∇×Q)/∂t| + κ · (1 - lock_integrity)

Routing conditions:

- Locked nodes: D(P) < T_anchor
- Compression corridor: T_anchor ≤ D(P) < T_diverge
- Divergence routed: D(P) ≥ T_diverge

Trace outputs:

- lock_integrity
- mutation_index
- divergence_index (D(P))

---

### 4) Ignition Envelope Formation

Ignition potential integrates divergence and curl intensity:

Ignition(P) = (D(P) · |curl_t|)^(0.7)

The envelope visualization is captured in:

- `images/QESR_ignition_threshold_evolution.mp4`
- `images/QESR_ignition_threshold_evolution.gif`

Optional frame index:

- `images/QESR_ignition_threshold_frames/metadata.csv`

---

### 5) Containment Shell Stabilization

The ignition threshold mesh defines the outer pressure envelope suitable for shell-based
containment or Unity emission surfaces:

- `prototypes/Nivalis_Node_Phase_I/modules/QESR_ignition_threshold_shell.obj`

Use this mesh for:

- Emission shell shading
- Collider routing for particle emitters
- Tunnel corridor alignment

---

## Variable Map

- Q(x, y, t): harmonic fusion energy output field
- D(P): divergence threshold pressure
- θ, φ: spin harmonics and phase offset
- lock_integrity: local vortex equilibrium confidence
- mutation_index: divergence-related state change

---

## Animation Callouts (High-Res)

For publication-grade dynamic visuals (1024×768):

- `images/QESR_simulation_field_evolution_fixed_1024x768.mp4`
- `images/QESR_simulation_field_evolution_fixed_1024x768.gif`
- `images/QESR_nano_lattice_sweep_1024x768.mp4`
- `images/QESR_nano_lattice_sweep_1024x768.gif`

See `images/README_dynamic_visuals.md` for frame folders and zip archives.
