#!/usr/bin/env python3
from pathlib import Path
import sys, tempfile, subprocess
ROOT=Path(__file__).resolve().parents[1]; errors=[]
if (ROOT/'VERSION').read_text(encoding='utf-8').strip()!='0.2.0': errors.append('VERSION != 0.2.0')
if '# Competition Workspace Factory v0.2.0' not in (ROOT/'README.md').read_text(encoding='utf-8'): errors.append('README version/title mismatch')
required=['DESIGN_GUARDRAILS.md','scripts/contest_import.py','problem/SOURCE_MANIFEST.csv','problem/PREFLIGHT_REPORT.md','scripts/add_question.py','scripts/new_run.py','scripts/validate_repo.py','rules/OFFICIAL_RULES.md','rules/RULE_PROFILE.json','scripts/validate_submission.py','scripts/build_support.py','audit/SUBMISSION_MANIFEST.csv','audit/SUPPORT_MANIFEST.csv','ai/AI_USAGE_DETAILS_TEMPLATE.md','workspace_templates/selection/SELECTION_STATUS.md','workspace_templates/selection/PROBLEM_CARDS.md','workspace_templates/selection/ROUTE_CARDS.md','workspace_templates/selection/PROBE_LEDGER.csv','workspace_templates/selection/DECISION.md','scripts/new_selection_workspace.py','scripts/validate_selection.py','scripts/promote_selection.py']
for rel in required:
    if not (ROOT/rel).exists(): errors.append('missing '+rel)
for base in ['models','src','paper/latex/sections/questions','paper/word/questions']:
    p=ROOT/base
    if p.exists():
        bad=[x for x in p.iterdir() if x.name.lower() in {'q1','q2','q3','q4','q1.tex','q2.tex','q3.tex','q4.tex','q1.md','q2.md','q3.md','q4.md'}]
        if bad: errors.append('fixed question scaffold in '+base)
guard=(ROOT/'DESIGN_GUARDRAILS.md').read_text(encoding='utf-8')
for phrase in ['State over Stage','Selection is exploratory; Competition Repo is formal','Information gain over exhaustive scoring']:
    if phrase not in guard: errors.append('guardrail missing '+phrase)
sub=(ROOT/'scripts/validate_submission.py').read_text(encoding='utf-8')
for phrase in ['blocking_unknowns','page_size','first_page_abstract','source_code_required','details_pdf_required']:
    if phrase not in sub: errors.append('submission validator missing '+phrase)
if not errors:
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'sel'
        r=subprocess.run([sys.executable,str(ROOT/'scripts/new_selection_workspace.py'),'--output',str(out),'--candidate','A','--candidate','B'],capture_output=True,text=True)
        if r.returncode: errors.append('selection creator failed: '+r.stderr.strip())
        else:
            v=subprocess.run([sys.executable,str(ROOT/'scripts/validate_selection.py'),'--root',str(out)],capture_output=True,text=True)
            if v.returncode: errors.append('selection validator failed: '+v.stdout+v.stderr)
if errors:
    print('TEMPLATE_VALIDATION_FAIL'); [print('-',e) for e in errors]; sys.exit(1)
print('TEMPLATE_VALIDATION_PASS: formal repo + optional selection workspace + no automatic fact promotion + official-rules closure')
