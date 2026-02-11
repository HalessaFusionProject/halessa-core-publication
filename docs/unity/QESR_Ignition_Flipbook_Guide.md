# QESR Ignition Flipbook Integration (Unity)

## Inputs

- Atlas: `images/QESR_ignition_threshold_atlas.png`
- Columns: 6
- Rows: 4
- Frames: 24
- FrameRate: 12 fps

## Shader Graph (URP/HDRP) Setup

1) Create a new Shader Graph (Unlit or Lit).
2) Add properties:
   - _AtlasTex (Texture2D)
   - _Columns (Float) = 6
   - _Rows (Float) = 4
   - _FrameRate (Float) = 12
3) Compute totalFrames = _Columns * _Rows.
4) Compute frameIndex:
   - frame = floor(frac(_Time.y * _FrameRate / totalFrames) * totalFrames)
5) Derive UV offsets:
   - col = fmod(frame, _Columns)
   - row = floor(frame / _Columns)
   - uv = (UV / float2(_Columns, _Rows)) + float2(col / _Columns, row / _Rows)
6) Sample _AtlasTex at uv.
7) Output:
   - Unlit: BaseColor = sample, Alpha = sample.a
   - Lit: BaseColor = sample, Emission = sample * EmissionStrength

## Material Presets

### Tunnel Corridor .obj
- Shader: Lit
- BaseColor: low (dark)
- Emission: enabled (strength 2.0-5.0)
- Blend: Alpha or Additive (if supported)
- ZWrite: Off (for layered glow)

### Emission Shell
- Shader: Unlit
- BaseColor: black
- Emission: sample * 3.0
- Blend: Additive

## Loop Settings

- FrameRate: 12 (matches source)
- Loop: use frac() for wrap
- Filtering: Bilinear or Trilinear for smoothness

## Optional: Emissive Heatmap Pipeline

If you want lighter runtime cost:
- Bake a single emissive heatmap and animate phase via UV rotation.
- Use a normal map for surface detail.
- Good for stable glow without full flipbook frames.
