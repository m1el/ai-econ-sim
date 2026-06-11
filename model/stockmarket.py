# /// script
# dependencies = ["numpy", "matplotlib"]
# ///
"""Crude stock-market sketches for the five narratives (real total return, 2026=100).

These are illustrations of the mechanisms described in NARRATIVES.md, not
model output: each curve is a hand-set growth path implied by the scenario's
profit share, taxation, expropriation, and (for E) denominator failure.

Run: uv run model/stockmarket.py
"""
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

YEARS = np.arange(2026, 2057)
T = len(YEARS)


def path(segments):
    """segments: list of (n_years, annual_growth). Returns index starting at 100."""
    g = np.concatenate([np.full(n, r) for n, r in segments])[: T - 1]
    return np.concatenate([[100.0], 100.0 * np.cumprod(1 + g)])


def save(fname, title, lines, note=None):
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    for label, y, color, ls in lines:
        ax.plot(YEARS, y, lw=2.5, color=color, ls=ls, label=label)
    ax.set_yscale("log")
    ax.axhline(100, color="k", ls=":", lw=1)
    ax.set_title(title)
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=9)
    if note:
        ax.set_xlabel(note, fontsize=9, color="#666666")
    fig.tight_layout()
    fig.savefig(f"model/{fname}", dpi=520)
    print(f"wrote model/{fname}")


# A. Plateau: bubble top, dot-com-sized AI drawdown, capex recession, boring decades
ai = path([(2, 0.18), (3, -0.38), (26, 0.06)])
broad = path([(2, 0.07), (3, -0.13), (26, 0.045)])
save("market_plateau.png", "Stock market — A. Nothing ever happens (real, 2026 = 100)",
     [("broad index", broad, "tab:blue", "-"),
      ("AI cluster (~35% of index in 2026)", ai, "tab:red", "-")],
     "Crash first, lost decade after; value and dividends quietly lead the recovery.")

# B. FALGSC: strong earnings, then AI-rent taxes + higher rates trim the slice
b = path([(9, 0.08), (21, 0.055)])
save("market_prosperity.png", "Stock market — B. FALGSC (real, 2026 = 100)",
     [("broad index, after AI-rent taxes", b, "tab:green", "-")],
     "Solid high-single-digit returns, low drama; the surplus is shared by design.")

# C. Velvet cage: profit share of GDP nearly doubles; index decouples from welfare
c = path([(30, 0.10)])
welfare = path([(30, 0.005)])
save("market_squeeze.png", "Stock market — C. The velvet cage (real, 2026 = 100)",
     [("broad index", c, "tab:blue", "-"),
      ("median welfare (same scale)", welfare, "tab:gray", "--")],
     "The decoupling is not a malfunction of this scenario; it is its definition.")

# D. Techno-feudalism: like C until ~2038, then listed claims rot while insiders keep compounding
d_listed = path([(12, 0.11), (18, -0.02)])
d_inside = path([(12, 0.11), (18, 0.10)])
save("market_feudalism.png", "Stock market — D. Techno-feudalism (real, 2026 = 100)",
     [("listed market (your index fund)", d_listed, "tab:blue", "-"),
      ("insider / private wealth", d_inside, "tab:red", "--")],
     "Public markets hollow as the best assets migrate private and minorities get diluted.")

# E. Machine takeover: vertical in dollars; falling in command over energy and land
e_nominal = path([(14, 0.12), (16, 0.25)])
res_price = path([(14, 0.05), (16, 0.35)]) / 100.0   # essentials price index
e_real = e_nominal / res_price
save("market_breakaway.png", "Stock market — E. Machine takeover (2026 = 100)",
     [("index in dollars", e_nominal, "black", "-"),
      ("index in essentials (energy, land)", e_real, "tab:red", "-")],
     "Number goes up forever, commands less every year: the denominator fails.")
