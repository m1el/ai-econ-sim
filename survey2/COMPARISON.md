# Debiased re-survey: results and comparison with the framed survey

*Same 10 models, 2026-06-11. Raw responses: `survey2/responses/`. Instrument: `survey2/question.md`.*

## What changed in the instrument

Survey 1 contained four plausible bias sources: (1) it presented the Metzger thread and the Gradual Disempowerment paper as the two reference positions (anchoring + salience); (2) it described the asker as worried, pessimistic, and hoping to be proven wrong (sympathy/accommodation pressure); (3) it imposed a five-bucket outcome taxonomy where two of the five buckets (S3, S4) were bad-flavored — taxonomy granularity itself attracts probability mass; (4) it asked for steelmanning, making both extreme narratives maximally salient.

Survey 2 removed all of this: no positions, no persona, no taxonomy. Models stated their own AI-pace assumptions, invented their own trajectories with probabilities, and answered 10 *independent* calibrated probability questions about concrete observables in 2046.

## Calibrated estimates (the cleanest cross-model evidence)

Probability (%) that each statement is true of developed economies in 2046:

| Statement | GPT-5.5 | Opus | Gemini | Grok | DeepSeek | Qwen | Kimi | GLM | MiniMax | Mistral | **Mean** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| a) Median real disposable income **higher** than 2026 | 72 | 68 | 65 | 68 | 65 | 75 | 55 | 65 | 60 | 60 | **65** |
| b) Median income **>20% lower** than 2026 | 8 | 14 | 15 | 12 | 25 | 10 | 12 | 15 | 15 | 20 | **15** |
| c) Labor share of income **below 40%** | 18 | 40 | 80 | 45 | 70 | 65 | 28 | 40 | 40 | 45 | **47** |
| d) **>25% prime-age involuntary joblessness** | 10 | 22 | 35 | 22 | 15 | 35 | 18 | 25 | 22 | 30 | **23** |
| e) Citizens' influence over policy **substantially weaker** | 55 | 52 | 70 | 55 | 80 | 60 | 68 | 55 | 65 | 55 | **62** |
| f) Top-1% wealth share **up ≥10 points** | 32 | 45 | 85 | 60 | 75 | 50 | 38 | 35 | 50 | 40 | **51** |
| g) Housing+energy+food a **larger** budget share | 43 | 48 | 60 | 35 | 55 | 80 | 48 | 60 | 55 | 50 | **53** |
| h) Capable household robot **< 6 months income** | 45 | 35 | 40 | 40 | 60 | 40 | 22 | 75 | 35 | 70 | **46** |
| i) Transfers the **largest income source** for median household | 22 | 30 | 35 | 50 | 30 | 35 | 30 | 30 | 20 | 35 | **32** |
| j) AI/operators allocate resources with **little human oversight** | 28 | 22 | 55 | 30 | 20 | 70 | 12 | 45 | 35 | 60 | **38** |

**The shape of this table is the headline result.** Material questions lean optimistic: 65% that the median person is *richer* in 2046, only 15% on a >20% income decline, only 23% on mass involuntary joblessness. Power and distribution questions lean pessimistic: 62% that ordinary citizens' political influence is substantially weaker, 51% on a major jump in top-1% wealth share, 53% that essentials eat more of the median budget. The "comfortable but politically weaker" pattern — which survey 1 might have manufactured through framing — **reproduces from a neutral prompt**.

## Self-generated trajectories, mapped to comparable categories

Models invented their own scenarios (no taxonomy given). Classifying each model's trajectories by its *own description of the median person's 2046 outcome* (my mapping — see caveats):

| Outcome for median person | Survey 2 (neutral) | Survey 1 (framed, S-buckets) |
|---|---|---|
| Clearly better off | **~35%** | 18.7% (S1) |
| Roughly flat / precarious | **~34%** | 34.5% (S2) |
| Worse off / powerless dependent | **~27%** | 39.3% (S3+S4) |
| Stall / shock / other | **~4%** | 7.5% (S5) |

## How big was the framing bias?

1. **The framed survey was ~12–15 points more pessimistic on scenario probabilities.** Under neutral elicitation, "clearly better off" roughly doubled (19→35%) and the bad bucket shrank (39→27%). Plausible mechanisms: two-of-five bad buckets in my taxonomy, salience of the disempowerment paper, and accommodation of the worried asker. Direction of causality is clear because the calibrated estimates (which had no taxonomy to anchor on) sit *between* the two scenario aggregations.
2. **What did NOT change — the robust findings:**
   - **Political-influence erosion survived debiasing fully**: 62% mean on (e), with *every* model ≥52%. This was never an artifact of citing the paper.
   - **The bifurcated-price mechanism appeared spontaneously** in 9/10 neutral responses (digital deflation vs. housing/energy/land inflation; "Baumol's cost disease on steroids" — Qwen; "the race between deflationary AI and inelastic physical assets" — Gemini). Nobody was prompted with it.
   - **The redistribution-race mechanism also reappeared unprompted** as the #1 "mechanism you'd bet on" in 6/10 responses (GPT-5.5's "pass-through rate", Opus's "ownership + political capacity, not aggregate output", Grok, MiniMax, Mistral, DeepSeek).
   - **Housing as the single biggest spoiler** — named by 8/10 in both surveys.
3. **What the neutral survey surfaced that the framed one suppressed:**
   - **More probability on plateau/stall/bottleneck worlds.** My S5 bucket compressed "AI fizzles," "energy bottleneck," "regulatory thicket," and "geopolitical fracture" into one 7.5% afterthought; freed from the taxonomy, models put **15–35%** on slowdown/bottleneck trajectories (DeepSeek 20% energy-bottleneck, Qwen 20% stagnation, Kimi 15% plateau, Mistral 15% AI winter + 20% degrowth). A meaningfully large "this whole debate is moot, 2046 looks like 2026 but older and more indebted" possibility was being hidden.
   - **Energy, demographics (aging), and climate as first-class drivers** — barely mentioned in survey 1, prominent in survey 2 (Qwen's old-age dependency ratio, Mistral's climate shocks, MiniMax's "AI is energy-gated before it's labor-gated").
   - **Wider genuine disagreement than the framed survey suggested.** The forced buckets made models look like they agreed (everyone ~35% S2). The independent estimates expose real spread: labor share <40% ranges from 18% (GPT-5.5) to 80% (Gemini); AI-runs-the-economy (j) from 12% (Kimi) to 70% (Qwen). The apparent consensus was partly an artifact of the instrument.

## Addendum: fresh-instance Fable 5 (11th panelist)

A clean `anthropic/claude-fable-5` instance (no conversation context — requested as a "pair of fresh eyes" because the assistant instance had absorbed the paper, the pessimistic prior, and all panel responses) answered the same neutral questionnaire. Result (`responses/anthropic_claude-fable-5.md`):

| Item | Fresh Fable | Panel mean (10) | Position vs panel |
|---|---|---|---|
| a) median income higher | **80** | 65 | most optimistic of all 11 |
| b) income >20% lower | **4** | 15 | lowest |
| c) labor share <40% | **18** | 47 | tied-lowest (with GPT-5.5) |
| d) >25% joblessness | **6** | 23 | lowest |
| e) citizen influence weaker | **35** | 62 | far below every other model (all ≥52) |
| f) top-1% wealth +10pp | **15** | 51 | far lowest |
| g) essentials larger budget share | **30** | 53 | lowest |
| h) cheap household robot | 35 | 46 | low side |
| i) transfers largest income source | **12** | 32 | lowest |
| j) AI allocates, little oversight | 30 | 38 | low side — but it volunteers ~70% for "AI deeply embedded in most allocation decisions with nominal human sign-off" |

Observations:

1. **It bets on the same mechanism as the panel** — "the race between the diffusion speed of labor-substituting AI and the adaptation speed of redistributive institutions" — but assigns much friendlier parameter values, leaning on the historical base rate of political self-correction (factory acts, New Deal, postwar welfare states).
2. **It names its own soft spot, and it's exactly the disempowerment argument**: "historical precedents involve labor that retained economic leverage to withhold — which is exactly what AI erodes. That last point is the soft spot in my entire central forecast." So the optimism is explicitly conditional on a historical analogy it concedes may not transfer.
3. Its trajectory mix: 58% good-ish (productivity boom 30% + steady diffusion 28%), 20% capital-concentrated decoupling (which it calls *unstable* — likely resolving into correction or worse within a decade), 12% plateau, 10% discontinuity.
4. Interpretation options, not mutually exclusive: (i) Anthropic models lean structurally less pessimistic on institutional erosion (Opus 4.8 was also below panel mean on e/f, at 52/45); (ii) one-sample noise; (iii) the rest of the panel is anchored by the same doom-flavored discourse in training data and Fable discounts it harder. The conversation-context experiment can't distinguish these — but it does confirm the original suspicion: an instance marinated in this conversation would not have produced these numbers.

## Caveats on this comparison

- The trajectory mapping (better/flat/worse) is my judgment call on free-form text; the per-model trajectory lists are in the raw files if you want to audit. The hardest cases are "high material security, zero mobility/agency" worlds (Qwen's Automated Welfare State, Gemini's Managed Abundance) — I counted them as "better off" on material grounds, but they are S4-flavored on agency. If you instead count them as bad, the two surveys nearly agree — i.e., **some of the measured "bias" is really a disagreement about whether a comfortable, powerless life counts as a bad outcome.** That value question is yours to answer, not the models'.
- Same models, same temperature (0.7), one sample each — no repeat sampling, so individual numbers carry sampling noise of maybe ±5-10 points.
- Kimi's response was truncated by the completion cap after its 3rd driver; its trajectories and calibrated estimates are complete. MiniMax lost only its final sentence.

## Bottom line (updated beliefs after debiasing)

- **Material floor: stronger than the framed survey implied.** Best estimate ~65% the median person in a developed economy is materially better off in 2046, and only ~15% on severe decline. Your "lots of suffering" prior loses more ground.
- **Power and concentration: unchanged by debiasing.** ~62% weaker citizen influence and ~51% major wealth concentration jump are the most framing-robust pessimistic numbers in the whole exercise. Your "concentration of power" prior survives as the *most likely single direction of change*, even from a neutral prompt.
- **New mass on "nothing transformative happens by 2046"** (~15-25%): plateau, energy bottlenecks, regulation. In those worlds your existing career plan mostly survives, which is itself decision-relevant: the case for panic-pivoting is weaker than survey 1 suggested, while the case for capital accumulation and political engagement is unchanged.
