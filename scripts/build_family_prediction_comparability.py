#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDS = [
    "comparability_id",
    "family_id",
    "numeric_prediction_rows_written",
    "prediction_basis_status",
    "comparability_status",
    "allowed_scoring_mode",
    "blocked_scoring_mode",
    "next_required_artifact",
    "endpoint_scoring_allowed",
    "dark_sector_verdict_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "families_checked",
    "families_with_numeric_predictions",
    "families_without_numeric_predictions",
    "m0_adequacy_scoring_basis_available",
    "family_comparison_scoring_allowed",
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


def family_prediction_counts() -> dict[str, int]:
    counts = {"M0": 0, "M1": 0, "M2": 0}
    for row in read_csv(DERIVED / "family_prediction_tables_v08.csv"):
        family = row["family_id"]
        if family in counts and row["v_pred_km_s"]:
            counts[family] += 1
    return counts


def status_rows() -> list[dict[str, object]]:
    counts = family_prediction_counts()
    m1_adm = read_csv(DERIVED / "m1_admissibility_table_summary_v06.csv")[0]
    m2_nuisance = read_csv(DERIVED / "m2_nuisance_policy_table_summary_v06.csv")[0]
    rows = [
        {
            "comparability_id": "FPC09_M0",
            "family_id": "M0",
            "numeric_prediction_rows_written": counts["M0"],
            "prediction_basis_status": "M0_NO_DARK_NUMERIC_PREDICTION_ROWS_PRESENT",
            "comparability_status": "COMPARABLE_AS_SINGLE_FAMILY_ADEQUACY_BASIS_ONLY",
            "allowed_scoring_mode": "M0_ADEQUACY_DIAGNOSTIC_ONLY",
            "blocked_scoring_mode": "M0_M1_M2_FAMILY_COMPARISON",
            "next_required_artifact": "control_runner_outputs_v08.csv",
        },
        {
            "comparability_id": "FPC09_M1",
            "family_id": "M1",
            "numeric_prediction_rows_written": counts["M1"],
            "prediction_basis_status": m1_adm["overall_status"],
            "comparability_status": "NOT_COMPARABLE_NO_M1_NUMERIC_PREDICTION_ROWS",
            "allowed_scoring_mode": "NONE",
            "blocked_scoring_mode": "M1_RESPONSE_COMPARISON",
            "next_required_artifact": "m1_response_value_freeze_or_explicit_ineligibility_gate_v01",
        },
        {
            "comparability_id": "FPC09_M2",
            "family_id": "M2",
            "numeric_prediction_rows_written": counts["M2"],
            "prediction_basis_status": m2_nuisance["overall_status"],
            "comparability_status": "NOT_COMPARABLE_NO_M2_NUMERIC_PREDICTION_ROWS",
            "allowed_scoring_mode": "NONE",
            "blocked_scoring_mode": "M2_BENCHMARK_COMPARISON",
            "next_required_artifact": "m2_benchmark_value_freeze_or_explicit_ineligibility_gate_v01",
        },
    ]
    for row in rows:
        row["endpoint_scoring_allowed"] = "false"
        row["dark_sector_verdict_allowed"] = "false"
        row["claim_boundary"] = "family_prediction_comparability_only_no_scores_no_dark_sector_verdict"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    with_predictions = sum(int(row["numeric_prediction_rows_written"]) > 0 for row in rows)
    without_predictions = len(rows) - with_predictions
    family_comparison_allowed = with_predictions == len(rows)
    return [
        {
            "summary_id": "FAMILY_PREDICTION_COMPARABILITY_V09",
            "families_checked": len(rows),
            "families_with_numeric_predictions": with_predictions,
            "families_without_numeric_predictions": without_predictions,
            "m0_adequacy_scoring_basis_available": str(with_predictions >= 1).lower(),
            "family_comparison_scoring_allowed": str(family_comparison_allowed).lower(),
            "endpoint_scoring_allowed_anywhere": "false",
            "dark_sector_verdict_allowed_anywhere": "false",
            "overall_status": "FAMILY_PREDICTION_COMPARABILITY_M0_ONLY_FAMILY_COMPARISON_BLOCKED"
            if not family_comparison_allowed
            else "FAMILY_PREDICTION_COMPARABILITY_READY_FOR_FULL_FAMILY_COMPARISON_PREFLIGHT",
            "next_required_artifact": "control_runner_outputs_v08.csv"
            if not family_comparison_allowed
            else "scoring_preflight_v07.csv",
            "claim_boundary": "family_prediction_comparability_only_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "family_prediction_comparability_v09.md").write_text(
        """# Family Prediction Comparability v09

**Doc class:** family prediction comparability gate
**Status:** M0 adequacy basis available; full M0/M1/M2 comparison blocked

Script:

```text
scripts/build_family_prediction_comparability.py
```

Derived outputs:

```text
data/derived/family_prediction_comparability_v09.csv
data/derived/family_prediction_comparability_summary_v09.csv
```

This gate checks whether the declared families have numeric prediction rows in
`family_prediction_tables_v08.csv`. It does not create new predictions. It only
separates two scoring modes:

- M0 adequacy diagnostics can be prepared from the existing M0 numeric rows.
- Full M0/M1/M2 family-comparison scoring remains blocked until M1 and M2 have
  numeric prediction rows or a later explicit ineligibility rule is frozen.

## Claim Boundary

This artifact writes no endpoint scores, runs no controls, compares no families,
and makes no dark-sector verdict. It prevents M1/M2 absence from being silently
converted into evidence for M0.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = status_rows()
    write_csv(DERIVED / "family_prediction_comparability_v09.csv", rows, FIELDS)
    write_csv(DERIVED / "family_prediction_comparability_summary_v09.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_FAMILY_PREDICTION_COMPARABILITY_V09_BUILT")


if __name__ == "__main__":
    main()
