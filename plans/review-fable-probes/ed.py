# ed.py FILE EDITS.json: exact-string edits, each must match exactly once (FR2's helper; small edits, never a rewrite)
import sys, json
f = sys.argv[1]; s = open(f, encoding='utf-8').read()
for old, new in json.load(open(sys.argv[2], encoding='utf-8')):
    n = s.count(old)
    if n != 1: sys.exit(f'NOT APPLIED: {n} matches for: {old[:90]!r}')
    s = s.replace(old, new, 1)
open(f, 'w', encoding='utf-8').write(s); print('ok', f)
