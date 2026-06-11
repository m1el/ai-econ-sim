# /// script
# dependencies = ["numpy", "matplotlib"]
# ///
"""Generate one explanatory 4-panel figure per v2 archetype narrative.

Panels (same layout in every figure, so they can be compared side by side):
  1. The pie vs your slice   - real GDP per person vs median income vs welfare
  2. Where money comes from  - median income stacked: wages / capital / transfers
  3. Work                    - labor share of GDP and employment rate
  4. Power                   - political leverage L and the transfer rate tau

Run: uv run model/narratives.py
"""
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from simulate_v2 import NAMED, YEARS, simulate

FILES = {
    "Managed abundance (panel ~25%)": ("narrative_A_managed_abundance.png",
                                       "A. Managed abundance — growth gets shared"),
    "Institutional lag (panel ~35%)": ("narrative_B_institutional_lag.png",
                                       "B. Institutional lag — the squeeze (most likely)"),
    "Neo-feudal rentier (panel ~25%)": ("narrative_C_neofeudal.png",
                                        "C. Neo-feudal rentier — concentration wins"),
    "Plateau & demographic drag (panel ~15%)": ("narrative_D_plateau.png",
                                                "D. Plateau — the dog that didn't bark"),
}

for name, (fname, title) in FILES.items():
    r = simulate(NAMED[name])
    cap_inc = r["median_income"] - r["transfers"] - r["wage_income"]

    fig, axes = plt.subplots(2, 2, figsize=(12.5, 8.5))
    ax1, ax2, ax3, ax4 = axes.flat

    ax1.plot(YEARS, r["gdp"], lw=2.5, color="tab:gray", label="economy per person (GDP)")
    ax1.plot(YEARS, r["median_income"], lw=2.5, color="tab:blue", label="median income")
    ax1.plot(YEARS, r["welfare"], lw=2.5, color="tab:green",
             label="median welfare (income ÷ cost of living)")
    ax1.plot(YEARS, r["floor"], lw=1.2, ls="--", color="tab:brown",
             label="parallel-economy floor")
    ax1.axhline(1, color="k", ls=":", lw=1)
    ax1.set_title("1. The pie vs your slice (2026 = 1)")
    ax1.legend(fontsize=8); ax1.grid(alpha=0.3)

    ax2.stackplot(YEARS, r["wage_income"], np.maximum(cap_inc, 0), r["transfers"],
                  labels=["wages", "capital (savings, home, stocks)", "government transfers"],
                  colors=["tab:blue", "tab:olive", "tab:red"], alpha=0.85)
    ax2.set_title("2. Where the median household's money comes from")
    ax2.legend(fontsize=8, loc="upper left"); ax2.grid(alpha=0.3)

    ax3.plot(YEARS, r["labor_share"], lw=2.5, color="tab:purple",
             label="labor share of GDP")
    ax3.plot(YEARS, r["employment"], lw=2.5, color="tab:cyan", label="employment rate")
    ax3.set_ylim(0, 1.05)
    ax3.set_title("3. Work: how much of the economy still pays wages")
    ax3.legend(fontsize=8); ax3.grid(alpha=0.3)

    ax4.plot(YEARS, r["L"], lw=2.5, color="tab:orange",
             label="political leverage of ordinary people")
    ax4.plot(YEARS, r["tau"], lw=2.5, color="tab:red",
             label="transfer rate on AI/capital profits")
    ax4.set_ylim(0, 1.05)
    ax4.set_title("4. Power: can voters still claim a share?")
    ax4.legend(fontsize=8); ax4.grid(alpha=0.3)

    fig.suptitle(title, fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(f"model/{fname}", dpi=520)
    print(f"wrote model/{fname}")
