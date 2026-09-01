#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_csv(path: Path):
    if not path.exists(): return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def main():
    ap = argparse.ArgumentParser(description="Lightweight repository consistency check. Warnings are advisory unless --strict.")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    warnings, errors = [], []

    required = ["PROJECT_STATUS.md","problem/FACTS.md","problem/QUESTION_MAP.md","runs/RUN_LEDGER.csv","audit/CLAIM_EVIDENCE_MAP.csv"]
    for rel in required:
        if not (ROOT / rel).exists(): errors.append(f"missing: {rel}")

    ledger = load_csv(ROOT / "runs/RUN_LEDGER.csv")
    ids = [r.get("run_id", "") for r in ledger if r.get("run_id")]
    if len(ids) != len(set(ids)): errors.append("duplicate run_id in RUN_LEDGER.csv")

    final_rows = load_csv(ROOT / "runs/FINAL_RUNS.csv")
    byq = {}
    for r in final_rows:
        q = r.get("question", "").strip()
        rid = r.get("run_id", "").strip()
        if not q or not rid: continue
        if q in byq: errors.append(f"multiple FINAL runs selected for {q}: {byq[q]}, {rid}")
        byq[q] = rid
        if rid not in ids: warnings.append(f"FINAL run {rid} for {q} not found in RUN_LEDGER.csv")
        rp = r.get("result_path", "").strip()
        if rp and not (ROOT / rp).exists(): warnings.append(f"FINAL result path missing: {rp}")

    source_manifest = load_csv(ROOT / "problem/SOURCE_MANIFEST.csv")
    for r in source_manifest:
        rel=(r.get("relative_path") or "").strip()
        if rel and not Path(rel).is_absolute() and not (ROOT/rel).exists():
            warnings.append(f"source manifest path missing: {rel}")

    claims = load_csv(ROOT / "audit/CLAIM_EVIDENCE_MAP.csv")
    for r in claims:
        status = (r.get("status") or "").strip().lower()
        claim = (r.get("claim") or "").strip()
        ev = (r.get("evidence_path") or "").strip()
        if claim and not ev and status not in {"draft","planned","open"}:
            warnings.append(f"claim without evidence_path: {r.get('claim_id','?')}")
        if ev and not (ROOT / ev).exists():
            warnings.append(f"claim evidence path missing: {ev}")

    print(f"errors={len(errors)} warnings={len(warnings)}")
    for x in errors: print("ERROR", x)
    for x in warnings: print("WARN ", x)
    if errors or (args.strict and warnings): raise SystemExit(1)

if __name__ == "__main__":
    main()
