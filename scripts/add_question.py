#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import re

ROOT = Path(__file__).resolve().parents[1]

def valid_name(s: str) -> str:
    s = s.strip()
    if not re.fullmatch(r"[A-Za-z0-9._-]+", s):
        raise argparse.ArgumentTypeError("question name may contain only letters, digits, . _ -")
    return s

def main():
    ap = argparse.ArgumentParser(description="Create directories for one actual contest question. This does not impose solve order.")
    ap.add_argument("question", type=valid_name)
    ap.add_argument("--paper-track", choices=["none","latex","word"], default="none")
    args = ap.parse_args()
    q = args.question

    targets = [ROOT / "models" / q, ROOT / "src" / q, ROOT / "results" / q, ROOT / "figures" / q]
    for d in targets:
        d.mkdir(parents=True, exist_ok=True)

    contract = ROOT / "models" / q / "METHOD_CONTRACT.md"
    if not contract.exists():
        text = (ROOT / "models" / "_template" / "METHOD_CONTRACT.md").read_text(encoding="utf-8")
        contract.write_text(text.replace("<question>", q), encoding="utf-8")

    readme = ROOT / "src" / q / "README.md"
    if not readme.exists():
        readme.write_text(f"# {q} source\n\nRecord the runnable entry point here.\n", encoding="utf-8")

    if args.paper_track == "latex":
        dst = ROOT / "paper" / "latex" / "sections" / "questions" / f"{q}.tex"
        if not dst.exists():
            text = (ROOT / "paper" / "latex" / "question_template.tex").read_text(encoding="utf-8")
            dst.write_text(text.replace("<QUESTION>", q), encoding="utf-8")
        print(f"Created {dst.relative_to(ROOT)}. Add \\input{{sections/questions/{q}}} to paper/latex/main.tex when desired.")
    elif args.paper_track == "word":
        dst = ROOT / "paper" / "word" / "questions" / f"{q}.md"
        if not dst.exists():
            text = (ROOT / "paper" / "word" / "question_template.md").read_text(encoding="utf-8")
            dst.write_text(text.replace("<QUESTION>", q), encoding="utf-8")
        print(f"Created {dst.relative_to(ROOT)}. Merge/include it in the active Word manuscript when desired.")

    print(f"Question scaffold ready: {q}")
    print("Reminder: add/update its row in problem/QUESTION_MAP.md and PROJECT_STATUS.md only when useful.")

if __name__ == "__main__":
    main()
