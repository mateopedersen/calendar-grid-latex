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
with tempfile.TemporaryDirectory(prefix="calendar-grid-api-") as temp:
    from pathlib import Path
    consumer = Path(temp) / "api-check.tex"
    consumer.write_text(r"""\documentclass{article}
\usepackage{calendar-grid}
\begin{document}
\CalendarGridEvent{2027-01-15}{Meeting}
\CalendarGridRange[style=test]{2026-12-30}{2027-01-03}
\CalendarGrid[year=2027,month=1,week-start=saturday,layout=fixed,overflow=adjacent]
\CalendarGrid[year=2027,month=2,week-start=sunday,layout=compact,overflow=blank]
\CalendarYear[year=2027,columns=3,layout=compact]
\end{document}
""")
    for engine in engines:
        subprocess.run(
            [engine, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", f"-output-directory={temp}", str(consumer)],
            cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        )
        print(f"PASS {engine} public API, events, ranges, month and year rendering")
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
