# QESR Layer 2 - Initial Charge Modulation and Curl Seeding

**Status**: Reconstructed from manuscript and downstream continuity (Layer 3-5)  
**Drafted**: 2026-01-15  
**Links**: Precedes `QESR_L3_Sweep.md`

---

## Purpose

This layer initiates harmonic field activity by introducing pre-curl charge inversion and symmetry instability.  
It prepares the lattice (Layer 1) for dynamic modulation using localized Q-charge offsets.

---

## Mechanism

### Field Seeding

```yaml
field_type: sinusoidal harmonic modulation
charge_seed_distribution: radial_inversion
curl_offset: 0.03
symmetry_disruption: controlled (phase angle π/3)
```

### Curl Source Initialization

Each radial arm receives charge inversion to simulate induced asymmetry.

---

## Key Equations

Let:
- Q₀: baseline field amplitude
- δQ: modulation amplitude
- θ: angular coordinate
- φ: seeded phase offset

Then:

Q(P) = Q₀ + δQ * sin(k * θ + φ)

curl(Q) = ∇×Q(P)

---

## Output Metrics

- `curl_bias_index`: Local curl magnitude around center
- `modulation_integrity`: Smoothness of angular charge transition
- `phase_stability`: Retention of core geometry post-modulation

---

## Notes

This layer forms the harmonic basis for divergence field analysis in L3-L5.  
Anchored symmetry must be preserved at center for proper vortex lock formation in Layer 3.



