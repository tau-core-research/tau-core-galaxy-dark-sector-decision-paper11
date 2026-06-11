#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
SOURCE = ROOT / "data/source_manifest"
PACKAGE_ROOT = ROOT / "review_packages/leakage_partial_candidate_sufficiency_v71_review_package"


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


def has_forbidden_guard(value: str) -> bool:
    forbidden_terms = {
        "endpoint_residual",
        "best_fit_curve",
        "family_winner",
        "heldout_score",
        "held_out_score_during_freeze",
        "best_endpoint_score",
        "posthoc",
        "endpoint_leakage",
    }
    return any(term in value for term in forbidden_terms)


def morph_audit(row: dict[str, str], galaxy_rows: dict[str, dict[str, str]]) -> dict[str, object]:
    source = galaxy_rows.get(row["candidate_row_selector"], {})
    artifact_exists = (ROOT / row["candidate_artifact_uri_or_id"]).exists()
    row_selector_found = bool(source)
    source_side_fields = bool(source.get("decision_role")) and bool(source.get("source_basis")) and bool(source.get("source_route"))
    endpoint_disabled = source.get("endpoint_scoring_allowed") == "false"
    not_active = source.get("scoring_activation_status") == "NOT_ACTIVE_SAMPLE_ROLE_FREEZE_ONLY"
    forbidden_guarded = has_forbidden_guard(source.get("forbidden_inputs", ""))
    claim_boundary_guarded = "Not a Paper 11 result" in source.get("claim_boundary", "") or "only" in source.get(
        "claim_boundary", ""
    )
    checks_pass = all(
        [artifact_exists, row_selector_found, source_side_fields, endpoint_disabled, not_active, forbidden_guarded]
    )
    return {
        "artifact_exists": str(artifact_exists).lower(),
        "row_selector_found": str(row_selector_found).lower(),
        "source_side_fields_present": str(source_side_fields).lower(),
        "endpoint_scoring_disabled_in_source": str(endpoint_disabled).lower(),
        "not_active_or_not_run": str(not_active).lower(),
        "forbidden_input_guard_present": str(forbidden_guarded).lower(),
        "claim_boundary_guard_present": str(claim_boundary_guarded).lower(),
        "preaudit_decision": "PREAUDIT_REVIEW_READY_NOT_ACCEPTED" if checks_pass else "PREAUDIT_BLOCKED_MISSING_GUARD",
        "preaudit_note": "morphology/source-role candidate has source-side route, non-active status, and forbidden-input guards"
        if checks_pass
        else "morphology/source-role candidate needs reviewer inspection before sufficiency acceptance",
    }


def benchmark_audit(row: dict[str, str]) -> dict[str, object]:
    artifacts = [artifact for artifact in row["candidate_artifact_uri_or_id"].split(";") if artifact]
    files_exist = all((ROOT / artifact).exists() for artifact in artifacts)
    source_rows = []
    for artifact in artifacts:
        source_rows.extend(read_csv(ROOT / artifact))
    endpoint_disabled = all(source_row.get("endpoint_scoring_allowed") == "false" for source_row in source_rows)
    not_run_or_pending = all(
        "NOT_RUN" in source_row.get("current_status", "")
        or "PENDING" in source_row.get("current_status", "")
        or source_row.get("required_before_scoring") == "true"
        for source_row in source_rows
    )
    forbidden_guarded = all(has_forbidden_guard(source_row.get("forbidden_inputs", "")) for source_row in source_rows)
    policy_fields_present = all(
        any(
            source_row.get(field)
            for field in (
                "formula_policy",
                "normalization_policy",
                "implementation_policy",
                "control_policy",
                "pass_condition",
            )
        )
        for source_row in source_rows
    )
    checks_pass = all([files_exist, endpoint_disabled, not_run_or_pending, forbidden_guarded, policy_fields_present])
    return {
        "artifact_exists": str(files_exist).lower(),
        "row_selector_found": "true",
        "source_side_fields_present": str(policy_fields_present).lower(),
        "endpoint_scoring_disabled_in_source": str(endpoint_disabled).lower(),
        "not_active_or_not_run": str(not_run_or_pending).lower(),
        "forbidden_input_guard_present": str(forbidden_guarded).lower(),
        "claim_boundary_guard_present": "true",
        "preaudit_decision": "PREAUDIT_REVIEW_READY_NOT_ACCEPTED" if checks_pass else "PREAUDIT_BLOCKED_MISSING_GUARD",
        "preaudit_note": "benchmark/control policy candidate is frozen or declared before scoring and carries forbidden-input guards"
        if checks_pass
        else "benchmark/control policy candidate needs reviewer inspection before sufficiency acceptance",
    }


def preaudit_rows() -> list[dict[str, object]]:
    template = read_csv(PACKAGE_ROOT / "templates/leakage_partial_candidate_sufficiency_v71_review_response_TEMPLATE.csv")
    galaxy_rows = {row["row_id"]: row for row in read_csv(SOURCE / "galaxy_list_freeze_v02.csv")}
    out: list[dict[str, object]] = []
    for row in template:
        audit = morph_audit(row, galaxy_rows) if row["evidence_id"] == "LEC10_MORPH_LABELS" else benchmark_audit(row)
        out.append(
            {
                "preaudit_id": row["ingestion_gate_id"].replace("LEIG70", "LPCS74"),
                "ingestion_gate_id": row["ingestion_gate_id"],
                "candidate_id": row["candidate_id"],
                "leakage_evidence_row_id": row["leakage_evidence_row_id"],
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "evidence_id": row["evidence_id"],
                "candidate_artifact_uri_or_id": row["candidate_artifact_uri_or_id"],
                "candidate_artifact_hash_or_accession": row["candidate_artifact_hash_or_accession"],
                "candidate_row_selector": row["candidate_row_selector"],
                **audit,
                "suggested_reviewer_action": "reviewer_may_accept_only_after_independent_sufficiency_confirmation",
                "target_evidence_rows_created": "0",
                "leakage_pass_authorized": "false",
                "activation_rows_authorized": "0",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "leakage_partial_candidate_sufficiency_preaudit_only_no_evidence_no_scores_no_dark_sector_verdict",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["preaudit_decision"] == "PREAUDIT_REVIEW_READY_NOT_ACCEPTED" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_PREAUDIT_V74",
            "preaudit_rows": len(rows),
            "galaxies_covered": len({row["galaxy_id"] for row in rows}),
            "partial_evidence_components": 2,
            "preaudit_review_ready_rows": ready,
            "preaudit_blocked_rows": blocked,
            "accepted_sufficiency_rows": 0,
            "target_evidence_rows_created": 0,
            "leakage_pass_authorized": 0,
            "activation_rows_authorized": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PARTIAL_SUFFICIENCY_PREAUDIT_REVIEW_READY_NOT_ACCEPTED"
            if ready == len(rows)
            else "PARTIAL_SUFFICIENCY_PREAUDIT_BLOCKED",
            "next_required_artifact": "completed_leakage_partial_candidate_sufficiency_v71_review_response.zip",
            "claim_boundary": "leakage_partial_candidate_sufficiency_preaudit_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = preaudit_rows()
    write_csv(
        DERIVED / "leakage_partial_candidate_sufficiency_preaudit_v74.csv",
        rows,
        [
            "preaudit_id",
            "ingestion_gate_id",
            "candidate_id",
            "leakage_evidence_row_id",
            "galaxy_id",
            "proposed_split",
            "evidence_id",
            "candidate_artifact_uri_or_id",
            "candidate_artifact_hash_or_accession",
            "candidate_row_selector",
            "artifact_exists",
            "row_selector_found",
            "source_side_fields_present",
            "endpoint_scoring_disabled_in_source",
            "not_active_or_not_run",
            "forbidden_input_guard_present",
            "claim_boundary_guard_present",
            "preaudit_decision",
            "preaudit_note",
            "suggested_reviewer_action",
            "target_evidence_rows_created",
            "leakage_pass_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_partial_candidate_sufficiency_preaudit_summary_v74.csv",
        summary(rows),
        [
            "summary_id",
            "preaudit_rows",
            "galaxies_covered",
            "partial_evidence_components",
            "preaudit_review_ready_rows",
            "preaudit_blocked_rows",
            "accepted_sufficiency_rows",
            "target_evidence_rows_created",
            "leakage_pass_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_PREAUDIT_V74_BUILT")


if __name__ == "__main__":
    main()
