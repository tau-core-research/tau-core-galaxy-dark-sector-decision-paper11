#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m1_response_parameter_inventory_v10.csv"
CLAIM_BOUNDARY = "m0_per_galaxy_privilege_count_freeze_only_no_parsimony_no_scores"

FIELDS = [
    "freeze_row_id",
    "audit_row_id",
    "galaxy_id",
    "decision_role",
    "frozen_per_galaxy_privilege_count",
    "freeze_status",
    "audit_status",
    "source_activation_status",
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
    "per_galaxy_count_frozen",
    "frozen_per_galaxy_privilege_count_total",
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
    rows = read_csv(DERIVED / "m0_per_galaxy_privilege_count_audit_summary_v10.csv")
    if len(rows) != 1:
        raise ValueError("expected one M0 per-galaxy privilege audit summary row")
    return rows[0]


def freeze_rows() -> list[dict[str, object]]:
    audit_rows = read_csv(DERIVED / "m0_per_galaxy_privilege_count_audit_v10.csv")
    rows: list[dict[str, object]] = []
    for index, row in enumerate(audit_rows, start=1):
        rows.append(
            {
                "freeze_row_id": f"M0PGPCF11_{index:03d}",
                "audit_row_id": row["audit_row_id"],
                "galaxy_id": row["galaxy_id"],
                "decision_role": row["decision_role"],
                "frozen_per_galaxy_privilege_count": row["per_galaxy_privilege_count_value"],
                "freeze_status": "M0_PER_GALAXY_PRIVILEGE_COUNT_FREEZE_V11_FROZEN",
                "audit_status": row["row_privilege_status"],
                "source_activation_status": row["source_activation_status"],
                "parsimony_input_allowed": "false",
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_parameter_discount",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    audit = audit_summary()
    frozen_zero = [row for row in rows if row["frozen_per_galaxy_privilege_count"] == "0"]
    unresolved = len(rows) - len(frozen_zero)
    return [
        {
            "summary_id": "M0_PER_GALAXY_PRIVILEGE_COUNT_FREEZE_V11",
            "freeze_artifact": "m0_per_galaxy_privilege_count_freeze_v11",
            "audit_status": audit["overall_status"],
            "source_rows_checked": len(rows),
            "frozen_zero_rows": len(frozen_zero),
            "unresolved_rows": unresolved,
            "per_galaxy_count_frozen": "true" if unresolved == 0 else "false",
            "frozen_per_galaxy_privilege_count_total": sum(
                int(row["frozen_per_galaxy_privilege_count"]) for row in rows
            ),
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_PER_GALAXY_PRIVILEGE_COUNT_FREEZE_V11_READY_M1_GLOBAL_COUNT_PENDING"
            if unresolved == 0
            else "M0_PER_GALAXY_PRIVILEGE_COUNT_FREEZE_V11_BLOCKED",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_per_galaxy_privilege_count_freeze_v11.md").write_text(
        f"""# M0 Per-Galaxy Privilege Count Freeze v11

**Doc class:** per-galaxy M0 privilege-count freeze
**Status:** frozen count ready; no parsimony, no scoring

Script:

```text
scripts/build_m0_per_galaxy_privilege_count_freeze.py
```

Derived outputs:

```text
data/derived/m0_per_galaxy_privilege_count_freeze_v11.csv
data/derived/m0_per_galaxy_privilege_count_freeze_summary_v11.csv
```

This artifact freezes the v10 per-galaxy M0 privilege-count audit. All eighteen
source-manifest rows are frozen at zero row-specific M0 privileges.

The next count-readiness blocker is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This freeze records only the per-galaxy M0 privilege-count values. It does not
compute a parsimony penalty, activate endpoint scoring, compare families, or
decide the dark-sector question.

Claim boundary:

```text
{CLAIM_BOUNDARY}
```
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = freeze_rows()
    write_csv(DERIVED / "m0_per_galaxy_privilege_count_freeze_v11.csv", rows, FIELDS)
    write_csv(DERIVED / "m0_per_galaxy_privilege_count_freeze_summary_v11.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_M0_PER_GALAXY_PRIVILEGE_COUNT_FREEZE_V11_BUILT")


if __name__ == "__main__":
    main()
