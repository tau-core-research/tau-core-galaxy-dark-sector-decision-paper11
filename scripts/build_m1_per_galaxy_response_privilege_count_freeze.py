#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m2_benchmark_parameter_inventory_v10.csv"
CLAIM_BOUNDARY = "m1_per_galaxy_response_privilege_count_freeze_only_no_response_values_no_parsimony_no_scores"

FIELDS = [
    "freeze_row_id",
    "audit_row_id",
    "source_audit_id",
    "galaxy_id",
    "decision_role",
    "frozen_per_galaxy_response_privilege_count",
    "freeze_status",
    "audit_status",
    "source_activation_status",
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
    "audit_status",
    "source_rows_checked",
    "frozen_zero_rows",
    "unresolved_rows",
    "per_galaxy_response_count_frozen",
    "frozen_per_galaxy_response_privilege_count_total",
    "numeric_response_values_written",
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


def audit_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m1_per_galaxy_response_privilege_count_audit_summary_v10.csv")
    if len(rows) != 1:
        raise ValueError("expected one M1 per-galaxy response-privilege audit summary row")
    return rows[0]


def freeze_rows() -> list[dict[str, object]]:
    audit_rows = read_csv(DERIVED / "m1_per_galaxy_response_privilege_count_audit_v10.csv")
    rows: list[dict[str, object]] = []
    for index, row in enumerate(audit_rows, start=1):
        rows.append(
            {
                "freeze_row_id": f"M1PGRPCF11_{index:03d}",
                "audit_row_id": row["audit_row_id"],
                "source_audit_id": row["source_audit_id"],
                "galaxy_id": row["galaxy_id"],
                "decision_role": row["decision_role"],
                "frozen_per_galaxy_response_privilege_count": row["per_galaxy_response_privilege_count_value"],
                "freeze_status": "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_FREEZE_V11_FROZEN",
                "audit_status": row["row_response_privilege_status"],
                "source_activation_status": row["source_activation_status"],
                "response_value_input_allowed": "false",
                "parsimony_input_allowed": "false",
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": (
                    "endpoint_residual;heldout_score;family_winner;best_fit_curve;"
                    "posthoc_response_activation;posthoc_response_amplitude;numeric_score_value"
                ),
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    audit = audit_summary()
    frozen_zero = [row for row in rows if row["frozen_per_galaxy_response_privilege_count"] == "0"]
    unresolved = len(rows) - len(frozen_zero)
    return [
        {
            "summary_id": "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_FREEZE_V11",
            "freeze_artifact": "m1_per_galaxy_response_privilege_count_freeze_v11",
            "audit_status": audit["overall_status"],
            "source_rows_checked": len(rows),
            "frozen_zero_rows": len(frozen_zero),
            "unresolved_rows": unresolved,
            "per_galaxy_response_count_frozen": "true" if unresolved == 0 else "false",
            "frozen_per_galaxy_response_privilege_count_total": sum(
                int(row["frozen_per_galaxy_response_privilege_count"]) for row in rows
            ),
            "numeric_response_values_written": 0,
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_FREEZE_V11_READY_M2_GLOBAL_COUNT_PENDING"
            if unresolved == 0
            else "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_FREEZE_V11_BLOCKED",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m1_per_galaxy_response_privilege_count_freeze_v11.md").write_text(
        f"""# M1 Per-Galaxy Response-Privilege Count Freeze v11

**Doc class:** per-galaxy M1 response-privilege count freeze
**Status:** frozen count ready; no `Response_tau`, no response values, no parsimony, no scoring

Script:

```text
scripts/build_m1_per_galaxy_response_privilege_count_freeze.py
```

Derived outputs:

```text
data/derived/m1_per_galaxy_response_privilege_count_freeze_v11.csv
data/derived/m1_per_galaxy_response_privilege_count_freeze_summary_v11.csv
```

This artifact freezes the v10 M1 per-galaxy response-privilege audit. All
eighteen source-manifest rows are frozen at zero row-specific M1 response
privileges under the current no-response/no-values scaffold.

The next count-readiness blocker is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This freeze records only protocol-local per-galaxy M1 response-privilege count
values. It does not construct or evaluate `Response_tau`, write response
values, compute a parsimony penalty, activate endpoint scoring, compare
families, or decide the dark-sector question.

Claim boundary:

```text
{CLAIM_BOUNDARY}
```
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = freeze_rows()
    write_csv(DERIVED / "m1_per_galaxy_response_privilege_count_freeze_v11.csv", rows, FIELDS)
    write_csv(
        DERIVED / "m1_per_galaxy_response_privilege_count_freeze_summary_v11.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER11_M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_FREEZE_V11_BUILT")


if __name__ == "__main__":
    main()
