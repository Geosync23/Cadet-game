#!/usr/bin/env python3
"""near_dupes.py BRANCH FILE: lines new in FILE on BRANCH (vs claude/integration) that already appear elsewhere in content/,
exactly or nearly (difflib, 0.82). Covers script lines, replies, asks, hints and "// IF" comment lines. The crew stories' editor's check (CS1).
Run from the repo root after "git fetch origin claude/integration". ALL=1 checks every line, not only new ones."""
import subprocess,sys,re,os,difflib
br,f=sys.argv[1],sys.argv[2]
new=subprocess.run(['git','show',f'{br}:{f}'],capture_output=True,text=True).stdout
try: old=subprocess.run(['git','show',f'origin/claude/integration:{f}'],capture_output=True,text=True,check=True).stdout
except Exception: old=''
oldset=set() if os.environ.get("ALL") else set(old.splitlines())
def text(l):
    l=l.strip()
    m=re.match(r'//\s*IF [^:]+(?::[^:]+)*?:\s*([\w-]+):\s*(.*)',l)
    if l.startswith('// IF'):
        m=re.match(r'//\s*IF .*?:\s*([a-z-]+|them|you):\s*(.*)',l)
        return m.group(2) if m else None
    m=re.match(r'^\s*(?:\+\s*)?(?:[a-z-]+):\s*(.*)',l)
    if m and not re.match(r'^(tone|tier|gapDays|duty|where|when|hint|mem|flag|mail|keepsake|learn|metDays|who|crisis)\b',l): return m.group(1)
    m=re.match(r'^\*\s*(.*?)\s{2,}flavour',l)
    if m: return m.group(1)
    if l.startswith('hint:'): return l[5:]
    return None
def norm(s): return re.sub(r'\[.*?\]','',re.sub(r'\s+',' ',s)).strip().lower().rstrip('.!?')
corpus={}
for root,_,fs in os.walk('content'):
    for x in fs:
        p=os.path.join(root,x)
        if os.path.normpath(p)==os.path.normpath(f) or x=='outlines.md': continue
        for i,l in enumerate(open(p,errors='ignore')):
            t=re.sub(r'^[^:]*:\s*','',l.strip()) if ':' in l[:40] else l.strip().lstrip('- ')
            n=norm(t)
            if len(n)>12: corpus.setdefault(n,[]).append(f'{p}:{i+1}')
keys=list(corpus)
for l in new.splitlines():
    if l in oldset: continue
    t=text(l)
    if not t: continue
    n=norm(t)
    if len(n)<=12: continue
    if n in corpus: print('EXACT',repr(t),corpus[n][:2]); continue
    for k in difflib.get_close_matches(n,keys,n=1,cutoff=0.82):
        print('NEAR ',repr(t),'~',corpus[k][:1])
print('done')
