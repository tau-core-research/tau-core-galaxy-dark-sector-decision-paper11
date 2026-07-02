#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source_manifest"
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m0_global_parameter_inventory_v10.csv"
COUNTABILITY_ARTIFACT = "m0_global_parameter_count_classification_v11.csv"
COUNT_VALUE_ARTIFACT = "m0_global_parameter_count_value_ledger_v12.csv"
ADJUSTABLE_SLOT_ARTIFACT = "m0_global_adjustable_slot_resolution_v13.csv"
FINAL_COUNT_CANDIDATE_ARTIFACT = "m0_global_final_count_candidate_v14.csv"
FINAL_COUNT_FREEZE_ARTIFACT = "m0_global_final_count_freeze_v15.csv"
M0_PER_GALAXY_AUDIT_ARTIFACT = "m0_per_galaxy_privilege_count_audit_v10.csv"
M0_PER_GALAXY_FREEZE_ARTIFACT = "m0_per_galaxy_privilege_count_freeze_v11.csv"
STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_PARAMETER_INVENTORY"
COUNTABILITY_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M0_GLOBAL_COUNTABILITY_CLASSIFICATION"
COUNT_VALUE_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M0_GLOBAL_COUNT_VALUE_LEDGER"
ADJUSTABLE_SLOT_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M0_GLOBAL_ADJUSTABLE_SLOT_RESOLUTION"
FINAL_COUNT_CANDIDATE_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M0_GLOBAL_FINAL_COUNT_CANDIDATE"
FINAL_COUNT_FREEZE_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M0_GLOBAL_FINAL_COUNT_FREEZE"
M0_PER_GALAXY_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M0_PER_GALAXY_PRIVILEGE_AUDIT"
M0_PER_GALAXY_FREEZE_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M0_PER_GALAXY_PRIVILEGE_FREEZE"
M1_GLOBAL_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M1_GLOBAL_PARAMETER_INVENTORY"
M1_GLOBAL_COUNTABILITY_ARTIFACT = "m1_response_parameter_count_classification_v11.csv"
M1_GLOBAL_COUNTABILITY_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M1_GLOBAL_COUNTABILITY_CLASSIFICATION"
M1_GLOBAL_COUNT_VALUE_ARTIFACT = "m1_response_parameter_count_value_ledger_v12.csv"
M1_GLOBAL_COUNT_VALUE_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M1_GLOBAL_COUNT_VALUE_LEDGER"
M1_GLOBAL_ADJUSTABLE_SLOT_ARTIFACT = "m1_response_parameter_adjustable_slot_resolution_v13.csv"
M1_GLOBAL_ADJUSTABLE_SLOT_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M1_GLOBAL_ADJUSTABLE_SLOT_RESOLUTION"
M1_GLOBAL_FINAL_COUNT_CANDIDATE_ARTIFACT = "m1_response_parameter_final_count_candidate_v14.csv"
M1_GLOBAL_FINAL_COUNT_CANDIDATE_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M1_GLOBAL_FINAL_COUNT_CANDIDATE"
M1_GLOBAL_FINAL_COUNT_FREEZE_ARTIFACT = "m1_response_parameter_final_count_freeze_v15.csv"
M1_GLOBAL_FINAL_COUNT_FREEZE_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M1_GLOBAL_FINAL_COUNT_FREEZE"
M1_PER_GALAXY_AUDIT_ARTIFACT = "m1_per_galaxy_response_privilege_count_audit_v10.csv"
M1_PER_GALAXY_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M1_PER_GALAXY_RESPONSE_PRIVILEGE_AUDIT"
M1_PER_GALAXY_FREEZE_ARTIFACT = "m1_per_galaxy_response_privilege_count_freeze_v11.csv"
M1_PER_GALAXY_FREEZE_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M1_PER_GALAXY_RESPONSE_PRIVILEGE_FREEZE"
M2_GLOBAL_INVENTORY_ARTIFACT = "m2_benchmark_parameter_inventory_v10.csv"
M2_GLOBAL_INVENTORY_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M2_GLOBAL_PARAMETER_INVENTORY"
M2_GLOBAL_COUNTABILITY_ARTIFACT = "m2_benchmark_parameter_count_classification_v11.csv"
M2_GLOBAL_COUNTABILITY_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M2_GLOBAL_COUNTABILITY_CLASSIFICATION"
M2_GLOBAL_COUNT_VALUE_ARTIFACT = "m2_benchmark_parameter_count_value_ledger_v12.csv"
M2_GLOBAL_COUNT_VALUE_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M2_GLOBAL_COUNT_VALUE_LEDGER"
M2_GLOBAL_ADJUSTABLE_SLOT_ARTIFACT = "m2_benchmark_parameter_adjustable_slot_resolution_v13.csv"
M2_GLOBAL_ADJUSTABLE_SLOT_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M2_GLOBAL_ADJUSTABLE_SLOT_RESOLUTION"
M2_GLOBAL_FINAL_COUNT_CANDIDATE_ARTIFACT = "m2_benchmark_parameter_final_count_candidate_v14.csv"
M2_GLOBAL_FINAL_COUNT_CANDIDATE_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M2_GLOBAL_FINAL_COUNT_CANDIDATE"
M2_GLOBAL_FINAL_COUNT_FREEZE_ARTIFACT = "m2_benchmark_parameter_final_count_freeze_v15.csv"
M2_GLOBAL_FINAL_COUNT_FREEZE_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M2_GLOBAL_FINAL_COUNT_FREEZE"
M2_PER_GALAXY_AUDIT_ARTIFACT = "m2_per_galaxy_benchmark_privilege_count_audit_v10.csv"
M2_PER_GALAXY_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M2_PER_GALAXY_BENCHMARK_PRIVILEGE_AUDIT"
M2_PER_GALAXY_FREEZE_ARTIFACT = "m2_per_galaxy_benchmark_privilege_count_freeze_v11.csv"
M2_PER_GALAXY_FREEZE_STATUS = (
    "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_M2_PER_GALAXY_BENCHMARK_PRIVILEGE_FREEZE"
)
SHARED_COUNT_DISCOUNT_ARTIFACT = "shared_input_count_discount_policy_v10.csv"
SHARED_COUNT_DISCOUNT_STATUS = "NUMERIC_COUNT_READINESS_CLOSURE_BLOCKED_ON_SHARED_INPUT_COUNT_DISCOUNT_POLICY"

FIELDS = [
    "closure_row_id",
    "readiness_id",
    "family_id",
    "count_domain",
    "source_readiness_status",
    "upstream_artifacts",
    "upstream_artifact_status",
    "minimum_completion_condition",
    "closure_blocker",
    "closure_decision",
    "next_required_artifact",
    "numeric_count_values_written",
    "parsimony_scores_written",
    "endpoint_scoring_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "closure_artifact",
    "v08_status",
    "readiness_rows_checked",
    "closure_ready_rows",
    "closure_blocked_rows",
    "numeric_count_values_written",
    "parsimony_scores_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

CLOSURE_PLAN = {
    "NCR05_M0_GLOBAL": (
        "m0_global_parameter_inventory_missing",
        "m0_global_parameter_inventory_v10.csv",
    ),
    "NCR05_M0_PER_GALAXY": (
        "m0_per_galaxy_privilege_audit_missing",
        M0_PER_GALAXY_AUDIT_ARTIFACT,
    ),
    "NCR05_M1_GLOBAL": (
        "m1_response_parameter_inventory_missing",
        "m1_response_parameter_inventory_v10.csv",
    ),
    "NCR05_M1_PER_GALAXY": (
        "m1_per_galaxy_response_privilege_audit_missing",
        "m1_per_galaxy_response_privilege_count_audit_v10.csv",
    ),
    "NCR05_M2_GLOBAL": (
        "m2_benchmark_parameter_inventory_missing",
        "m2_benchmark_parameter_inventory_v10.csv",
    ),
    "NCR05_M2_PER_GALAXY": (
        "m2_per_galaxy_benchmark_privilege_audit_missing",
        "m2_per_galaxy_benchmark_privilege_count_audit_v10.csv",
    ),
    "NCR05_SHARED": (
        "shared_input_count_discount_policy_missing",
        "shared_input_count_discount_policy_v10.csv",
    ),
}

ARTIFACT_STATUS_FILES = {
    "m0_no_dark_formula_table_v06": ("m0_no_dark_formula_table_contract_summary_v06.csv", "overall_status"),
    "m0_label_rule_table_v06": ("m0_label_rule_table_summary_v06.csv", "overall_status"),
    "m1_tau_response_formula_table_v06": ("m1_tau_response_formula_table_summary_v06.csv", "overall_status"),
    "m1_admissibility_table_v06": ("m1_admissibility_table_summary_v06.csv", "overall_status"),
    "m2_benchmark_profile_table_v06": ("m2_benchmark_profile_table_summary_v06.csv", "overall_status"),
    "m2_nuisance_policy_table_v06": ("m2_nuisance_policy_table_summary_v06.csv", "overall_status"),
    "shared_scoring_input_table_v06": ("shared_scoring_input_table_summary_v06.csv", "overall_status"),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def v08_status() -> str:
    rows = read_csv(DERIVED / "numeric_parameter_count_table_summary_v08.csv")
    if not rows:
        return "NUMERIC_PARAMETER_COUNT_TABLE_V08_MISSING"
    return rows[0]["overall_status"]


def artifact_status(artifact: str) -> str:
    if artifact == "source_row_audit_v05":
        rows = read_csv(SOURCE / "source_row_audit_v05.csv")
        if rows and all(row["activation_status"] == "ACTIVATION_BLOCKED" for row in rows):
            return "SOURCE_ROW_AUDIT_SKELETON_PRESENT_NOT_COUNT_READY"
        return "SOURCE_ROW_AUDIT_MISSING_OR_UNKNOWN"
    spec = ARTIFACT_STATUS_FILES.get(artifact)
    if not spec:
        return "STATUS_NOT_MAPPED"
    filename, field = spec
    rows = read_csv(DERIVED / filename)
    if not rows:
        return "SUMMARY_MISSING"
    return rows[0][field]


def upstream_status(blocked_by: str) -> str:
    artifacts = blocked_by.split(";")
    return ";".join(f"{artifact}:{artifact_status(artifact)}" for artifact in artifacts)


def m0_inventory_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m0_global_parameter_inventory_summary_v10.csv")
    return rows[0] if rows else {}


def m0_count_classification_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m0_global_parameter_count_classification_summary_v11.csv")
    return rows[0] if rows else {}


def m0_count_value_ledger_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m0_global_parameter_count_value_ledger_summary_v12.csv")
    return rows[0] if rows else {}


def m0_adjustable_slot_resolution_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m0_global_adjustable_slot_resolution_summary_v13.csv")
    return rows[0] if rows else {}


def m0_final_count_candidate_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m0_global_final_count_candidate_summary_v14.csv")
    return rows[0] if rows else {}


def m0_final_count_freeze_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m0_global_final_count_freeze_summary_v15.csv")
    return rows[0] if rows else {}


def m0_per_galaxy_privilege_count_audit_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m0_per_galaxy_privilege_count_audit_summary_v10.csv")
    return rows[0] if rows else {}


def m0_per_galaxy_privilege_count_freeze_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m0_per_galaxy_privilege_count_freeze_summary_v11.csv")
    return rows[0] if rows else {}


def m1_response_parameter_inventory_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m1_response_parameter_inventory_summary_v10.csv")
    return rows[0] if rows else {}


def m1_response_parameter_count_classification_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m1_response_parameter_count_classification_summary_v11.csv")
    return rows[0] if rows else {}


def m1_response_parameter_count_value_ledger_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m1_response_parameter_count_value_ledger_summary_v12.csv")
    return rows[0] if rows else {}


def m1_response_parameter_adjustable_slot_resolution_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m1_response_parameter_adjustable_slot_resolution_summary_v13.csv")
    return rows[0] if rows else {}


def m1_response_parameter_final_count_candidate_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m1_response_parameter_final_count_candidate_summary_v14.csv")
    return rows[0] if rows else {}


def m1_response_parameter_final_count_freeze_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m1_response_parameter_final_count_freeze_summary_v15.csv")
    return rows[0] if rows else {}


def m1_per_galaxy_response_privilege_count_audit_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m1_per_galaxy_response_privilege_count_audit_summary_v10.csv")
    return rows[0] if rows else {}


def m1_per_galaxy_response_privilege_count_freeze_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m1_per_galaxy_response_privilege_count_freeze_summary_v11.csv")
    return rows[0] if rows else {}


def m2_benchmark_parameter_inventory_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m2_benchmark_parameter_inventory_summary_v10.csv")
    return rows[0] if rows else {}


def m2_benchmark_parameter_count_classification_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m2_benchmark_parameter_count_classification_summary_v11.csv")
    return rows[0] if rows else {}


def m2_benchmark_parameter_count_value_ledger_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m2_benchmark_parameter_count_value_ledger_summary_v12.csv")
    return rows[0] if rows else {}


def m2_benchmark_parameter_adjustable_slot_resolution_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m2_benchmark_parameter_adjustable_slot_resolution_summary_v13.csv")
    return rows[0] if rows else {}


def m2_benchmark_parameter_final_count_candidate_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m2_benchmark_parameter_final_count_candidate_summary_v14.csv")
    return rows[0] if rows else {}


def m2_benchmark_parameter_final_count_freeze_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m2_benchmark_parameter_final_count_freeze_summary_v15.csv")
    return rows[0] if rows else {}


def m2_per_galaxy_benchmark_privilege_count_audit_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m2_per_galaxy_benchmark_privilege_count_audit_summary_v10.csv")
    return rows[0] if rows else {}


def m2_per_galaxy_benchmark_privilege_count_freeze_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "m2_per_galaxy_benchmark_privilege_count_freeze_summary_v11.csv")
    return rows[0] if rows else {}


def shared_input_count_discount_policy_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "shared_input_count_discount_policy_summary_v10.csv")
    return rows[0] if rows else {}


def closure_override_ready(readiness_id: str) -> bool:
    if readiness_id == "NCR05_M0_GLOBAL":
        freeze = m0_final_count_freeze_summary()
        return freeze.get("overall_status") == "M0_GLOBAL_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_PRIVILEGE_AUDIT_PENDING"
    if readiness_id == "NCR05_M0_PER_GALAXY":
        freeze = m0_per_galaxy_privilege_count_freeze_summary()
        return freeze.get("overall_status") == "M0_PER_GALAXY_PRIVILEGE_COUNT_FREEZE_V11_READY_M1_GLOBAL_COUNT_PENDING"
    if readiness_id == "NCR05_M1_GLOBAL":
        freeze = m1_response_parameter_final_count_freeze_summary()
        return (
            freeze.get("overall_status")
            == "M1_RESPONSE_PARAMETER_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_RESPONSE_PRIVILEGE_AUDIT_PENDING"
        )
    if readiness_id == "NCR05_M1_PER_GALAXY":
        freeze = m1_per_galaxy_response_privilege_count_freeze_summary()
        return (
            freeze.get("overall_status")
            == "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_FREEZE_V11_READY_M2_GLOBAL_COUNT_PENDING"
        )
    if readiness_id == "NCR05_M2_GLOBAL":
        freeze = m2_benchmark_parameter_final_count_freeze_summary()
        return (
            freeze.get("overall_status")
            == "M2_BENCHMARK_PARAMETER_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_BENCHMARK_PRIVILEGE_AUDIT_PENDING"
        )
    if readiness_id == "NCR05_M2_PER_GALAXY":
        freeze = m2_per_galaxy_benchmark_privilege_count_freeze_summary()
        return (
            freeze.get("overall_status")
            == "M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_FREEZE_V11_READY_SHARED_COUNT_PENDING"
        )
    if readiness_id == "NCR05_SHARED":
        policy = shared_input_count_discount_policy_summary()
        return policy.get("overall_status") == "SHARED_INPUT_COUNT_DISCOUNT_POLICY_V10_READY_FINAL_NUMERIC_COUNTS_PENDING"
    return False


def closure_plan_for(readiness_id: str) -> tuple[str, str]:
    blocker, next_artifact = CLOSURE_PLAN[readiness_id]
    if readiness_id == "NCR05_M0_PER_GALAXY":
        freeze = m0_per_galaxy_privilege_count_freeze_summary()
        if freeze.get("overall_status") == "M0_PER_GALAXY_PRIVILEGE_COUNT_FREEZE_V11_READY_M1_GLOBAL_COUNT_PENDING":
            return "none", "none"
        audit = m0_per_galaxy_privilege_count_audit_summary()
        if audit.get("overall_status") == "M0_PER_GALAXY_PRIVILEGE_COUNT_AUDIT_V10_READY_FOR_FREEZE":
            return "m0_per_galaxy_privilege_count_freeze_pending", M0_PER_GALAXY_FREEZE_ARTIFACT
        return blocker, next_artifact
    if readiness_id == "NCR05_M1_GLOBAL":
        final_count_freeze = m1_response_parameter_final_count_freeze_summary()
        if (
            final_count_freeze.get("overall_status")
            == "M1_RESPONSE_PARAMETER_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_RESPONSE_PRIVILEGE_AUDIT_PENDING"
        ):
            return "none", "none"
        final_count_candidate = m1_response_parameter_final_count_candidate_summary()
        if final_count_candidate.get("overall_status") == "M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE":
            return "m1_response_parameter_final_count_freeze_pending", M1_GLOBAL_FINAL_COUNT_FREEZE_ARTIFACT
        adjustable_slots = m1_response_parameter_adjustable_slot_resolution_summary()
        if adjustable_slots.get("overall_status") == "M1_RESPONSE_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE":
            return "m1_response_parameter_final_count_candidate_pending", M1_GLOBAL_FINAL_COUNT_CANDIDATE_ARTIFACT
        value_ledger = m1_response_parameter_count_value_ledger_summary()
        if value_ledger.get("overall_status") == "M1_RESPONSE_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING":
            return "m1_response_parameter_adjustable_slot_resolution_pending", M1_GLOBAL_ADJUSTABLE_SLOT_ARTIFACT
        classification = m1_response_parameter_count_classification_summary()
        if classification.get("overall_status") == "M1_RESPONSE_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING":
            return "m1_response_parameter_count_value_ledger_pending", M1_GLOBAL_COUNT_VALUE_ARTIFACT
        inventory = m1_response_parameter_inventory_summary()
        if inventory.get("overall_status") == "M1_RESPONSE_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING":
            return "m1_response_parameter_countability_classification_pending", M1_GLOBAL_COUNTABILITY_ARTIFACT
        return blocker, next_artifact
    if readiness_id == "NCR05_M1_PER_GALAXY":
        freeze = m1_per_galaxy_response_privilege_count_freeze_summary()
        if freeze.get("overall_status") == "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_FREEZE_V11_READY_M2_GLOBAL_COUNT_PENDING":
            return "none", "none"
        audit = m1_per_galaxy_response_privilege_count_audit_summary()
        if audit.get("overall_status") == "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_AUDIT_V10_READY_FOR_FREEZE":
            return "m1_per_galaxy_response_privilege_count_freeze_pending", M1_PER_GALAXY_FREEZE_ARTIFACT
        return blocker, next_artifact
    if readiness_id == "NCR05_M2_GLOBAL":
        final_count_freeze = m2_benchmark_parameter_final_count_freeze_summary()
        if (
            final_count_freeze.get("overall_status")
            == "M2_BENCHMARK_PARAMETER_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_BENCHMARK_PRIVILEGE_AUDIT_PENDING"
        ):
            return "none", "none"
        final_count_candidate = m2_benchmark_parameter_final_count_candidate_summary()
        if (
            final_count_candidate.get("overall_status")
            == "M2_BENCHMARK_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE"
        ):
            return "m2_benchmark_parameter_final_count_freeze_pending", M2_GLOBAL_FINAL_COUNT_FREEZE_ARTIFACT
        adjustable_slots = m2_benchmark_parameter_adjustable_slot_resolution_summary()
        if (
            adjustable_slots.get("overall_status")
            == "M2_BENCHMARK_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE"
        ):
            return "m2_benchmark_parameter_final_count_candidate_pending", M2_GLOBAL_FINAL_COUNT_CANDIDATE_ARTIFACT
        value_ledger = m2_benchmark_parameter_count_value_ledger_summary()
        if (
            value_ledger.get("overall_status")
            == "M2_BENCHMARK_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING"
        ):
            return "m2_benchmark_parameter_adjustable_slot_resolution_pending", M2_GLOBAL_ADJUSTABLE_SLOT_ARTIFACT
        classification = m2_benchmark_parameter_count_classification_summary()
        if classification.get("overall_status") == "M2_BENCHMARK_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING":
            return "m2_benchmark_parameter_count_value_ledger_pending", M2_GLOBAL_COUNT_VALUE_ARTIFACT
        inventory = m2_benchmark_parameter_inventory_summary()
        if inventory.get("overall_status") == "M2_BENCHMARK_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING":
            return "m2_benchmark_parameter_countability_classification_pending", M2_GLOBAL_COUNTABILITY_ARTIFACT
        return blocker, next_artifact
    if readiness_id == "NCR05_M2_PER_GALAXY":
        freeze = m2_per_galaxy_benchmark_privilege_count_freeze_summary()
        if (
            freeze.get("overall_status")
            == "M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_FREEZE_V11_READY_SHARED_COUNT_PENDING"
        ):
            return "none", "none"
        audit = m2_per_galaxy_benchmark_privilege_count_audit_summary()
        if (
            audit.get("overall_status")
            == "M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_AUDIT_V10_READY_FOR_FREEZE"
        ):
            return "m2_per_galaxy_benchmark_privilege_count_freeze_pending", M2_PER_GALAXY_FREEZE_ARTIFACT
        return blocker, next_artifact
    if readiness_id == "NCR05_SHARED":
        policy = shared_input_count_discount_policy_summary()
        if policy.get("overall_status") == "SHARED_INPUT_COUNT_DISCOUNT_POLICY_V10_READY_FINAL_NUMERIC_COUNTS_PENDING":
            return "none", "none"
        return blocker, next_artifact
    if readiness_id != "NCR05_M0_GLOBAL":
        return blocker, next_artifact
    final_count_freeze = m0_final_count_freeze_summary()
    if final_count_freeze.get("overall_status") == "M0_GLOBAL_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_PRIVILEGE_AUDIT_PENDING":
        return "none", "none"
    final_count_candidate = m0_final_count_candidate_summary()
    if final_count_candidate.get("overall_status") == "M0_GLOBAL_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE":
        return "m0_global_final_count_freeze_pending", FINAL_COUNT_FREEZE_ARTIFACT
    adjustable_slots = m0_adjustable_slot_resolution_summary()
    if adjustable_slots.get("overall_status") == "M0_GLOBAL_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE":
        return "m0_global_final_count_candidate_pending", FINAL_COUNT_CANDIDATE_ARTIFACT
    value_ledger = m0_count_value_ledger_summary()
    if value_ledger.get("overall_status") == "M0_GLOBAL_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING":
        return "m0_global_adjustable_slot_resolution_pending", ADJUSTABLE_SLOT_ARTIFACT
    classification = m0_count_classification_summary()
    if classification.get("overall_status") == "M0_GLOBAL_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING":
        return "m0_global_parameter_count_value_ledger_pending", COUNT_VALUE_ARTIFACT
    inventory = m0_inventory_summary()
    if inventory.get("overall_status") == "M0_GLOBAL_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING":
        return "m0_global_parameter_countability_classification_pending", COUNTABILITY_ARTIFACT
    return blocker, next_artifact


def closure_rows() -> list[dict[str, object]]:
    rows = read_csv(SOURCE / "numeric_count_readiness_v05.csv")
    out: list[dict[str, object]] = []
    for index, row in enumerate(rows, start=1):
        blocker, next_artifact = closure_plan_for(row["readiness_id"])
        source_ready = row["count_readiness_status"] == "COUNT_READY" or closure_override_ready(row["readiness_id"])
        out.append(
            {
                "closure_row_id": f"NCRC09_{index:03d}",
                "readiness_id": row["readiness_id"],
                "family_id": row["family_id"],
                "count_domain": row["count_domain"],
                "source_readiness_status": row["count_readiness_status"],
                "upstream_artifacts": row["blocked_by"],
                "upstream_artifact_status": upstream_status(row["blocked_by"]),
                "minimum_completion_condition": row["minimum_completion_condition"],
                "closure_blocker": "none" if source_ready else blocker,
                "closure_decision": "COUNT_READINESS_READY" if source_ready else "COUNT_READINESS_BLOCKED",
                "next_required_artifact": "none" if source_ready else next_artifact,
                "numeric_count_values_written": 0,
                "parsimony_scores_written": 0,
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "numeric_count_readiness_closure_only_no_counts_no_parsimony_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = [row for row in rows if row["closure_decision"] != "COUNT_READINESS_READY"]
    status = STATUS
    if blocked and blocked[0]["next_required_artifact"] == COUNTABILITY_ARTIFACT:
        status = COUNTABILITY_STATUS
    if blocked and blocked[0]["next_required_artifact"] == COUNT_VALUE_ARTIFACT:
        status = COUNT_VALUE_STATUS
    if blocked and blocked[0]["next_required_artifact"] == ADJUSTABLE_SLOT_ARTIFACT:
        status = ADJUSTABLE_SLOT_STATUS
    if blocked and blocked[0]["next_required_artifact"] == FINAL_COUNT_CANDIDATE_ARTIFACT:
        status = FINAL_COUNT_CANDIDATE_STATUS
    if blocked and blocked[0]["next_required_artifact"] == FINAL_COUNT_FREEZE_ARTIFACT:
        status = FINAL_COUNT_FREEZE_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M0_PER_GALAXY_AUDIT_ARTIFACT:
        status = M0_PER_GALAXY_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M0_PER_GALAXY_FREEZE_ARTIFACT:
        status = M0_PER_GALAXY_FREEZE_STATUS
    if blocked and blocked[0]["next_required_artifact"] == "m1_response_parameter_inventory_v10.csv":
        status = M1_GLOBAL_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M1_GLOBAL_COUNTABILITY_ARTIFACT:
        status = M1_GLOBAL_COUNTABILITY_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M1_GLOBAL_COUNT_VALUE_ARTIFACT:
        status = M1_GLOBAL_COUNT_VALUE_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M1_GLOBAL_ADJUSTABLE_SLOT_ARTIFACT:
        status = M1_GLOBAL_ADJUSTABLE_SLOT_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M1_GLOBAL_FINAL_COUNT_CANDIDATE_ARTIFACT:
        status = M1_GLOBAL_FINAL_COUNT_CANDIDATE_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M1_GLOBAL_FINAL_COUNT_FREEZE_ARTIFACT:
        status = M1_GLOBAL_FINAL_COUNT_FREEZE_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M1_PER_GALAXY_AUDIT_ARTIFACT:
        status = M1_PER_GALAXY_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M1_PER_GALAXY_FREEZE_ARTIFACT:
        status = M1_PER_GALAXY_FREEZE_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M2_GLOBAL_INVENTORY_ARTIFACT:
        status = M2_GLOBAL_INVENTORY_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M2_GLOBAL_COUNTABILITY_ARTIFACT:
        status = M2_GLOBAL_COUNTABILITY_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M2_GLOBAL_COUNT_VALUE_ARTIFACT:
        status = M2_GLOBAL_COUNT_VALUE_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M2_GLOBAL_ADJUSTABLE_SLOT_ARTIFACT:
        status = M2_GLOBAL_ADJUSTABLE_SLOT_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M2_GLOBAL_FINAL_COUNT_CANDIDATE_ARTIFACT:
        status = M2_GLOBAL_FINAL_COUNT_CANDIDATE_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M2_GLOBAL_FINAL_COUNT_FREEZE_ARTIFACT:
        status = M2_GLOBAL_FINAL_COUNT_FREEZE_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M2_PER_GALAXY_AUDIT_ARTIFACT:
        status = M2_PER_GALAXY_STATUS
    if blocked and blocked[0]["next_required_artifact"] == M2_PER_GALAXY_FREEZE_ARTIFACT:
        status = M2_PER_GALAXY_FREEZE_STATUS
    if blocked and blocked[0]["next_required_artifact"] == SHARED_COUNT_DISCOUNT_ARTIFACT:
        status = SHARED_COUNT_DISCOUNT_STATUS
    return [
        {
            "summary_id": "NUMERIC_COUNT_READINESS_CLOSURE_V09",
            "closure_artifact": "numeric_count_readiness_closure_v09",
            "v08_status": v08_status(),
            "readiness_rows_checked": len(rows),
            "closure_ready_rows": len(rows) - len(blocked),
            "closure_blocked_rows": len(blocked),
            "numeric_count_values_written": 0,
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": status if blocked else "NUMERIC_COUNT_READINESS_CLOSURE_READY_FOR_FINAL_COUNTS",
            "next_required_artifact": blocked[0]["next_required_artifact"] if blocked else "numeric_parameter_count_table_final_values_v10.csv",
            "claim_boundary": "numeric_count_readiness_closure_only_no_counts_no_parsimony_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "numeric_count_readiness_closure_v09.md").write_text(
        f"""# Numeric Count Readiness Closure v09

**Doc class:** numeric-count readiness closure ledger
**Status:** readiness closure ready for final numeric counts; no counts, no scoring

Script:

```text
scripts/build_numeric_count_readiness_closure.py
```

Derived outputs:

```text
data/derived/numeric_count_readiness_closure_v09.csv
data/derived/numeric_count_readiness_closure_summary_v09.csv
```

This artifact decomposes the v08 final-count blocker into explicit readiness
closure rows. It records which upstream policy/scaffold artifacts are present
and which count-readiness evidence is still missing before final numeric
parameter counts may be written.

## Current Result

The current status is:

```text
NUMERIC_COUNT_READINESS_CLOSURE_READY_FOR_FINAL_COUNTS
```

The next artifact required before final scoring can advance is:

```text
numeric_parameter_count_table_final_values_v10.csv
```

The historical readiness ladder audited by this ledger is preserved below.
Each step writes no counts and only clears the next count-readiness blocker.

If the M0 global inventory is present, the next required artifact becomes:

```text
{COUNTABILITY_ARTIFACT}
```

If the M0 global countability classification is present, the next required
artifact becomes:

```text
{COUNT_VALUE_ARTIFACT}
```

If the M0 global count-value ledger is present, the next required artifact
becomes:

```text
{ADJUSTABLE_SLOT_ARTIFACT}
```

If the M0 global adjustable-slot resolution is present, the next required
artifact becomes:

```text
{FINAL_COUNT_CANDIDATE_ARTIFACT}
```

If the M0 global final-count candidate is present, the next required artifact
becomes:

```text
{FINAL_COUNT_FREEZE_ARTIFACT}
```

If the M0 global final-count freeze is present, the M0 global closure row
becomes ready and the next required artifact becomes:

```text
{M0_PER_GALAXY_AUDIT_ARTIFACT}
```

If the M0 per-galaxy privilege-count audit is present, the next required
artifact becomes:

```text
{M0_PER_GALAXY_FREEZE_ARTIFACT}
```

If the M0 per-galaxy privilege-count freeze is present, the M0 per-galaxy
closure row becomes ready and the next required artifact becomes:

```text
m1_response_parameter_inventory_v10.csv
```

If the M1 response-parameter inventory is present, the next required artifact
becomes:

```text
{M1_GLOBAL_COUNTABILITY_ARTIFACT}
```

If the M1 response-parameter countability classification is present, the next
required artifact becomes:

```text
{M1_GLOBAL_COUNT_VALUE_ARTIFACT}
```

If the M1 response-parameter count-value ledger is present, the next required
artifact becomes:

```text
{M1_GLOBAL_ADJUSTABLE_SLOT_ARTIFACT}
```

If the M1 response-parameter adjustable-slot resolution is present, the next
required artifact becomes:

```text
{M1_GLOBAL_FINAL_COUNT_CANDIDATE_ARTIFACT}
```

If the M1 response-parameter final-count candidate is present, the next
required artifact becomes:

```text
{M1_GLOBAL_FINAL_COUNT_FREEZE_ARTIFACT}
```

If the M1 response-parameter final-count freeze is present, the M1 global
closure row becomes ready and the next required artifact becomes:

```text
{M1_PER_GALAXY_AUDIT_ARTIFACT}
```

If the M1 per-galaxy response-privilege audit is present, the next required
artifact becomes:

```text
{M1_PER_GALAXY_FREEZE_ARTIFACT}
```

If the M1 per-galaxy response-privilege freeze is present, the M1 per-galaxy
closure row becomes ready and the next required artifact becomes:

```text
{M2_GLOBAL_INVENTORY_ARTIFACT}
```

If the M2 benchmark-parameter inventory is present, the next required artifact
becomes:

```text
{M2_GLOBAL_COUNTABILITY_ARTIFACT}
```

If the M2 benchmark-parameter countability classification is present, the next
required artifact becomes:

```text
{M2_GLOBAL_COUNT_VALUE_ARTIFACT}
```

If the M2 benchmark-parameter count-value ledger is present, the next required
artifact becomes:

```text
{M2_GLOBAL_ADJUSTABLE_SLOT_ARTIFACT}
```

If the M2 benchmark-parameter adjustable-slot resolution is present, the next
required artifact becomes:

```text
{M2_GLOBAL_FINAL_COUNT_CANDIDATE_ARTIFACT}
```

If the M2 benchmark-parameter final-count candidate is present, the next
required artifact becomes:

```text
{M2_GLOBAL_FINAL_COUNT_FREEZE_ARTIFACT}
```

If the M2 benchmark-parameter final-count freeze is present, the M2 global
closure row becomes ready and the next required artifact becomes:

```text
{M2_PER_GALAXY_AUDIT_ARTIFACT}
```

If the M2 per-galaxy benchmark-privilege audit is present, the next required
artifact becomes:

```text
{M2_PER_GALAXY_FREEZE_ARTIFACT}
```

If the M2 per-galaxy benchmark-privilege freeze is present, the M2 per-galaxy
closure row becomes ready and the next required artifact becomes:

```text
{SHARED_COUNT_DISCOUNT_ARTIFACT}
```

## Claim Boundary

This closure ledger writes no numeric parameter counts, no per-galaxy privilege
counts, no parsimony penalty, no endpoint scores, and no dark-sector verdict.
It only identifies the first concrete count-readiness artifact needed before
the final count table can receive values.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = closure_rows()
    write_csv(DERIVED / "numeric_count_readiness_closure_v09.csv", rows, FIELDS)
    write_csv(DERIVED / "numeric_count_readiness_closure_summary_v09.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_NUMERIC_COUNT_READINESS_CLOSURE_V09_BUILT")


if __name__ == "__main__":
    main()
