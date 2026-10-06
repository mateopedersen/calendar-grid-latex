#!/usr/bin/env python3
"""Audit and exercise the exact ZIP produced by `l3build ctan`."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "build" / "distrib" / "ctan" / "calendar-grid-1.0.0.zip"
REQUIRED = {
    "calendar-grid.sty",
    "calendar-grid-doc.tex",
    "calendar-grid-doc.pdf",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "manifest.txt",
    "build.lua",
    "calendar-grid-regression.lvt",
    "calendar-grid-regression.tlg",
}


def main() -> None:
    if not ARCHIVE.is_file():
        raise SystemExit(f"Missing CTAN archive: {ARCHIVE}")
    with zipfile.ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        top = {name.split("/", 1)[0] for name in names if name.strip("/")}
        if top != {"calendar-grid"}:
            raise SystemExit(f"Expected one top-level calendar-grid directory, found: {sorted(top)}")
        prefix = "calendar-grid/"
        files = {name[len(prefix):] for name in names if name.startswith(prefix) and not name.endswith("/")}
        missing = REQUIRED - files
        if missing:
            raise SystemExit(f"Archive is missing required files: {sorted(missing)}")
        unwanted = [name for name in files if name.endswith((".aux", ".log", ".out", ".synctex.gz", ".fls", ".fdb_latexmk"))]
        if unwanted:
            raise SystemExit(f"Archive contains generated intermediates: {sorted(unwanted)}")
        with tempfile.TemporaryDirectory(prefix="calendar-grid-ctan-") as temp:
            archive.extractall(temp)
            package = Path(temp) / "calendar-grid"
            env = os.environ.copy()
            subprocess.run(["l3build", "check"], cwd=package, env=env, check=True)
            subprocess.run(["l3build", "doc"], cwd=package, env=env, check=True)
    print(f"Audited and checked {ARCHIVE.name}")


if __name__ == "__main__":
    main()
