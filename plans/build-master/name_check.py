# name_check.py HTML: duplicate top-level function / const / let / var names in the game script
import re, sys, collections
s = open(sys.argv[1]).read()
c = collections.Counter()
for m in re.finditer(r'^(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(|^(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=', s, re.M):
    c[m.group(1) or m.group(2)] += 1
d = {k: v for k, v in c.items() if v > 1}
print('NAMES OK' if not d else 'DUPLICATES ' + ', '.join(f'{k} x{v}' for k, v in sorted(d.items())), f'({len(c)} names)')
