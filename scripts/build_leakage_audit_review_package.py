#!/usr/bin/env python3
from __future__ import annotations

import csv
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
INPUT = ROOT / "data/input"
PACKAGE_ROOT = ROOT / "review_packages/leakage_audit_v58_review_package"
ZIP_PATH = ROOT / "review_packages/leakage_audit_v58_review_package.zip"

PACKAGE_FILES = [
    {
        "source": INPUT / "leakage_audit_evidence_v10_TEMPLATE.csv",
        "target": "templates/leakage_audit_evidence_v10_TEMPLATE.csv",
        "role": "fillable leakage-evidence response template",
    },
    {
        "source": DERIVED / "leakage_audit_evidence_template_summary_v58.csv",
        "target": "data/leakage_audit_evidence_template_summary_v58.csv",
        "role": "template summary and claim boundary",
    },
    {
        "source": DERIVED / "leakage_evidence_contract_v10.csv",
        "target": "data/leakage_evidence_contract_v10.csv",
        "role": "four leakage-evidence contract checks",
    },
    {
        "source": DERIVED / "source_import_leakage_summary_v09.csv",
        "target": "data/source_import_leakage_summary_v09.csv",
        "role": "current leakage frontier summary",
    },
    {
        "source": DERIVED / "source_import_real_values_summary_v12.csv",
        "target": "data/source_import_real_values_summary_v12.csv",
        "role": "real-values gate summary",
    },
    {
        "source": DERIVED / "scoring_unblock_priority_summary_v25.csv",
        "target": "data/scoring_unblock_priority_summary_v25.csv",
        "role": "current scoring frontier summary",
    },
]

README = """# Leakage Audit v58 Review Package

**Status:** review package only; not leakage evidence; no activation; no endpoint scoring.

This package is for reviewing the current Paper 11 leakage frontier before any
row can be considered for scoring activation.

## Reviewer Tasks

1. Review each of the 72 template rows: 18 galaxies times four leakage checks.
2. Verify that source routes and observed-input handling are pre-score.
3. Verify morphology/readout labels are not derived from endpoint residuals,
   family winners, or best-fit score outcomes.
4. Verify benchmark/profile inputs were frozen before family comparison.
5. Only a later ingestion gate may consume a completed response as active
   `data/input/leakage_audit_evidence_v10.csv`.

## Required Checks

```text
LEC10_SOURCE_ROUTE
LEC10_OBSERVED_INPUTS
LEC10_MORPH_LABELS
LEC10_BENCHMARK_INPUTS
```

## Hard Stops

- Do not treat this package as active leakage evidence.
- Do not copy the template into `data/input/leakage_audit_evidence_v10.csv`
  without a separate completed review response and ingestion gate.
- Do not mark leakage rows as passed from template rows.
- Do not activate scoring rows or compute model-family scores from this package.
- Do not use endpoint residuals, family winners, or score outcomes to approve
  leakage evidence.
"""

DO_NOT_COPY = """# Do Not Copy Without Completed Leakage Review

The files in this package are review artifacts. The template rows are marked
`TEMPLATE_ROW_DO_NOT_IMPORT` and are not active leakage evidence.

Rows may be copied into `data/input/leakage_audit_evidence_v10.csv` only after a
completed review response explicitly marks the relevant rows as reviewed and a
later ingestion gate accepts that response.
"""


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def response_template_rows() -> list[dict[str, object]]:
    rows = read_csv(INPUT / "leakage_audit_evidence_v10_TEMPLATE.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "leakage_evidence_row_id": row["leakage_evidence_row_id"],
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "evidence_id": row["evidence_id"],
                "checked_object": row["checked_object"],
                "required_evidence": row["required_evidence"],
                "source_artifact": row["source_artifact"],
                "review_decision": "KEEP_TEMPLATE_NOT_REVIEWED_NO_LEAKAGE_PASS",
                "reviewer_leakage_pass_authorized": "false",
                "may_activate_row_after_ingestion": "false",
                "endpoint_scoring_allowed": "false",
                "reviewer_notes": "",
            }
        )
    return out


def write_manifest(rows: list[dict[str, str]]) -> None:
    write_csv(
        PACKAGE_ROOT / "REVIEW_MANIFEST.csv",
        rows,
        ["package_path", "source_path", "role", "claim_boundary"],
    )


def build_package() -> None:
    if PACKAGE_ROOT.exists():
        shutil.rmtree(PACKAGE_ROOT)
    PACKAGE_ROOT.mkdir(parents=True, exist_ok=True)
    write_text(PACKAGE_ROOT / "README.md", README)
    write_text(PACKAGE_ROOT / "DO_NOT_COPY_WITHOUT_COMPLETED_REVIEW.md", DO_NOT_COPY)

    manifest_rows: list[dict[str, str]] = [
        {
            "package_path": "README.md",
            "source_path": "generated_by_leakage_audit_review_package_builder",
            "role": "review instructions",
            "claim_boundary": "leakage_review_package_only_no_evidence_no_scores",
        },
        {
            "package_path": "DO_NOT_COPY_WITHOUT_COMPLETED_REVIEW.md",
            "source_path": "generated_by_leakage_audit_review_package_builder",
            "role": "hard-stop notice",
            "claim_boundary": "leakage_review_package_only_no_evidence_no_scores",
        },
    ]

    for item in PACKAGE_FILES:
        target = PACKAGE_ROOT / item["target"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(item["source"], target)
        manifest_rows.append(
            {
                "package_path": item["target"],
                "source_path": str(item["source"].relative_to(ROOT)),
                "role": item["role"],
                "claim_boundary": "leakage_review_package_only_no_evidence_no_scores",
            }
        )

    response_target = PACKAGE_ROOT / "templates/leakage_audit_review_response_TEMPLATE.csv"
    write_csv(
        response_target,
        response_template_rows(),
        [
            "leakage_evidence_row_id",
            "galaxy_id",
            "proposed_split",
            "evidence_id",
            "checked_object",
            "required_evidence",
            "source_artifact",
            "review_decision",
            "reviewer_leakage_pass_authorized",
            "may_activate_row_after_ingestion",
            "endpoint_scoring_allowed",
            "reviewer_notes",
        ],
    )
    manifest_rows.append(
        {
            "package_path": "templates/leakage_audit_review_response_TEMPLATE.csv",
            "source_path": "generated_from_leakage_audit_evidence_v10_TEMPLATE",
            "role": "fillable leakage review response template",
            "claim_boundary": "leakage_review_package_only_no_evidence_no_scores",
        }
    )

    write_manifest(manifest_rows)

    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE_ROOT.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PACKAGE_ROOT.parent))


def main() -> None:
    build_package()
    print(f"PAPER11_LEAKAGE_AUDIT_REVIEW_PACKAGE_V59_BUILT {ZIP_PATH}")


if __name__ == "__main__":
    main()
