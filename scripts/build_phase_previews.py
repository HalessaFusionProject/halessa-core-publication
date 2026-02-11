#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError as exc:
    raise SystemExit("Missing dependency: matplotlib. Install with `pip install matplotlib`.") from exc


def resolve_path(path_value, repo_root):
    path = Path(path_value)
    if path.is_absolute():
        return path
    return repo_root / path


def load_registry(registry_path, repo_root):
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    for entry in registry:
        entry["input"] = resolve_path(entry["input"], repo_root)
        entry["output"] = resolve_path(entry["output"], repo_root)
    return registry


def build_preview(array):
    if array.ndim == 3:
        slice_idx = array.shape[0] // 2
        return array[slice_idx]
    if array.ndim == 2:
        return array
    return array.reshape(1, -1)


def save_preview(array, output_path, title, cmap, dpi, include_title):
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.imshow(array, cmap=cmap)
    ax.axis("off")
    if include_title:
        ax.set_title(title)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=dpi)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Generate PNG previews for QESR phase fields.")
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("data/config/phase_preview_registry.json"),
        help="Path to a JSON registry of preview outputs.",
    )
    parser.add_argument("--cmap", default="inferno", help="Matplotlib colormap for previews.")
    parser.add_argument("--dpi", type=int, default=150, help="Output DPI for saved PNGs.")
    parser.add_argument("--no-title", action="store_true", help="Disable plot titles.")
    args = parser.parse_args()

    repo_root = Path.cwd()
    if not args.registry.exists():
        raise SystemExit(f"Registry not found: {args.registry}")
    registry = load_registry(args.registry, repo_root)

    for entry in registry:
        input_path = entry["input"]
        output_path = entry["output"]
        title = f"{entry.get('phase_id', '')} - {entry.get('label', '')}".strip(" -")

        if not input_path.exists():
            print(f"MISSING: {input_path}")
            continue

        array = np.load(input_path, mmap_mode="r")
        preview = build_preview(array)
        save_preview(preview, output_path, title, args.cmap, args.dpi, not args.no_title)
        print(f"Wrote: {output_path}")


if __name__ == "__main__":
    main()
