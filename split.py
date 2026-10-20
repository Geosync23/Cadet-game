# split.py: cut starship-cadet.html into its pieces (pieces/ORDER says which, in what order, and where each starts).
#   python3 split.py                 cut the game file into pieces/ (only pieces that change are written; it names them)
#   python3 split.py GAME.html DIR   cut another file into DIR (DIR/ORDER is copied from pieces/ORDER)
# Bytes in, bytes out: gluing the pieces back (build.py) gives the same file, letter for letter.
# Usually you don't run this yourself: build.py decides whether to glue or to cut, and calls this when cutting is right.
import sys, os, re
ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(ROOT, 'starship-cadet.html')
PIECES = os.path.join(ROOT, 'pieces')

class SplitError(Exception): pass

def read_order(text):
    """pieces/ORDER -> [(piece, pick, back, regex)]; the first piece has no marker."""
    out = []
    for n, line in enumerate(text.split('\n'), 1):
        if not line.strip() or line.startswith('#'): continue
        f = line.split(None, 3)
        if not out:
            if len(f) != 1: raise SplitError(f'ORDER line {n}: the first piece has no marker')
            out.append((f[0], None, 0, None)); continue
        if len(f) != 4 or f[1] not in ('once', 'first', 'last'):
            raise SplitError(f'ORDER line {n}: expected "PIECE once|first|last BACK MARKER", got {line!r}')
        try: rx = re.compile(f[3].encode())
        except re.error as e: raise SplitError(f'ORDER line {n}: bad marker {f[3]!r}: {e}')
        out.append((f[0], f[1], int(f[2]), rx))
    names = [o[0] for o in out]
    dup = {x for x in names if names.count(x) > 1}
    if dup: raise SplitError('ORDER names a piece twice: ' + ', '.join(sorted(dup)))
    return out

def order_names(text):
    return [o[0] for o in read_order(text)]

def split(data, order):
    """Cut the game file's bytes at the markers. Returns [(piece, bytes)]; b''.join of them == data."""
    if not data.endswith(b'\n'): raise SplitError('the game file does not end with a new line')
    L = data.split(b'\n')[:-1]          # lines without their '\n'
    starts = [0]
    for name, pick, back, rx in order[1:]:
        hits = [i for i, l in enumerate(L) if rx.search(l)]
        if pick == 'first': hits = hits[:1]
        if pick == 'last': hits = hits[-1:]
        if len(hits) != 1:
            raise SplitError(f'{name}: its marker {rx.pattern.decode()!r} is in the game file {len(hits)} times, not once '
                             f'(a section heading renamed, removed or copied? fix the heading or pieces/ORDER)')
        s = hits[0] - back
        if s <= starts[-1]:
            raise SplitError(f'{name}: its marker comes before the previous piece\'s (pieces moved in the game file? pieces/ORDER must follow the file)')
        starts.append(s)
    starts.append(len(L))
    return [(order[k][0], b''.join(l + b'\n' for l in L[starts[k]:starts[k + 1]])) for k in range(len(order))]

def write_pieces(pieces, outdir):
    changed = []
    for name, chunk in pieces:
        p = os.path.join(outdir, name)
        old = open(p, 'rb').read() if os.path.exists(p) else None
        if old != chunk:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'wb') as f: f.write(chunk)
            changed.append(name)
    return changed

def main(argv):
    args = [a for a in argv if not a.startswith('-')]
    game = args[0] if args else GAME
    outdir = args[1] if len(args) > 1 else PIECES
    try:
        otext = open(os.path.join(PIECES, 'ORDER'), encoding='utf-8').read()
        ps = split(open(game, 'rb').read(), read_order(otext))
    except SplitError as e:
        print('split: STOPPED, nothing written: ' + str(e)); return 2
    if os.path.abspath(outdir) != os.path.abspath(PIECES):
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, 'ORDER'), 'w', encoding='utf-8') as f: f.write(otext)
    changed = write_pieces(ps, outdir)
    print(f'split: {len(ps)} pieces; ' + (('changed: ' + ', '.join(changed)) if changed else 'none changed'))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
