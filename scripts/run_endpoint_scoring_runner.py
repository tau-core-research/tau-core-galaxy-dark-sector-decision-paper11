#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
INPUT = ROOT / "data/input"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "endpoint_scoring_runner_v01_raw_m0_adequacy_diagnostic_only_no_family_comparison_no_verdict"

FIELDS = [
    "raw_score_row_id",
    "scoring_row_id",
    "galaxy_id",
    "family_id",
    "radial_points_scored",
    "chi2_full_raw",
    "chi2_inner_raw",
    "chi2_outer_raw",
    "parsimony_penalty_raw",
    "raw_m0_adequacy_diagnostic",
    "raw_score_status",
    "family_comparison_allowed",
    "control_pass_claim_allowed",
    "endpoint_scoring_allowed",
    "dark_sector_verdict_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "scoring_mode",
    "preflight_status",
    "raw_diagnostic_rows_written",
    "radial_points_scored",
    "families_scored",
    "family_comparison_rows_written",
    "control_result_rows_written",
    "endpoint_verdict_scores_written",
    "family_comparison_allowed_anywhere",
    "control_pass_claim_allowed_anywhere",
    "endpoint_scoring_allowed_anywhere",
    "dark_sector_verdict_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("cannot average an empty sequence")
    return sum(values) / len(values)


def fmt(value: float) -> str:
    return f"{value:.6f}"


def m0_parsimony_penalty() -> float:
    rows = read_csv(DERIVED / "numeric_parameter_count_table_final_values_v10.csv")
    return sum(
        float(row["final_parsimony_count_value"])
        for row in rows
        if row["family_id"] == "M0" and row["parsimony_input_allowed"] == "true"
    )


def build_rows() -> list[dict[str, object]]:
    preflight = read_csv(DERIVED / "scoring_preflight_summary_v07.csv")[0]
    if preflight["overall_status"] != "SCORING_PREFLIGHT_REQUIREMENTS_READY_RAW_M0_ADEQUACY_RUNNER_NEXT_VERDICT_BLOCKED":
        raise RuntimeError("scoring preflight is not ready for the raw M0 adequacy runner")

    observed = {
        (row["galaxy_id"], row["radial_index"]): row
        for row in read_csv(INPUT / "source_import_real_values_v12.csv")
    }
    predictions = [
        row
        for row in read_csv(DERIVED / "family_prediction_tables_v08.csv")
        if row["family_id"] == "M0"
    ]
    activation_order = {
        row["scoring_row_id"]: index
        for index, row in enumerate(read_csv(DERIVED / "activated_scoring_rows_v10.csv"))
    }

    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for prediction in predictions:
        key = (prediction["galaxy_id"], prediction["radial_index"])
        if key not in observed:
            raise RuntimeError(f"missing observed source row for {key}")
        grouped[(prediction["scoring_row_id"], prediction["galaxy_id"])].append(prediction)

    penalty = m0_parsimony_penalty()
    rows: list[dict[str, object]] = []
    for index, ((scoring_row_id, galaxy_id), galaxy_predictions) in enumerate(
        sorted(grouped.items(), key=lambda item: activation_order[item[0][0]]),
        start=1,
    ):
        ordered = sorted(galaxy_predictions, key=lambda row: int(row["radial_index"]))
        residual_terms: list[float] = []
        for prediction in ordered:
            source = observed[(prediction["galaxy_id"], prediction["radial_index"])]
            sigma = float(source["sigma_v_km_s"])
            if sigma <= 0:
                raise RuntimeError(f"non-positive sigma for {galaxy_id} radial index {prediction['radial_index']}")
            residual_terms.append(
                ((float(source["v_obs_km_s"]) - float(prediction["v_pred_km_s"])) / sigma) ** 2
            )

        zone_width = max(1, len(residual_terms) // 3)
        chi2_full = mean(residual_terms)
        chi2_inner = mean(residual_terms[:zone_width])
        chi2_outer = mean(residual_terms[-zone_width:])
        raw_score = chi2_full + 0.5 * chi2_inner + 0.5 * chi2_outer + penalty

        rows.append(
            {
                "raw_score_row_id": f"ESR01_{index:03d}",
                "scoring_row_id": scoring_row_id,
                "galaxy_id": galaxy_id,
                "family_id": "M0",
                "radial_points_scored": str(len(residual_terms)),
                "chi2_full_raw": fmt(chi2_full),
                "chi2_inner_raw": fmt(chi2_inner),
                "chi2_outer_raw": fmt(chi2_outer),
                "parsimony_penalty_raw": fmt(penalty),
                "raw_m0_adequacy_diagnostic": fmt(raw_score),
                "raw_score_status": "RAW_M0_ADEQUACY_DIAGNOSTIC_WRITTEN_NOT_VERDICT",
                "family_comparison_allowed": "false",
                "control_pass_claim_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "dark_sector_verdict_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    preflight = read_csv(DERIVED / "scoring_preflight_summary_v07.csv")[0]
    return [
        {
            "summary_id": "ENDPOINT_SCORING_RUNNER_V01",
            "scoring_mode": "RAW_M0_ADEQUACY_DIAGNOSTIC_ONLY",
            "preflight_status": preflight["overall_status"],
            "raw_diagnostic_rows_written": str(len(rows)),
            "radial_points_scored": str(sum(int(row["radial_points_scored"]) for row in rows)),
            "families_scored": str(len({row["family_id"] for row in rows})),
            "family_comparison_rows_written": "0",
            "control_result_rows_written": "0",
            "endpoint_verdict_scores_written": "0",
            "family_comparison_allowed_anywhere": "false",
            "control_pass_claim_allowed_anywhere": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "dark_sector_verdict_allowed_anywhere": "false",
            "overall_status": "ENDPOINT_SCORING_RUNNER_V01_RAW_M0_ADEQUACY_DIAGNOSTICS_WRITTEN_VERDICT_BLOCKED",
            "next_required_artifact": "control_result_execution_v01.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "endpoint_scoring_runner_v01.md").write_text(
        """# Endpoint Scoring Runner v01

**Doc class:** raw M0 adequacy diagnostic runner
**Status:** raw M0 diagnostic values written; endpoint verdict remains blocked

Script:

```text
scripts/run_endpoint_scoring_runner.py
```

Derived outputs:

```text
data/derived/endpoint_scoring_runner_v01.csv
data/derived/endpoint_scoring_runner_summary_v01.csv
```

This runner is the first numeric post-preflight artifact. It joins the frozen
M0 prediction rows with imported SPARC observed velocity rows by galaxy and
radial index, then writes per-galaxy raw adequacy diagnostics.

The diagnostic formula is:

```text
raw_m0_adequacy_diagnostic =
  chi2_full_raw + 0.5 * chi2_inner_raw + 0.5 * chi2_outer_raw
  + parsimony_penalty_raw
```

where each chi2 term is the mean of `((v_obs - v_pred) / sigma_v)^2` on the
declared radial region. The inner and outer regions use the first and last
third of the sorted radial rows. The current M0 parsimony penalty is read from
the frozen numeric parameter-count table.

## Claim Boundary

This artifact does not compare M0 against M1 or M2, does not execute controls,
does not claim any control pass, does not authorize endpoint scoring, and does
not make a dark-sector necessity verdict. The word "runner" names the scaffold
that can compute raw diagnostics after preflight; it is not an endpoint verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = build_rows()
    write_csv(DERIVED / "endpoint_scoring_runner_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "endpoint_scoring_runner_summary_v01.csv", build_summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_ENDPOINT_SCORING_RUNNER_V01_BUILT")


if __name__ == "__main__":
    main()
