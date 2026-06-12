#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"

FULL_COMPONENTS = {
    "LEC10_SOURCE_ROUTE",
    "LEC10_OBSERVED_INPUTS",
    "LEC10_MORPH_LABELS",
    "LEC10_BENCHMARK_INPUTS",
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


def source_observed_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(DERIVED / "leakage_evidence_candidate_ingestion_gate_v70.csv")
        if row["evidence_id"] in {"LEC10_SOURCE_ROUTE", "LEC10_OBSERVED_INPUTS"}
        and row["draft_evidence_candidate_status"] == "DRAFT_CANDIDATE_AVAILABLE_FOR_LATER_LEAKAGE_EVIDENCE_ROW"
    ]


def partial_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(DERIVED / "leakage_partial_candidate_sufficiency_review_intake_v73.csv")
        if row["evidence_id"] in {"LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"}
        and row["sufficiency_candidate_status"] == "SUFFICIENCY_ACCEPTED_FOR_LATER_LEAKAGE_EVIDENCE_INGESTION"
        and row["may_promote_to_leakage_evidence_after_ingestion"] == "true"
    ]


def normalize_row(row: dict[str, str], source_gate: str) -> dict[str, object]:
    return {
        "full_ingestion_id": row["ingestion_gate_id"].replace("LEIG70", "FLEIG76"),
        "source_gate": source_gate,
        "candidate_id": row["candidate_id"],
        "leakage_evidence_row_id": row["leakage_evidence_row_id"],
        "galaxy_id": row["galaxy_id"],
        "proposed_split": row["proposed_split"],
        "evidence_id": row["evidence_id"],
        "request_family": row["request_family"],
        "candidate_artifact_uri_or_id": row["candidate_artifact_uri_or_id"],
        "candidate_artifact_hash_or_accession": row["candidate_artifact_hash_or_accession"],
        "candidate_row_selector": row["candidate_row_selector"],
        "full_ingestion_decision": "READY_FOR_LEAKAGE_EVIDENCE_ROW_WRITE_NOT_WRITTEN",
        "full_ingestion_component_status": "FULL_COMPONENT_READY_NOT_ACTIVE_EVIDENCE",
        "target_evidence_row_written": "false",
        "leakage_pass_authorized": "false",
        "activation_rows_authorized": "0",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": "full_leakage_evidence_ingestion_gate_only_no_evidence_write_no_scores",
    }


def gate_rows() -> list[dict[str, object]]:
    rows = [normalize_row(row, "v70_source_observed_candidate") for row in source_observed_rows()]
    rows.extend(normalize_row(row, "v73_partial_sufficiency_acceptance") for row in partial_rows())
    return sorted(rows, key=lambda row: (str(row["galaxy_id"]), str(row["evidence_id"])))


def coverage_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for galaxy_id in sorted({str(row["galaxy_id"]) for row in rows}):
        subset = [row for row in rows if row["galaxy_id"] == galaxy_id]
        components = {str(row["evidence_id"]) for row in subset}
        missing = sorted(FULL_COMPONENTS - components)
        out.append(
            {
                "galaxy_id": galaxy_id,
                "ready_components": len(components),
                "required_components": len(FULL_COMPONENTS),
                "missing_components": ";".join(missing),
                "full_leakage_evidence_ingestion_ready": "true" if not missing else "false",
                "target_evidence_rows_created": 0,
                "leakage_pass_authorized": "false",
                "activation_rows_authorized": 0,
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "full_leakage_evidence_ingestion_coverage_only_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]], coverage: list[dict[str, object]]) -> list[dict[str, object]]:
    full_ready_galaxies = sum(row["full_leakage_evidence_ingestion_ready"] == "true" for row in coverage)
    return [
        {
            "summary_id": "FULL_LEAKAGE_EVIDENCE_INGESTION_GATE_V76",
            "input_artifacts": "data/derived/leakage_evidence_candidate_ingestion_gate_v70.csv;data/derived/leakage_partial_candidate_sufficiency_review_intake_v73.csv",
            "gate_rows": len(rows),
            "galaxies_covered": len(coverage),
            "ready_component_rows": len(rows),
            "galaxies_with_all_four_ready_components": full_ready_galaxies,
            "target_evidence_rows_created": 0,
            "leakage_pass_rows_authorized": 0,
            "activation_rows_authorized": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FULL_LEAKAGE_EVIDENCE_INGESTION_READY_FOR_TARGET_EVIDENCE_WRITE"
            if full_ready_galaxies == len(coverage)
            else "FULL_LEAKAGE_EVIDENCE_INGESTION_BLOCKED",
            "next_required_artifact": "leakage_audit_evidence_v10_writer_from_v76_full_ingestion_gate",
            "claim_boundary": "full_leakage_evidence_ingestion_gate_only_no_evidence_write_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = gate_rows()
    coverage = coverage_rows(rows)
    summary_rows = summary(rows, coverage)
    write_csv(
        DERIVED / "full_leakage_evidence_ingestion_gate_v76.csv",
        rows,
        [
            "full_ingestion_id",
            "source_gate",
            "candidate_id",
            "leakage_evidence_row_id",
            "galaxy_id",
            "proposed_split",
            "evidence_id",
            "request_family",
            "candidate_artifact_uri_or_id",
            "candidate_artifact_hash_or_accession",
            "candidate_row_selector",
            "full_ingestion_decision",
            "full_ingestion_component_status",
            "target_evidence_row_written",
            "leakage_pass_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "full_leakage_evidence_ingestion_coverage_v76.csv",
        coverage,
        [
            "galaxy_id",
            "ready_components",
            "required_components",
            "missing_components",
            "full_leakage_evidence_ingestion_ready",
            "target_evidence_rows_created",
            "leakage_pass_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "full_leakage_evidence_ingestion_summary_v76.csv",
        summary_rows,
        [
            "summary_id",
            "input_artifacts",
            "gate_rows",
            "galaxies_covered",
            "ready_component_rows",
            "galaxies_with_all_four_ready_components",
            "target_evidence_rows_created",
            "leakage_pass_rows_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_FULL_LEAKAGE_EVIDENCE_INGESTION_GATE_V76_BUILT")


if __name__ == "__main__":
    main()
