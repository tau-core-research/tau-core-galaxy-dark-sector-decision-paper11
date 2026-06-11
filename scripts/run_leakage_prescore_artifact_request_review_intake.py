#!/usr/bin/env python3
from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
PACKAGE_ROOT = ROOT / "review_packages/leakage_prescore_artifact_request_v64_review_package"
RESPONSE_DIR = ROOT / "review_packages/leakage_prescore_artifact_request_v64_completed_review_response"
RESPONSE_ZIP = ROOT / "review_packages/leakage_prescore_artifact_request_v64_completed_review_response.zip"
RESPONSE_CSV = "leakage_prescore_artifact_request_v64_review_response.csv"
REQUIRED_RESPONSE_FILES = {
    RESPONSE_CSV,
    "leakage_prescore_artifact_request_v64_review_completed_summary.csv",
    "leakage_prescore_artifact_request_v64_review_notes.md",
    "leakage_prescore_artifact_request_v64_review_validation_log.txt",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def response_files_present() -> int:
    present = sum((RESPONSE_DIR / name).exists() for name in REQUIRED_RESPONSE_FILES)
    if RESPONSE_ZIP.exists():
        with zipfile.ZipFile(RESPONSE_ZIP) as archive:
            names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
        present = max(present, len(names & REQUIRED_RESPONSE_FILES))
    return present


def source_rows() -> tuple[list[dict[str, str]], str]:
    response_path = RESPONSE_DIR / RESPONSE_CSV
    if response_path.exists():
        return read_csv(response_path), "completed_response"
    return (
        read_csv(PACKAGE_ROOT / "templates/leakage_prescore_artifact_request_review_response_TEMPLATE.csv"),
        "template_absent_completed_response",
    )


def candidate_acceptance(row: dict[str, str], source_mode: str) -> tuple[str, str]:
    if source_mode != "completed_response":
        return (
            "BLOCKED_COMPLETED_PRESCORE_REQUEST_REVIEW_RESPONSE_ABSENT",
            "NOT_CANDIDATE_COMPLETED_RESPONSE_ABSENT",
        )
    artifact_reviewed = row["artifact_review_decision"] == "PRESCORE_ARTIFACT_REVIEWED_ACCEPT"
    fields_covered = row["minimal_required_fields_covered"] == "true"
    artifact_prescore = row["artifact_is_prescore"] == "true"
    no_forbidden_inputs = row["artifact_uses_forbidden_inputs"] == "false"
    promotable = row["may_promote_to_leakage_evidence_after_ingestion"] == "true"
    no_activation = row["may_activate_row_after_ingestion"] == "false"
    no_scoring = row["endpoint_scoring_allowed"] == "false"
    filled_uri = row["prescore_artifact_uri_or_id"] not in {
        "FILL_REVIEWED_PRESCORE_ARTIFACT",
        "PRESCORE_ARTIFACT_NOT_PROVIDED_IN_V64_PACKAGE",
    }
    filled_hash = row["prescore_artifact_hash_or_accession"] not in {
        "FILL_HASH_OR_ACCESSION",
        "HASH_OR_ACCESSION_NOT_PROVIDED_IN_V64_PACKAGE",
    }
    if all(
        [
            artifact_reviewed,
            fields_covered,
            artifact_prescore,
            no_forbidden_inputs,
            promotable,
            no_activation,
            no_scoring,
            filled_uri,
            filled_hash,
        ]
    ):
        return (
            "ACCEPT_AS_PRESCORE_REQUEST_CANDIDATE_NOT_EVIDENCE",
            "CANDIDATE_FOR_LATER_LEAKAGE_EVIDENCE_INGESTION",
        )
    return (
        "BLOCKED_PRESCORE_REQUEST_REVIEW_INCOMPLETE_OR_UNSAFE",
        "NOT_CANDIDATE_REVIEW_INCOMPLETE_OR_UNSAFE",
    )


def intake_rows() -> list[dict[str, object]]:
    rows, source_mode = source_rows()
    out: list[dict[str, object]] = []
    for row in rows:
        intake_decision, candidate_status = candidate_acceptance(row, source_mode)
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
                "prescore_artifact_uri_or_id": row["prescore_artifact_uri_or_id"],
                "prescore_artifact_hash_or_accession": row["prescore_artifact_hash_or_accession"],
                "artifact_review_decision": row["artifact_review_decision"],
                "minimal_required_fields_covered": row["minimal_required_fields_covered"],
                "artifact_is_prescore": row["artifact_is_prescore"],
                "artifact_uses_forbidden_inputs": row["artifact_uses_forbidden_inputs"],
                "may_promote_to_leakage_evidence_after_ingestion": row[
                    "may_promote_to_leakage_evidence_after_ingestion"
                ],
                "may_activate_row_after_ingestion": row["may_activate_row_after_ingestion"],
                "endpoint_scoring_allowed": row["endpoint_scoring_allowed"],
                "source_mode": source_mode,
                "intake_decision": intake_decision,
                "leakage_evidence_candidate_status": candidate_status,
                "claim_boundary": "leakage_prescore_artifact_request_review_intake_only_no_evidence_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    candidate_rows = sum(
        row["leakage_evidence_candidate_status"] == "CANDIDATE_FOR_LATER_LEAKAGE_EVIDENCE_INGESTION" for row in rows
    )
    blocked_rows = len(rows) - candidate_rows
    response_files = response_files_present()
    response_present = response_files == len(REQUIRED_RESPONSE_FILES)
    all_candidates = response_present and candidate_rows == len(rows)
    return [
        {
            "summary_id": "LEAKAGE_PRESCORE_ARTIFACT_REQUEST_REVIEW_INTAKE_V66",
            "response_zip": "review_packages/leakage_prescore_artifact_request_v64_completed_review_response.zip",
            "response_files_present": response_files,
            "intake_rows": len(rows),
            "galaxies_covered": len({row["galaxy_id"] for row in rows}),
            "evidence_checks_per_galaxy": 4,
            "completed_response_present": str(response_present).lower(),
            "candidate_rows_for_later_leakage_evidence": candidate_rows,
            "blocked_or_missing_rows": blocked_rows,
            "leakage_evidence_rows_created": 0,
            "activation_rows_authorized": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PRESCORE_REQUEST_REVIEW_READY_FOR_LATER_LEAKAGE_EVIDENCE_GATE"
            if all_candidates
            else "PRESCORE_REQUEST_REVIEW_RESPONSE_PRESENT_BUT_BLOCKED"
            if response_present
            else "PRESCORE_REQUEST_REVIEW_RESPONSE_BLOCKED_OR_ABSENT",
            "next_required_artifact": "completed_prescore_artifact_response_with_uri_hash_or_accession_for_each_open_request"
            if not all_candidates
            else "data/input/leakage_audit_evidence_v10.csv",
            "claim_boundary": "leakage_prescore_artifact_request_review_intake_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = intake_rows()
    write_csv(
        DERIVED / "leakage_prescore_artifact_request_review_intake_v66.csv",
        rows,
        [
            "request_id",
            "work_order_id",
            "leakage_evidence_row_id",
            "galaxy_id",
            "proposed_split",
            "evidence_id",
            "checked_object",
            "request_family",
            "prescore_artifact_uri_or_id",
            "prescore_artifact_hash_or_accession",
            "artifact_review_decision",
            "minimal_required_fields_covered",
            "artifact_is_prescore",
            "artifact_uses_forbidden_inputs",
            "may_promote_to_leakage_evidence_after_ingestion",
            "may_activate_row_after_ingestion",
            "endpoint_scoring_allowed",
            "source_mode",
            "intake_decision",
            "leakage_evidence_candidate_status",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_prescore_artifact_request_review_intake_summary_v66.csv",
        summary(rows),
        [
            "summary_id",
            "response_zip",
            "response_files_present",
            "intake_rows",
            "galaxies_covered",
            "evidence_checks_per_galaxy",
            "completed_response_present",
            "candidate_rows_for_later_leakage_evidence",
            "blocked_or_missing_rows",
            "leakage_evidence_rows_created",
            "activation_rows_authorized",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_LEAKAGE_PRESCORE_ARTIFACT_REQUEST_REVIEW_INTAKE_V66_BUILT")


if __name__ == "__main__":
    main()
