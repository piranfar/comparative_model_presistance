#!/usr/bin/env python
"""
Reproduce every number and every figure, from a clean checkout, in one command.

    python run_all.py

Order matters: the experiments write the tables and arrays that the figures
read. Each stage prints its own summary and writes a receipt under
results/receipts/ recording library versions and run parameters.

Runtime is roughly two to three minutes, dominated by the 9,216 ODE solves of
the global sensitivity analysis in exp03.

Nothing here downloads data or contacts a network. There is no experimental
dataset in this project, so every quantity is either recomputed from the
preprint's own equations and Table 1, or generated from the mechanistic model
and labelled synthetic.
"""
from __future__ import annotations

import runpy
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

STAGES = [
    ("exp01  recalculate every claim from the paper's own equations",
     "src.experiments.exp01_recalculate_equations"),
    ("exp02  fit the closed-form models and test identifiability",
     "src.experiments.exp02_fit_and_identifiability"),
    ("exp03  sensitivity analysis, one-at-a-time and global",
     "src.experiments.exp03_sensitivity"),
    ("fig 1  growth and the three survival strategies",
     "src.figures.fig01_growth_and_strategies"),
    ("fig 2  biphasic killing and its two corrections",
     "src.figures.fig02_biphasic_killing"),
    ("fig 3  model fitting, uncertainty and identifiability",
     "src.figures.fig03_model_fitting"),
    ("fig 4  sensitivity analysis",
     "src.figures.fig04_sensitivity"),
    ("fig 5  the mechanistic replacement",
     "src.figures.fig05_mechanistic_model"),
    ("fig 6  three strategies, three signatures",
     "src.figures.fig06_mic_mdk_plane"),
    ("fig S1 three statistical claims, checked",
     "src.figures.fig07_supplementary_diagnostics"),
]


def main() -> int:
    sys.path.insert(0, str(ROOT))
    failures = []
    t_start = time.perf_counter()

    for title, module in STAGES:
        print("\n" + "=" * 78)
        print(title)
        print("=" * 78)
        t0 = time.perf_counter()
        try:
            runpy.run_module(module, run_name="__main__")
        except SystemExit as exc:
            if exc.code not in (0, None):
                failures.append((module, f"exit code {exc.code}"))
        except Exception as exc:                      # noqa: BLE001
            failures.append((module, f"{type(exc).__name__}: {exc}"))
            print(f"  FAILED: {type(exc).__name__}: {exc}")
        print(f"  [{time.perf_counter() - t0:.1f}s]")

    print("\n" + "=" * 78)
    print(f"total {time.perf_counter() - t_start:.1f}s")
    if failures:
        print(f"{len(failures)} stage(s) failed:")
        for module, why in failures:
            print(f"  {module}: {why}")
        return 1
    print("all stages completed")
    print(f"  tables   {ROOT / 'results' / 'tables'}")
    print(f"  figures  {ROOT / 'results' / 'figures'}")
    print(f"  receipts {ROOT / 'results' / 'receipts'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
