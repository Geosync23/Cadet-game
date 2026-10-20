# clash_kinds.py (split rehearsal SX1): what were the real clashes, once the build number is out of the way?
# For each merge the sweep found still clashing (sweep.py --norm-build), merge the whole game file with git's diff3
# style and sort every clash:
#   add/add  - both sides only ADDED lines at the same spot (the base part is empty): what labelled per-seat slots
#              (SR2's option d) would have avoided; the split avoids it only if the two additions land in different pieces
#   edit     - at least one side changed or removed existing lines: the same code touched twice; nothing mechanical avoids it
#   and, for add/add, whether the real merge kept both (in either order): a "keep both" a slot would have done for free
#   python3 plans/split-rehearsal/clash_kinds.py SWEEP_NORM.json
import sys, os, json, re, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
import sweep as W

def git(*a):
    r = subprocess.run(['git', '-C', SRC] + list(a), capture_output=True)
    return r.stdout if r.returncode == 0 else None

def norm(d, bl): return W.set_build(d, bl)

def main(argv):
    res = json.load(open(argv[0]))
    cl = [r for r in res if r.get('whole_clashes')]
    tot = {'add/add': 0, 'add/add kept both': 0, 'edit': 0, 'generated words': 0}
    per = []
    with tempfile.TemporaryDirectory() as t:
        for r in cl:
            m = git('rev-parse', r['m']).decode().strip()
            p1, p2 = git('log', '-1', '--format=%P', m).decode().split()
            mb = git('merge-base', p1, p2).decode().split()[0]
            base, o, th, real = (git('show', f'{c}:starship-cadet.html') for c in (mb, p1, p2, m))
            bl = W.build_lines(base)
            o, th, real = norm(o, bl), norm(th, bl), norm(real, bl)
            fs = []
            for k, x in (('o', o), ('b', base), ('t', th)):
                p = os.path.join(t, k); open(p, 'wb').write(x); fs.append(p)
            out = subprocess.run(['git', 'merge-file', '--diff3', '-p', *fs], capture_output=True).stdout
            hunks = re.findall(rb'^<<<<<<< [^\n]*\n(.*?)^\|\|\|\|\|\|\| [^\n]*\n(.*?)^=======\n(.*?)^>>>>>>> [^\n]*\n', out, re.S | re.M)
            k = {'add/add': 0, 'add/add kept both': 0, 'edit': 0, 'generated words': 0}
            # where the generated words block sits in the merged output (clashes there are fixed by re-running content_gen)
            gb = out.find(b'// ---- BEGIN LINES'); ge = out.find(b'// ---- END TRADITIONS ----')
            pos = 0
            for h in hunks:
                ours, b, theirs = h
                at = out.find(b'<<<<<<< ', pos); pos = at + 1
                if gb >= 0 and gb < at < ge: k['generated words'] += 1; continue
                if b.strip() == b'':
                    k['add/add'] += 1
                    if (ours + theirs) in real or (theirs + ours) in real: k['add/add kept both'] += 1
                else: k['edit'] += 1
            for x in k: tot[x] += k[x]
            per.append((r['m'], k))
    n = sum(tot[x] for x in ('add/add', 'edit', 'generated words'))
    print(f'{len(cl)} merges still clashing with the build number out of the way; {n} clashes in all')
    for x, v in tot.items(): print(f'  {x}: {v}')
    merges_only_add = sum(1 for _, k in per if k['edit'] == 0 and k['generated words'] == 0)
    print(f'  merges whose every clash was add/add (slots would have made them clean): {merges_only_add} of {len(cl)}')
    json.dump(per, open(argv[0].replace('.json', '-kinds.json'), 'w'))

if __name__ == '__main__':
    main(sys.argv[1:])
