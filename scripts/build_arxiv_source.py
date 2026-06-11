#!/usr/bin/env python3
from __future__ import annotations

import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper11_submission_source"
OUT = ROOT / "arxiv_submission_source.zip"
EXCLUDED_SUFFIXES = {".aux", ".log", ".out", ".toc", ".pdf", ".fls", ".fdb_latexmk"}


def main() -> None:
    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(SOURCE.rglob("*")):
            if path.is_dir() or path.suffix in EXCLUDED_SUFFIXES:
                continue
            archive.write(path, path.relative_to(SOURCE))
    print(f"PAPER11_ARXIV_SOURCE_BUILT {OUT}")


if __name__ == "__main__":
    main()
