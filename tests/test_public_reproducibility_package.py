from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_files_exist() -> None:
    required = [
        "README.md",
        "DATA_NOTICE.md",
        "CITATION.cff",
        "LICENSE",
        "paper11_submission_source/main.tex",
        "paper11_submission_source/refs.bib",
        "docs/frozen_policy_bundle_instance_v01.md",
        "docs/galaxy_decision_endpoint_manifest_v01.md",
        "docs/galaxy_sample_freeze_v01.md",
        "docs/scoring_rule_freeze_v01.md",
        "docs/control_manifest_v01.md",
        "docs/decision_threshold_v01.md",
        "docs/galaxy_list_freeze_v02.md",
        "docs/scoring_formula_freeze_v02.md",
        "docs/family_parameter_count_freeze_v03.md",
        "docs/control_implementation_freeze_v03.md",
        "docs/source_field_completeness_v04.md",
        "docs/family_formula_registry_v04.md",
        "docs/control_runner_contract_v04.md",
        "docs/source_row_audit_v05.md",
        "docs/family_formula_table_v05.md",
        "docs/numeric_count_readiness_v05.md",
        "docs/readiness_audit_v06.md",
        "docs/scoring_preflight_v07.md",
        "data/derived/activation_blockers_v06.csv",
        "data/derived/formula_and_count_blockers_v06.csv",
        "data/derived/control_runner_blockers_v06.csv",
        "data/derived/readiness_summary_v06.csv",
        "data/derived/scoring_input_requirements_v07.csv",
        "data/derived/scoring_formula_components_v07.csv",
        "data/derived/scoring_preflight_summary_v07.csv",
        "scripts/run_readiness_audit.py",
        "scripts/run_scoring_preflight.py",
        "scripts/reproduce.py",
        "scripts/validate_protocol_manifests.py",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_manuscript_scope_and_forbidden_overclaims() -> None:
    text = (ROOT / "paper11_submission_source/main.tex").read_text()
    assert "dark-sector necessity" in text.lower()
    assert "Response" in text
    forbidden = [
        "dark matter does not exist",
        "Tau Core replaces the standard dark sector",
        "lensing, CMB, BAO, growth, or cosmology are solved",
    ]
    for phrase in forbidden:
        assert phrase in text


def test_model_family_manifest_is_endpoint_disabled() -> None:
    path = ROOT / "data/source_manifest/model_family_decision_protocol.csv"
    rows = list(csv.DictReader(path.open()))
    assert {row["family_id"] for row in rows} == {"M0", "M1", "M2"}
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)


def test_policy_bundle_and_endpoint_manifest_are_not_results() -> None:
    bundle = list(csv.DictReader((ROOT / "data/source_manifest/frozen_policy_bundle_instance_v01.csv").open()))
    endpoint = list(csv.DictReader((ROOT / "data/source_manifest/galaxy_decision_endpoint_manifest_v01.csv").open()))
    assert len(bundle) == 9
    assert len(endpoint) == 8
    assert all(row["endpoint_scoring_allowed"] == "false" for row in bundle)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in endpoint)
    statuses = " ".join(row["current_status"] for row in endpoint)
    assert "M0_wins" not in statuses
    assert "M1_wins" not in statuses
    assert "M2_wins" not in statuses


def test_pre_registration_manifests_are_not_endpoint_results() -> None:
    files = [
        "galaxy_sample_freeze_v01.csv",
        "scoring_rule_freeze_v01.csv",
        "control_manifest_v01.csv",
    ]
    for name in files:
        rows = list(csv.DictReader((ROOT / "data/source_manifest" / name).open()))
        assert rows
        assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    thresholds = list(csv.DictReader((ROOT / "data/source_manifest/decision_threshold_v01.csv").open()))
    assert {row["verdict_label"] for row in thresholds} == {
        "M0_SUFFICIENT",
        "M1_FAVORED",
        "M2_BENCHMARK_STRONGER",
        "UNRESOLVED",
    }
    assert all("PENDING" in row["current_status"] for row in thresholds)


def test_v02_freezes_are_concrete_but_not_activated() -> None:
    galaxy_rows = list(csv.DictReader((ROOT / "data/source_manifest/galaxy_list_freeze_v02.csv").open()))
    assert len(galaxy_rows) >= 10
    assert {"NGC4088", "UGC12506", "NGC4183"}.issubset({row["galaxy_id"] for row in galaxy_rows})
    assert all(row["endpoint_scoring_allowed"] == "false" for row in galaxy_rows)
    assert all("NOT_ACTIVE" in row["scoring_activation_status"] for row in galaxy_rows)

    formula_rows = list(csv.DictReader((ROOT / "data/source_manifest/scoring_formula_freeze_v02.csv").open()))
    assert {row["formula_id"] for row in formula_rows} == {
        "SF02_FULL_CURVE",
        "SF02_INNER_ZONE",
        "SF02_OUTER_ZONE",
        "SF02_PARSIMONY",
        "SF02_GALAXY_SCORE",
        "SF02_HELDOUT",
        "SF02_CONTROL_VETO",
    }
    assert all(row["endpoint_scoring_allowed"] == "false" for row in formula_rows)
    assert all("FORMULA_POLICY_FROZEN_NOT_RUN" in row["current_status"] for row in formula_rows)


def test_v03_family_budget_and_controls_are_frozen_not_run() -> None:
    budget_rows = list(csv.DictReader((ROOT / "data/source_manifest/family_parameter_count_freeze_v03.csv").open()))
    assert {"M0", "M1", "M2", "ALL"}.issubset({row["family_id"] for row in budget_rows})
    assert all(row["endpoint_scoring_allowed"] == "false" for row in budget_rows)
    assert all("COUNT_RULE_FROZEN_NUMERIC_COUNT_PENDING" in row["numeric_count_status"] for row in budget_rows)
    assert any("Response_tau formula claimed" in row["claim_boundary"] for row in budget_rows)

    control_rows = list(csv.DictReader((ROOT / "data/source_manifest/control_implementation_freeze_v03.csv").open()))
    assert {row["control_id"] for row in control_rows} == {
        "CIF03_SHUFFLE",
        "CIF03_WRONG_FAMILY",
        "CIF03_NULL_SOURCE",
        "CIF03_LEAKAGE",
        "CIF03_RADIAL",
        "CIF03_PARITY",
    }
    assert all(row["endpoint_scoring_allowed"] == "false" for row in control_rows)
    assert all("IMPLEMENTATION_POLICY_FROZEN_NOT_RUN" in row["current_status"] for row in control_rows)


def test_v04_contracts_are_declared_not_implemented() -> None:
    source_rows = list(csv.DictReader((ROOT / "data/source_manifest/source_field_completeness_v04.csv").open()))
    assert len(source_rows) >= 6
    assert all(row["endpoint_scoring_allowed"] == "false" for row in source_rows)
    assert all("PENDING" in row["activation_status"] for row in source_rows)
    assert any(row["required_field"] == "source_packet_leakage_audit" for row in source_rows)

    registry_rows = list(csv.DictReader((ROOT / "data/source_manifest/family_formula_registry_v04.csv").open()))
    assert {"M0", "M1", "M2", "ALL"}.issubset({row["family_id"] for row in registry_rows})
    assert all(row["endpoint_scoring_allowed"] == "false" for row in registry_rows)
    assert all("PENDING" in row["numeric_count_status"] for row in registry_rows)
    assert any("Response_tau formula" in row["claim_boundary"] for row in registry_rows)

    runner_rows = list(csv.DictReader((ROOT / "data/source_manifest/control_runner_contract_v04.csv").open()))
    assert {row["control_id"] for row in runner_rows} == {
        "CIF03_SHUFFLE",
        "CIF03_WRONG_FAMILY",
        "CIF03_NULL_SOURCE",
        "CIF03_LEAKAGE",
        "CIF03_RADIAL",
        "CIF03_PARITY",
    }
    assert all(row["endpoint_scoring_allowed"] == "false" for row in runner_rows)
    assert all(row["execution_status"] == "RUNNER_CONTRACT_DECLARED_NOT_IMPLEMENTED" for row in runner_rows)


def test_v05_readiness_ledgers_block_activation_and_counts() -> None:
    audit_rows = list(csv.DictReader((ROOT / "data/source_manifest/source_row_audit_v05.csv").open()))
    galaxy_rows = list(csv.DictReader((ROOT / "data/source_manifest/galaxy_list_freeze_v02.csv").open()))
    assert {row["galaxy_id"] for row in audit_rows} == {row["galaxy_id"] for row in galaxy_rows}
    assert all(row["endpoint_scoring_allowed"] == "false" for row in audit_rows)
    assert all(row["activation_status"] == "ACTIVATION_BLOCKED" for row in audit_rows)
    assert all("PENDING" in row["leakage_audit_status"] for row in audit_rows)

    formula_rows = list(csv.DictReader((ROOT / "data/source_manifest/family_formula_table_v05.csv").open()))
    assert {"M0", "M1", "M2", "ALL"}.issubset({row["family_id"] for row in formula_rows})
    assert all(row["endpoint_scoring_allowed"] == "false" for row in formula_rows)
    assert all(row["formula_table_status"] == "FORMULA_TABLE_REQUIRED_NOT_FILLED" for row in formula_rows)
    assert any("Response_tau formula" in row["claim_boundary"] for row in formula_rows)

    count_rows = list(csv.DictReader((ROOT / "data/source_manifest/numeric_count_readiness_v05.csv").open()))
    assert {"M0", "M1", "M2", "ALL"}.issubset({row["family_id"] for row in count_rows})
    assert all(row["endpoint_scoring_allowed"] == "false" for row in count_rows)
    assert all(row["count_readiness_status"] == "COUNT_NOT_READY" for row in count_rows)


def test_v06_readiness_audit_blocks_endpoint_scoring() -> None:
    activation_rows = list(csv.DictReader((ROOT / "data/derived/activation_blockers_v06.csv").open()))
    assert len(activation_rows) == 18
    assert all(row["activation_status"] == "ACTIVATION_BLOCKED" for row in activation_rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in activation_rows)

    formula_rows = list(csv.DictReader((ROOT / "data/derived/formula_and_count_blockers_v06.csv").open()))
    assert any(row["blocker_type"] == "formula_table" for row in formula_rows)
    assert any(row["blocker_type"] == "numeric_count" for row in formula_rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in formula_rows)

    runner_rows = list(csv.DictReader((ROOT / "data/derived/control_runner_blockers_v06.csv").open()))
    assert len(runner_rows) == 6
    assert all(row["execution_status"] == "RUNNER_CONTRACT_DECLARED_NOT_IMPLEMENTED" for row in runner_rows)

    summary = list(csv.DictReader((ROOT / "data/derived/readiness_summary_v06.csv").open()))
    assert summary == [
        {
            "summary_id": "READINESS_V06",
            "blocked_galaxy_rows": "18",
            "unfilled_formula_tables": "8",
            "blocked_numeric_counts": "7",
            "unimplemented_control_runners": "6",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "ENDPOINT_SCORING_BLOCKED",
            "claim_boundary": "readiness_audit_only_no_dark_sector_verdict",
        }
    ]


def test_v07_scoring_preflight_names_required_inputs_without_scoring() -> None:
    requirements = list(csv.DictReader((ROOT / "data/derived/scoring_input_requirements_v07.csv").open()))
    assert {row["required_artifact"] for row in requirements} == {
        "activated_scoring_rows_v08.csv",
        "scoring_observed_inputs_v08.csv",
        "family_prediction_tables_v08.csv",
        "numeric_parameter_count_table_v08.csv",
        "control_runner_outputs_v08.csv",
        "numeric_decision_thresholds_v08.csv",
    }
    assert all(row["endpoint_scoring_allowed"] == "false" for row in requirements)
    assert all(row["current_status"].startswith("BLOCKED") for row in requirements)

    components = list(csv.DictReader((ROOT / "data/derived/scoring_formula_components_v07.csv").open()))
    assert len(components) == 7
    assert all(row["formula_policy_status"] == "READY_AS_POLICY_NOT_RUN" for row in components)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in components)

    summary = list(csv.DictReader((ROOT / "data/derived/scoring_preflight_summary_v07.csv").open()))
    assert summary == [
        {
            "summary_id": "SCORING_PREFLIGHT_V07",
            "readiness_dependency": "ENDPOINT_SCORING_BLOCKED",
            "blocked_scoring_requirements": "6",
            "formula_policy_components_ready": "7",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_NOT_READY",
            "next_required_artifact": "activated_scoring_rows_v08.csv",
            "claim_boundary": "scoring_preflight_only_no_dark_sector_verdict",
        }
    ]


def test_arxiv_zip_is_source_only_if_present() -> None:
    zip_path = ROOT / "arxiv_submission_source.zip"
    if not zip_path.exists():
        return
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert "main.tex" in names
    assert "refs.bib" in names
    assert "main.pdf" not in names
