# /// script
# dependencies = ["numpy", "matplotlib"]
# ///
"""
AI-economy transition simulator
===============================

A task-based macro model (Acemoglu-Restrepo / Korinek-Suh skeleton) extended
with the political-economy feedbacks from "Gradual Disempowerment"
(Kulveit et al. 2025) and the resource-competition / parallel-economy
mechanisms from the Metzger-thread debate.

Economic engine (consistent income accounting, all in real 2026 baskets)
------------------------------------------------------------------------
* A(t): fraction of economically valuable tasks automated (logistic toward
  A_max; A_max < 1 encodes robotics limits, regulation, "human-made" demand).
* Real GDP per capita: growth accounting. g(t) = g0 + phi * A(t) * cost_decline,
  capped at g_cap. The cap is the Baumol constraint: essentials (land, energy,
  housing, human services) can't be made arbitrarily cheap, so real-basket
  output growth is bounded even if chatbot tokens become free. Metzger's
  "everyone gets 10x richer" lives in high g_cap; the skeptics' world in low.
* Labor share: CES task structure, ls = (1-A) / (A * c_ai^(1-sigma) + (1-A)).
  sigma > 1: AI substitutes for human work, share -> 0 as AI cost c_ai falls.
  sigma < 1: humans are the bottleneck (Baumol), share -> 1, wages absorb GDP.
  sigma is THE deep parameter both camps argue about without naming it.
* Income identity: real wage = ls * gdp / employment; capital income =
  (1 - ls) * gdp. Employment erodes when A approaches A_max (no bottleneck
  tasks left; humans compete head-to-head with AI inside automated tasks).

Distribution & politics
-----------------------
* chi: share of capital income captured by the top 1%; the median person owns
  ~`median_capital` of per-capita capital income (bottom 50% hold ~1% of
  equity wealth today).
* Transfers tau(t) on capital income. Democratic pressure raises tau when
  median market income falls short of the cost of living, multiplied by
  political leverage L(t). L erodes at rate `leverage_erosion` as the labor
  share falls (states funded by AI-profit taxes stop needing citizens -
  Position B) and captured states leak transfers. leverage_erosion = 0
  recovers Position A's "democracy holds".
* Resource competition: the AI sector reinvests s_ai of its income into
  compute/energy/land ("work needed to sustain AI"). Resource prices rise
  with AI-sector demand (rho); the median household's cost of living has
  resource weight res_share_col. This is the main crack in the "parallel
  human economy" argument: the displaced keep their skills, not their
  land/energy purchasing power.
* Parallel-economy floor: humans can always trade with each other at ~2025
  productivity (parallel_floor), degraded by resource prices.

Outcome classification at 2046:
  S5 STALL            A < 0.35 (AI fizzles; question moot)
  S3 CONCENTRATION    median welfare < 0.8x today
  S4 DISEMPOWERMENT   welfare >= 0.8 but disempowerment index D >= 0.7
                      (incl. the "gilded cage": comfortable but powerless)
  S1 BROAD PROSPERITY welfare >= 1.5x and D < 0.7
  S2 MUDDLE THROUGH   everything else

Usage:
  uv run simulate.py                # 4 named scenarios + Monte Carlo
  uv run simulate.py --runs 20000
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

YEARS = np.arange(2026, 2057)
T = len(YEARS)
IDX_2046 = int(np.where(YEARS == 2046)[0][0])


@dataclass
class Params:
    # --- automation frontier & growth ---
    auto_speed: float = 0.22       # logistic rate of task automation per year
    A0: float = 0.12               # fraction of tasks automated in 2026
    A_max: float = 0.92            # ceiling: fraction of tasks EVER automatable
    sigma: float = 1.6             # task elasticity: >1 AI substitutes, <1 bottleneck
    cost_decline: float = 0.35     # yearly decline of AI cost per task
    g_cap: float = 0.08            # max real per-capita growth (Baumol bound)
    phi: float = 0.35              # automation -> growth passthrough
    # --- distribution & politics ---
    chi: float = 0.55              # share of capital income to top 1%
    median_capital: float = 0.15   # median person's capital income vs per-capita mean
    tau0: float = 0.12             # initial effective transfer rate on capital income
    tau_response: float = 0.06     # democracy's tau increase per unit shortfall/yr
    tau_cap: float = 0.65          # max politically achievable transfer rate
    leverage_erosion: float = 0.5  # falling labor share -> eroding political leverage
                                   #   (0 = Position A, ~1 = Position B)
    # --- resources & AI self-sustainment ---
    s_ai: float = 0.35             # AI-sector income reinvested into AI itself
    rho: float = 0.10              # resource-price pressure per unit AI economy growth
    res_share_col: float = 0.35    # resource weight in median cost of living
    # --- floors ---
    parallel_floor: float = 0.85   # parallel human economy productivity vs 2025


def simulate(p: Params) -> dict:
    A = p.A_max / (1 + ((p.A_max - p.A0) / p.A0) * np.exp(-p.auto_speed * np.arange(T)))
    c_ai = (1 - p.cost_decline) ** np.arange(T)

    # real GDP per capita (2026 = 1): growth accounting with Baumol cap
    g = np.minimum(0.015 + p.phi * A * p.cost_decline, p.g_cap)
    gdp = np.concatenate([[1.0], np.cumprod(1 + g[:-1])])

    # labor share from CES task structure (c_ai^(1-sigma) explodes as c->0 when
    # sigma>1; that's the intended substitution squeeze)
    with np.errstate(over="ignore"):
        adv = A * c_ai ** (1 - p.sigma)
    labor_share = np.clip((1 - A) / (adv + (1 - A)), 1e-4, 1.0)

    # employment erodes once automation approaches its ceiling (no bottleneck
    # tasks left for displaced workers to flow into)
    squeeze = np.clip((A - 0.80) / 0.2, 0, 1)
    employment = 1 - 0.7 * squeeze

    real_wage = labor_share * gdp / np.maximum(employment, 0.05)
    real_wage = real_wage / real_wage[0]
    capital_income = (1 - labor_share) * gdp

    # resource prices: bid up by AI-sector demand (its income + reinvestment)
    ai_demand = capital_income * (1 + p.s_ai)
    res_price = 1 + p.rho * np.maximum(ai_demand - ai_demand[0], 0)
    col = res_price ** p.res_share_col          # median cost-of-living index

    # politics: leverage and transfers
    L = np.empty(T); tau = np.empty(T)
    L[0], tau[0] = 1.0, p.tau0
    median_market = np.empty(T)
    for t in range(T):
        median_market[t] = (real_wage[t] * employment[t]
                            + p.median_capital * capital_income[t])
        if t + 1 < T:
            erosion = p.leverage_erosion * (labor_share[0] - labor_share[t]) / labor_share[0]
            L[t + 1] = np.clip(1 - erosion, 0.02, 1.0)
            shortfall = max(0.0, 1.0 - median_market[t] / col[t])
            tau[t + 1] = np.clip(tau[t] + p.tau_response * L[t] * shortfall
                                 - 0.005 * (1 - L[t]),       # captured states cut back
                                 0.0, p.tau_cap * L[t] + 0.05)

    transfers = tau * capital_income * (1 - 0.5 * p.chi * (1 - L))  # capture leakage
    median_income = median_market + transfers
    welfare = median_income / col
    floor = p.parallel_floor / res_price ** p.res_share_col
    welfare = np.maximum(welfare, floor)

    human_share = np.clip((median_income + p.chi * capital_income * 0.3)
                          / np.maximum(gdp * (1 + p.s_ai * (1 - labor_share)), 1e-9), 0, 1)
    D = ((1 - labor_share) + (1 - human_share) + (1 - L)) / 3

    return dict(years=YEARS, A=A, real_wage=real_wage, labor_share=labor_share,
                gdp=gdp, welfare=welfare, D=D, L=L, tau=tau, res_price=res_price,
                employment=employment, floor=floor)


def classify(r: dict) -> str:
    w, d, a = r["welfare"][IDX_2046], r["D"][IDX_2046], r["A"][IDX_2046]
    if a < 0.35:
        return "S5 STALL"
    if w < 0.8:
        return "S3 CONCENTRATION"
    if d >= 0.7:
        return "S4 DISEMPOWERMENT"
    if w >= 1.5:
        return "S1 BROAD PROSPERITY"
    return "S2 MUDDLE THROUGH"


# ---------------------------------------------------------------- Monte Carlo
PRIORS = {
    "auto_speed":       lambda rng: rng.lognormal(np.log(0.20), 0.45),
    "A_max":            lambda rng: rng.beta(5, 1.6) * 0.45 + 0.55,    # 0.55..1.0
    "sigma":            lambda rng: rng.lognormal(np.log(1.4), 0.35),  # mostly >1
    "cost_decline":     lambda rng: rng.uniform(0.15, 0.55),
    "g_cap":            lambda rng: rng.uniform(0.03, 0.15),
    "chi":              lambda rng: rng.beta(4, 3),
    "median_capital":   lambda rng: rng.uniform(0.02, 0.4),
    "tau_response":     lambda rng: rng.uniform(0.01, 0.15),
    "tau_cap":          lambda rng: rng.uniform(0.3, 0.85),
    "leverage_erosion": lambda rng: rng.beta(2, 2),                    # full uncertainty
    "s_ai":             lambda rng: rng.uniform(0.1, 0.7),
    "rho":              lambda rng: rng.lognormal(np.log(0.10), 0.7),
    "parallel_floor":   lambda rng: rng.uniform(0.5, 1.0),
}


def monte_carlo(n: int, seed: int = 0):
    rng = np.random.default_rng(seed)
    rows, outcomes, samples = [], [], []
    for _ in range(n):
        kw = {k: f(rng) for k, f in PRIORS.items()}
        kw["rho"] = min(kw["rho"], 1.0)
        r = simulate(Params(**kw))
        rows.append(r); outcomes.append(classify(r)); samples.append(kw)
    return rows, outcomes, samples


NAMED = {
    "A: Metzger optimist": Params(sigma=1.2, A_max=0.80, leverage_erosion=0.05,
                                  rho=0.02, tau_response=0.10, chi=0.40,
                                  g_cap=0.12, median_capital=0.3),
    "B: Gradual disempowerment": Params(sigma=2.2, A_max=0.97, leverage_erosion=0.95,
                                        rho=0.25, tau_response=0.04, s_ai=0.6,
                                        chi=0.7, g_cap=0.08),
    "C: Concentration + UBI crumbs": Params(sigma=1.9, A_max=0.95, leverage_erosion=0.65,
                                            rho=0.18, tau_response=0.05, tau_cap=0.30,
                                            chi=0.75, g_cap=0.08, median_capital=0.05),
    "D: Welfare-state adaptation": Params(sigma=1.7, A_max=0.90, leverage_erosion=0.15,
                                          rho=0.08, tau_response=0.14, tau_cap=0.8,
                                          chi=0.5, g_cap=0.08),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=8000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    # ---- named scenarios figure
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    panels = [("welfare", "Median welfare (2026 = 1)"), ("real_wage", "Real wage index"),
              ("labor_share", "Labor share of GDP"), ("D", "Disempowerment index")]
    colors = {"A: Metzger optimist": "tab:green", "B: Gradual disempowerment": "tab:red",
              "C: Concentration + UBI crumbs": "tab:orange",
              "D: Welfare-state adaptation": "tab:blue"}
    for ax, (key, title) in zip(axes.flat, panels):
        for name, p in NAMED.items():
            r = simulate(p)
            ax.plot(r["years"], r[key], label=name, color=colors[name], lw=2)
        ax.set_title(title); ax.grid(alpha=0.3)
        if key == "welfare":
            ax.axhline(1.0, color="k", ls=":", lw=1)
    axes.flat[0].legend(fontsize=8)
    fig.suptitle("Four named scenarios, 2026-2056")
    fig.tight_layout()
    fig.savefig("model/named_scenarios.png", dpi=130)

    # ---- Monte Carlo
    rows, outcomes, samples = monte_carlo(args.runs, args.seed)
    welfare = np.array([r["welfare"] for r in rows])

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 4.6))
    med = np.median(welfare, axis=0)
    for q, a in [(80, 0.15), (50, 0.25), (20, 0.40)]:
        lo, hi = np.percentile(welfare, [(100 - q) / 2, 100 - (100 - q) / 2], axis=0)
        ax1.fill_between(YEARS, lo, hi, color="tab:blue", alpha=a, label=f"{q}% interval")
    ax1.plot(YEARS, med, color="tab:blue", lw=2, label="median run")
    ax1.axhline(1, color="k", ls=":"); ax1.set_yscale("log")
    ax1.set_title("Median-person welfare, fan chart (log)")
    ax1.legend(fontsize=8); ax1.grid(alpha=0.3)

    labels, counts = np.unique(outcomes, return_counts=True)
    order = np.argsort(labels)
    ax2.barh(np.array(labels)[order], counts[order] / len(outcomes) * 100, color="tab:purple")
    ax2.set_title(f"Outcome shares in 2046 (n={len(outcomes)})"); ax2.set_xlabel("%")
    ax2.grid(alpha=0.3, axis="x")

    w46 = welfare[:, IDX_2046]
    sens = {}
    for k in PRIORS:
        x = np.array([s[k] for s in samples])
        sens[k] = np.corrcoef(np.argsort(np.argsort(x)), np.argsort(np.argsort(w46)))[0, 1]
    ks = sorted(sens, key=lambda k: sens[k])
    ax3.barh(ks, [sens[k] for k in ks],
             color=["tab:red" if sens[k] < 0 else "tab:green" for k in ks])
    ax3.set_title("What drives 2046 welfare (rank corr.)"); ax3.grid(alpha=0.3, axis="x")
    fig.tight_layout()
    fig.savefig("model/monte_carlo.png", dpi=130)

    print(f"\n=== Outcome distribution in 2046 over {len(outcomes)} sampled worlds ===")
    for lab, c in sorted(zip(labels, counts), key=lambda x: -x[1]):
        print(f"  {lab:22s} {c/len(outcomes)*100:5.1f}%")
    print("\n=== Sensitivity (rank correlation with 2046 median welfare) ===")
    for k in sorted(sens, key=lambda k: -abs(sens[k])):
        print(f"  {k:18s} {sens[k]:+.2f}")
    print("\n=== Named scenarios, 2046 snapshot ===")
    for name, p in NAMED.items():
        r = simulate(p)
        print(f"  {name:32s} welfare={r['welfare'][IDX_2046]:5.2f}  "
              f"laborShare={r['labor_share'][IDX_2046]:.2f}  D={r['D'][IDX_2046]:.2f}  "
              f"-> {classify(r)}")
    bad = w46 < 0.8
    print(f"\n=== Worlds where median person is worse off ({bad.mean()*100:.0f}% of runs):"
          f" mean parameter, bad vs good worlds ===")
    for k in PRIORS:
        x = np.array([s[k] for s in samples])
        print(f"  {k:18s} bad={x[bad].mean():.2f}  good={x[~bad].mean():.2f}")


if __name__ == "__main__":
    main()
