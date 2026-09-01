#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, datetime as dt, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "runs" / "RUN_LEDGER.csv"

def git_value(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""

def next_id() -> str:
    maxn = 0
    if LEDGER.exists():
        with LEDGER.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                m = re.fullmatch(r"R(\d+)", row.get("run_id", ""))
                if m: maxn = max(maxn, int(m.group(1)))
    return f"R{maxn+1:03d}"

def main():
    ap = argparse.ArgumentParser(description="Create a traceable run record; use only for runs worth remembering.")
    ap.add_argument("--question", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--seed", default="")
    ap.add_argument("--status", default="planned")
    ap.add_argument("--notes", default="")
    args = ap.parse_args()

    run_id = next_id()
    stamp = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    branch = git_value("branch", "--show-current")
    commit = git_value("rev-parse", "HEAD")
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", f"{run_id}_{args.question}_{args.model}").strip("-")
    run_dir = ROOT / "runs" / slug
    run_dir.mkdir(parents=True, exist_ok=False)

    meta = {
        "run_id": run_id, "question": args.question, "model": args.model,
        "created_at": stamp, "branch": branch, "commit": commit,
        "seed": args.seed, "status": args.status, "notes": args.notes,
        "command": "", "input_snapshot": "", "config_path": "",
        "key_result": "", "result_path": "", "verification": "",
        "supersedes": ""
    }
    (run_dir / "run.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    tmpl = (ROOT / "runs" / "run_template.md").read_text(encoding="utf-8").replace("<RUN_ID>", run_id)
    (run_dir / "README.md").write_text(tmpl, encoding="utf-8")

    fields = ["run_id","question","created_at","branch","commit","model","status","seed","input_snapshot","config_path","key_result","result_path","verification","supersedes","notes"]
    exists = LEDGER.exists() and LEDGER.stat().st_size > 0
    with LEDGER.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if not exists: w.writeheader()
        w.writerow({k: meta.get(k, "") for k in fields})

    print(run_id)
    print(run_dir.relative_to(ROOT))

if __name__ == "__main__":
    main()
