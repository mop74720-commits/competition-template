#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

CODE_EXTS={'.py','.m','.r','.R','.jl','.ipynb','.cpp','.cc','.c','.h','.hpp','.java','.scala','.sh','.ps1'}

def load_profile():
    p=ROOT/'rules/RULE_PROFILE.json'
    if not p.exists(): return None
    try:return json.loads(p.read_text(encoding='utf-8'))
    except Exception:return None

def pdf_text_pages(path:Path):
    try:
        from pypdf import PdfReader
        rd=PdfReader(str(path))
        return rd, [(pg.extract_text() or '') for pg in rd.pages]
    except Exception:
        return None, []

def check_pdf_paper(path:Path, pr:dict, E:list[str], W:list[str]):
    rd,pages=pdf_text_pages(path)
    if rd is None:
        W.append('PDF structural checks skipped: pypdf unavailable or PDF unreadable')
        return
    expected=(pr.get('page_size') or '').upper()
    if expected=='A4':
        target=(595.276,841.890); tol=6.0
        bad=[]
        for i,pg in enumerate(rd.pages,1):
            w=float(pg.mediabox.width); h=float(pg.mediabox.height)
            ok=(abs(w-target[0])<=tol and abs(h-target[1])<=tol) or (abs(h-target[0])<=tol and abs(w-target[1])<=tol)
            if not ok: bad.append((i,round(w,1),round(h,1)))
        if bad:E.append('paper page size is not A4 on pages: '+', '.join(f'{i}({w}x{h}pt)' for i,w,h in bad[:8]))
    if pr.get('first_page_abstract') is True:
        t=(pages[0] if pages else '').replace(' ','')
        if '摘要' not in t:E.append('first page does not appear to be the required abstract page')
    if pr.get('appendix_source_code_required') is True:
        alltxt='\n'.join(pages)
        if '附录' not in alltxt:E.append('paper appendix required but no appendix marker found in PDF text')
        if not re.search(r'\.(?:py|m|R|r|jl|ipynb|cpp|c|java)\b', alltxt):
            E.append('paper appendix requires source code, but no source-code filename marker was found')

def inspect_support(path:Path, sr:dict, ar:dict, E:list[str], W:list[str]):
    if path.suffix.lower()!='.zip':
        if sr.get('source_code_required') or ar.get('details_pdf_required'):
            W.append('support content inspection only implemented for ZIP; inspect RAR manually')
        return
    try:
        with zipfile.ZipFile(path) as z:
            names=[n.replace('\\','/') for n in z.namelist() if not n.endswith('/')]
    except Exception as ex:
        E.append(f'support ZIP unreadable: {ex}'); return
    if sr.get('source_code_required') is True and not any(Path(n).suffix in CODE_EXTS for n in names):
        E.append('support archive requires runnable source code but no recognized source file was found')
    if ar.get('ai_used') is True and ar.get('details_pdf_required') is True:
        fn=ar.get('details_filename') or 'AI工具使用详情.pdf'
        if not any(Path(n).name==fn for n in names):E.append(f'support archive missing required AI details PDF: {fn}')

def main():
    ap=argparse.ArgumentParser(description='Pre-submission hard check. Unlike validate_repo.py, official rules are mandatory here.')
    ap.add_argument('--paper',default='')
    ap.add_argument('--support',default='')
    args=ap.parse_args(); E=[]; W=[]
    prof=load_profile()
    if not prof: E.append('missing/unreadable rules/RULE_PROFILE.json')
    else:
        if prof.get('schema')!='mathmodel-competition-rules/v1': E.append('rule profile schema mismatch')
        if not prof.get('verified'): E.append('official rules are not verified')
        if not prof.get('contest') or not prof.get('season'): E.append('contest/season missing in rule profile')
        if not prof.get('sources'): E.append('no official rule source recorded')
        blocking={str(x) for x in (prof.get('blocking_unknowns') or [])}
        for u in prof.get('unknowns') or []:
            if str(u) not in blocking: W.append('rule unknown: '+str(u))
        for u in prof.get('blocking_unknowns') or []: E.append('blocking rule/compliance unknown: '+str(u))
    req=(prof or {}).get('requirements',{}); pr=req.get('paper',{}) or {}; sr=req.get('support',{}) or {}; ar=req.get('ai',{}) or {}
    paper=Path(args.paper) if args.paper else None
    if paper:
        if not paper.is_absolute(): paper=ROOT/paper
        if not paper.exists(): E.append(f'paper missing: {paper}')
        else:
            allowed=[x.lower() for x in pr.get('allowed_extensions') or []]
            if allowed and paper.suffix.lower() not in allowed:E.append(f'paper extension {paper.suffix} not allowed: {allowed}')
            mx=pr.get('max_size_mb')
            if mx and paper.stat().st_size>float(mx)*1024*1024:E.append(f'paper exceeds {mx} MB')
            if paper.suffix.lower()=='.pdf':check_pdf_paper(paper,pr,E,W)
    elif pr:
        E.append('paper rules exist but --paper not provided')
    support=Path(args.support) if args.support else None
    if sr.get('required') is True:
        if not support:E.append('support archive required but --support not provided')
        else:
            if not support.is_absolute():support=ROOT/support
            if not support.exists():E.append(f'support archive missing: {support}')
            else:
                allowed=[x.lower() for x in sr.get('allowed_extensions') or []]
                if allowed and support.suffix.lower() not in allowed:E.append(f'support extension {support.suffix} not allowed: {allowed}')
                mx=sr.get('max_size_mb')
                if mx and support.stat().st_size>float(mx)*1024*1024:E.append(f'support exceeds {mx} MB')
                inspect_support(support,sr,ar,E,W)
    if ar.get('ai_used') is True and ar.get('details_pdf_required') is True:
        fn=ar.get('details_filename') or 'AI工具使用详情.pdf'
        if not (ROOT/'ai'/fn).exists():E.append(f'AI details PDF required but missing: ai/{fn}')
        log=ROOT/'ai/AI_USAGE_LOG.md'
        if not log.exists() or len([ln for ln in log.read_text(encoding='utf-8').splitlines() if ln.startswith('|')])<=2:E.append('AI use is declared but AI_USAGE_LOG has no evidence rows')
    print(f'errors={len(E)} warnings={len(W)}')
    for x in E:print('ERROR',x)
    for x in W:print('WARN ',x)
    if E:raise SystemExit(1)
if __name__=='__main__':main()
