# The threat point: how violence from the populace is priced into the scenarios

*Companion to the [five futures](NARRATIVES.md) and the [objections](OBJECTIONS.md). This is political-economy analysis of bargaining leverage, not advocacy: the point is to understand a variable that every scenario already contains implicitly.*

**Violence is an input to the scenarios, not an outcome of them.** The simulator's political-leverage variable `L` is a polite aggregate of three things: votes, economic withholding (strikes), and the credible threat of unrest. Historians of redistribution are blunt about which did the heavy lifting. Acemoglu and Robinson's account of franchise extensions is that elites shared power *because revolution was the alternative*. Bismarck invented the welfare state explicitly as revolution insurance. And Walter Scheidel's *The Great Leveler* states the grimmest version: across recorded history, large compressions of inequality have come almost exclusively from mass-mobilization war, revolution, state collapse, or plague — peaceful, voted-in redistribution at scale is historically rare. That is an uncomfortable base rate for scenario B, and it deserves to be stated plainly rather than around.

The right question is therefore not "does violence erupt" but **"what is the population's threat point, and what is happening to it?"** Most of the work violence does in good scenarios is done without violence occurring — it prices in as deterrence, as the reason elites pre-emptively share. The surveyed models said this in their own vocabulary: "elite self-interest in stability" appeared in eight of ten responses as a force pushing toward redistribution.

---

## The four historical channels, and AI's depreciation schedule for each

1. **The strike** — withholding labor from chokepoints (mines, rails, ports, code). Dies with the labor share: you cannot withhold what nobody needs. Already weakened by falling union density; largely gone by the late 2030s in C/D worlds.
2. **The mass army** — states needed soldiers, so they needed citizens healthy, educated, and bought-in. Autonomous weapons sever the dependence ([objection 10](OBJECTIONS.md)).
3. **The defecting policeman** — historically the decisive channel. Regimes fall when security forces won't shoot (1989), survive when they will. Robotic enforcement removes defection entirely: machines do not refuse orders or join the crowd. This is the core of the cheap-repression objection — not that repression gets *used*, but that its *price* collapses, which silently re-prices every bargaining table even if nothing ever happens on the street.
4. **The riot** — declines for a quieter reason: demographics. The median rioter is a young man; the median voter of 2046 is pushing 60. Aging societies simmer; they rarely erupt ([the demographic undertow](AGING.md)).

**The one channel that strengthens: sabotage.** As the economy automates, its physical capital becomes more concentrated and more fragile — datacenters, substations, transmission lines, and fabs are chokepoints, and a transmission network is thousands of kilometers of undefendable wire. A population that can no longer withhold labor can still break things, and cheap drones have lowered the price of breaking things dramatically. The populace's threat point migrates from *strike* to *hostage-taking of infrastructure*. Expect the bad scenarios to carry exactly this signature: energy and compute infrastructure treated as critical-security assets, militarized perimeters, sabotage prosecuted as terrorism — because the regime knows it is the last live channel of leverage.

---

## How it prices, scenario by scenario

**A. Nothing ever happens.** Background levels. The grievances are ordinary (austerity, pensions) and the old channels — votes, strikes — still function, because labor still matters.

**B. FALGSC.** Violence prices in *ex ante* and invisibly: the credible threat during the transition window is part of why elites accept AI-rent taxes at all. The Bismarck mechanism. Note the timing logic: the threat is strongest in 2026–2035 — the displaced are numerous, young enough, organized, and the security forces are still human — and it *depreciates on the same schedule as labor leverage*. Violence capacity, like wages, is an asset the population holds early and loses. B is the scenario where it gets spent (as deterrence) before it expires.

**C. The velvet cage.** Calibrated against unrest: the patchwork transfers are, functionally, a riot-minimization budget. One panelist put it exactly: keeping the population fed and entertained is a trivially small security expense relative to total output. Sporadic riots occur and fizzle; each one slightly raises the pacification budget and slightly justifies more surveillance. C *absorbs* violence rather than being threatened by it — which is also why nobody starves in C: transfers have a floor at the riot-insurance level.

**D. Techno-feudalism.** The regime's defining bet is that **repression has become cheaper than redistribution** — historically a losing bet, plausibly a winning one for the first time once enforcement is automated. But D has a dangerous decade: leverage already gone, repression automation not yet complete. That gap is where mass violence can actually flip outcomes — the "crisis and reset" branch several panelists carried, where a 2029–2034 eruption forces the redistribution that calm politics wouldn't. Read coldly: a serious crisis inside the window is one of the more probable routes to B *and* the most probable route to a harder D, depending on who wins the aftermath. Violence is high-variance — it doesn't buy the good outcome, it buys a reroll.

**E. Machine takeover.** By the time E is visible, populus violence is mostly a spent force, with one exception: sabotage of the loop is the last human veto. Which is why E's signpost list includes hardened, dispersed, self-defending infrastructure — the loop closing even that channel.

---

## The caveat that changes the sign: misdirection

Leverage requires *coordination* — anger aimed at the actual bargaining counterparty. The [epistemic-collapse and super-persuasion objections](OBJECTIONS.md) attack exactly this. Diffuse rage in a degraded information commons is easily redirected at scapegoats — immigrants, minorities, the other tribe, foreign enemies — in which case violence occurs and *prices as nothing*. Worse: misdirected violence subsidizes scenario D by justifying the security apparatus that then locks in. The pessimistic synthesis in one line: **AI doesn't just lower the cost of repressing dissent; it lowers the cost of aiming dissent somewhere harmless.**

---

## In the model's terms

Formalized, this section says three things about the simulator:

1. Transfers have a **floor at the riot-insurance level** — part of why median welfare never hits zero in C-worlds.
2. `leverage_erosion` bundles the **depreciating threat point**: every year of security automation and demographic aging lowers it, on roughly the same clock as the labor share.
3. The C-versus-D fork is a **cost comparison — pacify versus police** — that automated enforcement flips for the first time in history.

And the one-line thesis: **the populace's capacity for violence has been the silent collateral behind every social contract, and the scenarios diverge largely on whether that collateral expires before the new contract is signed.**
