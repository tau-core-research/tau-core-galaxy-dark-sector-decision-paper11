#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source_manifest"
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDS = [
    "control_readiness_id",
    "runner_id",
    "control_id",
    "output_contract_status",
    "execution_timing",
    "score_calculation_preflight_status",
    "verdict_control_status",
    "control_result_rows_written",
    "control_scores_written",
    "control_pass_claim_allowed",
    "endpoint_scoring_allowed",
    "dark_sector_verdict_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "controls_checked",
    "score_calculation_ready_controls",
    "verdict_ready_controls",
    "control_result_rows_written",
    "control_scores_written",
    "control_pass_claim_allowed_anywhere",
    "score_calculation_preflight_ready",
    "family_verdict_controls_ready",
    "endpoint_scoring_allowed_anywhere",
    "dark_sector_verdict_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def timing(control_type: str) -> str:
    if control_type in {"shuffled_source_labels", "wrong_family_assignment", "null_source_baseline", "radial_zone_perturbation"}:
        return "POST_PRIMARY_SCORE_REQUIRED"
    return "PRE_SCORE_AUDIT_OR_POLICY"


def readiness_rows() -> list[dict[str, object]]:
    contracts = {row["control_id"]: row for row in read_csv(DERIVED / "control_runner_outputs_v08.csv")}
    implementation = read_csv(SOURCE / "control_implementation_freeze_v03.csv")
    rows: list[dict[str, object]] = []
    for index, row in enumerate(implementation, start=1):
        contract = contracts[row["control_id"]]
        contract_ready = contract["output_contract_status"] == "OUTPUT_CONTRACT_READY_NOT_RUN"
        rows.append(
            {
                "control_readiness_id": f"CER09_{index:03d}",
                "runner_id": contract["runner_id"],
                "control_id": row["control_id"],
                "output_contract_status": contract["output_contract_status"],
                "execution_timing": timing(row["control_type"]),
                "score_calculation_preflight_status": "READY_FOR_SCORE_CALCULATION_PRECHECK"
                if contract_ready
                else "BLOCKED_CONTRACT_MISSING",
                "verdict_control_status": "BLOCKED_NOT_EXECUTED_NO_PASS_CLAIM",
                "control_result_rows_written": "0",
                "control_scores_written": "0",
                "control_pass_claim_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "dark_sector_verdict_allowed": "false",
                "claim_boundary": "control_execution_readiness_only_no_control_results_no_scores_no_verdict",
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    score_ready = sum(row["score_calculation_preflight_status"] == "READY_FOR_SCORE_CALCULATION_PRECHECK" for row in rows)
    verdict_ready = sum(row["verdict_control_status"] == "READY_CONTROL_PASS_REVIEWED" for row in rows)
    return [
        {
            "summary_id": "CONTROL_EXECUTION_READINESS_V09",
            "controls_checked": len(rows),
            "score_calculation_ready_controls": score_ready,
            "verdict_ready_controls": verdict_ready,
            "control_result_rows_written": "0",
            "control_scores_written": "0",
            "control_pass_claim_allowed_anywhere": "false",
            "score_calculation_preflight_ready": str(score_ready == len(rows)).lower(),
            "family_verdict_controls_ready": str(verdict_ready == len(rows)).lower(),
            "endpoint_scoring_allowed_anywhere": "false",
            "dark_sector_verdict_allowed_anywhere": "false",
            "overall_status": "CONTROL_EXECUTION_READINESS_SCORE_CALCULATION_READY_VERDICT_CONTROLS_BLOCKED",
            "next_required_artifact": "endpoint_scoring_runner_v01",
            "claim_boundary": "control_execution_readiness_only_no_control_results_no_scores_no_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "control_execution_readiness_v09.md").write_text(
        """# Control Execution Readiness v09

**Doc class:** control execution readiness gate
**Status:** control contracts ready for score-calculation preflight; verdict controls not executed

Script:

```text
scripts/build_control_execution_readiness.py
```

Derived outputs:

```text
data/derived/control_execution_readiness_v09.csv
data/derived/control_execution_readiness_summary_v09.csv
```

This gate separates two things that must not be conflated:

- score-calculation preflight readiness, where each control has a frozen output
  contract and can be scheduled around the primary scoring run;
- verdict-control readiness, which requires executed control result rows and
  reviewed pass/fail outcomes.

Several controls require the primary score table before they can be evaluated.
Therefore this artifact does not claim that controls have passed. It only
records that the control contracts are ready enough not to block the first raw
score-calculation runner.

## Claim Boundary

This artifact writes no control result rows, computes no control scores, claims
no control pass, authorizes no endpoint verdict, and makes no dark-sector
verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = readiness_rows()
    write_csv(DERIVED / "control_execution_readiness_v09.csv", rows, FIELDS)
    write_csv(DERIVED / "control_execution_readiness_summary_v09.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_CONTROL_EXECUTION_READINESS_V09_BUILT")


if __name__ == "__main__":
    main()
