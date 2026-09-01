#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
if (ROOT/'VERSION').read_text(encoding='utf-8').strip()!='0.1.1': errors.append('VERSION != 0.1.1')
if '# Competition Repository Template v0.1.1' not in (ROOT/'README.md').read_text(encoding='utf-8'): errors.append('README version mismatch')
for rel in ['DESIGN_GUARDRAILS.md','scripts/contest_import.py','problem/SOURCE_MANIFEST.csv','problem/PREFLIGHT_REPORT.md','scripts/add_question.py','scripts/new_run.py','scripts/validate_repo.py']:
    if not (ROOT/rel).exists(): errors.append('missing '+rel)
# no fixed q1-q4 scaffolds
for base in ['models','src','paper/latex/sections/questions','paper/word/questions']:
    p=ROOT/base
    if p.exists():
        bad=[x for x in p.iterdir() if x.name.lower() in {'q1','q2','q3','q4','q1.tex','q2.tex','q3.tex','q4.tex','q1.md','q2.md','q3.md','q4.md'}]
        if bad: errors.append(f'fixed question scaffold in {base}: {bad}')
if 'State over Stage' not in (ROOT/'DESIGN_GUARDRAILS.md').read_text(encoding='utf-8'): errors.append('State-over-Stage guardrail missing')
if errors:
    print('TEMPLATE_VALIDATION_FAIL'); [print('-',e) for e in errors]; sys.exit(1)
print('TEMPLATE_VALIDATION_PASS: dynamic questions + preflight + state-first guardrails')
