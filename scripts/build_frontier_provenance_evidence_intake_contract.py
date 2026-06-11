#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"

REVIEW_RULES = [
    {
        "field_name": "galaxy_id",
        "review_rule": "must_match_one_frozen_v19_manifest_galaxy_id",
        "reject_if": "missing;unknown_galaxy;duplicate_unreviewed_row",
    },
    {
        "field_name": "catalog",
        "review_rule": "must_name_primary_external_source_catalog_or_archive",
        "reject_if": "placeholder;unsourced_note;derived_from_endpoint_score",
    },
    {
        "field_name": "table_or_file",
        "review_rule": "must_identify_stable_table_file_or_release_object",
        "reject_if": "placeholder;ambiguous_file;private_unreviewed_transform",
    },
    {
        "field_name": "version_or_date",
        "review_rule": "must_record_release_version_publication_date_or_access_date",
        "reject_if": "placeholder;undated_source",
    },
    {
        "field_name": "row_id",
        "review_rule": "must_record_stable_source_row_id_or_reproducible_row_selector",
        "reject_if": "placeholder;non_reproducible_manual_pick",
    },
    {
        "field_name": "sha256_or_external_accession",
        "review_rule": "must_record_sha256_for_local_source_file_or_external_accession",
        "reject_if": "placeholder;unverifiable_source_identity",
    },
    {
        "field_name": "source_route",
        "review_rule": "must_record_reproducible_pre_score_source_route",
        "reject_if": "placeholder;uses_rotation_residual_or_family_score;not_reproducible",
    },
    {
        "field_name": "leakage_evidence_id",
        "review_rule": "must_link_to_pre_score_leakage_evidence_or_blindness_audit_id",
        "reject_if": "placeholder;post_score_selection;missing_blindness_link",
    },
    {
        "field_name": "provenance_evidence_status",
        "review_rule": "must_equal_PROVENANCE_EVIDENCE_COMPLETE_only_after_review",
        "reject_if": "template_status;incomplete_review;unreviewed_complete_claim",
    },
]


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


def rule_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": f"FPEIC44_RULE_{index:03d}",
            "target_evidence_file": "data/input/source_import_provenance_evidence_v21.csv",
            "field_name": rule["field_name"],
            "review_rule": rule["review_rule"],
            "reject_if": rule["reject_if"],
            "required_before_promotion": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "frontier_evidence_intake_contract_rule_only_no_source_claim",
        }
        for index, rule in enumerate(REVIEW_RULES, start=1)
    ]


def row_checklist() -> list[dict[str, object]]:
    work_orders = read_csv(DERIVED / "post_writer_frontier_work_order_recheck_v43.csv")
    rows: list[dict[str, object]] = []
    for index, row in enumerate(work_orders, start=1):
        rows.append(
            {
                "checklist_id": f"FPEIC44_ROW_{index:03d}",
                "galaxy_id": row["galaxy_id"],
                "work_order_recheck_source": "data/derived/post_writer_frontier_work_order_recheck_v43.csv",
                "target_evidence_file": row["target_evidence_artifact"],
                "required_review_fields": ";".join(rule["field_name"] for rule in REVIEW_RULES),
                "manual_collection_status": "READY_FOR_REVIEWED_SOURCE_COLLECTION",
                "may_copy_template_to_evidence_input": "true",
                "may_mark_complete_without_review": "false",
                "may_promote_after_contract_only": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "frontier_evidence_intake_checklist_only_no_evidence_no_scores",
            }
        )
    return rows


def summary(rule_rows_: list[dict[str, object]], checklist_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "FRONTIER_PROVENANCE_EVIDENCE_INTAKE_CONTRACT_V44",
            "target_evidence_file": "data/input/source_import_provenance_evidence_v21.csv",
            "review_rule_rows": len(rule_rows_),
            "row_checklist_rows": len(checklist_rows),
            "manual_collection_ready_rows": len(checklist_rows),
            "evidence_rows_created_by_contract": "0",
            "promotion_allowed_by_contract_only": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_EVIDENCE_INTAKE_CONTRACT_READY_NOT_EVIDENCE",
            "claim_boundary": "frontier_evidence_intake_contract_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rules = rule_rows()
    checklist = row_checklist()
    write_csv(
        DERIVED / "frontier_provenance_evidence_intake_contract_v44.csv",
        rules,
        [
            "contract_id",
            "target_evidence_file",
            "field_name",
            "review_rule",
            "reject_if",
            "required_before_promotion",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "frontier_provenance_evidence_intake_checklist_v44.csv",
        checklist,
        [
            "checklist_id",
            "galaxy_id",
            "work_order_recheck_source",
            "target_evidence_file",
            "required_review_fields",
            "manual_collection_status",
            "may_copy_template_to_evidence_input",
            "may_mark_complete_without_review",
            "may_promote_after_contract_only",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "frontier_provenance_evidence_intake_contract_summary_v44.csv",
        summary(rules, checklist),
        [
            "summary_id",
            "target_evidence_file",
            "review_rule_rows",
            "row_checklist_rows",
            "manual_collection_ready_rows",
            "evidence_rows_created_by_contract",
            "promotion_allowed_by_contract_only",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_FRONTIER_PROVENANCE_EVIDENCE_INTAKE_CONTRACT_V44_BUILT")


if __name__ == "__main__":
    main()
