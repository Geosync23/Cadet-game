# Bytes of the game file by section, raw and gzipped, plus the biggest single lines (generated data)
import sys, re, gzip, subprocess
f = sys.argv[1] if len(sys.argv) > 1 else 'starship-cadet.html'
L = open(f, encoding='utf-8').read().split('\n')
sec = subprocess.run(['python3', 'tools/section.py'], capture_output=True, text=True).stdout
S = [(m[1], int(m[2]), int(m[3])) for m in (re.match(r'\s*(\S+)\s+(\d+)-(\d+)', l) for l in sec.splitlines()) if m]
raw = '\n'.join(L).encode(); print(f'file {len(raw)/1e6:.2f} MB, gzip {len(gzip.compress(raw, 9))/1e6:.2f} MB, {len(L)} lines')
rows = []
for n, a, b in S:
    t = '\n'.join(L[a-1:b]).encode(); rows.append((len(t), len(gzip.compress(t, 9)), n))
for r, z, n in sorted(rows, reverse=True)[:14]: print(f'  {n:5} {r/1e6:6.2f} MB raw  {z/1e6:5.2f} MB gz  {100*r/len(raw):4.1f}%')
big = sorted(((len(l), i+1) for i, l in enumerate(L)), reverse=True)[:12]
for n, i in big: print(f'  line {i}: {n/1e3:.0f} kB  {L[i-1][:90]!r}')
