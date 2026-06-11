# ai-econ-sim

What happens to the median person's employment and welfare under advanced AI —
an attempt to answer it well enough to plan a life around.

**Site:** https://m1el.github.io/ai-econ-sim/

## What's here

- **Two LLM surveys** of 10–11 frontier models via OpenRouter:
  - `survey/` — first attempt, framed by two reference positions (Metzger's
    comparative-advantage optimism vs. Kulveit et al.'s *Gradual
    Disempowerment*) and the asker's pessimistic prior.
  - `survey2/` — debiased re-run: neutral instrument, no positions, no
    persona, models generate their own trajectories plus independent
    calibrated probability estimates. `survey2/COMPARISON.md` measures how
    much the framing skewed the first survey (~12–15 points toward
    pessimism), what survived debiasing (political-influence erosion: 62%
    mean, every model ≥52%), and includes a fresh-context Fable 5 as an
    11th panelist.
- **A simulator** (`model/`):
  - `simulate.py` — v1: task-based automation macro model (Acemoglu–Restrepo
    / Korinek–Suh skeleton) with political-leverage feedback, resource
    competition, and a parallel-economy floor; hand-set priors.
  - `simulate_v2.py` — v2: same engine, priors re-derived from the debiased
    survey, validated by a built-in calibration table against the panel's
    statement probabilities. One statement refuses to calibrate, and the
    docstring explains why that residual is itself a finding.
  - `narratives.py` + `runaway.py` — render the five scenario figures.
- **The synthesis** — `REPORT.md` (survey 1 + v1 model) and `NARRATIVES.md`
  (five futures with graphs and observable signposts), built into a static
  site by `build_site.py` and deployed by GitHub Actions
  (`.github/workflows/pages.yml`).

## Run things

Everything uses [uv](https://docs.astral.sh/uv/) inline-script metadata —
no setup:

```sh
uv run model/simulate_v2.py          # Monte Carlo + calibration table
uv run model/narratives.py           # regenerate scenario figures
uv run build_site.py                 # build the static site into site/
OPENROUTER_API_KEY=... uv run survey2/run_survey.py   # re-run the survey (~$2)
```

## Honest caveats

The simulator is a belief-rendering device, not a crystal ball: a simple
engine tuned so its statistics match what 11 AI models collectively expect.
The probabilities are soft. The scenario *shapes* and the signposts that
distinguish them are the useful part. Model responses are LLM outputs from
June 2026 and inherit whatever is wrong with their training data.
