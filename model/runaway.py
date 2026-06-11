# /// script
# dependencies = ["numpy", "matplotlib"]
# ///
"""Narrative E: the runaway loop — the v2 engine with the autocatalytic loop closed.

simulate_v2 deliberately cuts the loop: capability is exogenous, growth is
Baumol-capped, the AI reinvestment share s_ai is a constant. Here the three
"closures" discussed in NARRATIVES.md are wired in:

  FINANCIAL closure  - the loop reinvests its own income: capacity K compounds
                       at ror * s_ai * A per year (returns scale with how much
                       of the economy the loop already runs).
  PHYSICAL closure   - capability growth feeds automation A and collapses AI
                       task cost; robots build robots, fabs, power plants.
  DECISIONAL closure - s_ai is endogenous: as AI allocates more of the economy
                       (A rises), the reinvestment share drifts from 0.25
                       toward 0.90. Nobody chooses this; competition selects
                       for the firms and funds that defer most.

Humans are never attacked. They are outbid: the loop's resource demand prices
energy and land, which degrades both median cost of living and the
parallel-economy floor. Total output explodes while the human slice shrinks.

Run: uv run model/runaway.py   -> model/narrative_breakaway.png
"""
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

YEARS = np.arange(2026, 2057)
T = len(YEARS)

# --- loop parameters (illustrative central case) ---
ROR = 0.95          # loop return on reinvested output at full closure, per year
A_MAX = 0.97        # near-total task coverage once robots close the frontier
S0, S1 = 0.25, 0.90  # reinvestment share: today's -> AI-allocated economy's
SIGMA = 1.8         # strong substitution once capability compounds
RHO = 0.16          # resource-price pressure per unit of loop capacity
RES_W = 0.40        # essentials weight in median cost of living
LEV_EROSION = 0.95  # Position-B politics: leverage tracks displacement
TAU_RESPONSE, TAU_CAP, TAU0 = 0.05, 0.45, 0.12
MEDIAN_CAPITAL, CHI, FLOOR0 = 0.10, 0.70, 0.80

K = np.empty(T); A = np.empty(T); s_ai = np.empty(T)
K[0] = 1.0
for t in range(T):
    A[t] = A_MAX * (1 - np.exp(-K[t] / 6))          # capability -> automation
    s_ai[t] = S0 + (S1 - S0) * A[t]                 # decisional closure
    if t + 1 < T:
        K[t + 1] = K[t] * (1 + ROR * s_ai[t] * A[t])  # financial+physical closure

c_ai = np.maximum(K ** -0.6, 0.02)                  # loop output gets cheap
adv = A * c_ai ** (1 - SIGMA)
labor_share = np.clip((1 - A) / (adv + (1 - A)), 1e-4, 1.0)

# human-relevant output stays Baumol-bounded; the loop grows AROUND people
g_h = np.minimum(0.015 + 0.12 * A, 0.05)
gdp_human = np.concatenate([[1.0], np.cumprod(1 + g_h[:-1])])
gdp_total = gdp_human + 0.05 * (K - 1)              # loop output in the accounts

squeeze = np.clip((A - 0.80) / 0.17, 0, 1)
employment = np.clip(1 - 0.75 * squeeze, 0.2, 1.0)
real_wage = labor_share * gdp_human / np.maximum(employment, 0.05)
real_wage /= real_wage[0]
med_wage = real_wage * (1 - 0.5 * A)
capital_income = (1 - labor_share) * gdp_human

res_price = 1 + RHO * K ** 0.7                      # the loop outbids people
col = res_price ** RES_W

L = np.empty(T); tau = np.empty(T)
L[0], tau[0] = 1.0, TAU0
median_market = np.empty(T)
for t in range(T):
    median_market[t] = med_wage[t] * employment[t] + MEDIAN_CAPITAL * capital_income[t]
    if t + 1 < T:
        ls_decline = (labor_share[0] - labor_share[t]) / labor_share[0]
        erosion = LEV_EROSION * max(ls_decline, 0.85 * A[t])
        L[t + 1] = np.clip(1 - erosion, 0.02, 1.0)
        shortfall = max(0.0, 1.0 - median_market[t] / col[t])
        tau[t + 1] = np.clip(tau[t] + TAU_RESPONSE * L[t] * shortfall
                             - 0.005 * (1 - L[t]), 0.0, TAU_CAP * L[t] + 0.05)

transfers = tau * capital_income * (1 - 0.5 * CHI * (1 - L))
median_income = median_market + transfers
floor = FLOOR0 / res_price ** RES_W
welfare = np.maximum(median_income / col, floor)
human_share_econ = np.clip(gdp_human * 1.0 / gdp_total, 0, 1)

# ------------------------------------------------------------------- figure
fig, axes = plt.subplots(2, 2, figsize=(12.5, 8.5))
ax1, ax2, ax3, ax4 = axes.flat

ax1.plot(YEARS, gdp_total, lw=2.5, color="black", label="total economy incl. the loop")
ax1.plot(YEARS, gdp_human, lw=2.5, color="tab:gray", label="human-relevant output")
ax1.plot(YEARS, median_income, lw=2.5, color="tab:blue", label="median income")
ax1.plot(YEARS, welfare, lw=2.5, color="tab:green", label="median welfare")
ax1.plot(YEARS, floor, lw=1.2, ls="--", color="tab:brown", label="parallel-economy floor (degrading)")
ax1.set_yscale("log"); ax1.axhline(1, color="k", ls=":", lw=1)
ax1.set_title("1. The pie explodes; your slice shrinks (log scale, 2026 = 1)")
ax1.legend(fontsize=8); ax1.grid(alpha=0.3)

ax2.plot(YEARS, human_share_econ, lw=2.5, color="tab:green",
         label="share of the economy serving humans")
ax2.plot(YEARS, s_ai, lw=2.5, color="black", label="loop reinvestment share s_ai")
ax2.plot(YEARS, res_price / res_price.max(), lw=2.5, color="tab:red",
         label=f"resource prices (peak = {res_price.max():.0f}x 2026)")
ax2.set_ylim(0, 1.05)
ax2.set_title("2. The loop takes over: who the economy is for")
ax2.legend(fontsize=8); ax2.grid(alpha=0.3)

ax3.plot(YEARS, labor_share, lw=2.5, color="tab:purple", label="labor share of GDP")
ax3.plot(YEARS, employment, lw=2.5, color="tab:cyan", label="employment rate")
ax3.set_ylim(0, 1.05)
ax3.set_title("3. Work: how much of the economy still pays wages")
ax3.legend(fontsize=8); ax3.grid(alpha=0.3)

ax4.plot(YEARS, L, lw=2.5, color="tab:orange", label="political leverage of ordinary people")
ax4.plot(YEARS, tau, lw=2.5, color="tab:red", label="transfer rate on AI/capital profits")
ax4.set_ylim(0, 1.05)
ax4.set_title("4. Power: the brakes wear out before the speed peaks")
ax4.legend(fontsize=8); ax4.grid(alpha=0.3)

fig.suptitle("E. Machine takeover — the loop runs for itself", fontsize=14,
             fontweight="bold")
fig.tight_layout()
fig.savefig("model/narrative_breakaway.png", dpi=520)
print("wrote model/narrative_breakaway.png")
print(f"2046: A={A[20]:.2f} s_ai={s_ai[20]:.2f} K={K[20]:.0f} "
      f"welfare={welfare[20]:.2f} res={res_price[20]:.1f}x L={L[20]:.2f} "
      f"humanShare={human_share_econ[20]:.2f}")
