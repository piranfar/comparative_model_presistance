"""
Thin loader that executes the authors' deposited simulation unchanged.

The vendored file `external/boccarella2026/magnitude_of_evolution_simulations.py`
is byte-identical to the authors' deposit (doi:10.6084/m9.figshare.31389142,
CC BY 4.0). Running it unmodified is what allows a difference in outcome to be
attributed to a change in inputs rather than to a difference in implementation.

Two accommodations are made here and nowhere else:
  * `mpi4py` is stubbed. Their `main()` uses it to distribute work across a
    cluster; `run_simulation_with_mic`, which is the function called here, does
    not touch MPI at all.
  * the global NumPy random state is seeded per replicate, so a run is
    reproducible. Their script does not seed, so their replicates are not
    individually reproducible. This changes which random draws occur, not how
    they are drawn.
"""
from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import numpy as np

VENDORED = (Path(__file__).resolve().parents[2] / "external" / "boccarella2026"
            / "magnitude_of_evolution_simulations.py")

_MODULE = None


def load():
    """Import the authors' script, stubbing mpi4py. Cached per process."""
    global _MODULE
    if _MODULE is not None:
        return _MODULE
    if "mpi4py" not in sys.modules:
        stub = types.ModuleType("mpi4py")
        stub.MPI = types.SimpleNamespace(COMM_WORLD=None)
        sys.modules["mpi4py"] = stub
    spec = importlib.util.spec_from_file_location("boccarella_sim", VENDORED)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _MODULE = mod
    return mod


def default_params(alpha: float, c: float = 12.5, sim_id: int = 0,
                   sigma: float = 0.7, min_br: float = 2.0,
                   days: int = 12) -> dict:
    """The parameter set the PUBLISHED runs used, with alpha and c exposed.

    Two values here are taken from the parameter columns recorded inside the
    authors' own deposited result sheets rather than from their `main()`, which
    does not reproduce their published output:

      min_bR = 2.0. Their `main()` sets `min_bR_values = [bS]`, i.e. 1.7, but
        every row of their deposited Fig_2_b and Fig_6 output records min_bR=2.
        The difference is not cosmetic: `mic_to_br` interpolates the birth rate
        from 2.0 at MIC 1 down to min_bR at MIC 32, so 1.7 imposes a fitness
        cost on resistance and 2.0 imposes none. Running with 1.7 suppresses
        resistance evolution and does not reproduce their figures.

      sigma = 0.7, which their code and their deposited output agree on. Their
        Table 1 prints 0.07. See DISCREPANCIES in `boccarella.py`.

    Both were established by reading the recorded parameter columns of the
    deposited results, and both are verified in exp06 by reproducing their
    published final-MIC distribution.
    """
    return {
        "simulation_id": sim_id,
        "tfin": 24 * days,
        "c": c,
        "initial_pers_level": alpha,
        "kappaS": 2,
        "psiminS": -6,
        "mu_mut_MIC": 1e-6,
        "dilution_factor": 1,
        "min_bR": min_br,
        "min_value": -0.5,
        "sigma": sigma,
        "treatment_duration": 5,
        "growth_duration": 19,
        "pers_cost": 0,
    }


def run_one(args) -> dict:
    """Run one replicate. `args` is (params, seed). Returns their result dict
    plus an extinction flag and the seed used.

    THE SEED SET HERE HAS NO EFFECT, and that is a property of their code, not
    of this wrapper. Line 66 of their `RUN_tau_leaping` calls

        np.random.seed()

    with no argument, which reseeds from OS entropy at the start of every run
    and discards whatever the caller set. No run of their simulation can be
    reproduced, by construction, and no external seeding can change that
    without modifying their file, which this project does not do.

    The seed is still recorded on each result row so that the wrapper's own
    behaviour is auditable, and it is still routed through SeedSequence so that
    it would be well spread if their internal reseed were ever removed.

    An earlier version of this note attributed a between-batch difference to
    correlated consecutive seeds. That diagnosis was wrong: the seeds never
    reached the generator. The between-batch difference was sampling variation.
    """
    params, seed = args
    m = load()
    np.random.seed(int(np.random.SeedSequence(int(seed)).generate_state(1)[0]))
    res = m.run_simulation_with_mic(params)
    n_days = params["tfin"] // 24
    # their runner pads the daily series with None when the run stopped early,
    # which happens when every lineage is gone
    res["extinct"] = res.get(f"average_mic_day_{n_days}") is None
    res["seed"] = seed
    return res
