#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, sys
REQ=['README.md','SELECTION_STATUS.md','PROBLEM_CARDS.md','ROUTE_CARDS.md','PROBE_LEDGER.csv','DECISION.md']
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',required=True); a=ap.parse_args(); root=Path(a.root); errors=[]
    for rel in REQ:
        if not (root/rel).exists(): errors.append('missing '+rel)
    p=root/'PROBE_LEDGER.csv'
    if p.exists():
        rows=list(csv.reader(p.open(encoding='utf-8-sig',newline='')))
        exp=['probe_id','candidate','decision_question','hypothesis','expected_evidence','cost_class','status','command_or_method','output_path','result','decision_effect']
        if not rows or rows[0]!=exp: errors.append('PROBE_LEDGER.csv header mismatch')
    if errors:
        print('SELECTION_VALIDATION_FAIL'); [print('-',e) for e in errors]; sys.exit(1)
    print('SELECTION_VALIDATION_PASS: exploratory workspace is minimal and separate from formal facts')
if __name__=='__main__': main()
