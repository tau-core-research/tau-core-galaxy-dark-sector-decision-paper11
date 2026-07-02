#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source_manifest"
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

STATUS = "NUMERIC_DECISION_THRESHOLDS_V08_READY_FOR_SCORING_PREFLIGHT"
NEXT_ARTIFACT = "scoring_preflight_v07.csv"
CLAIM_BOUNDARY = "numeric_decision_thresholds_v08_threshold_freeze_only_no_scores_no_verdict"

FIELDS = [
    "numeric_threshold_id",
    "source_threshold_id",
    "verdict_label",
    "rank_required",
    "minimum_heldout_margin",
    "maximum_control_failures",
    "stability_required",
    "unresolved_fallback_allowed",
    "numeric_threshold_status",
    "allowed_interpretation",
    "forbidden_interpretation",
    "next_required_artifact",
    "endpoint_scoring_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "threshold_artifact",
    "source_threshold_rows_checked",
    "numeric_threshold_rows_written",
    "endpoint_scores_written",
    "verdicts_written",
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


def threshold_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, row in enumerate(read_csv(SOURCE / "decision_threshold_v01.csv"), start=1):
        unresolved = row["verdict_label"] == "UNRESOLVED"
        rows.append(
            {
                "numeric_threshold_id": f"NDT08_{index:03d}",
                "source_threshold_id": row["threshold_id"],
                "verdict_label": row["verdict_label"],
                "rank_required": 0 if unresolved else 1,
                "minimum_heldout_margin": 0,
                "maximum_control_failures": 0,
                "stability_required": "true",
                "unresolved_fallback_allowed": "true" if unresolved else "false",
                "numeric_threshold_status": "NUMERIC_THRESHOLD_FROZEN_NOT_EVALUATED",
                "allowed_interpretation": row["allowed_interpretation"],
                "forbidden_interpretation": row["forbidden_interpretation"],
                "next_required_artifact": NEXT_ARTIFACT,
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "NUMERIC_DECISION_THRESHOLDS_V08",
            "threshold_artifact": "numeric_decision_thresholds_v08",
            "source_threshold_rows_checked": len(rows),
            "numeric_threshold_rows_written": len(rows),
            "endpoint_scores_written": 0,
            "verdicts_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": STATUS,
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "numeric_decision_thresholds_v08.md").write_text(
        f"""# Numeric Decision Thresholds v08

**Doc class:** numeric decision-threshold freeze
**Status:** numeric threshold rules frozen; no endpoint scores or verdicts
**Canonical parent:** Decision threshold v01

Script:

```text
scripts/build_numeric_decision_thresholds.py
```

Derived outputs:

```text
data/derived/numeric_decision_thresholds_v08.csv
data/derived/numeric_decision_thresholds_summary_v08.csv
```

This artifact freezes the numerical decision-threshold policy before endpoint
scores are evaluated. It does not evaluate any family, galaxy, control, or
held-out score.

The frozen policy is deliberately minimal:

```text
rank_required = 1 for M0/M1/M2 family-favoring labels
minimum_heldout_margin = 0
maximum_control_failures = 0
stability_required = true
UNRESOLVED is the only fallback label
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This artifact writes threshold rules only. It computes no endpoint scores,
evaluates no held-out ranking, runs no controls, writes no verdict labels, and
makes no dark-sector decision.

Claim boundary:

```text
{CLAIM_BOUNDARY}
```
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = threshold_rows()
    write_csv(DERIVED / "numeric_decision_thresholds_v08.csv", rows, FIELDS)
    write_csv(DERIVED / "numeric_decision_thresholds_summary_v08.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_NUMERIC_DECISION_THRESHOLDS_V08_BUILT")


if __name__ == "__main__":
    main()
