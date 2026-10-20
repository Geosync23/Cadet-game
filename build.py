# build.py: keep starship-cadet.html and its pieces (pieces/, in pieces/ORDER's order) in step.
#   python3 build.py           after any change or merge: works out what changed and does the safe thing
#                              (glue the pieces, or cut the game file, or combine both), and says which it did
#   python3 build.py --check   changes nothing; exit 1 (and say which pieces) if the game file and the pieces differ
# Never fix starship-cadet.html by hand: edit the pieces and run this.
import sys, os, re, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import split as S
ROOT, GAME, PIECES = S.ROOT, S.GAME, S.PIECES
GAME_REL = 'starship-cadet.html'
CONFLICT = re.compile(rb'^(<<<<<<<|>>>>>>>)( |$)', re.M)

def git(*a, ok=(0,)):
    r = subprocess.run(['git', '-C', ROOT] + list(a), capture_output=True)
    return r.stdout if r.returncode in ok else None

def show(rev, path):
    return git('show', f'{rev}:{path}')

def glue_at(rev):
    """The glued file and the pieces' glue at a commit, or None if that commit has no pieces."""
    o = show(rev, 'pieces/ORDER'); g = show(rev, GAME_REL)
    if o is None or g is None: return None
    try: names = S.order_names(o.decode('utf-8'))
    except S.SplitError: return None
    parts = [show(rev, 'pieces/' + n) for n in names]
    if any(p is None for p in parts): return None
    return g, b''.join(parts)

def in_step_ref():
    """The newest commit along HEAD's first parents whose glued file matches its pieces: the last agreed point."""
    for k in range(30):
        rev = 'HEAD' + '^' * k
        if git('rev-parse', '-q', '--verify', rev + '^{commit}') is None: return None
        gp = glue_at(rev)
        if gp and gp[0] == gp[1]: return rev, gp[0]
    return None

def problems():
    """Things wrong with the pieces themselves. Returns (messages, glue or None)."""
    msgs = []
    try: order = S.read_order(open(os.path.join(PIECES, 'ORDER'), encoding='utf-8').read())
    except (OSError, S.SplitError) as e: return [f'pieces/ORDER: {e}'], None
    names = [o[0] for o in order]; parts = []
    for n in names:
        p = os.path.join(PIECES, n)
        if not os.path.exists(p): msgs.append(f'{n}: listed in pieces/ORDER but missing'); continue
        b = open(p, 'rb').read()
        if not b.endswith(b'\n'):
            msgs.append(f'{n}: does not end with a new line (its last line would join the next piece\'s first)')
        if CONFLICT.search(b): msgs.append(f'{n}: still has git clash markers (<<<<<<< / >>>>>>>): fix the clash first')
        parts.append(b)
    for d, _, fs in os.walk(PIECES):
        for f in fs:
            rel = os.path.relpath(os.path.join(d, f), PIECES).replace(os.sep, '/')
            if rel != 'ORDER' and rel not in names: msgs.append(f'{rel}: in pieces/ but not in pieces/ORDER (left behind? add it or delete it)')
    return msgs, (b''.join(parts) if len(parts) == len(names) else None)

def diff_pieces(game_bytes):
    """Which pieces differ between the game file and pieces/ (cutting the game file in memory)."""
    try:
        order = S.read_order(open(os.path.join(PIECES, 'ORDER'), encoding='utf-8').read())
        ps = S.split(game_bytes, order)
    except S.SplitError as e: return [f'(the game file can\'t be cut: {e})']
    out = []
    for n, chunk in ps:
        p = os.path.join(PIECES, n)
        if not os.path.exists(p) or open(p, 'rb').read() != chunk: out.append(n)
    return out

def unmerged():
    o = git('diff', '--name-only', '--diff-filter=U')
    return o.decode().split() if o else []

def write_game(b):
    with open(GAME, 'wb') as f: f.write(b)

def cut(b):
    order = S.read_order(open(os.path.join(PIECES, 'ORDER'), encoding='utf-8').read())
    ch = S.write_pieces(S.split(b, order), PIECES)
    return ch

def check():
    msgs, glued = problems()
    game = open(GAME, 'rb').read() if os.path.exists(GAME) else None
    if game is None: msgs.append('starship-cadet.html is missing')
    elif glued is not None and glued != game:
        d = diff_pieces(game)
        msgs.append('starship-cadet.html does not match its pieces' + (' (differs in: ' + ', '.join(d) + ')' if d else '')
                    + '. Run python3 build.py; it works out which side is newer.')
    if game is not None and CONFLICT.search(game): msgs.append('starship-cadet.html has git clash markers')
    if game is not None and glued is not None and glued == game:
        # the cut must give back the same pieces: else a renamed or copied section heading breaks the next merge's cut
        try:
            order = S.read_order(open(os.path.join(PIECES, 'ORDER'), encoding='utf-8').read())
            for n, chunk in S.split(game, order):
                if open(os.path.join(PIECES, n), 'rb').read() != chunk:
                    msgs.append(f'{n}: the game file would not cut back into this piece (a section heading in pieces/ORDER moved, renamed or copied?)')
        except S.SplitError as e:
            msgs.append(f'the game file would not cut back into its pieces: {e}')
    for m in msgs: print('build --check: FAIL ' + m)
    if not msgs: print(f'build --check: OK, starship-cadet.html matches its {len(S.order_names(open(os.path.join(PIECES, "ORDER"), encoding="utf-8").read()))} pieces')
    return 1 if msgs else 0

def sync():
    msgs, glued = problems()
    nl = [m for m in msgs if 'new line' in m]
    for m in nl:   # a lost final new line is put back: the joined file would otherwise run two lines together
        n = m.split(':')[0]; p = os.path.join(PIECES, n)
        with open(p, 'ab') as f: f.write(b'\n')
        print(f'build: {n} had lost its final new line; put back')
    if nl: msgs, glued = problems()
    if msgs or glued is None:
        for m in msgs: print('build: STOPPED ' + m)
        return 2
    game = open(GAME, 'rb').read()
    ref_order = show('HEAD', 'pieces/ORDER')
    if ref_order is not None:
        try:
            if S.order_names(ref_order.decode('utf-8')) != S.order_names(open(os.path.join(PIECES, 'ORDER'), encoding='utf-8').read()):
                print('build: WARNING the pieces\' order changed since the last commit. Order is part of the game (load order, R()): '
                      'the full check set must run before this goes anywhere.')
        except S.SplitError: pass
    if game == glued: print('build: in step, nothing to do'); return 0
    um = unmerged()
    merging = git('rev-parse', '-q', '--verify', 'MERGE_HEAD') is not None
    if CONFLICT.search(game) or GAME_REL in um:
        # the glued file clashed in a merge. Its clash is the pieces' clash, already fixed in the pieces,
        # as long as the other side kept its work in its pieces (it's from after the split, and in step).
        other = glue_at('MERGE_HEAD') if merging else None
        if other is None:
            print('build: STOPPED starship-cadet.html has a clash, and the other side of this merge has no pieces '
                  '(a branch from before the split): its work is only in the game file. Fix the clash in starship-cadet.html '
                  '(the one time to edit it), then run python3 build.py again: it will cut it into pieces.')
            return 2
        if other[0] != other[1]:
            print('build: STOPPED starship-cadet.html has a clash, and the other side\'s game file did not match its own pieces, '
                  'so some of its work may be only in the game file. Ask the build master.')
            return 2
        write_game(glued)
        if GAME_REL in um: git('add', GAME_REL)
        print('build: GLUED (the game file\'s clash was the pieces\' clash, which is fixed; both sides\' work is in the pieces)')
        return 0
    ref = in_step_ref()
    if ref is None:
        print('build: STOPPED the game file and the pieces differ, and no recent commit has them in step to compare with. Ask the build master.')
        return 2
    rev, base = ref
    dp, dg = glued != base, game != base
    if not dg:
        write_game(glued); print(f'build: GLUED (pieces changed since {rev}; the game file had not): {", ".join(diff_pieces(base)) or "?"}')
        return 0
    if not dp:
        ch = cut(game)
        print(f'build: CUT (the game file changed since {rev}, e.g. a merge of a branch from before the split, or a hand edit; '
              f'the pieces had not): changed pieces: {", ".join(ch)}')
        return verify()
    # both changed: combine the two the way git would, with the agreed point as the common base
    with tempfile.TemporaryDirectory() as t:
        fp, fb, fg = (os.path.join(t, x) for x in ('pieces', 'base', 'game'))
        for f, b in ((fp, glued), (fb, base), (fg, game)): open(f, 'wb').write(b)
        r = subprocess.run(['git', 'merge-file', '-p', '-L', 'pieces', '-L', rev, '-L', 'game file', fp, fb, fg], capture_output=True)
        if r.returncode != 0:
            print(f'build: STOPPED both the pieces and the game file changed since {rev}, differently, and they clash in {r.returncode} '
                  f'place(s). Nothing written. Ask the build master (or put the game-file change into its piece and run again).')
            return 2
        merged = r.stdout
    write_game(merged); ch = cut(merged)
    print(f'build: COMBINED (both the pieces and the game file changed since {rev}; no clash): changed pieces: {", ".join(ch) or "none"}')
    return verify()

def verify():
    msgs, glued = problems()
    if msgs or glued != open(GAME, 'rb').read():
        print('build: FAIL after the cut the pieces do not glue back to the game file'); return 2
    return 0

if __name__ == '__main__':
    try: sys.exit(check() if '--check' in sys.argv else sync())
    except S.SplitError as e:
        print('build: STOPPED the game file can\'t be cut into its pieces: ' + str(e)); sys.exit(2)
