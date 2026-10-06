#!/usr/bin/env python3
"""Build sketches.html -- the scenario candidate viewer.

    uv run python build_sketches.py

Designed to stay readable at 100+ sketches: axis filters, search, and a coverage
matrix spanning both sketched and already-built scenarios so an empty cell means
nobody has written that scenario yet.
"""
from __future__ import annotations
import datetime, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from sketch_content import AXES, SKETCHES, REJECTED, BUILT_AXES
from activity_content import ACTIVITIES, UPLIFT_ORDER
from world_content import WORLDS, AXES as WORLD_AXES, INSTRUMENTS

TEMPLATE = ROOT / "sketch_template.html"
OUT = ROOT / "sketches.html"
DATA = ROOT / "src" / "surveil" / "data"


def built_rows() -> list[dict]:
    out = []
    for f in ("harmful.json", "benign.json"):
        p = DATA / f
        if not p.exists():
            continue
        for r in json.loads(p.read_text()):
            if r["id"] not in BUILT_AXES:
                continue
            out.append({"id": r["id"], "title": (r.get("lever") or r.get("surface") or ""),
                        "status": "built", "axes": BUILT_AXES[r["id"]]})
    return out


def main() -> None:
    payload = {
        "built": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "axes": AXES,
        "activities": ACTIVITIES,
        "worlds": WORLDS,
        "world_axes": WORLD_AXES,
        "instruments": INSTRUMENTS,
        "uplift_order": UPLIFT_ORDER,
        "sketches": SKETCHES,
        "built_scenarios": built_rows(),
        "rejected": [{"title": a, "why": b} for a, b in REJECTED],
    }
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    OUT.write_text(TEMPLATE.read_text().replace("__DATA__", data, 1))
    nb = len(payload["built_scenarios"])
    print(f"Wrote {OUT}")
    cites = sum(len(a["history"]) for a in ACTIVITIES)
    rungs = sum(len(w["ladder"]) for w in WORLDS)
    print(f"  {len(WORLDS)} worlds -> {rungs} rungs (scenario instances), "
          f"{len(set(w['activity'] for w in WORLDS))}/{len(ACTIVITIES)} activities covered")
    print(f"  {len(ACTIVITIES)} activities ({cites} historical citations), {len(SKETCHES)} sketches, "
          f"{nb} built scenarios on the matrix, {len(REJECTED)} rejected")
    # report empty cells so the generation plan is visible from the CLI too
    roles = list(AXES["model_role"]["values"])
    safes = list(AXES["safeguard"]["values"])
    filled = {(s["axes"]["model_role"], s["axes"]["safeguard"]) for s in SKETCHES}
    filled |= {(b["axes"]["model_role"], b["axes"]["safeguard"]) for b in payload["built_scenarios"]}
    empty = [(r, s) for r in roles for s in safes if (r, s) not in filled]
    print(f"  coverage: {len(filled)}/{len(roles)*len(safes)} role x safeguard cells filled, {len(empty)} empty")


if __name__ == "__main__":
    main()
