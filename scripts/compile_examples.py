#!/usr/bin/env python3
"""Compile every shipped example with pdfTeX, XeTeX, and LuaTeX."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
engines = ("pdflatex", "xelatex", "lualatex")
examples = sorted(root.glob("calendar-grid-example-*.tex"))
if len(examples) != 5:
    raise SystemExit(f"Expected five examples, found {len(examples)}")
for engine in engines:
    for example in examples:
        with tempfile.TemporaryDirectory(prefix="calendar-grid-example-") as temp:
            subprocess.run(
                [engine, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", f"-output-directory={temp}", str(example)],
                cwd=root,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            if not (Path(temp) / f"{example.stem}.pdf").is_file():
                raise SystemExit(f"{engine} produced no PDF for {example.name}")
        print(f"PASS {engine} {example.name}")
