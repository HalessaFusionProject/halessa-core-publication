#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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
        f.write("# QESR Phase Mesh\n")
        for v in verts:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in faces:
            f.write(f"f {face[0]} {face[1]} {face[2]}\n")


def resolve_path(path_value, repo_root):
    if path_value is None:
        return None
    path = Path(path_value)
    if path.is_absolute():
        return path
    return repo_root / path


def load_registry(registry_path, repo_root):
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    for entry in registry:
        if "input" in entry:
            entry["input"] = resolve_path(entry["input"], repo_root)
        if "output" in entry:
            entry["output"] = resolve_path(entry["output"], repo_root)
    return registry


def default_registry(repo_root):
    return [
        {
            "phase_id": "Phase XIII",
            "label": "Quantum Confinement Lens",
            "input": repo_root / "data/fields/Q_confinement_lens_field.npy",
            "output": repo_root / "prototypes/Nivalis_Node_Phase_I/modules/QESR_confinement_lens.obj",
            "z_scale": 1.0,
            "xy_scale": 1.0,
        }
    ]


def build_meshes(registry, verbose=True):
    for entry in registry:
        input_path = entry.get("input")
        output_path = entry.get("output")
        if not input_path or not output_path:
            continue
        if not Path(input_path).exists():
            if verbose:
                print(f"MISSING: {input_path}")
            continue
        heightmap = np.load(input_path)
        write_obj_from_heightmap(
            heightmap,
            output_path,
            z_scale=float(entry.get("z_scale", 1.0)),
            xy_scale=float(entry.get("xy_scale", 1.0)),
        )
        if verbose:
            print(f"Wrote: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Build OBJ meshes for QESR phases from .npy fields.")
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("data/config/phase_mesh_registry.json"),
        help="Path to a JSON registry for phase meshes.",
    )
    parser.add_argument(
        "--use-default",
        action="store_true",
        help="Use the built-in default registry instead of the JSON file.",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    registry = default_registry(repo_root) if args.use_default else None
    if registry is None:
        if args.registry.exists():
            registry = load_registry(args.registry, repo_root)
        else:
            registry = default_registry(repo_root)
    build_meshes(registry)


if __name__ == "__main__":
    main()
