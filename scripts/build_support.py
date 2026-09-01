#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def sha(p):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser(description='Build an explicit support ZIP. Defaults to source code; add other evidence with --include.')
 ap.add_argument('--out',default='results/final/submission/support.zip')
 ap.add_argument('--include',action='append',default=[])
 args=ap.parse_args()
 roots=['src']+args.include
 aip=ROOT/'ai/AI工具使用详情.pdf'
 if aip.exists(): roots.append('ai/AI工具使用详情.pdf')
 files=[]
 for rel in roots:
  p=ROOT/rel
  if not p.exists():continue
  if p.is_file():files.append((p,p.relative_to(ROOT)))
  else:
   for f in sorted(p.rglob('*')):
    if f.is_file() and '.git' not in f.parts and '__pycache__' not in f.parts and '_template' not in f.parts and f.name != '.gitkeep' and not f.name.endswith(('.pyc','.pyo')):
     files.append((f,f.relative_to(ROOT)))
 # dedupe
 seen=set(); uniq=[]
 for f,r in files:
  key=str(r).replace('\\','/')
  if key not in seen:seen.add(key);uniq.append((f,r))
 out=ROOT/args.out if not Path(args.out).is_absolute() else Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  for f,r in uniq:z.write(f,str(r).replace('\\','/'))
 man=ROOT/'audit/SUPPORT_MANIFEST.csv'
 with man.open('w',encoding='utf-8-sig',newline='') as fp:
  w=csv.writer(fp);w.writerow(['path','sha256','size_bytes','reason'])
  for f,r in uniq:w.writerow([str(r).replace('\\','/'),sha(f),f.stat().st_size,'support'])
 print(f'WROTE {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out} files={len(uniq)} bytes={out.stat().st_size}')
if __name__=='__main__':main()
