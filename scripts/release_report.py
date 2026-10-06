#!/usr/bin/env python3
"""Report PDF and CTAN ZIP sizes and SHA-256 checksums for the CI release."""
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for path in (root / "calendar-grid-doc.pdf", root / "calendar-grid-1.0.0.zip"):
    if not path.is_file() or not path.stat().st_size:
        raise SystemExit(f"Missing release artifact: {path}")
    print(f"{path.name}: {path.stat().st_size} bytes SHA256 {hashlib.sha256(path.read_bytes()).hexdigest()}")
