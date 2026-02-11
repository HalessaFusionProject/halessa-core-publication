#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
from typing import Iterable, List, Dict, Any
import zipfile


def _iter_files(paths: Iterable[Path]) -> Iterable[Path]:
    seen = set()
    for p in paths:
        if p.is_dir():
            for child in p.rglob("*"):
                if child.is_file():
                    resolved = child.resolve()
                    if resolved not in seen:
                        seen.add(resolved)
                        yield child
        elif p.is_file():
            resolved = p.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield p


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _find_manuscript(manuscript: Path, docs_dir: Path) -> Dict[str, Any]:
    if manuscript.exists():
        return {"path": manuscript, "resolved_from": None}
    # fallback search within docs dir
    candidate = None
    if docs_dir.exists():
        for match in docs_dir.rglob(manuscript.name):
            candidate = match
            break
    if candidate:
        return {"path": candidate, "resolved_from": manuscript}
    raise FileNotFoundError(f"Manuscript not found: {manuscript}")


def _generate_tree(paths: Iterable[Path], root: Path) -> List[str]:
    # Build a simple tree for included paths
    files = sorted({p.resolve() for p in _iter_files(paths)})
    rels = [p.relative_to(root).as_posix() for p in files]
    lines = ["halessa-fusion-model/"]
    for rel in rels:
        parts = rel.split("/")
        prefix = ""
        for i, part in enumerate(parts):
            if i == 0:
                prefix = "|-- " + part
            else:
                prefix = "    " * i + "|-- " + part
            if prefix not in lines:
                lines.append(prefix)
    return lines


def stage_publication_repo(
    manuscript: str,
    docs_dir: str,
    prototypes_dir: str,
    prompts_dir: str,
    ledger_dir: str,
    publication_zip: str,
    diagnostics_dir: str | None = None,
    verify_integrity: bool = True,
    create_export_tree: bool = True,
    report_path: str | None = None,
) -> Dict[str, Any]:
    repo_root = Path.cwd()
    docs_dir = (repo_root / docs_dir).resolve()
    prototypes_dir = (repo_root / prototypes_dir).resolve()
    prompts_dir = (repo_root / prompts_dir).resolve()
    ledger_dir = (repo_root / ledger_dir).resolve()
    diagnostics_path = (repo_root / diagnostics_dir).resolve() if diagnostics_dir else None
    manuscript_path = (repo_root / manuscript).resolve()
    publication_zip = (repo_root / publication_zip).resolve()

    manuscript_info = _find_manuscript(manuscript_path, docs_dir)
    manuscript_path = manuscript_info["path"].resolve()

    required = {
        "docs_dir": docs_dir,
        "prototypes_dir": prototypes_dir,
        "prompts_dir": prompts_dir,
        "ledger_dir": ledger_dir,
        "manuscript": manuscript_path,
    }
    if diagnostics_path is not None:
        required["diagnostics_dir"] = diagnostics_path

    missing = {k: str(v) for k, v in required.items() if not v.exists()}
    if verify_integrity and missing:
        raise FileNotFoundError(f"Missing required paths: {missing}")

    include_paths = [
        manuscript_path,
        docs_dir,
        prototypes_dir,
        prompts_dir,
        ledger_dir,
    ]
    if diagnostics_path is not None:
        include_paths.append(diagnostics_path)

    files = list(_iter_files(include_paths))
    total_size = sum(p.stat().st_size for p in files)

    # Integrity check (hashes)
    file_checks = []
    for p in files:
        try:
            file_checks.append(
                {
                    "path": p.resolve().relative_to(repo_root).as_posix(),
                    "size": p.stat().st_size,
                    "sha256": _sha256(p) if verify_integrity else None,
                }
            )
        except Exception as exc:
            file_checks.append(
                {
                    "path": p.resolve().relative_to(repo_root).as_posix(),
                    "size": p.stat().st_size if p.exists() else None,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            if verify_integrity:
                raise

    # Zip generation
    publication_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(publication_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in files:
            arcname = p.resolve().relative_to(repo_root).as_posix()
            zf.write(p, arcname)

    export_tree_path = None
    if create_export_tree:
        export_lines = _generate_tree(include_paths, repo_root)
        export_tree_path = repo_root / "logs" / "publication" / "export_tree.txt"
        export_tree_path.parent.mkdir(parents=True, exist_ok=True)
        export_tree_path.write_text("\n".join(export_lines) + "\n", encoding="utf-8")

    report = {
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "manuscript": {
            "path": manuscript_path.relative_to(repo_root).as_posix(),
            "resolved_from": manuscript_info["resolved_from"].as_posix()
            if manuscript_info["resolved_from"]
            else None,
        },
        "inputs": {
            "docs_dir": docs_dir.relative_to(repo_root).as_posix(),
            "prototypes_dir": prototypes_dir.relative_to(repo_root).as_posix(),
            "prompts_dir": prompts_dir.relative_to(repo_root).as_posix(),
            "ledger_dir": ledger_dir.relative_to(repo_root).as_posix(),
            "diagnostics_dir": diagnostics_path.relative_to(repo_root).as_posix()
            if diagnostics_path is not None
            else None,
        },
        "publication_zip": publication_zip.relative_to(repo_root).as_posix(),
        "verify_integrity": verify_integrity,
        "create_export_tree": create_export_tree,
        "export_tree_path": export_tree_path.relative_to(repo_root).as_posix()
        if export_tree_path
        else None,
        "file_count": len(files),
        "total_size_bytes": total_size,
        "file_checks": file_checks,
    }

    if report_path:
        report_path = (repo_root / report_path).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    return report


def main():
    parser = argparse.ArgumentParser(description="Stage the Halessa publication repository.")
    parser.add_argument("--manuscript", required=True)
    parser.add_argument("--docs-dir", required=True)
    parser.add_argument("--prototypes-dir", required=True)
    parser.add_argument("--prompts-dir", required=True)
    parser.add_argument("--ledger-dir", required=True)
    parser.add_argument("--diagnostics-dir", default=None)
    parser.add_argument("--publication-zip", required=True)
    parser.add_argument("--verify-integrity", action="store_true")
    parser.add_argument("--create-export-tree", action="store_true")
    parser.add_argument("--report-path", default=None)
    args = parser.parse_args()

    stage_publication_repo(
        manuscript=args.manuscript,
        docs_dir=args.docs_dir,
        prototypes_dir=args.prototypes_dir,
        prompts_dir=args.prompts_dir,
        ledger_dir=args.ledger_dir,
        diagnostics_dir=args.diagnostics_dir,
        publication_zip=args.publication_zip,
        verify_integrity=args.verify_integrity,
        create_export_tree=args.create_export_tree,
        report_path=args.report_path,
    )


if __name__ == "__main__":
    main()
