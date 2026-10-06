#!/usr/bin/env python3
"""Install package into a temporary TEXMF tree and compile an external consumer."""
from pathlib import Path
import os
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix="calendar-grid-install-") as temp:
    texmf = Path(temp) / "texmf"
    target = texmf / "tex" / "latex" / "calendar-grid"
    target.mkdir(parents=True)
    (target / "calendar-grid.sty").write_bytes((root / "calendar-grid.sty").read_bytes())
    subprocess.run(["mktexlsr", str(texmf)], check=True)
    env = os.environ.copy()
    env["TEXMFHOME"] = str(texmf)
    found = subprocess.run(
        ["kpsewhich", "calendar-grid.sty"],
        env=env,
        cwd=temp,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if Path(found).resolve() != (target / "calendar-grid.sty").resolve():
        raise SystemExit(f"kpsewhich selected the wrong package: {found}")
    consumer = Path(temp) / "consumer.tex"
    consumer.write_text(r"""\documentclass{article}
\usepackage{calendar-grid}
\begin{document}
\CalendarGrid[year=2027,month=1,week-start=monday,layout=fixed,overflow=adjacent]
\end{document}
""")
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", f"-output-directory={temp}", str(consumer)], env=env, check=True, cwd=temp)
print(f"Installed package resolved and consumer compiled: {found}")
