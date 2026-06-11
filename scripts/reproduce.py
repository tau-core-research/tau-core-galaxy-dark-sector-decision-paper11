#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper11_submission_source"


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> None:
    env = os.environ.copy()
    env.setdefault("SOURCE_DATE_EPOCH", "1781136000")
    run(["python", "scripts/run_readiness_audit.py"])
    run(["python", "scripts/build_scoring_input_scaffold.py"])
    run(["python", "scripts/build_source_import_contract.py"])
    run(["python", "scripts/build_source_import_values.py"])
    run(["python", "scripts/build_source_import_real_values_template.py"])
    run(["python", "scripts/run_source_import_raw_adapter.py"])
    run(["python", "scripts/run_source_import_write_authorization.py"])
    run(["python", "scripts/run_source_import_real_values_gate.py"])
    run(["python", "scripts/run_source_import_leakage_audit.py"])
    run(["python", "scripts/run_scoring_activation_gate.py"])
    run(["python", "scripts/run_scoring_preflight.py"])
    run(["python", "scripts/validate_protocol_manifests.py"])
    run(["tectonic", "main.tex"], cwd=SOURCE)
    run(["python", "scripts/build_arxiv_source.py"])
    run(["pytest", "-q"])
    print("PAPER11_REPRODUCTION_COMPLETE")


if __name__ == "__main__":
    main()
