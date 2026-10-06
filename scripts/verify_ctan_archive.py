#!/usr/bin/env python3
"""Audit, unpack, and rebuild the exact archive produced by `l3build ctan`."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "calendar-grid-1.0.0.zip"
REQUIRED = {
    "calendar-grid.sty", "calendar-grid-doc.tex", "calendar-grid-doc.pdf",
    "README.md", "LICENSE", "CHANGELOG.md", "manifest.txt", "build.lua",
    "calendar-grid-example-basic-month.tex", "calendar-grid-example-fixed-grid.tex",
    "calendar-grid-example-year-overview.tex", "calendar-grid-example-events.tex",
    "calendar-grid-example-ranges.tex", "calendar-grid-regression.lvt",
    "calendar-grid-regression.tlg",
}
FORBIDDEN_PARTS = {".git", ".github", "__MACOSX", "build", "__pycache__"}
FORBIDDEN_SUFFIXES = (".aux", ".log", ".toc", ".out", ".fls", ".fdb_latexmk", ".synctex.gz", ".xdv", ".pyc", "~")


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
        unwanted = [name for name in files if FORBIDDEN_PARTS.intersection(Path(name).parts) or Path(name).name == ".DS_Store" or name.endswith(FORBIDDEN_SUFFIXES)]
        if unwanted:
            raise SystemExit(f"Archive contains forbidden/generated files: {sorted(unwanted)}")
        with tempfile.TemporaryDirectory(prefix="calendar-grid-ctan-") as temp:
            archive.extractall(temp)
            package = Path(temp) / "calendar-grid"
            env = os.environ.copy()
            subprocess.run(["l3build", "check"], cwd=package, env=env, check=True)
            subprocess.run(["l3build", "doc"], cwd=package, env=env, check=True)
            if not (package / "calendar-grid-doc.pdf").is_file():
                raise SystemExit("Archive rebuild produced no calendar-grid-doc.pdf")
            consumer = Path(temp) / "consumer.tex"
            consumer.write_text(r"""\documentclass{article}
\usepackage{calendar-grid}
\begin{document}
\CalendarGrid[year=2027,month=1,week-start=monday,layout=fixed,overflow=adjacent]
\end{document}
""")
            texenv = env.copy()
            texenv["TEXINPUTS"] = str(package) + os.pathsep + texenv.get("TEXINPUTS", "")
            subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", f"-output-directory={temp}", str(consumer)], cwd=temp, env=texenv, check=True)
    digest = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    print(f"Audited, rebuilt, and consumer-tested {ARCHIVE.name}")
    print(f"CTAN ZIP SHA256: {digest}")


if __name__ == "__main__":
    main()
