#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source_manifest"
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

STATUS = "CONTROL_RUNNER_OUTPUTS_V08_READY_FOR_DECISION_THRESHOLDS"
NEXT_ARTIFACT = "numeric_decision_thresholds_v08.csv"
CLAIM_BOUNDARY = "control_runner_outputs_v08_contract_only_no_control_results_no_scores_no_verdict"

FIELDS = [
    "control_output_id",
    "runner_id",
    "control_id",
    "source_execution_status",
    "output_contract",
    "output_contract_status",
    "control_result_rows_written",
    "control_scores_written",
    "control_pass_claim_allowed",
    "next_required_artifact",
    "endpoint_scoring_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "control_output_artifact",
    "runner_contract_rows_checked",
    "output_contract_rows_written",
    "control_result_rows_written",
    "control_scores_written",
    "control_pass_claim_allowed_anywhere",
    "endpoint_scoring_allowed_anywhere",
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


def output_rows() -> list[dict[str, object]]:
    rows = []
    for index, row in enumerate(read_csv(SOURCE / "control_runner_contract_v04.csv"), start=1):
        rows.append(
            {
                "control_output_id": f"CRO08_{index:03d}",
                "runner_id": row["runner_id"],
                "control_id": row["control_id"],
                "source_execution_status": row["execution_status"],
                "output_contract": row["output_contract"],
                "output_contract_status": "OUTPUT_CONTRACT_READY_NOT_RUN",
                "control_result_rows_written": 0,
                "control_scores_written": 0,
                "control_pass_claim_allowed": "false",
                "next_required_artifact": NEXT_ARTIFACT,
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "CONTROL_RUNNER_OUTPUTS_V08",
            "control_output_artifact": "control_runner_outputs_v08",
            "runner_contract_rows_checked": len(rows),
            "output_contract_rows_written": len(rows),
            "control_result_rows_written": sum(int(row["control_result_rows_written"]) for row in rows),
            "control_scores_written": sum(int(row["control_scores_written"]) for row in rows),
            "control_pass_claim_allowed_anywhere": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": STATUS,
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "control_runner_outputs_v08.md").write_text(
        f"""# Control Runner Outputs v08

**Doc class:** control-runner output-contract scaffold
**Status:** control output contracts ready; no control results or scores written
**Canonical parent:** Control runner contract v04

Script:

```text
scripts/build_control_runner_outputs.py
```

Derived outputs:

```text
data/derived/control_runner_outputs_v08.csv
data/derived/control_runner_outputs_summary_v08.csv
```

This artifact closes the global control-runner output-contract blocker without
claiming that numerical control runs have been executed. It materializes the
six declared control output contracts from `control_runner_contract_v04.csv`
as run-ready output-contract rows.

No shuffled-label, wrong-family, null-source, leakage, radial, parity, endpoint,
or family-comparison scores are written here.

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This artifact writes control output-contract rows only. It writes no control result rows,
computes no control scores, authorizes no endpoint scoring, compares no families,
and makes no dark-sector verdict.

Claim boundary:

```text
{CLAIM_BOUNDARY}
```
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = output_rows()
    write_csv(DERIVED / "control_runner_outputs_v08.csv", rows, FIELDS)
    write_csv(DERIVED / "control_runner_outputs_summary_v08.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_CONTROL_RUNNER_OUTPUTS_V08_BUILT")


if __name__ == "__main__":
    main()
