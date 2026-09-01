#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil, hashlib, csv, datetime

def sha256(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(description='Archive selection decision evidence into a formal Competition Repo; never auto-promote guesses into FACTS.')
    ap.add_argument('--selection',required=True); ap.add_argument('--repo',required=True); a=ap.parse_args()
    src=Path(a.selection).resolve(); repo=Path(a.repo).resolve()
    if not (repo/'problem/FACTS.md').exists(): raise SystemExit('repo missing problem/FACTS.md')
    target=repo/'audit/selection'; target.mkdir(parents=True,exist_ok=True); copied=[]
    for name in ['SELECTION_STATUS.md','PROBLEM_CARDS.md','ROUTE_CARDS.md','PROBE_LEDGER.csv','DECISION.md']:
        p=src/name
        if p.exists():
            q=target/name; shutil.copy2(p,q); copied.append((name,sha256(q)))
    with (target/'PROMOTION_MANIFEST.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f); w.writerow(['file','sha256']); w.writerows(copied)
    (repo/'problem/SELECTION_HANDOFF.md').write_text(
        '# Selection Handoff\n\nSelection evidence archived at `audit/selection/`.\n\n'
        '**No facts were automatically promoted.** Confirm adopted facts against original statement/attachments/official sources before writing `FACTS.md`. '
        'Probe outputs become formal evidence only after reproducible replay inside the Competition Repo.\n\n'
        f'Promotion time: {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n',encoding='utf-8')
    print(f'SELECTION_PROMOTION_PASS: {len(copied)} evidence files archived; zero automatic FACT promotion')
if __name__=='__main__': main()
