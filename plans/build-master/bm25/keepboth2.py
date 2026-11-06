# keepboth2.py FILE [BASE] (default: the merge base of HEAD and MERGE_HEAD) : table-row clashes: our rows, but a row we left as it was in BASE takes their newer copy;
# then their rows whose first cell isn't in ours
import sys, pathlib, subprocess
p = pathlib.Path(sys.argv[1]); L = p.read_text().split('\n')
mb = sys.argv[2] if len(sys.argv) > 2 else subprocess.run(['git', 'merge-base', 'HEAD', 'MERGE_HEAD'], capture_output=True, text=True).stdout.strip()
base = set(subprocess.run(['git', 'show', mb + ':' + sys.argv[1]], capture_output=True, text=True).stdout.split('\n'))
key = lambda r: r.split('|')[1].strip() if r.startswith('|') else r
while '<<<<<<< HEAD' in L:
    a = L.index('<<<<<<< HEAD'); m = L.index('=======', a); b = next(i for i in range(m, len(L)) if L[i].startswith('>>>>>>> '))
    ours, theirs = L[a+1:m], L[m+1:b]; tk = {key(t): t for t in theirs}; ok = {key(r) for r in ours}
    res = [tk[key(r)] if key(r) in tk and r in base and tk[key(r)] != r else r for r in ours]
    upd = sum(1 for x, y in zip(ours, res) if x != y)
    add = [t for t in theirs if key(t) not in ok]
    print(sys.argv[1], 'kept', len(ours), 'updated', upd, '+ added', [key(t)[:50] for t in add])
    L[a:b+1] = res + add
p.write_text('\n'.join(L))
