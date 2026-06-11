#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_model_families() -> None:
    rows = read_csv(ROOT / "data/source_manifest/model_family_decision_protocol.csv")
    ids = {row["family_id"] for row in rows}
    require(ids == {"M0", "M1", "M2"}, f"unexpected model families: {ids}")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "endpoint scoring must be disabled")
        require("claim" not in row["current_status"].lower(), "status must not be a claim")


def validate_freeze_requirements() -> None:
    rows = read_csv(ROOT / "data/source_manifest/policy_bundle_freeze_requirements.csv")
    require(len(rows) == 9, "expected nine policy-bundle requirements")
    for row in rows:
        require(row["required_before_endpoint"] == "true", f"{row['requirement_id']} must freeze before endpoint")
        forbidden = row["endpoint_forbidden_inputs"]
        require("endpoint" in forbidden or "rotation_residual" in forbidden, "missing forbidden endpoint inputs")


def validate_outcomes() -> None:
    rows = read_csv(ROOT / "data/source_manifest/decision_outcome_ladder.csv")
    ids = {row["outcome_id"] for row in rows}
    require(ids == {"O0", "O1", "O2", "O3", "O4"}, f"unexpected outcomes: {ids}")
    forbidden_joined = " ".join(row["forbidden_interpretation"] for row in rows).lower()
    require("global dark matter rejection" in forbidden_joined, "missing no-global-rejection guard")


def main() -> None:
    validate_model_families()
    validate_freeze_requirements()
    validate_outcomes()
    print("PAPER11_PROTOCOL_MANIFESTS_VALID")


if __name__ == "__main__":
    main()
