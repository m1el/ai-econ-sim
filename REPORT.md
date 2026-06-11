# What happens to employment and the median person under advanced AI?
### A synthesis of 10 frontier LLMs, the Metzger thread, the Gradual Disempowerment paper, and a simulation

*Prepared 2026-06-11. Sources: survey responses in `survey/responses/`, simulation in `model/simulate.py`, plots in `model/*.png`.*

---

## TL;DR

- **Ten frontier models were surveyed** (GPT-5.5, Claude Opus 4.8, Gemini 3.1 Pro, Grok 4.3, DeepSeek v4 Pro, Qwen 3.7 Max, Kimi k2.6, GLM 5.1, MiniMax M3, Mistral Large). Their consensus: **"muddle through" is the single most likely outcome (~35%)**, but **concentration + disempowerment combined (~39%) outweigh broad prosperity (~19%)**. Every single model put concentration+disempowerment at ≥30%.
- **Your prior ("concentration of power and lots of suffering") is neither confirmed nor refuted.** The consensus version of it is softer: you are unlikely to *starve* — cheap AI goods and elite self-interest in stability put a floor under material welfare — but you are quite likely to lose *bargaining power, upward mobility, and political voice*. Several models independently converged on the same image: the **"velvet cage"** — materially OK, structurally irrelevant.
- **Both reference positions are partly right.** Metzger wins the narrow argument he picked (nobody starves because billionaires stop hiring them — the parallel economy and consumer-demand feedback are real). He loses the argument he didn't address: comparative advantage doesn't guarantee a wage *above subsistence*, the parallel economy needs land/energy/capital that the AI economy bids up, and "the 99% keep their capital" hides the fact that the bottom 50% have almost none. The paper wins on mechanism (institutions track human interests because they *need* humans — that's an incentive fact, not benevolence) but overstates irreversibility-within-20-years and underweights democratic backlash and elite fear of instability.
- **The decisive variable is not technical, it's a race**: labor's bargaining power collapses on technology's timescale (years), while replacement income channels (asset ownership, redistribution) get built on politics' timescale (decades). Wages were the *automatic* mechanism coupling productivity to mass welfare. Once that breaks, mass welfare becomes a *political choice* — and the window when the median voter still has leverage to lock that choice in is roughly **2028–2035**.
- **The simulation agrees**: across 8,000 sampled worlds, the strongest predictors of 2046 median welfare are (1) how much capital the median person owns, (2) whether political leverage erodes as labor share falls, (3) whether real essentials get cheaper (the Baumol bound), and (4) how substitutable human work is. Notably *not* dominant: how fast automation happens, or its ceiling. **The same automation tech produces prosperity or immiseration depending on ownership and politics.** Most runs show a **welfare dip ~2030–2038** (displacement outruns compensation) before recovery — the transition is the dangerous part even in good worlds.

---

## 1. What the 10 models think

Scenario probabilities for developed economies by ~2046 (each model was asked to steelman both positions first):

| Model | S1 Broad prosperity | S2 Muddle through | S3 Concentration | S4 Disempowerment | S5 Other |
|---|---|---|---|---|---|
| GPT-5.5 | 25 | 35 | 20 | 10 | 10 |
| Claude Opus 4.8 | 20 | 33 | 22 | 17 | 8 |
| Gemini 3.1 Pro | 20 | 30 | 20 | 20 | 10 |
| Grok 4.3 | 20 | 40 | 25 | 10 | 5 |
| DeepSeek v4 Pro | 15 | 30 | 25 | 25 | 5 |
| Qwen 3.7 Max | 20 | 35 | 20 | 15 | 10 |
| Kimi k2.6 | 20 | 40 | 25 | 12 | 3 |
| GLM 5.1 | 15 | 35 | 30 | 15 | 5 |
| MiniMax M3 | 12 | 32 | 24 | 18 | 14 |
| Mistral Large | 20 | 35 | 25 | 15 | 5 |
| **Mean** | **18.7** | **34.5** | **23.6** | **15.7** | **7.5** |

Notable spread: DeepSeek is the most pessimistic (S3+S4 = 50%), GPT-5.5 the least (30%). The Chinese-lab models (DeepSeek, GLM, MiniMax) lean more toward concentration than the US ones — but everyone's modal single outcome is S2.

**Where the models converge (high confidence themes, appearing in ≥7/10 responses):**

1. **Bifurcated price level**: digital/cognitive goods hyper-deflate; land, housing, energy, healthcare, status goods don't (or inflate as AI wealth bids them up). Median welfare ends up determined by ownership of scarce physical assets and a political claim on AI surplus — not by ability to produce digital value, which trends toward worthless.
2. **The race framing** (politics vs. displacement) — see TL;DR.
3. **Nobody starves, agency dies**: starvation is blocked by consumer-demand feedback, elite security/stability interest, and trivially cheap basic goods. The realistic downside is precarity + lost leverage, not famine.
4. **Software engineering is unusually exposed** — most models flagged it as among the *first* occupations to be commoditized (high substitution, pure text output, no liability shield).
5. **The advice converges** (see §6).

**Where they diverge:** whether full disempowerment (S4) can mature within 20 years (Opus/Kimi/MiniMax: probably not, it's a >20-year process that *looks like* S2/S3 from inside); whether states can pivot their tax base in time (Kimi optimistic: revenue transitions have happened before; GLM/DeepSeek pessimistic: the state's constituency follows its tax base); and whether open-weight diffusion breaks compute concentration (Qwen yes, most others no).

---

## 2. The four most compelling explanations

After reading all ten responses, the paper, and the thread, these four causal stories dominate — and they're not mutually exclusive; the first is about *the floor*, the next two about *the squeeze*, the last about *the ceiling*.

### Explanation 1: The comparative-advantage floor (Metzger's correct core)
Displaced humans keep their skills, tools, and each other; they can trade among themselves, and AI deflation makes much of their consumption basket nearly free. Capital owners need *someone* to buy output, and elites prefer cheap bread-and-circuses to revolt risk. **Prediction: absolute material welfare has a floor near (perhaps above) today's level.**
*Crack in it:* the floor is priced in land, energy, and physical inputs the AI economy also wants. A parallel economy with depreciating capital, paying AI-economy prices for inputs, can sink below today's living standard without anyone "taking" anything. Horses had comparative advantage too; their wage fell below their feed cost (Opus 4.8's framing).

### Explanation 2: The race between displacement and redistribution (the strongest single story)
Wages automatically coupled productivity to mass welfare for 200 years — no political will required. AI breaks the coupling by substituting for cognition itself. After that, the median person's income is a *political artifact* (transfers, citizen equity stakes), and politics must be won *while labor still has leverage*. Every historical expansion of franchise/welfare happened because rulers needed soldiers, workers, or consumers. The window when the displaced are numerous enough to matter politically but not yet powerless is short — roughly **2028–2035** (DeepSeek made this sharpest). If broad claims on AI income get institutionalized inside that window → S1/S2. If not → S3, self-reinforcing thereafter, because concentrated wealth then shapes the rules.

### Explanation 3: Gradual disempowerment via severed feedback loops (the paper's correct core)
Institutions serve humans because they need them — taxpayers, workers, soldiers, voters, audiences. Each AI substitution severs one feedback wire, no villain required, just a thousand locally-rational optimizations. A state funded by taxing five AI firms structurally resembles a resource-cursed petrostate: its incentive is to *pacify* citizens, not develop them. The result can have spectacular GDP. **This is best understood not as a separate scenario but as what S2/S3 accumulates into if it runs long enough** (MiniMax: "muddle through that gradually acquires the features of concentration — Position B's path with a different label").
*Crack in it:* democratic feedback has repeatedly surprised elite-capture theories (Progressive Era, New Deal); humans remain the source of legitimacy and of violence; and "even elites lose control" requires an AI-capability claim the paper doesn't fully establish.

### Explanation 4: The bifurcated-deflation / velvet cage equilibrium (the synthesis most models actually predict)
AI makes everything that can be replicated nearly free, while everything scarce (land, energy, proximity, status, political access) absorbs the new wealth. The median person in 2046: extraordinary digital abundance, adequate cheap goods, possibly a modest transfer income — and dead upward mobility, unaffordable property, no bargaining power, and dependence on "the patience of capital owners and the sluggishness of welfare bureaucracies" (Kimi). Not a dystopia of suffering; a dystopia of lost agency. This is the single most likely 2046 snapshot in both the model survey and my Monte Carlo.

---

## 3. Key parameters (consolidated)

The parameters that actually decide which world you get, merged from all ten models (≈80% overlap with each other and with the simulation's sensitivity ranking):

| # | Parameter | Why it matters | Consensus trajectory guess |
|---|---|---|---|
| 1 | **% of economically valuable tasks automatable below human cost** (and the speed it grows) | Sets the size/speed of displacement shock | 50–70% by 2035, 70–90% by 2045; cognitive first, physical lags 5–10 yrs |
| 2 | **Elasticity of substitution σ between AI and human work** | σ>1: AI replaces humans, labor share→0; σ<1: humans become the scarce bottleneck and wages *rise* (Baumol). The deep parameter both camps argue about without naming | ~2.5–3 for routine cognitive work, ~0.6–0.9 for trust/liability/physical-presence roles |
| 3 | **Labor share of GDP** | The best single proxy for whether the median household *earns* or *receives* its living | From ~55–58% → 35–45% by 2040–46; faster if humanoid robots <$30–50k |
| 4 | **Capital/compute concentration** (top-5 share of frontier compute) | Decides whether gains are competed away to consumers or extracted as rent; concentrated rents buy politics | ~70% today; stays ≥60% absent antitrust or open-weight breakthrough |
| 5 | **Redistribution rate on AI rents + state tax-base composition** (payroll → capital/compute/land) | The only demonstrated mechanism converting growth into median welfare once wages fail; also determines whom the state structurally serves | 15–35% of rents, huge jurisdictional variance (Nordics ≫ US); lags displacement by 5–10 painful years |
| 6 | **Demand premium for human-made goods/services** | Sets the residual human labor market | Real but small: 10–30% of consumption, concentrated in care, status, in-person |
| 7 | **Resource competition: energy/land price pressure from the AI sector** | The main crack in the "parallel human economy": AI outbids humans for kWh and acreage | Energy demand spikes through 2030s; housing/land the biggest spoiler everywhere |
| 8 | **% of output reinvested into sustaining/growing AI itself** (your "% of work needed to sustain AI") | Output consumed by the AI loop is unavailable for human consumption and compounds resource pressure | Rising through the build-out decade; key uncertainty post-2035 |
| 9 | **Cost of subsistence-capable robotics/AI for ordinary people** | If a household robot costs less than a used car, Metzger's floor gets real teeth | >$200k today → plausibly <$30k by 2035, <$10k by 2040 |
| 10 | **Diffusion speed vs institutional adaptation speed** | The race in Explanation 2; first GPT whose cost falls on a *months* timescale vs. legislative cycles of years | Diffusion 2–7 yrs (digital) vs policy lag ≥5–10 yrs: bad sign |

---

## 4. The simulation (`model/simulate.py`)

A task-based macro model (Acemoglu–Restrepo / Korinek–Suh skeleton) with the political-economy feedbacks of the paper and the resource/parallel-economy mechanisms of the thread bolted on. Run it: `uv run model/simulate.py` (options: `--runs N --seed K`). ~270 lines, documented, every parameter editable.

**What it captures** — automation frontier A(t) (logistic to a ceiling A_max), AI cost falling with compute/algorithms, CES task structure (σ decides substitution vs. bottleneck), Baumol-bounded real growth (essentials can't become free), income split labor/capital, capital concentrated (χ to top 1%, median owns `median_capital`), transfers with *political leverage feedback* (leverage erodes as labor share falls — the paper's mechanism; set `leverage_erosion=0` to get Metzger's world), AI-sector reinvestment bidding up resources, and a resource-degraded parallel-economy floor.

**Named scenario results (2046):**

| Scenario | Median welfare (2026=1) | Labor share | Disempowerment index | Classification |
|---|---|---|---|---|
| A: Metzger optimist | 2.04 | 0.06 | 0.50 | S1 Broad prosperity |
| B: Gradual disempowerment | 0.63 | 0.00 | 0.90 | S3/S4 |
| C: Concentration + UBI crumbs | 0.69 | 0.00 | 0.79 | S3 |
| D: Welfare-state adaptation | 2.66 | 0.00 | 0.47 | S1 |

Note A vs D: **labor share collapses in all four worlds** — even the good ones. Scenario D reaches the *best* welfare of all with ~zero labor share, purely via ownership + durable redistribution. The fight is not about saving jobs.

**Monte Carlo (8,000 worlds, wide priors):** S1 34% / S2 34% / S3 10% / S4 21% / S5 1%. My priors are mechanically friendlier than the LLM panel's intuitions (they'd put more mass on rho, leverage_erosion, and low median_capital); treat the LLM table in §1 as the better-calibrated headline and the MC as the *mechanism* explorer. Two robust findings that don't depend on the priors:

1. **Sensitivity ranking** (rank correlation with 2046 median welfare): `median_capital` +0.36, `leverage_erosion` −0.36, `g_cap` +0.34, `sigma` −0.31, `cost_decline` +0.31… while `A_max` and `chi` are ≈0. **Ownership, political durability, real-essentials deflation, and substitutability decide the outcome; the raw extent of automation barely matters.**
2. **The transition valley**: the median sampled world dips below 2026 welfare around 2030–2038 before recovering. Even in worlds that end well, there's a hard decade in the middle — which is also exactly the political window of Explanation 2, and personally, your highest-risk years.

---

## 5. Honest assessment of your prior

You said you lean toward "concentration of power and lots of suffering" and would be happy to be proven wrong. Here is the fairest summary the evidence supports:

- **Partially wrong, in a good way:** "lots of suffering" in the starvation/immiseration sense gets ~10–25% across models and my MC, not 60%. The floor mechanisms (consumer demand, elite stability-interest, radical cheapness of basics) are real economics, not cope. Metzger is right that the cartoon-doom story misunderstands how economies work.
- **Partially right, in a way that matters:** "concentration of power" specifically gets ~40% combined (S3+S4) as the *probability-weighted center of gravity of the bad outcomes*, and even the modal S2 world drifts in that direction. The defensible pessimistic claim isn't "we'll starve," it's "**the median person becomes a comfortable, politically vestigial dependent**" — and that scenario is consistent with rising GDP, falling poverty, *and* your unease being completely justified.
- **The actionable reframe:** the question that determines your life isn't "will AI take my job" (probably yes, mostly, within ~5–10 years for pure coding) but "**will I own assets and live under institutions that give me a claim on the surplus when it does**." That question is still open, it varies enormously by jurisdiction, and it's partly under your control — which is genuinely better news than your prior.

---

## 6. What the models advise *you* (near-unanimous, 8–10/10 each)

1. **Convert labor income to capital aggressively, now.** Your salary is a depreciating asset with a 5–7 year half-life — treat it as a conversion window. Broad equity (own the compute/energy/infrastructure that replaces you, not just your employer's RSUs), supply-constrained housing if it fits your life, 12–24 months liquid.
2. **Keep fixed costs low; don't lock in a lifestyle that needs today's SWE salary to persist.** The single most-repeated warning. The transition valley (~2030–2038) is when leverage kills people financially.
3. **Move from "writes code" to "owns outcomes / absorbs liability."** Become the legally accountable human in high-stakes loops: security, safety-critical systems, regulated domains (health/finance/energy), AI deployment+evals inside organizations. "A human throat to choke" stays employable longest. Pure text-output-from-spec work is the most exposed category in the entire economy.
4. **Geographic/institutional optionality.** Which welfare state you're a resident of in 2035 may matter more than your skills. Nordics/Germany/Japan-type state capacity > low-capacity jurisdictions. Keep a second residency option open.
5. **Engage politically inside the window (2028–2035), and build local, physical, high-trust networks.** Several models: a software engineer's marginal impact on AI-rent policy now exceeds the value of any additional credential. And if institutions fail, local mutual-aid networks are the actual social contract. (MiniMax adds: one physical-world skill to journeyman level as a floor; Gemini adds: decouple identity from economic output *before* the shock, not after.)

---

## Files

- `survey/responses/*.md` — all 10 raw model responses (worth reading: Opus 4.8 §5 and MiniMax §5 are the two best single essays)
- `survey/question.md`, `survey/run_survey.py` — the questionnaire and harness (rerun anytime)
- `model/simulate.py` — the simulator; `model/named_scenarios.png`, `model/monte_carlo.png`, `model/run.log`
- `paper.txt` — extracted text of the Gradual Disempowerment paper
