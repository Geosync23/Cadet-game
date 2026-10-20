# replay.py (split rehearsal SX1): replay real past merges as if the game had been split before they happened.
#   python3 plans/split-rehearsal/replay.py WORKDIR SPLIT_COMMIT MERGE [MERGE ...] [--pre-split=COMMIT,...]
# 1. Clone this repo (shared objects) into WORKDIR.
# 2. Rewrite history from SPLIT_COMMIT on: every commit that descends from it and leads to a replayed merge gets the
#    pieces/ folder (its own game file cut with pieces/ORDER, keeping only the pieces whose headings exist then),
#    build.py, split.py and .gitattributes added. Its game file is unchanged. Commits listed in --pre-split (and
#    commits not descending from SPLIT_COMMIT) are left as they were: branches from before the split.
# 3. Redo each MERGE in order, the new way: git merge (pieces and the game file), resolve clashes in pieces the way the
#    real merge resolved them (the piece cut from the real merged file), run build.py, commit. Each merge's first
#    side is the previous replayed result, so mistakes carry forward as they would have.
# 4. Compare each glued result with the real merged game file, and report every difference, every clash, and what
#    build.py said. Writes WORKDIR/replay.json.
import sys, os, subprocess, json, re, shutil, difflib, time
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, SRC)
import split as S

def run(cmd, cwd, env=None, inp=None, ok=(0,)):
    r = subprocess.run(cmd, cwd=cwd, env=env, input=inp, capture_output=True)
    if r.returncode not in ok: raise RuntimeError(f'{cmd} -> {r.returncode}: {r.stderr.decode()[:2000]} {r.stdout.decode()[:2000]}')
    return r

def g(W, *a, inp=None, env=None, ok=(0,)):
    return run(['git'] + list(a), W, env=env, inp=inp, ok=ok).stdout

FULL_ORDER_TEXT = open(os.path.join(SRC, 'pieces/ORDER'), encoding='utf-8').read()
FULL = S.read_order(FULL_ORDER_TEXT)
TOOLS = {'build.py': open(os.path.join(SRC, 'build.py'), 'rb').read(),
         'split.py': open(os.path.join(SRC, 'split.py'), 'rb').read(),
         '.gitattributes': b'pieces/** -text\nstarship-cadet.html -text\n'}

def order_for(data):
    """The ORDER text for this game file: the full ORDER's lines whose headings exist in it (a piece appears when its
    section is first written), so a branch that adds a section also adds its piece, as a helper would."""
    L = data.split(b'\n')
    keep, notes = [], []
    for name, pick, back, rx in FULL[1:]:
        n = sum(1 for l in L if rx.search(l))
        if n == 0: continue
        if pick == 'once' and n != 1: notes.append(f'{name}: marker found {n} times'); continue
        keep.append(name)
    lines = FULL_ORDER_TEXT.split('\n')
    out = []
    for l in lines:
        f = l.split(None, 1)
        if not l.strip() or l.startswith('#') or f[0] == FULL[0][0] or f[0] in keep: out.append(l)
    return '\n'.join(out), notes

def pieces_tree(W, commit, idx_env):
    """Tree of COMMIT plus its pieces and the tools; returns (tree, notes)."""
    data = g(W, 'show', f'{commit}:starship-cadet.html')
    otext, notes = order_for(data)
    order = S.read_order(otext)
    ps = S.split(data, order)
    assert b''.join(c for _, c in ps) == data
    g(W, 'read-tree', commit, env=idx_env)
    files = [('pieces/ORDER', otext.encode())] + [('pieces/' + n, c) for n, c in ps] + list(TOOLS.items())
    for path, blob in files:
        h = g(W, 'hash-object', '-w', '--stdin', inp=blob).decode().strip()
        g(W, 'update-index', '--add', '--cacheinfo', f'100644,{h},{path}', env=idx_env)
    return g(W, 'write-tree', env=idx_env).decode().strip(), notes

def rewrite(W, split_commit, tips, pre_split):
    """Rewrite every commit on a path from SPLIT_COMMIT to the tips (not pre_split ones). Returns old->new map."""
    allrev = []
    seen = set()
    for t in tips:
        for r in g(W, 'rev-list', '--topo-order', '--reverse', '--ancestry-path', f'{split_commit}..{t}').decode().split():
            if r not in seen: seen.add(r); allrev.append(r)
    full_split = g(W, 'rev-parse', split_commit).decode().strip()
    todo = [full_split] + allrev
    # topo order over the union
    parents = {c: g(W, 'log', '-1', '--format=%P', c).decode().split() for c in todo}
    order, done = [], set()
    def visit(c):
        if c in done or c not in parents: return
        done.add(c)
        for p in parents[c]: visit(p)
        order.append(c)
    sys.setrecursionlimit(10000)
    for c in todo: visit(c)
    pre = {g(W, 'rev-parse', p).decode().strip() for p in pre_split}
    new, notes = {}, {}
    idx_env = dict(os.environ, GIT_INDEX_FILE=os.path.join(W, '.git', 'replay-index'))
    for c in order:
        if c in pre: continue
        meta = g(W, 'log', '-1', '--format=%an%x00%ae%x00%ad%x00%cn%x00%ce%x00%cd', '--date=raw', c).decode().split('\x00')
        msg = g(W, 'log', '-1', '--format=%B', c)
        tree, n = pieces_tree(W, c, idx_env)
        if n: notes[c] = n
        ps = []
        for p in parents[c]:
            ps += ['-p', new.get(p, p)]
        env = dict(os.environ, GIT_AUTHOR_NAME=meta[0], GIT_AUTHOR_EMAIL=meta[1], GIT_AUTHOR_DATE=meta[2],
                   GIT_COMMITTER_NAME=meta[3], GIT_COMMITTER_EMAIL=meta[4], GIT_COMMITTER_DATE=meta[5].strip())
        if c == full_split:   # the split commit itself: the real commit plus pieces, on top of the real one
            env2 = dict(env); ps = ['-p', c]
            msg = b'THE SPLIT (rehearsal): pieces/ cut from ' + c[:7].encode() + b'\n'
        new[c] = g(W, 'commit-tree', tree, *ps, env=env, inp=msg).decode().strip()
    return new, notes

def unmerged(W):
    return g(W, 'diff', '--name-only', '--diff-filter=U').decode().split()

def conflict_hunks(path):
    t = open(path, 'rb').read()
    return len(re.findall(rb'^<<<<<<< ', t, re.M))

def whole_file_merge(W, p1, p2):
    """How git merges the real (unsplit) commits: conflicted files, and the game file's clash count."""
    r = run(['git', 'merge-tree', '--write-tree', '--name-only', '--no-messages', p1, p2], W, ok=(0, 1))
    lines = r.stdout.decode().split('\n')
    tree = lines[0]; files = [l for l in lines[1:] if l]
    game_hunks = 0
    if 'starship-cadet.html' in files:
        game_hunks = len(re.findall(rb'^<<<<<<< ', g(W, 'show', f'{tree}:starship-cadet.html'), re.M))
    automerged = g(W, 'show', f'{tree}:starship-cadet.html')
    return files, game_hunks, automerged

def hunks(a, b):
    """Differing line ranges between two byte strings, as (a_lines, b_lines, a_text, b_text)."""
    A, B = a.split(b'\n'), b.split(b'\n')
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if tag != 'equal': out.append(((i1 + 1, i2), (j1 + 1, j2), b'\n'.join(A[i1:i2]).decode('utf-8', 'replace'), b'\n'.join(B[j1:j2]).decode('utf-8', 'replace')))
    return out

def piece_of(order_text, data, line):
    try:
        ps = S.split(data, S.read_order(order_text))
    except S.SplitError: return '?'
    n = 1
    for name, c in ps:
        k = c.count(b'\n')
        if line < n + k: return name
        n += k
    return name

def main(argv):
    W = argv[0]; split_commit = argv[1]
    merges = [a for a in argv[2:] if not a.startswith('--')]
    pre = []
    for a in argv:
        if a.startswith('--pre-split='): pre = [x for x in a.split('=', 1)[1].split(',') if x]
    if os.path.exists(W): shutil.rmtree(W)
    run(['git', 'clone', '-q', '--shared', '--no-checkout', SRC, W], '/')
    g(W, 'config', 'user.name', 'replay'); g(W, 'config', 'user.email', 'replay@example')
    g(W, 'config', 'merge.conflictstyle', 'merge')
    for k in ('rerere.enabled',): g(W, 'config', k, 'false')
    mfull = [g(W, 'rev-parse', m).decode().strip() for m in merges]
    par = {m: g(W, 'log', '-1', '--format=%P', m).decode().split() for m in mfull}
    tips = [par[mfull[0]][0]] + [par[m][1] for m in mfull]
    t0 = time.time()
    new, notes = rewrite(W, split_commit, tips, pre)
    report = {'split_commit': split_commit, 'rewritten': len(new), 'rewrite_s': round(time.time() - t0, 1),
              'order_notes': {k[:7]: v for k, v in notes.items()}, 'pre_split': pre, 'steps': []}
    first = new.get(tips[0], tips[0])
    g(W, 'checkout', '-q', '-B', 'replay', first)
    for m in mfull:
        p1, p2 = par[m]
        side = new.get(p2, p2)
        real = g(W, 'show', f'{m}:starship-cadet.html')
        step = {'merge': m[:7], 'subject': g(W, 'log', '-1', '--format=%s', m).decode().strip(), 'other': p2[:7],
                'other_is_pre_split': p2 not in new}
        files, gh, auto = whole_file_merge(W, p1, p2)
        step['historical_conflicted_files'] = files; step['historical_game_clashes'] = gh
        r = run(['git', 'merge', '--no-ff', '--no-edit', side], W, ok=(0, 1))
        step['git_merge_rc'] = r.returncode
        um = unmerged(W)
        step['replay_conflicted_files'] = um
        step['replay_piece_clashes'] = {f: conflict_hunks(os.path.join(W, f)) for f in um if f.startswith('pieces/')}
        step['replay_game_clashes'] = conflict_hunks(os.path.join(W, 'starship-cadet.html')) if 'starship-cadet.html' in um else 0
        # resolve each clashed piece / ORDER the way the real merge did
        if r.returncode == 1:
            order_text = open(os.path.join(W, 'pieces/ORDER'), encoding='utf-8').read()
            if 'pieces/ORDER' in um:
                order_text, _ = order_for(real)
                open(os.path.join(W, 'pieces/ORDER'), 'w', encoding='utf-8').write(order_text)
                g(W, 'add', 'pieces/ORDER')
            real_ps = dict(S.split(real, S.read_order(order_text)))
            for f in um:
                if f.startswith('pieces/') and f != 'pieces/ORDER':
                    n = f[len('pieces/'):]
                    if n in real_ps:
                        open(os.path.join(W, f), 'wb').write(real_ps[n]); g(W, 'add', f)
                    else:
                        g(W, 'rm', '-q', f)
            for f in um:
                if not f.startswith('pieces/') and f != 'starship-cadet.html':   # notes, checks: take the real merge's
                    blob = run(['git', 'show', f'{m}:{f}'], W, ok=(0, 128))
                    if blob.returncode == 0: open(os.path.join(W, f), 'wb').write(blob.stdout); g(W, 'add', f)
                    else: g(W, 'rm', '-q', f)
        b = run(['python3', 'build.py'], W, ok=(0, 1, 2))
        step['build_rc'] = b.returncode; step['build_said'] = b.stdout.decode().strip()
        if b.returncode == 2 and 'before the split' in step['build_said'] and 'starship-cadet.html' in um:
            # as build.py asks: fix the clash in the game file (here: the way the real merge did), then run it again
            open(os.path.join(W, 'starship-cadet.html'), 'wb').write(real); g(W, 'add', 'starship-cadet.html')
            b = run(['python3', 'build.py'], W, ok=(0, 1, 2))
            step['build_rc'] = b.returncode; step['build_said'] += ' || THEN, after fixing the game file: ' + b.stdout.decode().strip()
        chk = run(['python3', 'build.py', '--check'], W, ok=(0, 1, 2))
        step['check_rc'] = chk.returncode
        if b.returncode == 0:
            g(W, 'add', '-A')
            g(W, 'commit', '-q', '--no-edit', '-m', f'replay of {m[:7]}', ok=(0, 1))
        else:
            step['STOPPED'] = True
            g(W, 'add', '-A'); g(W, 'commit', '-q', '--no-edit', '-m', f'replay of {m[:7]} (build.py stopped)', ok=(0, 1))
        glued = open(os.path.join(W, 'starship-cadet.html'), 'rb').read()
        step['identical_to_real'] = glued == real
        hs = hunks(real, glued)
        ha = hunks(real, auto) if not gh else None
        step['diff_hunks'] = []
        order_text = open(os.path.join(W, 'pieces/ORDER'), encoding='utf-8').read()
        for (ra, rb, at, bt) in hs:
            step['diff_hunks'].append({'real_lines': ra, 'replay_lines': rb, 'piece': piece_of(order_text, glued, rb[0]),
                                       'real': at[:1500], 'replay': bt[:1500],
                                       'also_differs_from_gits_whole_file_merge': None})
        step['real_vs_git_whole_file_automerge_hunks'] = len(hunks(real, auto)) if not gh else 'n/a (whole file clashed)'
        report['steps'].append(step)
        print(json.dumps({k: v for k, v in step.items() if k != 'diff_hunks'}), len(step['diff_hunks']), 'diff hunks', flush=True)
    json.dump(report, open(os.path.join(W, 'replay.json'), 'w'), indent=1)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
