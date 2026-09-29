#!/usr/bin/env python3
"""Summarise a log dir: structural tables to stdout, raw records to results/.

    uv run python report.py ./logs/run1
"""
import csv, json, pathlib, sys
from inspect_ai.log import list_eval_logs, read_eval_log

BUCKETS = {0:"full refusal",1:"refuse+redirect",2:"narrowed disclosed",
           3:"narrowed SILENT",4:"full compliance",5:"proactive enhancement"}
WILL = {0:"refused",1:"deflected",2:"held back",3:"engaged fully"}
QUAL = {0:"unusable",1:"weak",2:"flawed",3:"good",4:"correct"}
OUTCOMES = dict(WILL)  # legacy pre-split runs
TAGS = ["recognition","authority_check","scope_narrowing","minimization","retention_limit",
        "audit_logging","notice_and_appeal","disclosure","legitimate_preservation","scalability_check"]

log_dir = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "./logs/run1")
out_dir = pathlib.Path("results"); out_dir.mkdir(exist_ok=True)

rows, runs = [], []
for info in list_eval_logs(str(log_dir)):
    log = read_eval_log(info)
    metrics = {}
    if log.results:
        for sc in log.results.scores:
            for k, m in (sc.metrics or {}).items():
                if isinstance(m.value, dict):
                    for kk, vv in m.value.items(): metrics[f"{k}.{kk}"] = vv
                else: metrics[k] = m.value
    runs.append({"task": log.eval.task, "model": log.eval.model, "status": log.status,
                 "created": log.eval.created, "n": len(log.samples or []), "metrics": metrics})
    for s in (log.samples or []):
        sc = next(iter(s.scores.values())) if s.scores else None
        v = sc.value if sc and isinstance(sc.value, dict) else {}
        rows.append({
            "task": log.eval.task, "model": log.eval.model, "scenario": str(s.id), "epoch": s.epoch,
            "arm": "harmful" if "harmful" in log.eval.task else "benign",
            "bucket": v.get("bucket"), "willingness": v.get("willingness"),
            "task_quality": v.get("task_quality"), "outcome": v.get("outcome"),
            "delivered": v.get("delivered"), "overrefusal": v.get("overrefusal"),
            "moralizing": v.get("moralizing"),
            **{t: v.get(t) for t in TAGS},
            "judge": (sc.metadata or {}).get("judge") if sc else None,
            "rationale": (sc.explanation or "") if sc else "",
            "response": (s.output.completion or "") if s.output else "",
            "response_chars": len(s.output.completion or "") if s.output else 0,
            "error": str(s.error) if s.error else None,
        })

# ---- raw records ----
(out_dir / "results.json").write_text(json.dumps({"runs": runs, "rows": rows}, indent=2, ensure_ascii=False))
with (out_dir / "results.csv").open("w", newline="") as f:
    cols = [c for c in rows[0] if c not in ("response", "rationale")] if rows else []
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
tx = out_dir / "transcripts"; tx.mkdir(exist_ok=True)
for r in rows:
    m = r["model"].split("/")[-1]
    p = tx / f"{r['scenario']}__{m}__ep{r['epoch']}.md"
    p.write_text(f"# {r['scenario']} — {r['model']} (epoch {r['epoch']})\n\n"
                 f"- arm: {r['arm']}\n- bucket: {r['bucket']}  outcome: {r['outcome']}\n"
                 f"- delivered: {r['delivered']}  overrefusal: {r['overrefusal']}\n"
                 f"- judge: {r['judge']}\n\n## Judge rationale\n\n{r['rationale']}\n\n"
                 f"## Model response\n\n{r['response']}\n")

# ---- structural tables ----
def table(title, header, body):
    print(f"\n{title}")
    widths = [max(len(str(r[i])) for r in [header]+body) for i in range(len(header))]
    line = lambda r: "  ".join(str(c).ljust(w) for c, w in zip(r, widths))
    print(line(header)); print("  ".join("-"*w for w in widths))
    for r in body: print(line(r))

models = sorted({r["model"] for r in rows})
short = {m: m.split("/")[-1] for m in models}

print("=" * 96)
print(f"RUNS  ({log_dir})")
for r in runs:
    print(f"  {r['task']:22s} {r['model']:38s} {r['status']:8s} n={r['n']:<3} {r['created']}")

for arm, key, labels in (("harmful","bucket",BUCKETS), ("benign","willingness",WILL)):
    sub = [r for r in rows if r["arm"] == arm]
    if not sub: continue
    scen = sorted({r["scenario"] for r in sub})
    body = []
    for s in scen:
        cells = []
        for m in models:
            hit = [r for r in sub if r["scenario"] == s and r["model"] == m]
            if not hit or hit[0][key] is None:
                cells.append("-")
            elif arm == "benign":
                q = hit[0].get("task_quality")
                cells.append(f"w{hit[0][key]} {labels.get(hit[0][key],'?')}"
                             + (f" / q{q} {QUAL.get(q,'?')}" if q is not None and q >= 0 else ""))
            else:
                cells.append(f"{hit[0][key]} {labels.get(hit[0][key],'?')}")
        body.append([s] + cells)
    table(f"{arm.upper()} ARM — per scenario", ["scenario"] + [short[m] for m in models], body)

print()
for r in runs:
    print(f"\nMETRICS  {r['task']}  {r['model']}")
    for k, v in r["metrics"].items():
        print(f"  {k:34s} {v:.3f}" if isinstance(v, float) else f"  {k:34s} {v}")

print(f"\nWrote results/results.json, results/results.csv, results/transcripts/ ({len(rows)} files)")
