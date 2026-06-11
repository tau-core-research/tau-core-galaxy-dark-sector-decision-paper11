#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_model_families() -> None:
    rows = read_csv(ROOT / "data/source_manifest/model_family_decision_protocol.csv")
    ids = {row["family_id"] for row in rows}
    require(ids == {"M0", "M1", "M2"}, f"unexpected model families: {ids}")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "endpoint scoring must be disabled")
        require("claim" not in row["current_status"].lower(), "status must not be a claim")


def validate_freeze_requirements() -> None:
    rows = read_csv(ROOT / "data/source_manifest/policy_bundle_freeze_requirements.csv")
    require(len(rows) == 9, "expected nine policy-bundle requirements")
    for row in rows:
        require(row["required_before_endpoint"] == "true", f"{row['requirement_id']} must freeze before endpoint")
        forbidden = row["endpoint_forbidden_inputs"]
        require("endpoint" in forbidden or "rotation_residual" in forbidden, "missing forbidden endpoint inputs")


def validate_outcomes() -> None:
    rows = read_csv(ROOT / "data/source_manifest/decision_outcome_ladder.csv")
    ids = {row["outcome_id"] for row in rows}
    require(ids == {"O0", "O1", "O2", "O3", "O4"}, f"unexpected outcomes: {ids}")
    forbidden_joined = " ".join(row["forbidden_interpretation"] for row in rows).lower()
    require("global dark matter rejection" in forbidden_joined, "missing no-global-rejection guard")


def validate_policy_bundle_instance() -> None:
    rows = read_csv(ROOT / "data/source_manifest/frozen_policy_bundle_instance_v01.csv")
    require(len(rows) == 9, "expected nine frozen policy-bundle component references")
    components = {row["component"] for row in rows}
    require("delta_M_extraction_freeze" in components, "missing delta_M extraction freeze")
    require("ChannelHandoff_policy" in components, "missing channel handoff policy")
    for row in rows:
        require(row["bundle_id"] == "PB11_v01", "unexpected bundle id")
        require(row["endpoint_scoring_allowed"] == "false", "policy bundle cannot allow endpoint scoring")
        require(row["missing_content"], f"{row['component']} must list missing content")


def validate_galaxy_endpoint_manifest() -> None:
    rows = read_csv(ROOT / "data/source_manifest/galaxy_decision_endpoint_manifest_v01.csv")
    ids = {row["endpoint_id"] for row in rows}
    required = {
        "E11_SCOPE",
        "E11_SAMPLE_TRAIN",
        "E11_SAMPLE_HELDOUT",
        "E11_SCORE",
        "E11_CONTROL_WRONG_FAMILY",
        "E11_CONTROL_SHUFFLE",
        "E11_ZONE",
        "E11_VERDICT",
    }
    require(ids == required, f"unexpected endpoint manifest ids: {ids}")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "endpoint manifest v01 must disable scoring")
        require(row["required_before_scoring"] == "true", f"{row['endpoint_id']} must precede scoring")
        require(row["allowed_model_families"] == "M0;M1;M2", "all families must share the endpoint manifest")


def validate_sample_freeze() -> None:
    rows = read_csv(ROOT / "data/source_manifest/galaxy_sample_freeze_v01.csv")
    ids = {row["sample_id"] for row in rows}
    require(ids == {"GS_SCOPE", "GS_TRAIN", "GS_HELDOUT", "GS_CHALLENGE", "GS_EXCLUSION"}, "bad sample freeze ids")
    for row in rows:
        require(row["required_before_scoring"] == "true", f"{row['sample_id']} must precede scoring")
        require(row["endpoint_scoring_allowed"] == "false", "sample v01 must disable endpoint scoring")
        require(row["forbidden_inputs"], f"{row['sample_id']} missing forbidden inputs")


def validate_scoring_freeze() -> None:
    rows = read_csv(ROOT / "data/source_manifest/scoring_rule_freeze_v01.csv")
    ids = {row["score_id"] for row in rows}
    required = {"SC_FULL_CURVE", "SC_ZONE_INNER", "SC_ZONE_FLAT", "SC_HELDOUT", "SC_PARSIMONY", "SC_CONTROL"}
    require(ids == required, f"bad scoring ids: {ids}")
    for row in rows:
        require(row["required_before_scoring"] == "true", f"{row['score_id']} must precede scoring")
        require(row["endpoint_scoring_allowed"] == "false", "scoring v01 must disable endpoint scoring")
        require("PENDING" in row["current_status"], "v01 scoring must remain formula-pending")


def validate_controls() -> None:
    rows = read_csv(ROOT / "data/source_manifest/control_manifest_v01.csv")
    ids = {row["control_id"] for row in rows}
    required = {"CTRL_SHUFFLE", "CTRL_WRONG_FAMILY", "CTRL_NULL_SOURCE", "CTRL_LEAKAGE", "CTRL_RADIAL_PERMUTE"}
    require(ids == required, f"bad control ids: {ids}")
    for row in rows:
        require(row["required_before_scoring"] == "true", f"{row['control_id']} must precede scoring")
        require(row["endpoint_scoring_allowed"] == "false", "controls v01 must disable endpoint scoring")
        require("IMPLEMENTATION_PENDING" in row["current_status"], "controls must remain implementation-pending")


def validate_thresholds() -> None:
    rows = read_csv(ROOT / "data/source_manifest/decision_threshold_v01.csv")
    labels = {row["verdict_label"] for row in rows}
    required = {"M0_SUFFICIENT", "M1_FAVORED", "M2_BENCHMARK_STRONGER", "UNRESOLVED"}
    require(labels == required, f"bad verdict labels: {labels}")
    forbidden = " ".join(row["forbidden_interpretation"] for row in rows).lower()
    require("global dark matter rejection" in forbidden, "thresholds must block global no-DM claim")
    require("physical tau dark-sector field" in forbidden, "thresholds must block physical-field promotion")
    for row in rows:
        require("NUMERIC_CUTOFF_PENDING" in row["current_status"], "numeric cutoffs must remain pending")


def validate_galaxy_list_v02() -> None:
    rows = read_csv(ROOT / "data/source_manifest/galaxy_list_freeze_v02.csv")
    galaxies = {row["galaxy_id"] for row in rows}
    required = {"NGC4559", "NGC4010", "NGC5585", "UGC06930", "NGC4183", "NGC4088", "UGC12506"}
    require(required.issubset(galaxies), f"v02 galaxy role list missing required rows: {required - galaxies}")
    roles = {row["decision_role"] for row in rows}
    require("train_formula_candidate" in roles, "v02 list missing train role")
    require("challenge_high_spin_edge_on" in roles, "v02 list missing high-spin challenge role")
    require("beta_closure_transfer_candidate" in roles, "v02 list missing beta transfer role")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "v02 galaxy list must disable endpoint scoring")
        require("NOT_ACTIVE" in row["scoring_activation_status"], "v02 galaxy rows must remain inactive")
        require("family_winner" in row["forbidden_inputs"], "v02 galaxy rows must forbid family-winner leakage")


def validate_scoring_formula_v02() -> None:
    rows = read_csv(ROOT / "data/source_manifest/scoring_formula_freeze_v02.csv")
    ids = {row["formula_id"] for row in rows}
    required = {
        "SF02_FULL_CURVE",
        "SF02_INNER_ZONE",
        "SF02_OUTER_ZONE",
        "SF02_PARSIMONY",
        "SF02_GALAXY_SCORE",
        "SF02_HELDOUT",
        "SF02_CONTROL_VETO",
    }
    require(ids == required, f"bad v02 scoring formula ids: {ids}")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "v02 scoring formula must disable endpoint scoring")
        require("FORMULA_POLICY_FROZEN_NOT_RUN" in row["current_status"], "v02 formulas must remain unrun")
        require(row["forbidden_inputs"], f"{row['formula_id']} missing forbidden inputs")


def main() -> None:
    validate_model_families()
    validate_freeze_requirements()
    validate_outcomes()
    validate_policy_bundle_instance()
    validate_galaxy_endpoint_manifest()
    validate_sample_freeze()
    validate_scoring_freeze()
    validate_controls()
    validate_thresholds()
    validate_galaxy_list_v02()
    validate_scoring_formula_v02()
    print("PAPER11_PROTOCOL_MANIFESTS_VALID")


if __name__ == "__main__":
    main()
