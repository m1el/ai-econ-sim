# /// script
# dependencies = ["numpy", "matplotlib"]
# ///
"""
AI-economy transition simulator, v2 — calibrated to the DEBIASED survey
=======================================================================

Same structural engine as simulate.py (task-based automation, CES labor
share, Baumol-bounded growth, political-leverage feedback, resource
competition, parallel-economy floor). What changed:

1. PRIORS are re-derived from survey2 (neutral instrument, 11 panelists:
   GPT-5.5, Opus 4.8, Gemini 3.1 Pro, Grok 4.3, DeepSeek v4, Qwen 3.7 Max,
   Kimi k2.6, GLM 5.1, MiniMax M3, Mistral Large, fresh Fable 5). Each prior
   cites its source numbers from survey2/responses/.
2. NAMED scenarios are the archetypes the panel generated on its own,
   not my survey-1 buckets.
3. CALIBRATION CHECK: each Monte Carlo run is scored against analogues of
   the ten survey-2 calibrated statements (a)-(j); the simulated
   probabilities are printed next to the panel means. Where the simulation
   can't express a statement (h: robot prices), it says so.

Panel-mean targets (probability each statement is true in 2046):
  a) median real disposable income higher than 2026 ............ 65%
  b) median income >20% lower ................................... 15%
  c) labor share of national income < 40% ....................... 47%
  d) >25% prime-age involuntary joblessness ..................... 23%
  e) citizens' policy influence substantially weaker ............ 62%
  f) top-1% income/wealth share up >= 10 points ................. 51%
  g) housing+energy+food a larger share of median budget ........ 53%
  h) capable household robot < 6 months income .................. 46%  (not modeled)
  i) transfers the largest income source for median household ... 32%
  j) AI/operators allocate with little effective oversight ...... 38%

Calibration result (8000 runs, seed 0): statements a-g and j match the panel
within +/-9 points. Statement (i) "transfers largest income source" stays ~18
points BELOW the panel's 32% and resists tuning. That residual is a finding,
not a bug: in this engine, large transfers require political leverage L to
survive (the cap tau_cap*L binds), but the worlds where wages fall enough for
transfers to dominate are exactly the worlds where L has eroded. The panel's
i=32% is structurally hard to reconcile with its own e=62% (weakened citizen
influence) unless dividends get LOCKED IN while leverage is still high - which
is precisely the "window" argument from the survey-1 synthesis. The model
enforces a consistency constraint the panelists' independent estimates don't.

Usage:
  uv run model/simulate_v2.py             # named archetypes + MC + calibration table
  uv run model/simulate_v2.py --runs 20000
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
    auto_speed: float = 0.15       # logistic rate of task automation per year
    A0: float = 0.12               # fraction of tasks automated in 2026
    A_max: float = 0.85            # ceiling: fraction of tasks EVER automatable
    sigma: float = 1.3             # task elasticity: >1 AI substitutes, <1 bottleneck
    cost_decline: float = 0.30     # yearly decline of AI cost per task
    c_floor: float = 0.10          # floor on AI cost per task (energy/hardware bound)
    g_cap: float = 0.045           # max real per-capita growth (Baumol bound)
    phi: float = 0.35              # automation -> growth passthrough
    # --- distribution & politics ---
    chi: float = 0.55              # share of capital income to top 1%
    median_capital: float = 0.15   # median person's capital income vs per-capita mean
    tau0: float = 0.12             # initial effective transfer rate on capital income
    tau_response: float = 0.06     # democracy's tau increase per unit shortfall/yr
    tau_cap: float = 0.55          # max politically achievable transfer rate
    ubi_drift: float = 0.008       # proactive dividend adoption per year per unit A
    leverage_erosion: float = 0.45 # falling labor share -> eroding political leverage
    wage_skew: float = 0.35        # median wage falls below mean wage as A rises
                                   #   (gains concentrate in AI-complementary top)
    # --- resources & AI self-sustainment ---
    s_ai: float = 0.30             # AI-sector income reinvested into AI itself
    rho: float = 0.08              # resource-price pressure per unit AI economy growth
    res_share_col: float = 0.35    # resource weight in median cost of living
    # --- floors & frictions ---
    parallel_floor: float = 0.80   # parallel human economy productivity vs 2025
    friction: float = 2.5          # joblessness per unit of yearly task displacement
                                   #   (retraining/reabsorption lag; MiniMax, Qwen d~35%)


def simulate(p: Params) -> dict:
    A = p.A_max / (1 + ((p.A_max - p.A0) / p.A0) * np.exp(-p.auto_speed * np.arange(T)))
    c_ai = np.maximum((1 - p.cost_decline) ** np.arange(T), p.c_floor)

    g = np.minimum(0.015 + p.phi * A * p.cost_decline, p.g_cap)
    gdp = np.concatenate([[1.0], np.cumprod(1 + g[:-1])])

    with np.errstate(over="ignore"):
        adv = A * c_ai ** (1 - p.sigma)
    labor_share = np.clip((1 - A) / (adv + (1 - A)), 1e-4, 1.0)

    squeeze = np.clip((A - 0.80) / 0.2, 0, 1)
    dA = np.concatenate([[0.0], np.diff(A)])
    churn = np.clip(p.friction * dA, 0, 0.6)     # displaced faster than reabsorbed
    employment = np.clip(1 - 0.7 * squeeze - churn, 0.2, 1.0)

    real_wage = labor_share * gdp / np.maximum(employment, 0.05)
    real_wage = real_wage / real_wage[0]
    med_wage = real_wage * (1 - p.wage_skew * A)        # median's slice of wage pie
    capital_income = (1 - labor_share) * gdp

    ai_demand = capital_income * (1 + p.s_ai)
    res_price = 1 + p.rho * np.maximum(ai_demand - ai_demand[0], 0)
    col = res_price ** p.res_share_col

    L = np.empty(T); tau = np.empty(T)
    L[0], tau[0] = 1.0, p.tau0
    median_market = np.empty(T)
    for t in range(T):
        median_market[t] = (med_wage[t] * employment[t]
                            + p.median_capital * capital_income[t])
        if t + 1 < T:
            ls_decline = (labor_share[0] - labor_share[t]) / labor_share[0]
            erosion = p.leverage_erosion * max(ls_decline, 0.85 * A[t])
            L[t + 1] = np.clip(1 - erosion, 0.02, 1.0)
            shortfall = max(0.0, 1.0 - median_market[t] / col[t])
            tau[t + 1] = np.clip(tau[t] + p.tau_response * L[t] * shortfall
                                 + p.ubi_drift * A[t] * L[t]
                                 - 0.005 * (1 - L[t]),
                                 0.0, p.tau_cap * L[t] + 0.05)

    transfers = tau * capital_income * (1 - 0.5 * p.chi * (1 - L))
    median_income = median_market + transfers
    welfare = median_income / col
    floor = p.parallel_floor / res_price ** p.res_share_col
    welfare = np.maximum(welfare, floor)

    human_share = np.clip((median_income + p.chi * capital_income * 0.3)
                          / np.maximum(gdp * (1 + p.s_ai * (1 - labor_share)), 1e-9), 0, 1)
    D = ((1 - labor_share) + (1 - human_share) + (1 - L)) / 3

    wage_income = med_wage * employment
    return dict(years=YEARS, A=A, real_wage=real_wage, labor_share=labor_share,
                gdp=gdp, welfare=welfare, D=D, L=L, tau=tau, res_price=res_price,
                employment=employment, floor=floor, transfers=transfers,
                wage_income=wage_income, median_income=median_income,
                capital_income=capital_income, col=col, chi=p.chi,
                res_share_col=p.res_share_col)


# ------------------------------------------------- survey-2 statement analogues
def statements(r: dict) -> dict:
    """Evaluate analogues of the survey-2 calibrated statements (a)-(j) at 2046.

    Mappings are approximations; (h) has no model analogue and is omitted.
    (f) uses top-1% *income* share (chi x capital share) as a proxy for the
    wealth-share statement. (g) compares essentials spending share of median
    income vs 2026. (j) proxies "little effective oversight" with deep automation plus
    weak civic leverage; the loosest mapping here.
    """
    i = IDX_2046
    top1 = r["chi"] * (1 - r["labor_share"])
    ess_share = np.clip(r["res_share_col"] * r["res_price"] / np.maximum(r["median_income"], 1e-9), 0, 1)
    return {
        "a": r["welfare"][i] > 1.0,
        "b": r["welfare"][i] < 0.8,
        "c": r["labor_share"][i] < 0.40,
        "d": r["employment"][i] < 0.75,
        "e": r["L"][i] < 0.65,
        # wealth stocks lag income flows; ~half pass-through over 20 yrs,
        # so a 10pp WEALTH-share rise needs ~20pp income-share rise
        "f": (top1[i] - top1[0]) >= 0.20,
        "g": ess_share[i] > ess_share[0],
        "i": r["transfers"][i] > max(r["wage_income"][i],
                                     r["median_income"][i] - r["transfers"][i] - r["wage_income"][i]),
        # "AI/operators allocate with little oversight": deep automation plus
        # weakened civic leverage (ceremonial sign-off)
        "j": (r["A"][i] > 0.60) and (r["L"][i] < 0.60),
    }


PANEL_TARGETS = {"a": 65, "b": 15, "c": 47, "d": 23, "e": 62, "f": 51,
                 "g": 53, "h": 46, "i": 32, "j": 38}
STATEMENT_TEXT = {
    "a": "median income higher than 2026",
    "b": "median income >20% lower",
    "c": "labor share < 40%",
    "d": ">25% involuntary joblessness",
    "e": "citizen influence substantially weaker",
    "f": "top-1% share up >= 10 points",
    "g": "essentials a larger budget share",
    "h": "cheap capable household robot",
    "i": "transfers largest income source",
    "j": "AI allocates, little oversight",
}


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
# Priors derived from survey-2 driver sections. Citations name the panelist
# whose estimate anchors each choice; ranges widen to cover panel spread.
def sample_params(rng) -> dict:
    kw = {}
    # Plateau mixture: panel put 10-25% on "AI fizzles / long plateau"
    # (Kimi 15%, Mistral 15%, Qwen 20%, Fable 12%, DeepSeek 5%).
    plateau = rng.random() < 0.13
    # auto_speed: deployment lag 5-15 yrs (Fable, Opus, Kimi, MiniMax) means
    # slower task-frontier growth than survey-1 priors assumed.
    kw["auto_speed"] = rng.lognormal(np.log(0.13), 0.40) * (0.35 if plateau else 1.0)
    # A_max: Gemini "85% cognitive by 2035, 60% physical by 2042"; Fable
    # "robotics lags 5-10 yrs"; plateau worlds cap far lower.
    kw["A_max"] = (rng.beta(4, 2) * 0.5 + 0.5) if not plateau else rng.uniform(0.30, 0.55)
    # sigma: Kimi "1.2-1.5 tradable, 0.6-0.8 non-tradable" -> blended ~1.0-1.5;
    # DeepSeek/GLM see stronger substitution. Lognormal mostly 0.9-1.8.
    kw["sigma"] = rng.lognormal(np.log(1.05), 0.22)
    # cost_decline: DeepSeek "1000x/decade then slowing" is tokens, not task
    # delivery; panel's economy-level guesses are tamer.
    kw["cost_decline"] = rng.uniform(0.10, 0.45)
    kw["c_floor"] = rng.uniform(0.03, 0.25)
    # g_cap: panel TFP boost ~0.5-2pp/yr (Fable ~1pp avg, MiniMax 2.5-3.5%
    # total growth, Kimi 40-60% over 20 yrs). Baseline 1.5% + boost.
    kw["g_cap"] = 0.02 + rng.lognormal(np.log(0.022), 0.55)
    kw["g_cap"] = min(kw["g_cap"], 0.10)
    # chi: top-1% capture of capital income; panel f-spread 15-85% implies
    # wide disagreement -> keep wide.
    kw["chi"] = rng.beta(4, 3)
    # median_capital: bottom-50% hold ~1-2% of equity, median household has
    # housing + pension claims; panel B/C trajectories assume thin median claims.
    kw["median_capital"] = rng.uniform(0.04, 0.35)
    # tau_response / tau_cap: GPT-5.5 "redistribution expands unevenly",
    # MiniMax "5-10 yr fiscal lag", Mistral "70% chance states lack tools".
    kw["tau_response"] = rng.uniform(0.02, 0.20)
    kw["tau0"] = rng.uniform(0.08, 0.22)
    kw["tau_cap"] = rng.uniform(0.35, 0.85)
    # leverage_erosion: panel e-target 62%; Fable's 35% vs Gemini/DeepSeek 70-80%
    # -> centered slightly above 0.5 with full spread.
    kw["leverage_erosion"] = rng.beta(3.8, 1.1)
    # s_ai: AI build-out reinvestment ("energy-gated before labor-gated",
    # MiniMax; 100GW+ clusters, DeepSeek).
    kw["s_ai"] = rng.uniform(0.10, 0.60)
    # rho: housing/energy absorption of the AI dividend is THE spoiler for
    # 8/11 panelists, but several see energy cheapening post-2035.
    kw["rho"] = min(rng.lognormal(np.log(0.22), 0.7), 1.0)
    # res_share_col: essentials weight in median budget, ~35-50% today across
    # developed economies (Kimi: housing+health already 45-55%).
    kw["res_share_col"] = rng.uniform(0.28, 0.50)
    # parallel_floor: GLM h=75% cheap robots vs Kimi 22% -> wide; cheap robots
    # raise the autarky floor.
    kw["parallel_floor"] = rng.uniform(0.45, 1.0)
    # friction: years-equivalent of displacement outpacing reabsorption;
    # wide because panel d ranges 6% (Fable) to 35% (Gemini, Qwen)
    kw["wage_skew"] = rng.uniform(0.15, 0.70)
    kw["ubi_drift"] = rng.uniform(0.0, 0.045)
    kw["friction"] = rng.lognormal(np.log(6.5), 0.9)
    return kw


def monte_carlo(n: int, seed: int = 0):
    rng = np.random.default_rng(seed)
    rows, outcomes, samples, stmts = [], [], [], []
    for _ in range(n):
        kw = sample_params(rng)
        r = simulate(Params(**kw))
        rows.append(r); outcomes.append(classify(r)); samples.append(kw)
        stmts.append(statements(r))
    return rows, outcomes, samples, stmts


# Named scenarios = archetypes the panel generated unprompted in survey 2.
NAMED = {
    # GPT-5.5 "managed abundance" / Opus "managed redistribution" / MiniMax "broad dividend"
    "Managed abundance (panel ~25%)": Params(
        sigma=1.15, A_max=0.85, auto_speed=0.15, g_cap=0.07, cost_decline=0.35,
        leverage_erosion=0.15, tau_response=0.12, tau_cap=0.75, chi=0.45,
        median_capital=0.28, rho=0.04, s_ai=0.25),
    # Kimi "institutional lag" / GLM "asymmetric automation" / MiniMax "capital concentrates" — the modal world
    "Institutional lag (panel ~35%)": Params(
        sigma=1.35, A_max=0.88, auto_speed=0.14, g_cap=0.045, cost_decline=0.30,
        leverage_erosion=0.55, tau_response=0.05, tau_cap=0.50, chi=0.60,
        median_capital=0.12, rho=0.12, res_share_col=0.45, s_ai=0.35),
    # Gemini "neofeudal" / Qwen "neo-feudal technocracy" / Kimi "rentier dystopia"
    "Neo-feudal rentier (panel ~25%)": Params(
        sigma=1.8, A_max=0.95, auto_speed=0.20, g_cap=0.055, cost_decline=0.40,
        leverage_erosion=0.90, tau_response=0.03, tau_cap=0.30, chi=0.75,
        median_capital=0.05, rho=0.20, res_share_col=0.45, s_ai=0.55),
    # Kimi "long plateau" / Fable "plateau & demographic drag" / Mistral "AI winter"
    "Plateau & demographic drag (panel ~15%)": Params(
        sigma=1.1, A_max=0.40, auto_speed=0.05, g_cap=0.025, cost_decline=0.15,
        leverage_erosion=0.25, tau_response=0.06, tau_cap=0.55, chi=0.50,
        median_capital=0.15, rho=0.03, s_ai=0.15),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=8000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    # ---- named archetypes figure
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    panels = [("welfare", "Median welfare (2026 = 1)"), ("real_wage", "Real wage index"),
              ("labor_share", "Labor share of GDP"), ("D", "Disempowerment index")]
    colors = dict(zip(NAMED, ["tab:green", "tab:orange", "tab:red", "tab:gray"]))
    for ax, (key, title) in zip(axes.flat, panels):
        for name, p in NAMED.items():
            r = simulate(p)
            ax.plot(r["years"], r[key], label=name, color=colors[name], lw=2)
        ax.set_title(title); ax.grid(alpha=0.3)
        if key == "welfare":
            ax.axhline(1.0, color="k", ls=":", lw=1)
    axes.flat[0].legend(fontsize=7)
    fig.suptitle("Survey-2 archetype scenarios, 2026-2056 (v2 calibration)")
    fig.tight_layout()
    fig.savefig("model/v2_named_scenarios.png", dpi=130)

    # ---- Monte Carlo
    rows, outcomes, samples, stmts = monte_carlo(args.runs, args.seed)
    welfare = np.array([r["welfare"] for r in rows])

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 4.6))
    med = np.median(welfare, axis=0)
    for q, a in [(80, 0.15), (50, 0.25), (20, 0.40)]:
        lo, hi = np.percentile(welfare, [(100 - q) / 2, 100 - (100 - q) / 2], axis=0)
        ax1.fill_between(YEARS, lo, hi, color="tab:blue", alpha=a, label=f"{q}% interval")
    ax1.plot(YEARS, med, color="tab:blue", lw=2, label="median run")
    ax1.axhline(1, color="k", ls=":"); ax1.set_yscale("log")
    ax1.set_title("Median-person welfare, fan chart (log), v2 priors")
    ax1.legend(fontsize=8); ax1.grid(alpha=0.3)

    labels, counts = np.unique(outcomes, return_counts=True)
    order = np.argsort(labels)
    ax2.barh(np.array(labels)[order], counts[order] / len(outcomes) * 100, color="tab:purple")
    ax2.set_title(f"Outcome shares in 2046 (n={len(outcomes)})"); ax2.set_xlabel("%")
    ax2.grid(alpha=0.3, axis="x")

    # calibration: simulated statement probabilities vs panel targets
    keys = [k for k in PANEL_TARGETS if k != "h"]
    sim_p = {k: 100 * np.mean([s[k] for s in stmts]) for k in keys}
    x = np.arange(len(keys)); w = 0.38
    ax3.bar(x - w / 2, [sim_p[k] for k in keys], w, label="simulation", color="tab:blue")
    ax3.bar(x + w / 2, [PANEL_TARGETS[k] for k in keys], w, label="panel mean", color="tab:orange")
    ax3.set_xticks(x); ax3.set_xticklabels(keys)
    ax3.set_title("Calibration: statements (a)-(j) vs 11-model panel")
    ax3.legend(fontsize=8); ax3.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig("model/v2_monte_carlo.png", dpi=130)

    print(f"\n=== v2 outcome distribution in 2046 over {len(outcomes)} sampled worlds ===")
    for lab, c in sorted(zip(labels, counts), key=lambda z: -z[1]):
        print(f"  {lab:22s} {c/len(outcomes)*100:5.1f}%")

    print("\n=== Calibration vs survey-2 panel means ===")
    print(f"  {'':2s} {'statement':40s} {'sim':>6s} {'panel':>6s} {'diff':>6s}")
    for k in PANEL_TARGETS:
        if k == "h":
            print(f"  {k:2s} {STATEMENT_TEXT[k]:40s} {'n/a':>6s} {PANEL_TARGETS[k]:>5d}%   (robot prices not modeled)")
            continue
        d = sim_p[k] - PANEL_TARGETS[k]
        print(f"  {k:2s} {STATEMENT_TEXT[k]:40s} {sim_p[k]:5.1f}% {PANEL_TARGETS[k]:>5d}% {d:+6.1f}")

    w46 = welfare[:, IDX_2046]
    sens = {}
    for k in samples[0]:
        xv = np.array([s[k] for s in samples])
        sens[k] = np.corrcoef(np.argsort(np.argsort(xv)), np.argsort(np.argsort(w46)))[0, 1]
    print("\n=== Sensitivity (rank correlation with 2046 median welfare) ===")
    for k in sorted(sens, key=lambda k: -abs(sens[k])):
        print(f"  {k:18s} {sens[k]:+.2f}")

    print("\n=== Survey-2 archetypes, 2046 snapshot ===")
    for name, p in NAMED.items():
        r = simulate(p)
        print(f"  {name:38s} welfare={r['welfare'][IDX_2046]:5.2f}  "
              f"laborShare={r['labor_share'][IDX_2046]:.2f}  D={r['D'][IDX_2046]:.2f}  "
              f"-> {classify(r)}")


if __name__ == "__main__":
    main()
