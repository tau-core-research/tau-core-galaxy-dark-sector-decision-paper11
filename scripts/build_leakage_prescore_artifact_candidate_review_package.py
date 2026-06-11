#!/usr/bin/env python3
from __future__ import annotations

import csv
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
PACKAGE_ROOT = ROOT / "review_packages/leakage_prescore_artifact_candidate_v67_review_package"
ZIP_PATH = ROOT / "review_packages/leakage_prescore_artifact_candidate_v67_review_package.zip"
CLAIM_BOUNDARY = "leakage_prescore_artifact_candidate_review_package_only_no_evidence_no_scores"

PACKAGE_FILES = [
    {
        "source": DERIVED / "leakage_prescore_artifact_candidate_ledger_v67.csv",
        "target": "data/leakage_prescore_artifact_candidate_ledger_v67.csv",
        "role": "72-row prescore artifact candidate ledger",
    },
    {
        "source": DERIVED / "leakage_prescore_artifact_candidate_coverage_v67.csv",
        "target": "data/leakage_prescore_artifact_candidate_coverage_v67.csv",
        "role": "candidate coverage by leakage check",
    },
    {
        "source": DERIVED / "leakage_prescore_artifact_candidate_summary_v67.csv",
        "target": "data/leakage_prescore_artifact_candidate_summary_v67.csv",
        "role": "candidate-ledger summary and claim boundary",
    },
    {
        "source": DERIVED / "leakage_prescore_artifact_request_review_intake_summary_v66.csv",
        "target": "data/leakage_prescore_artifact_request_review_intake_summary_v66.csv",
        "role": "completed request-review no-go intake summary",
    },
]

README = """# Leakage Prescore Artifact Candidate v67 Review Package

**Status:** candidate review package only; not leakage evidence; no activation; no endpoint scoring.

This package converts the v67 candidate ledger into a fillable response
template. It asks reviewers to accept or reject each candidate artifact before
any later leakage-evidence ingestion gate may consider it.

## Reviewer Tasks

1. Review the proposed candidate artifact URI/id and hash/accession.
2. Confirm whether the candidate covers the minimal required fields.
3. Confirm whether the candidate is prescore and uses no forbidden inputs.
4. Mark whether the row may become a leakage-evidence candidate after a later
   ingestion gate. Keep activation and endpoint scoring disabled.

## Hard Stops

- Do not treat this package as active leakage evidence.
- Do not copy rows into `data/input/leakage_audit_evidence_v10.csv`.
- Do not mark leakage rows as passed from this package.
- Do not activate scoring rows or compute endpoint scores.
"""

DO_NOT_COPY = """# Do Not Copy Without Completed Candidate Review

The files in this package are candidate-review artifacts. The response template
defaults every row to review-required and non-scoring.

Rows may be considered for later leakage-evidence ingestion only after a
completed candidate review response accepts them and a separate ingestion gate
validates that response.
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
    rows = read_csv(DERIVED / "leakage_prescore_artifact_candidate_ledger_v67.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "candidate_id": row["candidate_id"],
                "request_id": row["request_id"],
                "work_order_id": row["work_order_id"],
                "leakage_evidence_row_id": row["leakage_evidence_row_id"],
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "evidence_id": row["evidence_id"],
                "request_family": row["request_family"],
                "candidate_artifact_uri_or_id": row["candidate_artifact_uri_or_id"],
                "candidate_artifact_hash_or_accession": row["candidate_artifact_hash_or_accession"],
                "candidate_row_selector": row["candidate_row_selector"],
                "candidate_support_detail": row["candidate_support_detail"],
                "candidate_review_status": row["candidate_review_status"],
                "candidate_limitation": row["candidate_limitation"],
                "candidate_review_decision": "KEEP_REVIEW_REQUIRED_NOT_AUTHORIZED",
                "candidate_artifact_accepted": "false",
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
    write_text(PACKAGE_ROOT / "DO_NOT_COPY_WITHOUT_COMPLETED_CANDIDATE_REVIEW.md", DO_NOT_COPY)

    manifest_rows: list[dict[str, str]] = [
        {
            "package_path": "README.md",
            "source_path": "generated_by_leakage_prescore_artifact_candidate_review_package_builder",
            "role": "review instructions",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "package_path": "DO_NOT_COPY_WITHOUT_COMPLETED_CANDIDATE_REVIEW.md",
            "source_path": "generated_by_leakage_prescore_artifact_candidate_review_package_builder",
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

    response_target = PACKAGE_ROOT / "templates/leakage_prescore_artifact_candidate_review_response_TEMPLATE.csv"
    write_csv(
        response_target,
        response_template_rows(),
        [
            "candidate_id",
            "request_id",
            "work_order_id",
            "leakage_evidence_row_id",
            "galaxy_id",
            "proposed_split",
            "evidence_id",
            "request_family",
            "candidate_artifact_uri_or_id",
            "candidate_artifact_hash_or_accession",
            "candidate_row_selector",
            "candidate_support_detail",
            "candidate_review_status",
            "candidate_limitation",
            "candidate_review_decision",
            "candidate_artifact_accepted",
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
            "package_path": "templates/leakage_prescore_artifact_candidate_review_response_TEMPLATE.csv",
            "source_path": "generated_from_leakage_prescore_artifact_candidate_ledger_v67",
            "role": "fillable prescore artifact candidate review response template",
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
    print(f"PAPER11_LEAKAGE_PRESCORE_ARTIFACT_CANDIDATE_REVIEW_PACKAGE_V68_BUILT {ZIP_PATH}")


if __name__ == "__main__":
    main()
