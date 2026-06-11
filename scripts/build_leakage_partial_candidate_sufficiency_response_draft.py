#!/usr/bin/env python3
from __future__ import annotations

import csv
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
PACKAGE_ROOT = ROOT / "review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package"
ZIP_PATH = ROOT / "review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package.zip"
CLAIM_BOUNDARY = "leakage_partial_candidate_sufficiency_response_draft_only_no_evidence_no_scores"


README = """# Leakage Partial Candidate Sufficiency v75 Response Draft Package

**Status:** response draft only; not a completed review response; not leakage
evidence; no activation; no endpoint scoring.

This package converts the v74 preaudit into a proposed v71 sufficiency review
response. The draft is shaped so that an independent reviewer can inspect,
edit, and later submit it as a completed response package if accepted.

## Reviewer Tasks

1. Inspect the preaudit evidence and every proposed sufficiency decision.
2. Edit any row that should remain blocked.
3. Only after independent review, copy the completed response into the v71
   completed-response package expected by the v73 intake.

## Hard Stops

- Do not treat this draft as a completed response.
- Do not copy this draft into `data/input/leakage_audit_evidence_v10.csv`.
- Do not authorize leakage pass, row activation, or endpoint scoring from this
  draft package.
"""


DO_NOT_INGEST = """# Do Not Ingest Without Independent Review

This package is a draft proposal generated from the v74 preaudit. It is not a
completed review response.

The v73 intake must remain blocked until an independently reviewed completed
response is placed under:

`review_packages/leakage_partial_candidate_sufficiency_v71_completed_review_response.zip`
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


def draft_response_rows() -> list[dict[str, object]]:
    preaudit = read_csv(DERIVED / "leakage_partial_candidate_sufficiency_preaudit_v74.csv")
    rows: list[dict[str, object]] = []
    for row in preaudit:
        review_ready = row["preaudit_decision"] == "PREAUDIT_REVIEW_READY_NOT_ACCEPTED"
        rows.append(
            {
                "ingestion_gate_id": row["ingestion_gate_id"],
                "candidate_id": row["candidate_id"],
                "leakage_evidence_row_id": row["leakage_evidence_row_id"],
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "evidence_id": row["evidence_id"],
                "request_family": "morphology_label_prescore_artifact_request"
                if row["evidence_id"] == "LEC10_MORPH_LABELS"
                else "benchmark_policy_prescore_artifact_request",
                "candidate_artifact_uri_or_id": row["candidate_artifact_uri_or_id"],
                "candidate_artifact_hash_or_accession": row["candidate_artifact_hash_or_accession"],
                "candidate_row_selector": row["candidate_row_selector"],
                "sufficiency_review_decision": "ACCEPT_PARTIAL_CANDIDATE_SUFFICIENT_FOR_LATER_INGESTION_GATE"
                if review_ready
                else "KEEP_BLOCKED_PARTIAL_REVIEW_REQUIRED_NOT_AUTHORIZED",
                "partial_candidate_sufficient_for_later_ingestion": str(review_ready).lower(),
                "minimal_required_fields_covered": str(review_ready).lower(),
                "artifact_is_prescore": "true",
                "artifact_uses_forbidden_inputs": "false" if review_ready else "UNKNOWN_REVIEW_REQUIRED",
                "may_promote_to_leakage_evidence_after_ingestion": str(review_ready).lower(),
                "may_activate_row_after_ingestion": "false",
                "endpoint_scoring_allowed": "false",
                "reviewer_notes": (
                    "DRAFT ONLY: v74 preaudit found source/policy artifact, selector, prescore status, inactive/not-run "
                    "status, and forbidden-input guards. Independent reviewer must confirm before completed response."
                ),
            }
        )
    return rows


def summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    proposed_accept = sum(
        row["sufficiency_review_decision"] == "ACCEPT_PARTIAL_CANDIDATE_SUFFICIENT_FOR_LATER_INGESTION_GATE"
        for row in rows
    )
    return [
        {
            "summary_id": "LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_RESPONSE_DRAFT_V75",
            "draft_rows": len(rows),
            "galaxies_covered": len({row["galaxy_id"] for row in rows}),
            "partial_evidence_components": 2,
            "proposed_accept_rows": proposed_accept,
            "proposed_block_rows": len(rows) - proposed_accept,
            "completed_response_created": "false",
            "target_evidence_rows_created": 0,
            "leakage_pass_authorized": 0,
            "activation_rows_authorized": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "DRAFT_RESPONSE_READY_FOR_INDEPENDENT_REVIEW_NOT_INGESTED",
            "next_required_artifact": "independently_reviewed_completed_leakage_partial_candidate_sufficiency_v71_response",
            "claim_boundary": "leakage_partial_candidate_sufficiency_response_draft_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def build_package() -> None:
    if PACKAGE_ROOT.exists():
        shutil.rmtree(PACKAGE_ROOT)
    PACKAGE_ROOT.mkdir(parents=True, exist_ok=True)
    write_text(PACKAGE_ROOT / "README.md", README)
    write_text(PACKAGE_ROOT / "DO_NOT_INGEST_WITHOUT_INDEPENDENT_REVIEW.md", DO_NOT_INGEST)

    rows = draft_response_rows()
    summary = summary_rows(rows)
    response_target = PACKAGE_ROOT / "templates/leakage_partial_candidate_sufficiency_v71_review_response_DRAFT.csv"
    write_csv(
        response_target,
        rows,
        [
            "ingestion_gate_id",
            "candidate_id",
            "leakage_evidence_row_id",
            "galaxy_id",
            "proposed_split",
            "evidence_id",
            "request_family",
            "candidate_artifact_uri_or_id",
            "candidate_artifact_hash_or_accession",
            "candidate_row_selector",
            "sufficiency_review_decision",
            "partial_candidate_sufficient_for_later_ingestion",
            "minimal_required_fields_covered",
            "artifact_is_prescore",
            "artifact_uses_forbidden_inputs",
            "may_promote_to_leakage_evidence_after_ingestion",
            "may_activate_row_after_ingestion",
            "endpoint_scoring_allowed",
            "reviewer_notes",
        ],
    )
    write_csv(
        PACKAGE_ROOT / "data/leakage_partial_candidate_sufficiency_response_draft_summary_v75.csv",
        summary,
        [
            "summary_id",
            "draft_rows",
            "galaxies_covered",
            "partial_evidence_components",
            "proposed_accept_rows",
            "proposed_block_rows",
            "completed_response_created",
            "target_evidence_rows_created",
            "leakage_pass_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    shutil.copyfile(
        DERIVED / "leakage_partial_candidate_sufficiency_preaudit_v74.csv",
        PACKAGE_ROOT / "data/leakage_partial_candidate_sufficiency_preaudit_v74.csv",
    )
    shutil.copyfile(
        DERIVED / "leakage_partial_candidate_sufficiency_preaudit_summary_v74.csv",
        PACKAGE_ROOT / "data/leakage_partial_candidate_sufficiency_preaudit_summary_v74.csv",
    )

    manifest_rows = [
        {
            "package_path": "README.md",
            "source_path": "generated_by_leakage_partial_candidate_sufficiency_response_draft_builder",
            "role": "draft response instructions",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "package_path": "DO_NOT_INGEST_WITHOUT_INDEPENDENT_REVIEW.md",
            "source_path": "generated_by_leakage_partial_candidate_sufficiency_response_draft_builder",
            "role": "hard-stop notice",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "package_path": "templates/leakage_partial_candidate_sufficiency_v71_review_response_DRAFT.csv",
            "source_path": "data/derived/leakage_partial_candidate_sufficiency_preaudit_v74.csv",
            "role": "proposed completed-response draft",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "package_path": "data/leakage_partial_candidate_sufficiency_response_draft_summary_v75.csv",
            "source_path": "generated_summary",
            "role": "draft response summary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "package_path": "data/leakage_partial_candidate_sufficiency_preaudit_v74.csv",
            "source_path": "data/derived/leakage_partial_candidate_sufficiency_preaudit_v74.csv",
            "role": "preaudit source rows",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "package_path": "data/leakage_partial_candidate_sufficiency_preaudit_summary_v74.csv",
            "source_path": "data/derived/leakage_partial_candidate_sufficiency_preaudit_summary_v74.csv",
            "role": "preaudit summary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(PACKAGE_ROOT / "REVIEW_MANIFEST.csv", manifest_rows, ["package_path", "source_path", "role", "claim_boundary"])

    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE_ROOT.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PACKAGE_ROOT.parent))

    write_csv(
        DERIVED / "leakage_partial_candidate_sufficiency_response_draft_summary_v75.csv",
        summary,
        [
            "summary_id",
            "draft_rows",
            "galaxies_covered",
            "partial_evidence_components",
            "proposed_accept_rows",
            "proposed_block_rows",
            "completed_response_created",
            "target_evidence_rows_created",
            "leakage_pass_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )


def main() -> None:
    build_package()
    print(f"PAPER11_LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_RESPONSE_DRAFT_V75_BUILT {ZIP_PATH}")


if __name__ == "__main__":
    main()
