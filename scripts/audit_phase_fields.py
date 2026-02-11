#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np


def detect_anomaly(arr, threshold):
    std = float(np.std(arr))
    if std == 0:
        return False
    mean = float(np.mean(arr))
    return bool(np.any(np.abs(arr - mean) > threshold * std))


def main():
    parser = argparse.ArgumentParser(description="Audit QESR field arrays for shape and anomaly stats.")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data/fields"),
        help="Directory containing .npy field outputs.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/validation_charts/phase_field_audit.csv"),
        help="CSV output path for the audit report.",
    )
    parser.add_argument(
        "--std-threshold",
        type=float,
        default=2.5,
        help="Std-dev threshold for anomaly flagging.",
    )
    args = parser.parse_args()

    rows = []
    for path in sorted(args.input_dir.glob("*.npy")):
        arr = np.load(path, mmap_mode="r")
        rows.append(
            {
                "field": path.name,
                "shape": str(arr.shape),
                "mean": float(np.mean(arr)),
                "min": float(np.min(arr)),
                "max": float(np.max(arr)),
                "std": float(np.std(arr)),
                "anomaly": detect_anomaly(arr, args.std_threshold),
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys() if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)
    print(f"Wrote: {args.output}")


if __name__ == "__main__":
    main()
