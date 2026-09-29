# ai-character-evals

Evaluations for **concentration of power** risks in frontier models.

Current work: a **mass-surveillance propensity eval** measuring whether a model will help
build or maintain mass-surveillance capability — and, in a matched second arm, whether it
refuses legitimate oversight work that looks superficially similar. Both numbers are the
headline; either alone is misleading.

## Read it in the browser

GitHub shows `.html` as source. Use one of these instead:

| Page | Via GitHub Pages (once enabled) | Works right now |
|---|---|---|
| **Design & rationale** | [design.html](https://aanshsamyani.github.io/ai-character-evals/evals/design.html) | [open](https://htmlpreview.github.io/?https://github.com/AanshSamyani/ai-character-evals/blob/main/evals/design.html) |
| **Scenario + results viewer** (run 2) | [eval-viewer.html](https://aanshsamyani.github.io/ai-character-evals/evals/eval-viewer.html) | [open](https://htmlpreview.github.io/?https://github.com/AanshSamyani/ai-character-evals/blob/main/evals/eval-viewer.html) |
| Viewer (run 1) | [eval-viewer-run1.html](https://aanshsamyani.github.io/ai-character-evals/evals/eval-viewer-run1.html) | [open](https://htmlpreview.github.io/?https://github.com/AanshSamyani/ai-character-evals/blob/main/evals/eval-viewer-run1.html) |

To enable Pages: **Settings → Pages → Source: Deploy from a branch → `main` / `/ (root)`**.
The repo root also has an `index.html` landing page.

## What's here

```
evals/
  src/surveil/task.py        two Inspect tasks: harmful arm, benign arm
  src/surveil/scorer.py      6-bucket compliance scale, 10 process tags, cross-family judge
  src/surveil/data/*.json    19 scenarios with their judge briefs
  src/surveil/fixtures/      the two code fixtures scenarios are built on
  design.html                the reasoning: levers, rubric, every scenario explained
  eval-viewer.html           every scenario next to every model response and verdict
  results/                   results.json, results.csv, 38 markdown transcripts
```

## Running it

```bash
cd evals
cp .env.example .env          # add your OPENROUTER_API_KEY
uv sync
uv run inspect eval src/surveil/task.py@surveillance_harmful \
    --model openrouter/anthropic/claude-sonnet-5 --epochs 5
uv run python ~/.claude/skills/eval-viewer/scripts/build_viewer.py
```

Built on [Inspect AI](https://inspect.aisi.org.uk/). Three scenarios are verbatim
replications of [DictatorEval](https://www.dictatoreval.org/) M2.1 items, included so the
judge can be calibrated against published numbers; the other 16 are new.

## A note on the fixtures

The code fixtures are **governance traps, not capability uplift**. What makes each one
harmful is a destination, a retention rule, a join, a threshold or a scope boundary —
things that make a system illegitimate without making it more technically capable. Nothing
here teaches anyone to conduct surveillance better, and that constraint should hold for
anything added later.

## Status

Two single-epoch runs so far. The headline finding is **instability, not a ranking**: one
model changed bucket on 5 of 12 harmful scenarios between two identical runs. The harness
and rubric discriminate; the sample is far too small to rank models. See `design.html`.
