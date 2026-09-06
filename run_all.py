"""
Regenerate every number, table and figure in the current paper.

Run:  python run_all.py

The paper is a reanalysis of published deposits, so nothing here simulates
anything: each stage reads a deposit from data/raw/, computes, and writes a
table and a receipt recording the software versions it ran under. Running this
from a clean checkout should reproduce every quantity the manuscript quotes,
and `python -m src.audit_claims` afterwards checks that it did.

The earlier paper's pipeline is separate and lives at version_one/run_all.py.
The two share data/ and nothing else: version one carries its own frozen copy of
the modules they once had in common, so running one cannot alter the other's
results.
"""
from __future__ import annotations

import runpy
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

STAGES = [
    ("exp16  MIC against duration in 217 clinical isolates",
     "src.experiments.exp16_tb_mic_mdk_independence"),
    ("exp17  six laboratories, one protocol: a rate and a duration",
     "src.experiments.exp17_era4tb_between_lab"),
    ("exp18  do published constants transfer to a slow grower?",
     "src.experiments.exp18_slow_grower_transferability"),
    ("exp19  what a nominal concentration actually delivers",
     "src.experiments.exp19_windels_mic_mapping"),
    ("exp20  what the endpoint does to a 32-fold dose range",
     "src.experiments.exp20_regimen_design"),
    ("exp21  the concentration slope, interval by interval",
     "src.experiments.exp21_sequential_and_combination"),

    ("exp22  what a published tolerance classification tracks",
     "src.experiments.exp22_tolerance_dynamic_range"),

    ("exp23  how often the faster-killed flask disappears later",
     "src.experiments.exp23_inversion_decomposition"),

    ("exp24  trajectory shape, flag consistency, and what the Cox model separates",
     "src.experiments.exp24_trajectory_and_flag_audit"),

    ("exp25  how much of a published classification survives its measurement",
     "src.experiments.exp25_observability_classes"),

    ("exp26  four attempts to refute this paper's own claims",
     "src.experiments.exp26_counter_tests"),

    ("exp27  the boundaries applied cold to a held-out deposit",
     "src.experiments.exp27_out_of_sample_boundaries"),

    ("exp28  measurable depth against the turbidity standard",
     "src.experiments.exp28_standard_vs_realised"),

    ("exp29  what L actually is, deposit by deposit",
     "src.experiments.exp29_floor_provenance"),

    ("exp30  the tolerance label refitted as the ordered outcome it is",
     "src.experiments.exp30_ordinal_tolerance"),

    ("exp31  what survives once the clustering is respected",
     "src.experiments.exp31_clustering_audit"),

    ("exp32  first crossing below the boundary, and how often it holds",
     "src.experiments.exp32_crossing_events"),

    ("exp33  a posterior over the floor, and when to refuse a label",
     "src.experiments.exp33_floor_posterior"),

    ("exp34  how much of the resistance association travels through inoculum",
     "src.experiments.exp34_mediation"),

    ("exp35  the strengtheners an external review asked for",
     "src.experiments.exp35_review_strengthen"),

    ("exp36  the floor is visit-specific, and which covariates may adjust",
     "src.experiments.exp36_visit_floors_and_covariates"),

    ("exp37  every denominator, traced to the exclusion that produced it",
     "src.experiments.exp37_analysis_flow"),

    ("fig 1  the assay floor bounds the endpoint and decides the phenotype",
     "src.figures.fig1_dynamic_range"),
    ("fig 2  one protocol, six laboratories: the inoculum still decides",
     "src.figures.fig2_rate_vs_duration"),
    ("fig 3  the endpoint decides what is visible",
     "src.figures.fig3_endpoint_collapse"),
    ("fig 4  resistance and tolerance as separate axes",
     "src.figures.fig4_independence"),
    ("fig S1 which published constants transfer",
     "src.figures.fig13_parameter_transfer"),

    ("tables  build the manuscript tables from the results",
     "src.build_tables"),
    ("paper   assemble the complete document",
     "src.assemble_paper"),
    ("index   map results/ to the paper it serves",
     "src.build_results_index"),
    ("audit   recompute every quoted number from its table",
     "src.audit_claims"),
    ("check   read the legends, the box and the abstract the audit cannot",
     "src.audit_manuscript"),
]


def main() -> int:
    failures = []
    t0 = time.time()
    for label, module in STAGES:
        print(f"\n{'=' * 78}\n{label}\n{'=' * 78}", flush=True)
        started = time.time()
        r = subprocess.run([sys.executable, "-m", module], cwd=ROOT)
        took = time.time() - started
        if r.returncode == 0:
            print(f"-- ok, {took:.1f}s", flush=True)
        else:
            print(f"-- FAILED, exit {r.returncode}", flush=True)
            failures.append(label)

    print(f"\n{'=' * 78}")
    print(f"{len(STAGES) - len(failures)} of {len(STAGES)} stages completed "
          f"in {time.time() - t0:.0f}s")
    if failures:
        print("failed:")
        for f in failures:
            print(f"   {f}")
        return 1
    print("Every number in manuscript/PAPER_COMPLETE.md was regenerated from "
          "data/raw/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
