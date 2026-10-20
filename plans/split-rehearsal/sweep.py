# sweep.py (split rehearsal SX1): for every two-parent merge in the repo, does git merge the pieces the same way
# it merges the whole game file? For each merge: cut base, ours and theirs with the same ORDER (the pieces all three
# have), merge each piece with git merge-file, and compare with git merge-file on the whole file:
#   both clean   -> are the glued pieces byte-identical to the whole-file merge?
#   clashes      -> how many in the whole file, how many in pieces, and which pieces
#   and, for clean merges, is the result identical to the real merge commit's game file (hand edits aside)?
#   python3 plans/split-rehearsal/sweep.py OUT.json [--since=2026-10-01]
import sys, os, subprocess, json, re, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, SRC)
import split as S
FULL = S.read_order(open(os.path.join(SRC, 'pieces/ORDER'), encoding='utf-8').read())

def git(*a):
    r = subprocess.run(['git', '-C', SRC] + list(a), capture_output=True)
    return r.stdout if r.returncode == 0 else None

def common_order(*datas):
    keep = [FULL[0]]
    for e in FULL[1:]:
        name, pick, back, rx = e
        ok = True
        for d in datas:
            n = sum(1 for l in d.split(b'\n') if rx.search(l))
            if n == 0 or (pick == 'once' and n != 1): ok = False
        if ok: keep.append(e)
    return keep

NORM = '--norm-build' in sys.argv
BRX = [re.compile(rb'^   STARSHIP CADET: .*build [0-9.]+.*$', re.M), re.compile(rb"^const GAME_BUILD = .*$", re.M)]
def build_lines(d):
    return [(m.group(0) if m else None) for m in (rx.search(d) for rx in BRX)]
def set_build(d, bl):
    for rx, l in zip(BRX, bl):
        if l is not None: d = rx.sub(lambda m: l, d, count=1)
    return d

def mf(t, o, b, th):
    fs = []
    for k, x in (('o', o), ('b', b), ('t', th)):
        p = os.path.join(t, k); open(p, 'wb').write(x); fs.append(p)
    r = subprocess.run(['git', 'merge-file', '-p', *fs], capture_output=True)
    return r.returncode, r.stdout

def main(argv):
    out = argv[0]; since = '2026-09-01'
    for a in argv:
        if a.startswith('--since='): since = a.split('=', 1)[1]
    merges = git('rev-list', '--merges', '--remotes=origin', f'--since={since}').decode().split()
    res = []
    with tempfile.TemporaryDirectory() as t:
        for m in merges:
            ps = git('log', '-1', '--format=%P', m).decode().split()
            if len(ps) != 2: continue
            mb = git('merge-base', ps[0], ps[1])
            if not mb: continue
            mb = mb.decode().split()[0]
            fs = [git('show', f'{c}:starship-cadet.html') for c in (mb, ps[0], ps[1], m)]
            if any(f is None for f in fs): continue
            base, ours, theirs, real = fs
            if NORM:   # S6: helpers don't bump the build number; give both sides the base's build lines
                bl = build_lines(base)
                ours, theirs, real = (set_build(x, bl) for x in (ours, theirs, real))
            if ours == theirs or base == theirs or base == ours: kind = 'one-sided'
            else: kind = 'both'
            rec = {'m': m[:8], 'kind': kind}
            if kind == 'one-sided': res.append(rec); continue
            try:
                order = common_order(base, ours, theirs)
                pb, po, pt = (S.split(x, order) for x in (base, ours, theirs))
            except S.SplitError as e:
                rec['split_error'] = str(e); res.append(rec); continue
            wrc, whole = mf(t, ours, base, theirs)
            prc, glued, clashed = 0, b'', {}
            for (n, b), (_, o), (_, th) in zip(pb, po, pt):
                rc, x = mf(t, o, b, th)
                glued += x
                if rc: clashed[n] = rc; prc += rc
            rec.update(whole_clashes=wrc, piece_clashes=prc, pieces=clashed, pieces_n=len(order))
            if wrc == 0 and prc == 0:
                rec['same_as_whole'] = glued == whole
                rec['whole_equals_real'] = whole == real
            elif wrc == 0 or prc == 0:
                rec['MISMATCH'] = True
            res.append(rec)
    json.dump(res, open(out, 'w'), indent=0)
    both = [r for r in res if r['kind'] == 'both' and 'split_error' not in r]
    clean = [r for r in both if r.get('whole_clashes') == 0 and r.get('piece_clashes') == 0]
    cl = [r for r in both if r.get('whole_clashes') and r.get('piece_clashes')]
    print(f'{len(res)} merges; {len(res) - len(both)} one-sided or unsplittable; {len(both)} with game changes on both sides')
    print(f'  clean both ways: {len(clean)}; pieces identical to whole-file merge: {sum(r["same_as_whole"] for r in clean)}')
    print(f'  clashed both ways: {len(cl)}; same clash count: {sum(r["whole_clashes"] == r["piece_clashes"] for r in cl)}')
    print(f'  clashed one way only: {[r for r in both if r.get("MISMATCH")]}')
    print(f'  split errors: {[(r["m"], r["split_error"]) for r in res if "split_error" in r]}')
    diffcl = [r for r in cl if r['whole_clashes'] != r['piece_clashes']]
    for r in diffcl: print('  clash count differs:', r)
    bl = sum(1 for r in cl if set(r['pieces']) <= {'js/s01-setup-materials.js', 'js/s13-time-save.js'})
    print(f'  clashed merges whose only clashes were in the two build-number pieces: {bl} of {len(cl)}')

if __name__ == '__main__':
    main(sys.argv[1:])
