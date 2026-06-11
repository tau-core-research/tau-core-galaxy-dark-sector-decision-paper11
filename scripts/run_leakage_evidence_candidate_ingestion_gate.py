#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"


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


def gate_decision(row: dict[str, str]) -> tuple[str, str, str]:
    accepted = row["leakage_evidence_candidate_status"] == "CANDIDATE_FOR_LATER_LEAKAGE_EVIDENCE_INGESTION"
    if accepted:
        return (
            "ACCEPT_AS_LEAKAGE_EVIDENCE_DRAFT_CANDIDATE_NOT_IMPORTED",
            "DRAFT_CANDIDATE_AVAILABLE_FOR_LATER_LEAKAGE_EVIDENCE_ROW",
            "accepted prescore candidate may be considered by a later evidence writer, but this gate creates no active evidence",
        )
    return (
        "BLOCKED_PARTIAL_CANDIDATE_NOT_INGESTED",
        "NOT_AVAILABLE_FOR_LEAKAGE_EVIDENCE_ROW",
        "partial candidate still requires sufficiency review before evidence ingestion",
    )


def gate_rows() -> list[dict[str, object]]:
    rows = read_csv(DERIVED / "leakage_prescore_artifact_candidate_review_intake_v69.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        decision, status, note = gate_decision(row)
        out.append(
            {
                "ingestion_gate_id": row["candidate_id"].replace("LPAC67", "LEIG70"),
                "candidate_id": row["candidate_id"],
                "leakage_evidence_row_id": row["leakage_evidence_row_id"],
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "evidence_id": row["evidence_id"],
                "request_family": row["request_family"],
                "candidate_artifact_uri_or_id": row["candidate_artifact_uri_or_id"],
                "candidate_artifact_hash_or_accession": row["candidate_artifact_hash_or_accession"],
                "candidate_row_selector": row["candidate_row_selector"],
                "v69_candidate_status": row["leakage_evidence_candidate_status"],
                "ingestion_gate_decision": decision,
                "draft_evidence_candidate_status": status,
                "target_evidence_file_written": "false",
                "leakage_pass_authorized": "false",
                "activation_rows_authorized": "0",
                "endpoint_scoring_allowed": "false",
                "gate_note": note,
                "claim_boundary": "leakage_evidence_candidate_ingestion_gate_only_no_evidence_no_scores_no_dark_sector_verdict",
            }
        )
    return out


def coverage_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for evidence_id in sorted({str(row["evidence_id"]) for row in rows}):
        subset = [row for row in rows if row["evidence_id"] == evidence_id]
        accepted = [
            row
            for row in subset
            if row["draft_evidence_candidate_status"] == "DRAFT_CANDIDATE_AVAILABLE_FOR_LATER_LEAKAGE_EVIDENCE_ROW"
        ]
        out.append(
            {
                "evidence_id": evidence_id,
                "candidate_rows": len(subset),
                "draft_available_rows": len(accepted),
                "blocked_rows": len(subset) - len(accepted),
                "target_evidence_rows_created": 0,
                "leakage_pass_rows_authorized": 0,
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "leakage_evidence_candidate_ingestion_coverage_only_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    draft_rows = [
        row
        for row in rows
        if row["draft_evidence_candidate_status"] == "DRAFT_CANDIDATE_AVAILABLE_FOR_LATER_LEAKAGE_EVIDENCE_ROW"
    ]
    blocked_rows = len(rows) - len(draft_rows)
    per_galaxy: dict[str, set[str]] = {}
    for row in draft_rows:
        per_galaxy.setdefault(str(row["galaxy_id"]), set()).add(str(row["evidence_id"]))
    galaxies_with_source_and_observed = sum(
        {"LEC10_SOURCE_ROUTE", "LEC10_OBSERVED_INPUTS"}.issubset(evidence_ids)
        for evidence_ids in per_galaxy.values()
    )
    galaxies_with_all_four = sum(
        {
            "LEC10_SOURCE_ROUTE",
            "LEC10_OBSERVED_INPUTS",
            "LEC10_MORPH_LABELS",
            "LEC10_BENCHMARK_INPUTS",
        }.issubset(evidence_ids)
        for evidence_ids in per_galaxy.values()
    )
    return [
        {
            "summary_id": "LEAKAGE_EVIDENCE_CANDIDATE_INGESTION_GATE_V70",
            "input_artifact": "data/derived/leakage_prescore_artifact_candidate_review_intake_v69.csv",
            "gate_rows": len(rows),
            "galaxies_covered": len({row["galaxy_id"] for row in rows}),
            "draft_evidence_candidate_rows": len(draft_rows),
            "blocked_partial_rows": blocked_rows,
            "galaxies_with_source_and_observed_candidates": galaxies_with_source_and_observed,
            "galaxies_with_all_four_evidence_candidates": galaxies_with_all_four,
            "target_evidence_rows_created": 0,
            "leakage_pass_rows_authorized": 0,
            "activation_rows_authorized": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "LEAKAGE_EVIDENCE_INGESTION_GATE_PARTIAL_READY_STILL_BLOCKED",
            "next_required_artifact": "partial_candidate_sufficiency_review_or_minimum_leakage_policy_decision",
            "claim_boundary": "leakage_evidence_candidate_ingestion_gate_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = gate_rows()
    coverage = coverage_rows(rows)
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "leakage_evidence_candidate_ingestion_gate_v70.csv",
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
            "v69_candidate_status",
            "ingestion_gate_decision",
            "draft_evidence_candidate_status",
            "target_evidence_file_written",
            "leakage_pass_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed",
            "gate_note",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_evidence_candidate_ingestion_coverage_v70.csv",
        coverage,
        [
            "evidence_id",
            "candidate_rows",
            "draft_available_rows",
            "blocked_rows",
            "target_evidence_rows_created",
            "leakage_pass_rows_authorized",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_evidence_candidate_ingestion_summary_v70.csv",
        summary_rows,
        [
            "summary_id",
            "input_artifact",
            "gate_rows",
            "galaxies_covered",
            "draft_evidence_candidate_rows",
            "blocked_partial_rows",
            "galaxies_with_source_and_observed_candidates",
            "galaxies_with_all_four_evidence_candidates",
            "target_evidence_rows_created",
            "leakage_pass_rows_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_LEAKAGE_EVIDENCE_CANDIDATE_INGESTION_GATE_V70_BUILT")


if __name__ == "__main__":
    main()
