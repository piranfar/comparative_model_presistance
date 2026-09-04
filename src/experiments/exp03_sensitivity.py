"""
Sensitivity analysis done three ways, to show what the paper's version misses.

Run:  python -m src.experiments.exp03_sensitivity

Methods 2.3.2 reports a one-at-a-time analysis varying parameters by +/-10%,
concluding that Mtb persistence is most sensitive to k_slow and S. aureus to
k_T. exp01 shows that ranking is an algebraic identity of the printed equation,
not a result. This script provides:

  A. the paper's own OAT +/-10% analysis, reproduced faithfully on the printed
     Eq. 4, so the tautology is visible as a table rather than asserted;
  B. the same OAT analysis on the mechanistic two-compartment model, where all
     parameters act at all times, so the ranking carries information;
  C. a variance-based global analysis (Sobol first-order and total indices via
     the Saltelli estimator) on the mechanistic model, which is the only one of
     the three that can detect parameter interactions.

The gap between the first-order and total Sobol indices is the quantity a
one-at-a-time analysis cannot produce at all: it measures how much of the
outcome variance comes from parameters acting jointly rather than alone. If that
gap is large, OAT conclusions are not merely imprecise, they are the wrong kind
of statement.

Writes:
  results/tables/sensitivity_oat_printed.csv
  results/tables/sensitivity_oat_mechanistic.csv
  results/tables/sensitivity_sobol.csv
  data/processed/sobol_samples.npz
  results/receipts/exp03_receipt.json
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from dataclasses import replace
from scipy.stats import qmc

from ..models import corrected as fix
from ..models import paper_equations as eq
from ..models.mechanistic import PD_SPECIES, PDParams, mic, simulate
from ..models.parameters import LOD_CFU_ML, SPECIES

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "results" / "tables"
PROCESSED = ROOT / "data" / "processed"
RECEIPTS = ROOT / "results" / "receipts"

# Drug exposure. Two conventions, and the analysis is run under both because
# they are not interchangeable and the earlier version silently used the first.
#
#   "absolute"  C = 4 in units of the reference MIC, the same number for every
#               parameter set. The two species of Section 2.6 have MICs of 0.26
#               and 0.80, so this compares them at 15.1x and 5.0x their own MIC
#               and any between-species contrast is confounded with exposure.
#   "per_mic"   C = 4 x the MIC of that parameter set, recomputed for every
#               draw. Species are compared at matched exposure. Note this also
#               closes the route by which EC50 acts on the outcome through
#               exposure, so the two conventions ask genuinely different
#               questions of the same model.
C_MULTIPLE = 4.0
EXPOSURE_MODES = ("per_mic", "absolute")


def exposure(p: PDParams, mode: str) -> float:
    """Concentration for one parameter set under the chosen convention."""
    if mode == "absolute":
        return C_MULTIPLE
    if mode == "per_mic":
        m = mic(p)
        if not np.isfinite(m):
            return float("inf")
        return C_MULTIPLE * m
    raise ValueError(f"unknown exposure mode {mode!r}")
N0 = 1.0e6
T_ENDPOINT = 240.0
T_GRID = np.linspace(0.0, 2000.0, 1001)
SOBOL_LOG2N = 12         # N = 4096 base samples -> 4096 * (k+2) evaluations
PERTURB = 0.10           # the paper's +/-10%

# Parameters varied in the global analysis, with the multiplicative range
# applied to each. Ranges are deliberately wide, +/-50%, because the point of a
# global analysis is to cover the plausible parameter space rather than a small
# neighbourhood of one assumed point.
SOBOL_PARAMS = ["r", "Emax_S", "Emax_P", "EC50", "H", "k_SP", "k_PS"]
SOBOL_SPAN = 0.5


# --------------------------------------------------------------- endpoints ---

def endpoints_mechanistic(p: PDParams, mode: str = "per_mic") -> dict:
    """Three endpoints from one ODE solve, by interpolation on a fixed grid.

    Using a single solve per parameter draw is what makes a Sobol analysis of an
    ODE model affordable. Time to LOD is right-censored at the end of the grid
    and reported as such, never silently clipped.

    `mode` selects the exposure convention; see EXPOSURE_MODES above.
    """
    out = simulate(p, exposure(p, mode), T_GRID, N0=N0)
    total = np.maximum(out["total"], 1e-300)
    log10_total = np.log10(total)

    drop_240 = float(np.log10(N0) - np.interp(T_ENDPOINT, T_GRID, log10_total))

    def crossing(target_log10):
        below = np.where(log10_total <= target_log10)[0]
        if below.size == 0:
            return float(T_GRID[-1]), True      # censored
        i = int(below[0])
        if i == 0:
            return 0.0, False
        y0, y1 = log10_total[i - 1], log10_total[i]
        t0, t1 = T_GRID[i - 1], T_GRID[i]
        if y1 == y0:
            return float(t1), False
        return float(t0 + (target_log10 - y0) * (t1 - t0) / (y1 - y0)), False

    t_lod, lod_cens = crossing(np.log10(LOD_CFU_ML))
    t_mdk99, mdk_cens = crossing(np.log10(N0 * 0.01))

    return {
        "log10_drop_240h": drop_240,
        "time_to_LOD_h": t_lod,
        "time_to_LOD_censored": lod_cens,
        "MDK99_h": t_mdk99,
        "MDK99_censored": mdk_cens,
    }


def endpoints_printed(sp, k_fast=None, k_slow=None, f=None, t_c=None,
                      k_T=None) -> dict:
    """The same endpoints under the printed Eq. 4 and Eq. 3."""
    k_fast = sp.k_fast if k_fast is None else k_fast
    k_slow = sp.k_slow if k_slow is None else k_slow
    f = sp.f_dormant_point if f is None else f
    t_c = sp.t_c_asserted if t_c is None else t_c
    k_T = sp.k_T if k_T is None else k_T

    pers = lambda t: eq.persistence_as_printed(t, sp.N0, k_fast, k_slow, f, t_c)
    tol = lambda t: eq.tolerance_as_printed(t, sp.N0, k_T)
    return {
        "log10_drop_240h_persistence": fix.log10_drop(pers, sp.N0, T_ENDPOINT),
        "time_to_LOD_h_persistence": fix.time_to_lod(pers, LOD_CFU_ML),
        "log10_drop_240h_tolerance": fix.log10_drop(tol, sp.N0, T_ENDPOINT),
        "time_to_LOD_h_tolerance": fix.time_to_lod(tol, LOD_CFU_ML),
    }


# --------------------------------------------------------- A. OAT, printed ---

def oat_printed() -> pd.DataFrame:
    rows = []
    for short, sp in SPECIES.items():
        base = endpoints_printed(sp)
        for name in ("k_fast", "k_slow", "f_dormant", "t_c", "k_T"):
            for sign, tag in ((1 + PERTURB, "+10%"), (1 - PERTURB, "-10%")):
                kw = {}
                if name == "k_fast":
                    kw["k_fast"] = sp.k_fast * sign
                elif name == "k_slow":
                    kw["k_slow"] = sp.k_slow * sign
                elif name == "f_dormant":
                    kw["f"] = sp.f_dormant_point * sign
                elif name == "t_c":
                    kw["t_c"] = sp.t_c_asserted * sign
                else:
                    kw["k_T"] = sp.k_T * sign
                pert = endpoints_printed(sp, **kw)
                for ep in ("log10_drop_240h_persistence",
                           "log10_drop_240h_tolerance"):
                    b, v = base[ep], pert[ep]
                    rows.append({
                        "species": short, "model": "Eq. 4 / Eq. 3 as printed",
                        "parameter": name, "perturbation": tag,
                        "endpoint": ep, "baseline": b, "perturbed": v,
                        "abs_change": v - b,
                        "pct_change": 100.0 * (v - b) / b if b != 0 else np.nan,
                        "elasticity": ((v - b) / b) / (sign - 1.0)
                        if b != 0 else np.nan,
                    })
    df = pd.DataFrame(rows)
    return df


# ---------------------------------------------------- B. OAT, mechanistic ----

def oat_mechanistic(mode: str = "per_mic") -> pd.DataFrame:
    rows = []
    for short, p in PD_SPECIES.items():
        base = endpoints_mechanistic(p, mode)
        for name in SOBOL_PARAMS:
            for sign, tag in ((1 + PERTURB, "+10%"), (1 - PERTURB, "-10%")):
                pert_p = replace(p, **{name: getattr(p, name) * sign})
                pert = endpoints_mechanistic(pert_p, mode)
                for ep in ("log10_drop_240h", "time_to_LOD_h", "MDK99_h"):
                    b, v = base[ep], pert[ep]
                    rows.append({
                        "species": short, "model": "two-compartment mechanistic",
                        "parameter": name, "perturbation": tag,
                        "endpoint": ep, "baseline": b, "perturbed": v,
                        "abs_change": v - b,
                        "pct_change": 100.0 * (v - b) / b if b != 0 else np.nan,
                        "elasticity": ((v - b) / b) / (sign - 1.0)
                        if b != 0 else np.nan,
                        "censored": bool(base.get(ep.replace("_h", "") +
                                                  "_censored", False)),
                    })
    return pd.DataFrame(rows)


# ------------------------------------------------------ C. Sobol, Saltelli ---

def _scale(unit_sample: np.ndarray, p: PDParams) -> list[PDParams]:
    """Map a unit hypercube sample to parameter sets, log-uniform in each rate."""
    out = []
    for row in unit_sample:
        kw = {}
        for j, name in enumerate(SOBOL_PARAMS):
            base = getattr(p, name)
            lo, hi = base * (1 - SOBOL_SPAN), base * (1 + SOBOL_SPAN)
            # log-uniform: rates span orders of magnitude in the literature
            kw[name] = float(np.exp(np.log(lo) + row[j] * (np.log(hi) - np.log(lo))))
        out.append(replace(p, **kw))
    return out


N_BOOT = 2000


def _boot_ci(ya, yb, yabi, n_boot: int = N_BOOT, seed: int = 20260904):
    """Percentile bootstrap interval for one Saltelli index pair."""
    rng = np.random.default_rng(seed)
    n = ya.size
    idx = rng.integers(0, n, size=(n_boot, n))
    a, b, ab = ya[idx], yb[idx], yabi[idx]
    var = np.var(np.concatenate([a, b], axis=1), axis=1, ddof=1)
    var = np.where(var > 0, var, np.nan)
    s1 = np.mean(b * (ab - a), axis=1) / var
    st = np.mean((a - ab) ** 2, axis=1) / (2 * var)
    q = lambda v: (float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5)))
    return (*q(s1), *q(st))


def sobol_indices(mode: str = "per_mic") -> tuple[pd.DataFrame, dict]:
    k = len(SOBOL_PARAMS)
    rows = []
    store = {}
    for short, p in PD_SPECIES.items():
        sampler = qmc.Sobol(d=2 * k, scramble=True, seed=20250212)
        base = sampler.random_base2(SOBOL_LOG2N)
        A, B = base[:, :k], base[:, k:]
        n = A.shape[0]

        def evaluate(unit):
            eps = [endpoints_mechanistic(q, mode) for q in _scale(unit, p)]
            return {ep: np.array([e[ep] for e in eps]) for ep in
                    ("log10_drop_240h", "time_to_LOD_h", "MDK99_h")}

        YA = evaluate(A)
        YB = evaluate(B)
        YAB = []
        for i in range(k):
            ABi = A.copy()
            ABi[:, i] = B[:, i]
            YAB.append(evaluate(ABi))

        for ep in YA:
            ya, yb = YA[ep], YB[ep]
            var = float(np.var(np.concatenate([ya, yb]), ddof=1))
            store[f"{short}|{ep}|A"] = ya
            store[f"{short}|{ep}|B"] = yb
            for i, name in enumerate(SOBOL_PARAMS):
                yabi = YAB[i][ep]
                s1 = float(np.mean(yb * (yabi - ya)) / var) if var > 0 else np.nan
                st = float(np.mean((ya - yabi) ** 2) / (2 * var)) if var > 0 else np.nan
                # Bootstrap interval over the sample pairs. A first-order index
                # whose interval contains zero, or that comes out negative, is
                # Monte Carlo noise rather than an estimate, and saying so is
                # the only honest way to report an index near zero.
                s1_lo, s1_hi, st_lo, st_hi = _boot_ci(ya, yb, yabi)
                rows.append({
                    "species": short, "endpoint": ep, "parameter": name,
                    "S1_first_order": s1,
                    "S1_boot_lo": s1_lo,
                    "S1_boot_hi": s1_hi,
                    "ST_boot_lo": st_lo,
                    "ST_boot_hi": st_hi, "ST_total": st,
                    "interaction_ST_minus_S1": st - s1,
                    "output_variance": var, "n_base_samples": n,
                })
    df = pd.DataFrame(rows)
    return df, store


# ---------------------------------------------------------------------------

def main() -> int:
    for d in (TABLES, PROCESSED, RECEIPTS):
        d.mkdir(parents=True, exist_ok=True)

    t0 = time.perf_counter()
    oat_p = oat_printed()

    # Both exposure conventions, because the headline ranking is a claim about
    # the model and should not be a claim about which convention was used.
    oat_parts, sob_parts, store = [], [], {}
    for mode in EXPOSURE_MODES:
        om = oat_mechanistic(mode)
        om.insert(0, "exposure_mode", mode)
        oat_parts.append(om)
        sb, st = sobol_indices(mode)
        sb.insert(0, "exposure_mode", mode)
        sob_parts.append(sb)
        store.update({f"{mode}__{k}": v for k, v in st.items()})
    oat_m = pd.concat(oat_parts, ignore_index=True)
    sob = pd.concat(sob_parts, ignore_index=True)
    elapsed = time.perf_counter() - t0

    oat_p.to_csv(TABLES / "sensitivity_oat_printed.csv", index=False)
    oat_m.to_csv(TABLES / "sensitivity_oat_mechanistic.csv", index=False)
    sob.to_csv(TABLES / "sensitivity_sobol.csv", index=False)
    np.savez_compressed(PROCESSED / "sobol_samples.npz", **store)

    # The tautology, stated as a number: under the printed equation the
    # persistence endpoint at 240 h has exactly zero elasticity to k_fast.
    taut = (oat_p[(oat_p["endpoint"] == "log10_drop_240h_persistence") &
                  (oat_p["parameter"] == "k_fast")]["abs_change"].abs().max())

    # How much of the mechanistic variance is interaction rather than main
    # effect: the quantity OAT cannot produce.
    inter = (sob.groupby(["exposure_mode", "species", "endpoint"])
             .apply(lambda g: 1.0 - g["S1_first_order"].sum(),
                    include_groups=False)
             .rename("fraction_variance_from_interactions").reset_index())
    inter.to_csv(TABLES / "sensitivity_interaction_fraction.csv", index=False)

    receipt = {
        "script": "src/experiments/exp03_sensitivity.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "concentration_multiple_of_MIC": C_MULTIPLE,
        "exposure_modes": list(EXPOSURE_MODES),
        "reported_mode": "per_mic",
        "oat_perturbation": PERTURB,
        "sobol_base_samples": 2 ** SOBOL_LOG2N,
        "sobol_model_evaluations_per_species":
            int(2 ** SOBOL_LOG2N * (len(SOBOL_PARAMS) + 2)),
        "sobol_span_fraction": SOBOL_SPAN,
        "max_abs_change_from_k_fast_printed_240h": float(taut),
        "runtime_seconds": round(elapsed, 1),
        "max_interaction_fraction": float(
            inter["fraction_variance_from_interactions"].max()),
    }
    (RECEIPTS / "exp03_receipt.json").write_text(
        json.dumps(receipt, indent=2), encoding="utf-8")

    print(f"runtime {elapsed:.1f}s, "
          f"{receipt['sobol_model_evaluations_per_species']:,} ODE solves per species\n")

    print("-- A. paper's OAT +/-10% on the printed equation, "
          "persistence endpoint at 240 h --")
    a = oat_p[oat_p["endpoint"] == "log10_drop_240h_persistence"]
    print(a.pivot_table(index=["species", "parameter"], columns="perturbation",
                        values="pct_change").to_string(
        float_format=lambda v: f"{v:,.4g}"))

    print("\n-- B. OAT +/-10% on the mechanistic model, time to LOD --")
    b = oat_m[oat_m["endpoint"] == "time_to_LOD_h"]
    print(b.pivot_table(index=["species", "parameter"], columns="perturbation",
                        values="pct_change").to_string(
        float_format=lambda v: f"{v:,.4g}"))

    print("\n-- C. Sobol indices, time to LOD --")
    c = sob[sob["endpoint"] == "time_to_LOD_h"].sort_values(
        ["species", "ST_total"], ascending=[True, False])
    print(c[["species", "parameter", "S1_first_order", "ST_total",
             "interaction_ST_minus_S1"]].to_string(
        index=False, float_format=lambda v: f"{v:,.3f}"))

    print("\n-- fraction of output variance from interactions --")
    print(inter.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
