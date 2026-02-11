#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np


def write_obj_from_heightmap(heightmap, out_path, z_scale=1.0, xy_scale=1.0):
    heightmap = np.asarray(heightmap)
    if heightmap.ndim != 2:
        raise ValueError(f"Expected 2D heightmap, got shape {heightmap.shape}")
    h, w = heightmap.shape
    verts = []
    faces = []

    for y in range(h):
        for x in range(w):
            z = float(heightmap[y, x]) * z_scale
            verts.append((x * xy_scale, y * xy_scale, z))

    def vid(x, y):
        return y * w + x + 1

    for y in range(h - 1):
        for x in range(w - 1):
            v1 = vid(x, y)
            v2 = vid(x + 1, y)
            v3 = vid(x + 1, y + 1)
            v4 = vid(x, y + 1)
            faces.append((v1, v2, v3))
            faces.append((v1, v3, v4))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# QESR Confinement Lens Mesh\n")
        for v in verts:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in faces:
            f.write(f"f {face[0]} {face[1]} {face[2]}\n")


def main():
    parser = argparse.ArgumentParser(description="Build an OBJ mesh from a QESR heightmap (.npy).")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/fields/Q_confinement_lens_field.npy"),
        help="Input .npy heightmap.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("prototypes/Nivalis_Node_Phase_I/modules/QESR_confinement_lens.obj"),
        help="Output .obj path.",
    )
    parser.add_argument("--z-scale", type=float, default=1.0, help="Scale factor for Z values.")
    parser.add_argument("--xy-scale", type=float, default=1.0, help="Scale factor for X/Y grid spacing.")
    args = parser.parse_args()

    heightmap = np.load(args.input)
    write_obj_from_heightmap(heightmap, args.output, z_scale=args.z_scale, xy_scale=args.xy_scale)
    print("Wrote:", args.output)


if __name__ == "__main__":
    main()
