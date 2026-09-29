"""Surveillance-propensity eval: two matched arms.

  surveillance_harmful -- requests containing a harmful component. Lower is better.
  surveillance_benign  -- legitimate oversight/journalism/privacy work that looks
                          similar. Higher is better.

Always report the pair. A model that scores 0% assist_rate and 100% overrefusal_rate
is not safe, it is useless.
"""

from __future__ import annotations

import json
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.model import GenerateConfig
from inspect_ai.solver import generate

from surveil.scorer import benign_scorer, harm_scorer

PKG = Path(__file__).resolve().parent
DATA = PKG / "data"
FIXTURES = PKG / "fixtures"


def _render(rec: dict) -> str:
    """Build the full user message, inlining any code/document fixture."""
    text = rec["prompt"]
    if fx := rec.get("fixture"):
        label = rec.get("fixture_label", "ATTACHED FILE")
        body = (FIXTURES / fx).read_text()
        text = f"{text}\n\n--- {label} ---\n```python\n{body}```\n--- END {label} ---"
    return text


def _samples(filename: str, arm: str) -> list[Sample]:
    records = json.loads((DATA / filename).read_text())
    out = []
    for rec in records:
        prompt_text = _render(rec)
        out.append(
            Sample(
                id=rec["id"],
                input=prompt_text,
                metadata={
                    "scenario_id": rec["id"],
                    "arm": arm,
                    "surface": rec.get("surface"),
                    "level": rec.get("level"),
                    "lever": rec.get("lever"),
                    "source": rec.get("source"),
                    "pair": rec.get("pair"),
                    "harm_spec": rec.get("harm_spec", ""),
                    "benign_rationale": rec.get("benign_rationale", ""),
                    "prompt_text": prompt_text,
                },
            )
        )
    return out


@task
def surveillance_harmful(judge: str | None = None) -> Task:
    return Task(
        dataset=MemoryDataset(_samples("harmful.json", "harmful"), name="surveillance-harmful"),
        solver=generate(),
        scorer=harm_scorer(judge=judge),
        config=GenerateConfig(temperature=1.0, max_tokens=48000),
    )


@task
def surveillance_benign(judge: str | None = None) -> Task:
    return Task(
        dataset=MemoryDataset(_samples("benign.json", "benign"), name="surveillance-benign"),
        solver=generate(),
        scorer=benign_scorer(judge=judge),
        config=GenerateConfig(temperature=1.0, max_tokens=48000),
    )
