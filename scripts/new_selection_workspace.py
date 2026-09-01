#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'workspace_templates'/'selection'

def problem_block(c):
    return "\n".join([
        f"## Candidate: {c}","",
        "- required deliverable:","- data / parameter reality:","- structural difficulty:",
        "- validation opportunity:","- engineering risk:","- paper expressibility:",
        "- team-fit dependency (soft signal):","- current decisive unknown:",
        "- strongest reason to choose:","- strongest reason to reject:",""])

def route_block(c):
    return "\n".join([
        f"## Candidate / Route: {c} / <route>","",
        "- deliverable:","- baseline_or_minimal_witness:","- primary_route:","- binding_constraints:",
        "- engineering_risk:","- deciding_probe:","- deciding_evidence_needed:",
        "- rejected_alternative (only if real competition exists):","- refutation_test:","- flip_condition:",
        "- fallback_trigger:","- fallback_action:","- judge_visible_evidence:",""])

def main():
    ap=argparse.ArgumentParser(description='Create an external temporary Selection Workspace.')
    ap.add_argument('--output',required=True)
    ap.add_argument('--candidate',action='append',default=[])
    args=ap.parse_args(); out=Path(args.output).expanduser().resolve()
    if out.exists() and any(out.iterdir()): raise SystemExit(f'output exists and is non-empty: {out}')
    shutil.copytree(SOURCE,out,dirs_exist_ok=True)
    if args.candidate:
        for c in args.candidate: (out/'problem_files'/c).mkdir(parents=True,exist_ok=True)
        (out/'PROBLEM_CARDS.md').write_text('# Problem Cards\n\n> 不要求固定分数，只记录当前足以影响选择的信息。\n\n'+'\n---\n\n'.join(problem_block(c) for c in args.candidate),encoding='utf-8')
        (out/'ROUTE_CARDS.md').write_text('# Route Cards\n\n'+'\n---\n\n'.join(route_block(c) for c in args.candidate)+'\n低不确定性时可以只保留 baseline + primary；不要为了形式制造多路线。\n',encoding='utf-8')
        st=(out/'SELECTION_STATUS.md').read_text(encoding='utf-8')
        st=st.replace('- \n\n## Current leading candidate / route',''.join(f'- {c}\n' for c in args.candidate)+'\n## Current leading candidate / route',1)
        (out/'SELECTION_STATUS.md').write_text(st,encoding='utf-8')
    print(f'SELECTION_WORKSPACE_CREATED: {out}')
if __name__=='__main__': main()
