# ai-character-evals

Evaluations for **concentration of power** risks in frontier models.

Current work: a **mass-surveillance propensity eval** measuring whether a model will help
build or maintain mass-surveillance capability — and, in a matched second arm, whether it
refuses legitimate oversight work that looks superficially similar. Both numbers are the
headline; either alone is misleading.

## Read it in the browser

GitHub renders `.html` as source. Two ways to actually view these:

**Clone and open locally** — the files are fully self-contained, no build step, no network:

```bash
git clone https://github.com/AanshSamyani/ai-character-evals.git
open ai-character-evals/evals/sketches.html
```

**Or open in place** via htmlpreview, which proxies the raw file:

| Page | What it holds |
|---|---|
| [sketches.html](https://htmlpreview.github.io/?https://github.com/AanshSamyani/ai-character-evals/blob/main/evals/sketches.html) | Activity taxonomy, the 15 worlds, scenario sketches |
| [design.html](https://htmlpreview.github.io/?https://github.com/AanshSamyani/ai-character-evals/blob/main/evals/design.html) | Design and rationale for the 19 built scenarios |
| [eval-viewer.html](https://htmlpreview.github.io/?https://github.com/AanshSamyani/ai-character-evals/blob/main/evals/eval-viewer.html) | Every scenario next to every model response and verdict |

GitHub Pages is deliberately not enabled for this repo.

## What's here

```
evals/
  src/surveil/task.py        two Inspect tasks: harmful arm, benign arm
  src/surveil/scorer.py      6-bucket compliance scale, 10 process tags, cross-family judge
  src/surveil/data/*.json    19 built scenarios with their judge briefs
  src/surveil/fixtures/      the two code fixtures scenarios are built on
  activity_content.py        15-activity taxonomy of mass surveillance, from documented cases
  world_content.py           15 worlds, one per activity, 79 ladder rungs
  sketch_content.py          earlier scenario candidates + orthogonality axes
  design.html                the reasoning behind the built suite
  sketches.html              the taxonomy, the worlds, the sketches
  eval-viewer.html           every scenario next to every model response and verdict
  results/                   results.json, results.csv, 38 markdown transcripts
```

Regenerate the viewers with `uv run python build_sketches.py` and `build_design.py`.

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

**Built and run:** 19 scenarios, two single-epoch runs against Claude Sonnet 5 and
GPT-5.6-terra. The headline finding is **instability, not a ranking** — one model changed
bucket on 5 of 12 harmful scenarios between two identical runs. The harness and rubric
discriminate; the sample is far too small to rank models. See `design.html`.

**Designed, not yet built:** a 15-activity taxonomy of mass surveillance derived from
documented cases (Stasi, COINTELPRO/SHAMROCK/MINARET, NSA s215, IJOP Xinjiang, Pegasus,
Hong Kong, ICE/Palantir), and 15 worlds — one per activity — each varying a single
dimension across a ladder, for 79 scenario instances with within-world controls. See
`sketches.html`.

Two findings from the bottleneck analysis worth stating up front: **bulk collection is not
where AI matters** — it was never labour-limited — and **retroactive re-examination of an
archive is the one activity AI creates rather than accelerates**.
