#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m1_per_galaxy_response_privilege_count_audit_v10.csv"
STATUS = "M1_RESPONSE_PARAMETER_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_RESPONSE_PRIVILEGE_AUDIT_PENDING"
CLAIM_BOUNDARY = "m1_response_parameter_final_count_freeze_only_no_response_values_no_parsimony_no_scores"

FIELDS = [
    "freeze_row_id",
    "candidate_row_id",
    "family_id",
    "count_domain",
    "frozen_k_m1_global",
    "freeze_status",
    "candidate_status",
    "source_artifacts",
    "per_galaxy_response_privilege_input_allowed",
    "response_value_input_allowed",
    "parsimony_input_allowed",
    "next_required_artifact",
    "forbidden_inputs",
    "endpoint_scoring_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "freeze_artifact",
    "candidate_status",
    "frozen_k_m1_global",
    "final_count_frozen",
    "numeric_response_values_written",
    "per_galaxy_response_privilege_counts_written",
    "parsimony_scores_written",
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


def freeze_rows() -> list[dict[str, object]]:
    candidates = read_csv(DERIVED / "m1_response_parameter_final_count_candidate_v14.csv")
    if len(candidates) != 1:
        raise ValueError("expected one M1 response-parameter final-count candidate")
    candidate = candidates[0]
    if candidate["candidate_status"] != "M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE":
        raise ValueError("M1 response-parameter final-count candidate is not ready for freeze")
    return [
        {
            "freeze_row_id": "M1RPFCF15_001",
            "candidate_row_id": candidate["candidate_row_id"],
            "family_id": candidate["family_id"],
            "count_domain": candidate["count_domain"],
            "frozen_k_m1_global": candidate["candidate_k_m1_global"],
            "freeze_status": STATUS,
            "candidate_status": candidate["candidate_status"],
            "source_artifacts": candidate["input_artifacts"],
            "per_galaxy_response_privilege_input_allowed": "true",
            "response_value_input_allowed": "false",
            "parsimony_input_allowed": "false",
            "next_required_artifact": NEXT_ARTIFACT,
            "forbidden_inputs": candidate["forbidden_inputs"],
            "endpoint_scoring_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    row = rows[0]
    return [
        {
            "summary_id": "M1_RESPONSE_PARAMETER_FINAL_COUNT_FREEZE_V15",
            "freeze_artifact": "m1_response_parameter_final_count_freeze_v15",
            "candidate_status": row["candidate_status"],
            "frozen_k_m1_global": row["frozen_k_m1_global"],
            "final_count_frozen": "true",
            "numeric_response_values_written": 0,
            "per_galaxy_response_privilege_counts_written": 0,
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": row["freeze_status"],
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m1_response_parameter_final_count_freeze_v15.md").write_text(
        f"""# M1 Response Parameter Final Count Freeze v15

**Doc class:** M1 response-parameter final-count freeze
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** M1 global response-parameter count frozen; per-galaxy response privilege audit pending
**Canonical parent:** M1 response-parameter final-count candidate v14

Script:

```text
scripts/build_m1_response_parameter_final_count_freeze.py
```

Derived outputs:

```text
data/derived/m1_response_parameter_final_count_freeze_v15.csv
data/derived/m1_response_parameter_final_count_freeze_summary_v15.csv
```

## Current Result

The v15 freeze accepts the v14 candidate as the frozen M1 global
response-parameter count:

```text
k_M1_global = 0
```

The expected status is:

```text
{STATUS}
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This artifact freezes only the protocol-local global M1 response-parameter
count. It does not write `Response_tau`, does not write numeric response values,
does not write per-galaxy response privilege counts, does not compute parsimony,
does not authorize endpoint scoring, and does not decide whether a Tau response
or dark-sector layer is physically absent or necessary.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = freeze_rows()
    write_csv(DERIVED / "m1_response_parameter_final_count_freeze_v15.csv", rows, FIELDS)
    write_csv(DERIVED / "m1_response_parameter_final_count_freeze_summary_v15.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_M1_RESPONSE_PARAMETER_FINAL_COUNT_FREEZE_V15_BUILT")


if __name__ == "__main__":
    main()
