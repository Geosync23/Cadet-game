# ours_then_theirs.py FILE : every conflict block -> our lines, then their lines (both sides only added)
import sys, pathlib
p = pathlib.Path(sys.argv[1]); L = p.read_text().split('\n'); out = []; i = 0; n = 0
while i < len(L):
    if L[i].startswith('<<<<<<< '):
        m = next(j for j in range(i, len(L)) if L[j] == '======='); e = next(j for j in range(m, len(L)) if L[j].startswith('>>>>>>> '))
        out += L[i+1:m] + L[m+1:e]; i = e + 1; n += 1
    else: out.append(L[i]); i += 1
p.write_text('\n'.join(out)); print(sys.argv[1], 'blocks', n)
