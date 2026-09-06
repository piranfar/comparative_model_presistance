"""
Floor inference with uncertainty, and a refusal rule.

Run:  python -m src.floor_posterior

WHY THIS EXISTS. docs/22 showed that unconstrained networks learn the training
box of a closed-form boundary and fail outside it silently. The division of
labour that follows is: learn L under uncertainty; derive everything downstream.
src/infer_floor.py returns a point verdict. This module adds an interval and a
refusal: when the interval on L spans more than one log10, or the verdict is
WEAK or NONE, callers must not emit forced/undecidable observability labels.

METHOD. DERIVED floors (plated volume recorded, minimum equals 1000/V) are a
point mass. INFERRED floors over an MPN ladder place a discrete posterior on
every table rung at or below the observed minimum that is consistent with zero
readings below it, weighted by pile-up ties and by how many empty rungs sit
below the candidate. The 95% highest-posterior-density support is the interval.
WEAK and NONE refuse.

Writes nothing by itself; experiments and the CLI import floor_posterior().
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np

from .infer_floor import MPN_TABLE, infer, pile_up

# Refuse observability labels when the floor is this uncertain (log10 units).
MAX_LOG10_SPAN_FOR_LABELS = 1.0


@dataclass
class FloorPosterior:
    verdict: str
    candidate_floor: float | None
    ci_low: float | None
    ci_high: float | None
    log10_span: float | None
    refuse_labels: bool
    reason: str
    posterior: dict[str, float] | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def _hpd_support(support: np.ndarray, mass: np.ndarray, level: float = 0.95
                 ) -> tuple[float, float]:
    """Smallest contiguous support covering `level` of posterior mass."""
    order = np.argsort(support)
    s = support[order]
    m = mass[order]
    cum = np.cumsum(m)
    best = (s[0], s[-1])
    best_width = s[-1] / s[0] if s[0] > 0 else np.inf
    for i in range(len(s)):
        for j in range(i, len(s)):
            covered = cum[j] - (cum[i - 1] if i else 0.0)
            if covered + 1e-15 < level:
                continue
            width = s[j] / s[i] if s[i] > 0 else np.inf
            if width < best_width:
                best_width = width
                best = (float(s[i]), float(s[j]))
    return best


def _mpn_posterior(values: np.ndarray) -> tuple[dict[str, float], float, float, float]:
    """Discrete posterior over MPN table rungs at or below the observed minimum."""
    v = values[np.isfinite(values) & (values > 0)]
    lo = float(v.min())
    candidates = [float(x) for x in MPN_TABLE if x <= lo + 1e-9]
    if not candidates:
        candidates = [lo]
    weights = []
    for L in candidates:
        below = int((v < L - 1e-9).sum())
        if below:
            weights.append(0.0)
            continue
        ties = int(np.isclose(v, L).sum())
        empty_below = sum(1 for x in MPN_TABLE if x < L - 1e-9)
        # Prefer candidates with a pile-up and with unused lower rungs (ladder
        # signature). Soft weights, not a generative model of the full table.
        w = (1.0 + ties) * (1.0 + 0.25 * empty_below)
        weights.append(w)
    w = np.asarray(weights, dtype=float)
    if not w.sum():
        w = np.ones(len(candidates))
    mass = w / w.sum()
    post = {f"{c:g}": float(m) for c, m in zip(candidates, mass)}
    ci_lo, ci_hi = _hpd_support(np.asarray(candidates), mass)
    point = float(candidates[int(np.argmax(mass))])
    return post, point, ci_lo, ci_hi


def floor_posterior(values: np.ndarray, counts_per_ml: bool = True,
                    recorded_volume_ul: float | None = None,
                    below_limit_as_zero: bool = False) -> FloorPosterior:
    """Point verdict plus uncertainty; refuse labels when the floor is too soft.

    Set below_limit_as_zero when the deposit writes below-limit readings as exact
    zeros without naming L (Windels-style surviving fractions). Those zeros fix
    no absolute floor, so observability labels are refused.
    """
    if below_limit_as_zero:
        v = values[np.isfinite(values)]
        n_zero = int((v == 0).sum()) if len(v) else 0
        return FloorPosterior(
            verdict="NONE", candidate_floor=None,
            ci_low=None, ci_high=None, log10_span=None, refuse_labels=True,
            reason=(f"{n_zero} readings are exact zeros marking below-limit "
                    "without a named L; refuse observability labels"),
            posterior=None,
        )

    base = infer(values, counts_per_ml=counts_per_ml,
                 recorded_volume_ul=recorded_volume_ul)
    verdict = base["verdict"]
    cand = base.get("candidate_floor")

    if verdict == "DERIVED":
        L = float(cand)
        return FloorPosterior(
            verdict=verdict, candidate_floor=L, ci_low=L, ci_high=L,
            log10_span=0.0, refuse_labels=False,
            reason=base["reason"] + "; volume derivation is a point mass",
            posterior={f"{L:g}": 1.0},
        )

    if verdict in ("WEAK", "NONE") or cand is None:
        p = pile_up(values)
        lo = p.get("minimum")
        return FloorPosterior(
            verdict=verdict, candidate_floor=float(lo) if lo is not None else None,
            ci_low=None, ci_high=None, log10_span=None, refuse_labels=True,
            reason=base["reason"] + "; refuse observability labels",
            posterior=None,
        )

    # INFERRED: discrete MPN posterior (or bootstrap min if not on an MPN table).
    v = values[np.isfinite(values) & (values > 0)]
    on_table = any(abs(float(cand) - x) < 1e-6 for x in MPN_TABLE)
    if on_table:
        post, point, ci_lo, ci_hi = _mpn_posterior(v)
    else:
        # Bootstrap the observed minimum as a conformal-style interval.
        rng = np.random.default_rng(20260906)
        boots = [float(rng.choice(v, size=len(v), replace=True).min())
                 for _ in range(2000)]
        ci_lo, ci_hi = float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))
        point = float(cand)
        post = None

    span = float(np.log10(ci_hi) - np.log10(ci_lo)) if ci_lo > 0 else np.inf
    refuse = span > MAX_LOG10_SPAN_FOR_LABELS
    reason = base["reason"]
    if refuse:
        reason += (f"; 95% support spans {span:.2f} log10 "
                   f"(>{MAX_LOG10_SPAN_FOR_LABELS:g}); refuse observability labels")
    else:
        reason += f"; 95% support [{ci_lo:g}, {ci_hi:g}] (span {span:.3g} log10)"

    return FloorPosterior(
        verdict=verdict, candidate_floor=point, ci_low=ci_lo, ci_high=ci_hi,
        log10_span=span, refuse_labels=refuse, reason=reason, posterior=post,
    )
