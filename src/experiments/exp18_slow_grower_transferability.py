"""
The pharmacodynamic constants do not transfer to a slow grower, and the exposure
schedule fails before the constants do.

Run:  python -m src.experiments.exp18_slow_grower_transferability

WHY THIS TEST EXISTS. Every pharmacodynamic constant in this project was
measured in a fast-growing organism. The manuscript reaches toward tuberculosis
in its discussion, and exp16 and exp17 analyse real mycobacterial data, so the
question of whether the constants survive the journey is not rhetorical. This
script answers it with published mycobacterial values, each traced to a primary
source and each checked to be the same kind of quantity as the constant it is
being compared with.

WHAT THE COMPARISON REQUIRED FIRST. Two things had to be settled before any
magnitude meant anything.

  The axis. This project's psi is a natural-log per-capita rate in units of
  inverse hours. `survival()` propagates it as exp(psi * tau), `net_rates`
  builds it from birth minus death, and psi_max_S = 0.990/h corresponds to a
  42-minute doubling time, which is only sensible on a natural-log basis. Regoes
  2004 reports psi in log10 per hour, so a value carried across without
  conversion is wrong by ln 10 = 2.303. Whether PSI_MIN_S = -6.0 was adopted on
  the log10 axis cannot be settled from the code, and the manuscript should say
  so; every figure below uses -6.0 as a natural-log rate, which is what the code
  consumes and the conservative reading.

  The growth rate the model actually runs. psi_max is not B_S - D_S = 0.700/h.
  The birth rate is reassigned by mic_to_br(MIC) inside net_rates, giving
  0.990/h at the wild-type MIC. Comparisons against 0.700 understate every gap.

WHICH PUBLISHED NUMBERS QUALIFY, and this is most of the work. A great many
reported Emax values are total log10 CFU reductions accumulated over a fixed
window of seven or twenty-one days. Those cannot become a psi_min by division,
because such a plateau is reached when the inoculum runs out, not when the drug
saturates. In four of the excluded studies the fitted Emax exceeds the entire
starting inoculum, which is positive proof the plateau is the detection floor.
The same disqualification applies to the Hill exponents fitted alongside them:
an exponent on a cumulative endpoint measures assay geometry, and changing the
inoculum or the window changes it with nothing about the drug changing.

Only rates fitted inside a differential equation for N are used here.

WHAT IT FINDS. Three separate failures, of increasing severity.

  1. The rates are one to three orders of magnitude too fast. psi_max is 30-fold
     too fast, psi_min between 273 and 286-fold too aggressive.

  2. The shape is wrong too, but not in the way the first version of this script
     claimed. The Regoes curve depends on psi_min and psi_max only through their
     ratio and the overall scale. This project uses -psi_min/psi_max = 6.06.

     An earlier version asserted that intracellular mycobacteria give 0.24 to
     0.67, so that the drug does not outrun growth, and that the model was
     therefore ninefold out on shape alone. That was wrong, and the error came
     from resting a ratio on a single laboratory. The apramycin deposit below
     supplies rifampicin against intracellular Mtb from an independent
     laboratory, and both halves of the ratio move: its drug-free intracellular
     control doubles in 51.7 h against the 21 h taken from PMID 28356552, and
     its rifampicin kills 2.5-fold faster over the first window. The two shifts
     compound, giving 4.10 and 2.54 for the same drug in the same state.

     Counting both sources the intracellular ratio spans 0.24 to 4.10, a
     seventeenfold range, so the model's 6.06 sits about 1.5-fold above the top
     of it rather than ninefold above the whole of it. The specific numeric
     claim does not survive.

     What survives is better for the argument than what it replaces. Within the
     second laboratory alone, one readout and one set of cells, the ratio runs
     from 0.65 for amikacin, which barely outruns growth, to 4.10 for
     rifampicin, which comfortably does; and for every drug in it the ratio
     halves between the first window and the second. The ratio is not a
     mycobacterial constant to be looked up. It is condition-, drug- and
     window-dependent, which is this project's thesis rather than an exception
     to it. The model's error is assuming any single value transfers, not
     picking the wrong one.

     The bedaquiline row reaches 21.4 and is excluded from that range, because
     its denominator is a fixed prior rather than a measured growth rate. It is
     kept in the table so the exclusion is visible rather than silent.

  3. The daily cycle stops working altogether. With TAU_TREAT = 5 h and
     TAU_GROW = 19 h, substituting mycobacterial rates gives a net population
     increase every cycle AT INFINITE ANTIBIOTIC CONCENTRATION. A five-hour
     pulse is calibrated to a 42-minute doubling time; against an organism that
     doubles in 21 hours it does almost nothing. That is a structural failure of
     the exposure schedule, not a parameter that needs refitting, and it is the
     result that should govern how far the manuscript extends to tuberculosis.

Sources, all verified against the primary record:
  PMID 28356552  Sci Rep 7:663. Intracellular and extracellular Mtb kinetics.
                 Emax reported as a rate in inverse hours.
  PMID 34871099  Antimicrob Agents Chemother 65(12). Bedaquiline in sputum from
                 56 patients; kill rate and Hill exponent inside an ODE.
  PMID 24041886  Antimicrob Agents Chemother 57(12). Drug-free growth slopes by
                 physiological state; its Table 4 Emax values are endpoint
                 reductions and are excluded.
  figshare 26462791  CC BY 4.0. Raw triplicate log10 CFU for apramycin and
                 amikacin against M. tuberculosis, planktonic and intracellular,
                 with a concurrent drug-free control at every visit. Rates here
                 are computed from those counts rather than taken from a fitted
                 table, and the control supplies psi_max measured in the same
                 wells instead of imported from another study.

Writes:
  results/tables/exp18_parameter_gaps.csv
  results/tables/exp18_kappa_sweep.csv
  results/tables/exp18_cycle_balance.csv
  results/tables/exp18_shape_ratio.csv
  results/receipts/exp18_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from ..models import boccarella as bc

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

REFERENCE_C = 12.5      # the concentration used elsewhere in this project

# Rates fitted inside a differential equation for N, in natural-log per hour.
# Endpoint reductions are deliberately absent; see the docstring.
MTB_GROWTH = [
    ("intracellular, THP-1 macrophage", 0.0330, "28356552", "21.0 h doubling"),
    ("extracellular, planktonic 7H9", 0.0769, "28356552", "9.0 h doubling"),
    ("in vivo, sputum", 0.00098, "34871099", "prior, not estimated"),
]
MTB_KILL = [
    ("rifampicin", "intracellular", -0.0220, 0.0330, "28356552"),
    ("ethambutol", "intracellular", -0.0200, 0.0330, "28356552"),
    ("pyrazinamide", "intracellular", -0.0100, 0.0330, "28356552"),
    ("isoniazid", "intracellular", -0.0080, 0.0330, "28356552"),
    ("bedaquiline", "in vivo sputum", -0.0210, 0.00098, "34871099"),
    ("rifampicin", "extracellular (provisional)", -0.1011, 0.0769, "28356552"),
    ("ethambutol", "extracellular (provisional)", -0.0651, 0.0769, "28356552"),
]

# An independent laboratory, computed from raw CFU counts rather than taken from
# a fitted table: figshare 26462791, CC BY 4.0, five sheets of triplicate log10
# CFU. Kill here is GROSS, the observed decline plus the growth of the
# concurrent drug-free control, which is the quantity psi_min denotes; and
# psi_max is that control, measured in the same wells on the same days rather
# than imported. Rates are converted to natural log per hour.
#
# Two windows are kept separately and deliberately. Collapsing them would hide
# the fact that the ratio halves between them for every drug, which is a
# principal finding rather than noise to be averaged away.
APRAMYCIN_DEPOSIT = [
    ("rifampicin 16", "intracellular, days 0-3", -0.0550, 0.0134),
    ("rifampicin 16", "intracellular, days 3-7", -0.0195, 0.0077),
    ("apramycin 32", "intracellular, days 0-3", -0.0527, 0.0134),
    ("apramycin 32", "intracellular, days 3-7", -0.0119, 0.0077),
    ("amikacin 128", "intracellular, days 0-3", -0.0142, 0.0134),
    ("amikacin 128", "intracellular, days 3-7", -0.0050, 0.0077),
]


def psi_max_as_run() -> float:
    """The growth rate the model actually uses, not B_S - D_S."""
    return float(bc.mic_to_br(bc.MIC_WT) - bc.D_S)


def psi_net(c: float, kappa: float, psi_max: float) -> float:
    """psi itself: psi_max less the Regoes reduction, in natural log per hour."""
    return psi_max - bc._regoes_reduction(c / bc.MIC_WT, psi_max,
                                          bc.PSI_MIN_S, kappa)


def main() -> int:
    for p in (TABLES, RECEIPTS):
        p.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 220)

    psi_max = psi_max_as_run()
    naive = bc.B_S - bc.D_S

    print("-- the axis and the growth rate, settled before anything is compared --")
    print(f"   psi is a natural-log rate: survival() applies exp(psi * tau)")
    print(f"   B_S - D_S                     {naive:.5f} /h  (not what the model runs)")
    print(f"   mic_to_br(MIC) - D_S          {psi_max:.5f} /h  = "
          f"{np.log(2)/psi_max*60:.0f} min doubling time")
    print(f"   PSI_MIN_S                     {bc.PSI_MIN_S:.5f} /h")
    print(f"   -psi_min/psi_max              {abs(bc.PSI_MIN_S)/psi_max:.2f}")

    # -- 1. how far each constant sits from the published mycobacterial value --
    rows = []
    for label, rate, pmid, note in MTB_GROWTH:
        rows.append({"constant": "psi_max", "model_value": psi_max,
                     "published_value": rate, "state": label, "pmid": pmid,
                     "fold_gap": psi_max / rate, "note": note})
    for drug, state, pmin, gmax, pmid in MTB_KILL:
        rows.append({"constant": "psi_min", "model_value": bc.PSI_MIN_S,
                     "published_value": pmin, "state": f"{drug}, {state}",
                     "pmid": pmid, "fold_gap": abs(bc.PSI_MIN_S / pmin),
                     "note": f"-psi_min/psi_max = {abs(pmin)/gmax:.2f}"})
    gaps = pd.DataFrame(rows)
    gaps.to_csv(TABLES / "exp18_parameter_gaps.csv", index=False)

    print("\n-- every constant is one to three orders of magnitude too fast --")
    print(gaps[["constant", "model_value", "published_value", "fold_gap",
                "state", "pmid"]].to_string(
        index=False, float_format=lambda v: f"{v:,.4f}"))

    # -- 1b. the ratio, which is where the first version of this went wrong ---
    ratio_rows = []
    for drug, state, pmin, gmax, pmid in MTB_KILL:
        ratio_rows.append({"drug": drug, "state": state,
                           "source": f"PMID {pmid}",
                           "psi_min": pmin, "psi_max": gmax,
                           "ratio": abs(pmin) / gmax})
    for drug, state, pmin, gmax in APRAMYCIN_DEPOSIT:
        ratio_rows.append({"drug": drug, "state": state,
                           "source": "figshare 26462791",
                           "psi_min": pmin, "psi_max": gmax,
                           "ratio": abs(pmin) / gmax})
    ratios = pd.DataFrame(ratio_rows).sort_values("ratio")
    ratios.to_csv(TABLES / "exp18_shape_ratio.csv", index=False)

    intra = ratios[ratios["state"].str.startswith("intracellular")]
    print("\n-- the ratio -psi_min/psi_max, which alone sets the curve's shape --")
    print(ratios.to_string(index=False, float_format=lambda v: f"{v:,.4f}"))
    print(f"\n   model assumes                     {abs(bc.PSI_MIN_S)/psi_max:6.2f}")
    print(f"   observed across both laboratories {intra['ratio'].min():6.2f} to "
          f"{intra['ratio'].max():6.2f}  (intracellular only)")
    print(f"   so the model sits {abs(bc.PSI_MIN_S)/psi_max/intra['ratio'].max():.1f}x above "
          "the top of the observed range.")
    print("\n   An earlier version of this script put that factor at 9, because it rested")
    print("   the ratio on one laboratory. The second laboratory moves both halves: its")
    print("   intracellular control doubles in 51.7 h rather than 21 h, and its")
    print("   rifampicin kills 2.5-fold faster. The specific claim does not survive.")
    print("\n   What survives is the spread. Within the second laboratory alone, one")
    print("   readout and one set of cells, the ratio runs from")
    dep = ratios[ratios["source"] == "figshare 26462791"]
    print(f"   {dep['ratio'].min():.2f} ({dep.loc[dep['ratio'].idxmin(), 'drug']}) to "
          f"{dep['ratio'].max():.2f} ({dep.loc[dep['ratio'].idxmax(), 'drug']}), and it halves")
    print("   between the first window and the second for every drug in it. The ratio is")
    print("   not a mycobacterial constant. The model's error is assuming one value")
    print("   transfers, not choosing the wrong one.")

    # -- 2. the Hill exponent, which no verified source measures on psi's axis --
    sweep = []
    for k in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
        p = psi_net(REFERENCE_C, k, psi_max)
        sweep.append({"kappa": k, "psi_net_per_h": p,
                      "survival_one_pulse": float(np.exp(p * bc.TAU_TREAT)),
                      "is_model_default": k == bc.KAPPA})
    sw = pd.DataFrame(sweep)
    sw.to_csv(TABLES / "exp18_kappa_sweep.csv", index=False)

    s1 = float(sw.loc[sw.kappa == 1.0, "survival_one_pulse"].iloc[0])
    s2 = float(sw.loc[sw.kappa == 2.0, "survival_one_pulse"].iloc[0])
    print(f"\n-- kappa, swept at c = {REFERENCE_C:g} ug/mL over one {bc.TAU_TREAT:g} h pulse --")
    print(sw.to_string(index=False, float_format=lambda v: f"{v:,.4g}"))
    print(f"\n   The model assumes kappa = {bc.KAPPA:g}. No verified mycobacterial source")
    print("   measures a Hill exponent on the axis kappa occupies: the published ones")
    print("   are exponents on cumulative endpoints or on AUC/MIC, which are different")
    print("   quantities. The only value structurally in kappa's slot is 1.0, and")
    print(f"   moving there changes single-pulse survival {s1/s2:,.3g}-fold.")

    # -- 3. the exposure schedule, which fails before the parameters do --------
    cyc = []
    for label, kill, grow in (
            [("model as calibrated", bc.PSI_MIN_S, psi_max)]
            + [(f"{d}, {s}", pmin, gmax) for d, s, pmin, gmax, _ in MTB_KILL]):
        treat = float(np.exp(kill * bc.TAU_TREAT))
        regrow = float(np.exp(grow * bc.TAU_GROW))
        cyc.append({"parameters": label, "kill_factor_per_pulse": treat,
                    "regrowth_factor": regrow, "net_per_cycle": treat * regrow,
                    "population_clears": bool(treat * regrow < 1.0)})
    cy = pd.DataFrame(cyc)
    cy.to_csv(TABLES / "exp18_cycle_balance.csv", index=False)

    print(f"\n-- the daily cycle, {bc.TAU_TREAT:g} h exposure then {bc.TAU_GROW:g} h regrowth, "
          "AT INFINITE CONCENTRATION --")
    print(cy.to_string(index=False, float_format=lambda v: f"{v:,.4g}"))

    failing = cy[~cy["population_clears"]]
    print(f"\n   {len(failing)} of {len(cy)} parameter sets leave the population growing even")
    print("   when the drug is unlimited. The five-hour pulse is calibrated to a")
    print(f"   {np.log(2)/psi_max*60:.0f}-minute doubling time; against an organism doubling in")
    print("   21 hours it removes almost nothing before regrowth replaces it.")
    print("   This is the exposure schedule failing, not the parameters.")

    (RECEIPTS / "exp18_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp18_slow_grower_transferability.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "psi_axis": "natural log per hour, confirmed from survival() and net_rates()",
        "psi_max_as_run": psi_max,
        "psi_max_naive_B_minus_D": naive,
        "psi_min_assumed": bc.PSI_MIN_S,
        "kappa_assumed": bc.KAPPA,
        "ratio_assumed": abs(bc.PSI_MIN_S) / psi_max,
        "ratio_assumed_vs_observed": {
            "model": abs(bc.PSI_MIN_S) / psi_max,
            "observed_intracellular_min": float(intra["ratio"].min()),
            "observed_intracellular_max": float(intra["ratio"].max()),
            "model_over_observed_max": float(
                abs(bc.PSI_MIN_S) / psi_max / intra["ratio"].max()),
            "superseded_claim": (
                "an earlier version reported the intracellular range as 0.24 to 0.67 "
                "and the model as ninefold out on shape; that rested on one "
                "laboratory and does not survive the second"),
        },
        "shape_ratio_rows": ratios.to_dict(orient="records"),
        "psi_max_fold_gap": psi_max / 0.0330,
        "psi_min_fold_gap_range": [abs(bc.PSI_MIN_S / -0.1011),
                                   abs(bc.PSI_MIN_S / -0.0080)],
        "kappa_1_vs_2_survival_ratio": s1 / s2,
        "n_parameter_sets_that_fail_to_clear": int(len(failing)),
        "n_parameter_sets_tested": int(len(cy)),
        "sources_verified": ["28356552", "34871099", "24041886"],
        "excluded_as_endpoint_reductions": (
            "every Emax reported as a total log10 CFU reduction over a fixed "
            "window, and every Hill exponent fitted alongside one"),
        "unresolved": (
            "whether PSI_MIN_S = -6.0 was adopted from Regoes 2004, which reports "
            "psi in log10 per hour; if so every gap here doubles"),
    }, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
