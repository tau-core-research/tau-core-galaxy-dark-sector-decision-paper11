#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"

REQUEST_RULES = {
    "LEC10_SOURCE_ROUTE": {
        "request_family": "source_route_prescore_artifact_request",
        "minimal_required_fields": "source_catalog;source_file_or_release;row_selector;source_route;sha256_or_accession",
        "candidate_source_artifact_family": "SPARC_table_or_release_route_plus_hash",
        "forbidden_inputs": "endpoint_residual;family_winner;best_fit_score;post_score_selection",
        "review_question": "Can the galaxy source route be reproduced without endpoint residuals or family comparison?",
    },
    "LEC10_OBSERVED_INPUTS": {
        "request_family": "observed_input_prescore_artifact_request",
        "minimal_required_fields": "raw_input_file;import_script_or_gate;row_count;unit_contract;sha256_or_accession",
        "candidate_source_artifact_family": "v15_raw_input_plus_v12_authorized_writer_gate",
        "forbidden_inputs": "endpoint_residual;family_winner;score_weight;post_score_filter",
        "review_question": "Were observed inputs imported from source-side files before endpoint scoring?",
    },
    "LEC10_MORPH_LABELS": {
        "request_family": "morphology_label_prescore_artifact_request",
        "minimal_required_fields": "label_source;label_rule;freeze_artifact;row_selector;sha256_or_accession",
        "candidate_source_artifact_family": "pre_score_morphology_or_readout_label_freeze",
        "forbidden_inputs": "endpoint_residual;family_winner;score_outcome;post_score_relabeling",
        "review_question": "Were morphology/readout labels frozen independently of model-family outcomes?",
    },
    "LEC10_BENCHMARK_INPUTS": {
        "request_family": "benchmark_policy_prescore_artifact_request",
        "minimal_required_fields": "benchmark_policy;control_policy;freeze_artifact;version_or_commit;sha256_or_accession",
        "candidate_source_artifact_family": "pre_score_benchmark_policy_and_control_freeze",
        "forbidden_inputs": "endpoint_residual;family_winner;best_fit_score;post_score_threshold_tuning",
        "review_question": "Were benchmark/profile/control policies frozen before family comparison?",
    },
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


def ledger_rows() -> list[dict[str, object]]:
    intake = read_csv(DERIVED / "leakage_prescore_artifact_collection_intake_v63.csv")
    out: list[dict[str, object]] = []
    for index, row in enumerate(intake, start=1):
        rule = REQUEST_RULES[row["evidence_id"]]
        still_open = row["leakage_evidence_candidate_status"] != "CANDIDATE_FOR_LATER_LEAKAGE_EVIDENCE_INGESTION"
        out.append(
            {
                "request_id": f"LPAR64_{index:03d}",
                "work_order_id": row["work_order_id"],
                "leakage_evidence_row_id": row["leakage_evidence_row_id"],
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "evidence_id": row["evidence_id"],
                "checked_object": row["checked_object"],
                "request_family": rule["request_family"],
                "required_prescore_artifact": row["required_prescore_artifact"],
                "minimal_required_fields": rule["minimal_required_fields"],
                "candidate_source_artifact_family": rule["candidate_source_artifact_family"],
                "forbidden_inputs": rule["forbidden_inputs"],
                "review_question": rule["review_question"],
                "current_v63_status": row["leakage_evidence_candidate_status"],
                "request_status": "OPEN_REVIEWED_PRESCORE_ARTIFACT_REQUIRED" if still_open else "ALREADY_CANDIDATE_NO_REQUEST",
                "may_create_leakage_evidence_from_request": "false",
                "may_activate_row_from_request": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "leakage_prescore_artifact_request_ledger_only_no_evidence_no_scores",
            }
        )
    return out


def coverage_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for evidence_id in sorted(REQUEST_RULES):
        subset = [row for row in rows if row["evidence_id"] == evidence_id]
        open_rows = sum(row["request_status"] == "OPEN_REVIEWED_PRESCORE_ARTIFACT_REQUIRED" for row in subset)
        rule = REQUEST_RULES[evidence_id]
        out.append(
            {
                "coverage_id": f"LPAR64_{evidence_id}",
                "evidence_id": evidence_id,
                "request_family": rule["request_family"],
                "request_rows": len(subset),
                "open_request_rows": open_rows,
                "candidate_rows_already_available": len(subset) - open_rows,
                "minimal_required_fields": rule["minimal_required_fields"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "leakage_prescore_artifact_request_coverage_only_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    open_rows = sum(row["request_status"] == "OPEN_REVIEWED_PRESCORE_ARTIFACT_REQUIRED" for row in rows)
    return [
        {
            "summary_id": "LEAKAGE_PRESCORE_ARTIFACT_REQUEST_LEDGER_V64",
            "request_rows": len(rows),
            "galaxies_covered": len({row["galaxy_id"] for row in rows}),
            "evidence_checks_per_galaxy": 4,
            "open_request_rows": open_rows,
            "candidate_rows_already_available": len(rows) - open_rows,
            "leakage_evidence_rows_created": 0,
            "activation_rows_authorized": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PRESCORE_ARTIFACT_REQUEST_LEDGER_OPEN",
            "next_required_artifact": "completed_prescore_artifact_response_with_uri_hash_or_accession_for_each_open_request",
            "claim_boundary": "leakage_prescore_artifact_request_ledger_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = ledger_rows()
    coverage = coverage_rows(rows)
    write_csv(
        DERIVED / "leakage_prescore_artifact_request_ledger_v64.csv",
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
            "required_prescore_artifact",
            "minimal_required_fields",
            "candidate_source_artifact_family",
            "forbidden_inputs",
            "review_question",
            "current_v63_status",
            "request_status",
            "may_create_leakage_evidence_from_request",
            "may_activate_row_from_request",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_prescore_artifact_request_coverage_v64.csv",
        coverage,
        [
            "coverage_id",
            "evidence_id",
            "request_family",
            "request_rows",
            "open_request_rows",
            "candidate_rows_already_available",
            "minimal_required_fields",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_prescore_artifact_request_summary_v64.csv",
        summary(rows),
        [
            "summary_id",
            "request_rows",
            "galaxies_covered",
            "evidence_checks_per_galaxy",
            "open_request_rows",
            "candidate_rows_already_available",
            "leakage_evidence_rows_created",
            "activation_rows_authorized",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_LEAKAGE_PRESCORE_ARTIFACT_REQUEST_LEDGER_V64_BUILT")


if __name__ == "__main__":
    main()
