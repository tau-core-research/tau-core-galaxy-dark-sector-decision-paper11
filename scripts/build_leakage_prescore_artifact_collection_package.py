#!/usr/bin/env python3
from __future__ import annotations

import csv
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
PACKAGE_ROOT = ROOT / "review_packages/leakage_prescore_artifact_v61_collection_package"
ZIP_PATH = ROOT / "review_packages/leakage_prescore_artifact_v61_collection_package.zip"
CLAIM_BOUNDARY = "leakage_prescore_artifact_collection_package_only_no_evidence_no_scores"

PACKAGE_FILES = [
    {
        "source": DERIVED / "leakage_prescore_artifact_work_order_v61.csv",
        "target": "data/leakage_prescore_artifact_work_order_v61.csv",
        "role": "72-row prescore artifact work order",
    },
    {
        "source": DERIVED / "leakage_prescore_artifact_work_order_coverage_v61.csv",
        "target": "data/leakage_prescore_artifact_work_order_coverage_v61.csv",
        "role": "coverage summary by leakage check",
    },
    {
        "source": DERIVED / "leakage_prescore_artifact_work_order_summary_v61.csv",
        "target": "data/leakage_prescore_artifact_work_order_summary_v61.csv",
        "role": "work-order summary and claim boundary",
    },
    {
        "source": DERIVED / "leakage_audit_review_response_intake_summary_v60.csv",
        "target": "data/leakage_audit_review_response_intake_summary_v60.csv",
        "role": "no-go review-response intake summary",
    },
    {
        "source": DERIVED / "leakage_audit_evidence_template_summary_v58.csv",
        "target": "data/leakage_audit_evidence_template_summary_v58.csv",
        "role": "leakage-evidence template summary",
    },
]

README = """# Leakage Prescore Artifact v61 Collection Package

**Status:** collection package only; not leakage evidence; no activation; no endpoint scoring.

This package converts the v61 leakage prescore artifact work order into a
fillable collection response. It is the next narrow handoff before any leakage
row can be promoted toward active evidence.

## Reviewer Tasks

1. Provide reviewed prescore source or protocol artifacts for each open row.
2. Confirm that each artifact predates endpoint scoring and family comparison.
3. Confirm that no artifact uses endpoint residuals, family winners, or score
   outcomes.
4. Keep `endpoint_scoring_allowed=false`; a later ingestion gate must decide
   whether any row can become leakage evidence.

## Required Artifact Families

```text
LEC10_SOURCE_ROUTE
LEC10_OBSERVED_INPUTS
LEC10_MORPH_LABELS
LEC10_BENCHMARK_INPUTS
```

## Hard Stops

- Do not treat this package as leakage evidence.
- Do not copy rows into `data/input/leakage_audit_evidence_v10.csv`.
- Do not mark leakage rows as passed from this package.
- Do not activate scoring rows or compute endpoint scores.
- Do not use endpoint residuals, model-family winners, or score outcomes as
  prescore artifact support.
"""

DO_NOT_COPY = """# Do Not Copy Without Completed Prescore Artifact Review

The files in this package are collection artifacts. The response template
defaults every row to open and non-scoring.

Rows may be considered for later leakage-evidence ingestion only after a
completed review response provides reviewed prescore artifacts and a separate
ingestion gate accepts them.
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
    rows = read_csv(DERIVED / "leakage_prescore_artifact_work_order_v61.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "work_order_id": row["work_order_id"],
                "leakage_evidence_row_id": row["leakage_evidence_row_id"],
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "evidence_id": row["evidence_id"],
                "checked_object": row["checked_object"],
                "required_prescore_artifact": row["required_prescore_artifact"],
                "current_source_artifact": row["current_source_artifact"],
                "artifact_review_decision": "KEEP_OPEN_ARTIFACT_REQUIRED_NOT_FILLED",
                "prescore_artifact_uri_or_id": "FILL_REVIEWED_PRESCORE_ARTIFACT",
                "prescore_artifact_hash_or_accession": "FILL_HASH_OR_ACCESSION",
                "artifact_is_prescore": "false",
                "artifact_uses_endpoint_residual_or_family_winner": "UNKNOWN_REVIEW_REQUIRED",
                "may_promote_to_leakage_evidence_after_ingestion": "false",
                "may_activate_row_after_ingestion": "false",
                "endpoint_scoring_allowed": "false",
                "reviewer_notes": "",
            }
        )
    return out


def build_package() -> None:
    if PACKAGE_ROOT.exists():
        shutil.rmtree(PACKAGE_ROOT)
    PACKAGE_ROOT.mkdir(parents=True, exist_ok=True)

    write_text(PACKAGE_ROOT / "README.md", README)
    write_text(PACKAGE_ROOT / "DO_NOT_COPY_WITHOUT_COMPLETED_ARTIFACT_REVIEW.md", DO_NOT_COPY)

    manifest_rows: list[dict[str, str]] = [
        {
            "package_path": "README.md",
            "source_path": "generated_by_leakage_prescore_artifact_collection_package_builder",
            "role": "collection instructions",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "package_path": "DO_NOT_COPY_WITHOUT_COMPLETED_ARTIFACT_REVIEW.md",
            "source_path": "generated_by_leakage_prescore_artifact_collection_package_builder",
            "role": "hard-stop notice",
            "claim_boundary": CLAIM_BOUNDARY,
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
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    response_target = PACKAGE_ROOT / "templates/leakage_prescore_artifact_collection_response_TEMPLATE.csv"
    write_csv(
        response_target,
        response_template_rows(),
        [
            "work_order_id",
            "leakage_evidence_row_id",
            "galaxy_id",
            "proposed_split",
            "evidence_id",
            "checked_object",
            "required_prescore_artifact",
            "current_source_artifact",
            "artifact_review_decision",
            "prescore_artifact_uri_or_id",
            "prescore_artifact_hash_or_accession",
            "artifact_is_prescore",
            "artifact_uses_endpoint_residual_or_family_winner",
            "may_promote_to_leakage_evidence_after_ingestion",
            "may_activate_row_after_ingestion",
            "endpoint_scoring_allowed",
            "reviewer_notes",
        ],
    )
    manifest_rows.append(
        {
            "package_path": "templates/leakage_prescore_artifact_collection_response_TEMPLATE.csv",
            "source_path": "generated_from_leakage_prescore_artifact_work_order_v61",
            "role": "fillable prescore artifact collection response template",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )

    write_csv(
        PACKAGE_ROOT / "REVIEW_MANIFEST.csv",
        manifest_rows,
        ["package_path", "source_path", "role", "claim_boundary"],
    )

    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE_ROOT.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PACKAGE_ROOT.parent))


def main() -> None:
    build_package()
    print(f"PAPER11_LEAKAGE_PRESCORE_ARTIFACT_COLLECTION_PACKAGE_V62_BUILT {ZIP_PATH}")


if __name__ == "__main__":
    main()
