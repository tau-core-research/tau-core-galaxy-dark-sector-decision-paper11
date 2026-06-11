#!/usr/bin/env python3
from __future__ import annotations

import csv
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
PACKAGE_ROOT = ROOT / "review_packages/leakage_prescore_artifact_request_v64_review_package"
ZIP_PATH = ROOT / "review_packages/leakage_prescore_artifact_request_v64_review_package.zip"
CLAIM_BOUNDARY = "leakage_prescore_artifact_request_review_package_only_no_evidence_no_scores"

PACKAGE_FILES = [
    {
        "source": DERIVED / "leakage_prescore_artifact_request_ledger_v64.csv",
        "target": "data/leakage_prescore_artifact_request_ledger_v64.csv",
        "role": "72-row prescore artifact request ledger",
    },
    {
        "source": DERIVED / "leakage_prescore_artifact_request_coverage_v64.csv",
        "target": "data/leakage_prescore_artifact_request_coverage_v64.csv",
        "role": "request coverage by leakage check",
    },
    {
        "source": DERIVED / "leakage_prescore_artifact_request_summary_v64.csv",
        "target": "data/leakage_prescore_artifact_request_summary_v64.csv",
        "role": "request-ledger summary and claim boundary",
    },
    {
        "source": DERIVED / "leakage_prescore_artifact_collection_intake_summary_v63.csv",
        "target": "data/leakage_prescore_artifact_collection_intake_summary_v63.csv",
        "role": "completed collection no-go intake summary",
    },
]

README = """# Leakage Prescore Artifact Request v64 Review Package

**Status:** review package only; not leakage evidence; no activation; no endpoint scoring.

This package converts the v64 request ledger into a fillable response template.
It asks reviewers to provide reviewed prescore artifact identifiers and
hash/accession values for each open LEC10 row.

## Reviewer Tasks

1. Fill the requested prescore artifact URI/id and hash/accession.
2. Verify that all minimal required fields are covered.
3. Confirm the artifact is prescore and does not use endpoint residuals, family
   winners, best-fit scores, or post-score selections.
4. Keep activation and endpoint scoring disabled. A later ingestion gate must
   decide whether any row can become leakage evidence.

## Hard Stops

- Do not treat this package as active leakage evidence.
- Do not copy rows into `data/input/leakage_audit_evidence_v10.csv`.
- Do not mark leakage rows as passed from this package.
- Do not activate scoring rows or compute endpoint scores.
"""

DO_NOT_COPY = """# Do Not Copy Without Completed Request Review

The files in this package are request-review artifacts. The response template
defaults every row to open and non-scoring.

Rows may be considered for later leakage-evidence ingestion only after a
completed review response supplies reviewed prescore artifacts and a separate
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
    rows = read_csv(DERIVED / "leakage_prescore_artifact_request_ledger_v64.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "request_id": row["request_id"],
                "work_order_id": row["work_order_id"],
                "leakage_evidence_row_id": row["leakage_evidence_row_id"],
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "evidence_id": row["evidence_id"],
                "checked_object": row["checked_object"],
                "request_family": row["request_family"],
                "required_prescore_artifact": row["required_prescore_artifact"],
                "minimal_required_fields": row["minimal_required_fields"],
                "forbidden_inputs": row["forbidden_inputs"],
                "review_question": row["review_question"],
                "artifact_review_decision": "KEEP_OPEN_REVIEWED_PRESCORE_ARTIFACT_REQUIRED_NOT_FILLED",
                "prescore_artifact_uri_or_id": "FILL_REVIEWED_PRESCORE_ARTIFACT",
                "prescore_artifact_hash_or_accession": "FILL_HASH_OR_ACCESSION",
                "minimal_required_fields_covered": "false",
                "artifact_is_prescore": "false",
                "artifact_uses_forbidden_inputs": "UNKNOWN_REVIEW_REQUIRED",
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
    write_text(PACKAGE_ROOT / "DO_NOT_COPY_WITHOUT_COMPLETED_REQUEST_REVIEW.md", DO_NOT_COPY)

    manifest_rows: list[dict[str, str]] = [
        {
            "package_path": "README.md",
            "source_path": "generated_by_leakage_prescore_artifact_request_review_package_builder",
            "role": "review instructions",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "package_path": "DO_NOT_COPY_WITHOUT_COMPLETED_REQUEST_REVIEW.md",
            "source_path": "generated_by_leakage_prescore_artifact_request_review_package_builder",
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

    response_target = PACKAGE_ROOT / "templates/leakage_prescore_artifact_request_review_response_TEMPLATE.csv"
    write_csv(
        response_target,
        response_template_rows(),
        [
            "request_id",
            "work_order_id",
            "leakage_evidence_row_id",
            "galaxy_id",
            "proposed_split",
            "evidence_id",
            "checked_object",
            "request_family",
            "required_prescore_artifact",
            "minimal_required_fields",
            "forbidden_inputs",
            "review_question",
            "artifact_review_decision",
            "prescore_artifact_uri_or_id",
            "prescore_artifact_hash_or_accession",
            "minimal_required_fields_covered",
            "artifact_is_prescore",
            "artifact_uses_forbidden_inputs",
            "may_promote_to_leakage_evidence_after_ingestion",
            "may_activate_row_after_ingestion",
            "endpoint_scoring_allowed",
            "reviewer_notes",
        ],
    )
    manifest_rows.append(
        {
            "package_path": "templates/leakage_prescore_artifact_request_review_response_TEMPLATE.csv",
            "source_path": "generated_from_leakage_prescore_artifact_request_ledger_v64",
            "role": "fillable prescore artifact request review response template",
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
    print(f"PAPER11_LEAKAGE_PRESCORE_ARTIFACT_REQUEST_REVIEW_PACKAGE_V65_BUILT {ZIP_PATH}")


if __name__ == "__main__":
    main()
