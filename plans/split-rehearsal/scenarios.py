# scenarios.py (split rehearsal SX1): attack the split workflow, each case for real with git in its own scratch repo.
#   python3 plans/split-rehearsal/scenarios.py WORKDIR [NAME ...]      -> WORKDIR/scenarios.md (the transcript)
# Every repo starts as: commit A = the 0.64.2 game as one file (before the split), commit S = the split (pieces/,
# build.py, split.py, names_check.js, .gitattributes, content_gen pointing at its piece). Branch "integration" = S.
# Edits are marks appended to real, unique code lines ("// MARK-x"), so we can count afterwards whose work survived.
import sys, os, subprocess, shutil, re
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = []

def log(s=''): OUT.append(s); print(s, flush=True)

class Repo:
    def __init__(self, path):
        self.p = path
    def sh(self, cmd, show=True, ok=None):
        r = subprocess.run(cmd, shell=True, cwd=self.p, capture_output=True, text=True)
        o = (r.stdout + r.stderr).strip()
        if show:
            log(f'    $ {cmd}')
            for l in o.split('\n')[:14]:
                if l.strip(): log('      ' + l[:400])
            if r.returncode: log(f'      (exit {r.returncode})')
        return r.returncode, o
    def q(self, cmd): return self.sh(cmd, show=False)
    def read(self, rel): return open(os.path.join(self.p, rel), 'rb').read()
    def write(self, rel, b):
        os.makedirs(os.path.dirname(os.path.join(self.p, rel)) or '.', exist_ok=True)
        open(os.path.join(self.p, rel), 'wb').write(b)
    def mark(self, rel, k, tag, before=False):
        """Append (or prepend) '// MARK-tag' to the k-th line of rel that is unique in the whole game file."""
        game = self.read('starship-cadet.html')
        lines = self.read(rel).split(b'\n')
        cands = [i for i, l in enumerate(lines) if len(l) > 30 and b'MARK-' not in l and game.count(l) == 1 and not l.lstrip().startswith(b'//')]
        i = cands[k]
        lines[i] = (b'/* MARK-' + tag.encode() + b' */ ' + lines[i]) if before else (lines[i] + b' // MARK-' + tag.encode())
        self.write(rel, b'\n'.join(lines))
        return lines[i]
    def count(self, tag):
        g = self.read('starship-cadet.html').count(('MARK-' + tag).encode())
        p = 0
        for d, _, fs in os.walk(os.path.join(self.p, 'pieces')):
            for f in fs: p += open(os.path.join(d, f), 'rb').read().count(('MARK-' + tag).encode())
        return g, p
    def survived(self, *tags):
        res = {t: self.count(t) for t in tags}
        log('    marks (in the game file, in the pieces): ' + ', '.join(f'{t}={v}' for t, v in res.items()))
        return all(v == (1, 1) for v in res.values())

BASE = None
def make_base(work):
    """One template repo with commits A (one file) and S (split); scenarios clone it."""
    global BASE
    b = os.path.join(work, '_base')
    if os.path.exists(b): shutil.rmtree(b)
    os.makedirs(b)
    r = Repo(b)
    for f in ('starship-cadet.html', 'content_gen.py', 'plans/trad_parse.py'):
        os.makedirs(os.path.dirname(os.path.join(b, f)) or b, exist_ok=True); shutil.copy(os.path.join(SRC, f), os.path.join(b, f))
    shutil.copytree(os.path.join(SRC, 'content'), os.path.join(b, 'content'))
    # A: before the split, content_gen as it was (writes the game file)
    old_cg = subprocess.run(['git', '-C', SRC, 'show', '1eeb99c:content_gen.py'], capture_output=True).stdout
    r.write('content_gen.py', old_cg)
    r.q('git init -q -b main && git config user.name t && git config user.email t@t && git config merge.conflictstyle merge && git add -A && git commit -qm "A: 0.64.2, one file"')
    for f in ('build.py', 'split.py', 'names_check.js', '.gitattributes', 'content_gen.py'):
        shutil.copy(os.path.join(SRC, f), os.path.join(b, f))
    shutil.copytree(os.path.join(SRC, 'pieces'), os.path.join(b, 'pieces'))
    r.q('git add -A && git commit -qm "S: the split" && git branch integration && git tag A HEAD~1 && git tag S HEAD')
    BASE = b

def fresh(work, name):
    p = os.path.join(work, name)
    if os.path.exists(p): shutil.rmtree(p)
    subprocess.run(['git', 'clone', '-q', BASE, p], check=True)
    r = Repo(p)
    r.q('git config user.name t && git config user.email t@t && git config merge.conflictstyle merge && git fetch -q --tags')
    for br in ('integration',): r.q(f'git branch -f {br} origin/{br}')
    return r

def check(r, label='build.py --check'):
    rc, o = r.sh('python3 build.py --check')
    return rc

SCEN = {}
def scenario(f): SCEN[f.__name__] = f; return f

@scenario
def pre_split_branch_clean(W):
    """A branch from before the split (edits the one game file) is merged after the split; git merges it silently."""
    r = fresh(W, 'pre_split_branch_clean')
    r.q('git checkout -q -b old A')
    r.mark('starship-cadet.html', 5000, 'old1'); r.mark('starship-cadet.html', 20000, 'old2')
    r.q('git commit -qam "old branch: two edits in the one file"')
    r.q('git checkout -q integration')
    r.mark('pieces/js/s19-device.js', 40, 'new'); r.sh('python3 build.py'); r.q('git commit -qam "integration: a piece edit, glued"')
    r.sh('git merge --no-edit old')
    red = check(r) != 0
    log('    -- what the review found (plan\'s first version): glue again --')
    rc, _ = r.q('cp -r pieces /tmp/_pz && cp starship-cadet.html /tmp/_gz')
    r.sh('python3 -c "import split as S,os; o=S.order_names(open(\'pieces/ORDER\').read()); open(\'starship-cadet.html\',\'wb\').write(b\'\'.join(open(\'pieces/\'+n,\'rb\').read() for n in o))"  # plain glue')
    lost_plain = not r.survived('old1', 'old2', 'new')
    r.q('git checkout -- starship-cadet.html')
    log('    -- the rehearsal build.py --')
    r.sh('python3 build.py'); ok = r.survived('old1', 'old2', 'new'); check(r)
    return dict(check_red=red, lost=not ok, note=f'plain glue would lose work: {lost_plain}')

@scenario
def pre_split_branch_clash(W):
    """A pre-split branch and the integration edit the same line."""
    r = fresh(W, 'pre_split_branch_clash')
    line_owner = 'pieces/js/s16-galley.js'
    r.q('git checkout -q integration')
    r.mark(line_owner, 10, 'new'); r.sh('python3 build.py'); r.q('git commit -qam "integration edit"'); r.q('git checkout -q -b old A')
    # the same line, in the one file
    g = r.read('starship-cadet.html'); pl = r.q('git show integration:' + line_owner)[1]
    tgt = [l for l in pl.split('\n') if 'MARK-new' in l][0].replace(' // MARK-new', '')
    r.write('starship-cadet.html', g.replace(tgt.encode(), tgt.encode() + b' // MARK-old', 1)); r.q('git commit -qam "old: same line"')
    r.q('git checkout -q integration')
    r.sh('git merge --no-edit old')
    r.sh('python3 build.py')
    log('    (fixing the clash in starship-cadet.html: keep both marks)')
    g = r.read('starship-cadet.html').decode()
    g = re.sub(r'<<<<<<< HEAD\n(.*?) // MARK-new\n=======\n.*? // MARK-old\n>>>>>>> old\n', lambda m: m.group(1) + ' // MARK-new // MARK-old\n', g, flags=re.S)
    r.write('starship-cadet.html', g.encode()); r.q('git add starship-cadet.html')
    r.sh('python3 build.py'); ok = r.survived('old', 'new'); rc = check(r)
    r.sh('git commit -qam "merge old"')
    return dict(check_red=True, lost=not ok, note='build.py stopped and said to fix the clash in the game file, then cut it')

@scenario
def same_piece_two_seats(W):
    """Two seats edit the same piece: (a) different lines, (b) the same line."""
    r = fresh(W, 'same_piece_two_seats')
    for br, k, tag in (('seatA', 100, 'a'), ('seatB', 300, 'b')):
        r.q(f'git checkout -q -b {br} integration'); r.mark('pieces/js/s14-schedules.js', k, tag); r.q('python3 build.py'); r.q(f'git commit -qam "{br}"')
    r.q('git checkout -q integration'); r.sh('git merge --no-edit seatA'); r.sh('git merge --no-edit seatB')
    r.sh('python3 build.py'); a_ok = r.survived('a', 'b'); check(r)
    log('    (b) the same line:')
    for br, tag in (('seatC', 'c'), ('seatD', 'd')):
        r.q(f'git checkout -q -b {br} integration'); r.mark('pieces/js/s14-schedules.js', 200, tag); r.q('python3 build.py'); r.q(f'git commit -qam "{br}"')
    r.q('git checkout -q integration'); r.sh('git merge --no-edit seatC'); r.sh('git merge --no-edit seatD')
    r.sh('git diff --name-only --diff-filter=U')
    log('    (fixing the clash in the piece only: keep both)')
    t = r.read('pieces/js/s14-schedules.js').decode()
    t = re.sub(r'<<<<<<< HEAD\n(.*?) // MARK-c\n=======\n.*? // MARK-d\n>>>>>>> seatD\n', lambda m: m.group(1) + ' // MARK-c // MARK-d\n', t, flags=re.S)
    r.write('pieces/js/s14-schedules.js', t.encode()); r.q('git add pieces/js/s14-schedules.js')
    r.sh('python3 build.py'); b_ok = r.survived('c', 'd'); rc = check(r); r.q('git commit -qam merge')
    return dict(check_red=False, lost=not (a_ok and b_ok), note='(a) clean; (b) the piece and the game file clashed in the same place; fix the piece, build.py glued')

@scenario
def boundary_clash(W):
    """Seat A edits the last code line of one piece, seat B the first code line of the next: pieces merge cleanly,
    the game file clashes (the two lines are neighbours there)."""
    r = fresh(W, 'boundary_clash')
    a = 'pieces/js/s16-galley.js'; b = 'pieces/js/s17-machines-jobs.js'
    ta = r.read(a).split(b'\n'); i = max(k for k, l in enumerate(ta) if l.strip())
    tb = r.read(b).split(b'\n')
    r.q('git checkout -q -b seatA integration'); ta[i] += b' // MARK-a'; r.write(a, b'\n'.join(ta)); r.q('python3 build.py'); r.q('git commit -qam A')
    r.q('git checkout -q -b seatB integration'); tb[0] += b' // MARK-b'; r.write(b, b'\n'.join(tb)); r.q('python3 build.py'); r.q('git commit -qam B')
    r.q('git checkout -q integration'); r.sh('git merge --no-edit seatA'); r.sh('git merge --no-edit seatB')
    r.sh('git diff --name-only --diff-filter=U')
    r.sh('python3 build.py'); ok = r.survived('a', 'b'); check(r); r.q('git commit -qam merge')
    return dict(check_red=True, lost=not ok, note='only the game file clashed; build.py glued the cleanly merged pieces')

@scenario
def hand_edit_glued(W):
    """A seat edits starship-cadet.html by habit, commits, and pushes; then (b) the same on a branch that also edits a
    piece; then (c) that out-of-step branch is merged into integration without fixing it."""
    r = fresh(W, 'hand_edit_glued')
    r.q('git checkout -q -b habit integration')
    r.mark('starship-cadet.html', 30000, 'hand'); r.q('git commit -qam "edit the game file by hand"')
    red = check(r) != 0
    r.mark('pieces/js/s20-social.js', 50, 'piece'); r.q('git commit -qam "and a piece edit, no glue"')
    check(r)
    r.q('git checkout -q -b fixme habit')
    r.sh('python3 build.py'); ok1 = r.survived('hand', 'piece')
    log('    (c) merge the out-of-step branch into integration as it is, then build.py there:')
    r.q('git checkout -q integration'); r.mark('pieces/js/s10-walkers.js', 30, 'integ'); r.q('python3 build.py'); r.q('git commit -qam integ')
    r.sh('git merge --no-edit habit'); check(r)
    r.sh('python3 build.py'); ok2 = r.survived('hand', 'piece', 'integ'); check(r)
    log('    (d) a hand edit and a piece edit of the SAME line, differently:')
    r.q('git commit -qam merged'); r.q('git checkout -q -b clash integration')
    line = r.mark('pieces/js/s18-events.js', 20, 'pc')
    g = r.read('starship-cadet.html'); orig = line.replace(b' // MARK-pc', b'')
    r.write('starship-cadet.html', g.replace(orig, orig + b' // MARK-gl', 1))
    rc, o = r.sh('python3 build.py'); stopped = rc == 2
    return dict(check_red=red, lost=not (ok1 and ok2), note=f'(b) build.py combined both; (c) on integration too; (d) same line both ways: build.py stopped = {stopped}')

@scenario
def forgotten_glue(W):
    """A piece edited, committed and pushed without running build.py."""
    r = fresh(W, 'forgotten_glue')
    r.q('git checkout -q -b seat integration'); r.mark('pieces/js/s21-arrival-clothes.js', 10, 'f'); r.q('git commit -qam "piece only"')
    red = check(r) != 0
    r.q('git checkout -q integration'); r.sh('git merge --no-edit seat'); check(r)
    r.sh('python3 build.py'); ok = r.survived('f'); check(r)
    return dict(check_red=red, lost=not ok, note='merged unglued into integration: build.py glued there (the game file had not changed)')

@scenario
def no_final_newline(W):
    """A piece loses its final new line (some editors strip it)."""
    r = fresh(W, 'no_final_newline')
    p = 'pieces/content/s22-words.gen.js'; b = r.read(p); r.write(p, b.rstrip(b'\n'))
    log(f'    piece ends: {b.rstrip(chr(10).encode())[-40:]!r}; next piece starts: {r.read("pieces/js/s22-lines-engine-2.js")[:40]!r}')
    red = check(r) != 0
    log('    -- what a plain concatenation would make --')
    r.sh('python3 -c "import split as S; o=S.order_names(open(\'pieces/ORDER\').read()); open(\'/tmp/_naive.html\',\'wb\').write(b\'\'.join(open(\'pieces/\'+n,\'rb\').read() for n in o))" && grep -n "END TRADITIONS ----const" /tmp/_naive.html | cut -c1-120 && CADET_WORK=/tmp/cadet-work node names_check.js /tmp/_naive.html')
    r.sh('python3 build.py'); rc = check(r)
    return dict(check_red=red, lost=False, note='build --check red; build.py put the new line back; a plain glue would have commented out `const LINE_TIER` and names_check would NOT have noticed')

@scenario
def renamed_heading(W):
    """A seat renames a section heading that pieces/ORDER uses ("// 19. DEVICE" -> "// 19. YOUR DEVICE")."""
    r = fresh(W, 'renamed_heading')
    p = 'pieces/js/s19-device.js'; r.write(p, r.read(p).replace(b'// 19. DEVICE', b'// 19. YOUR DEVICE', 1))
    r.sh('python3 build.py'); red = check(r) != 0
    r.sh('python3 split.py')
    log('    fix: update the marker in pieces/ORDER')
    r.write('pieces/ORDER', r.read('pieces/ORDER').replace(b'^// 19\\. DEVICE', b'^// 19\\. YOUR DEVICE'))
    rc = check(r)
    log('    a copied heading: a comment "// 4c. see the deck build" pasted at the top of a line in another piece')
    p2 = 'pieces/js/s20-social.js'; t = r.read(p2).split(b'\n'); t.insert(5, b'// 4c. see the deck build'); r.write(p2, b'\n'.join(t))
    r.sh('python3 build.py'); check(r)
    return dict(check_red=red, lost=False, note='--check goes red at once (the cut would not give the same pieces); build.py glues but the next cut would stop')

@scenario
def moved_in_order(W):
    """Two lines of pieces/ORDER swapped (load order changes: part of the game)."""
    r = fresh(W, 'moved_in_order')
    o = r.read('pieces/ORDER').split(b'\n')
    i = [k for k, l in enumerate(o) if l.startswith(b'js/s19-device.js')][0]
    o[i], o[i + 1] = o[i + 1], o[i]
    r.write('pieces/ORDER', b'\n'.join(o))
    r.sh('python3 build.py'); rc = check(r)
    r.sh('CADET_WORK=/tmp/cadet-work node names_check.js')
    r.sh('git diff --stat')
    r.q('cp starship-cadet.html ' + os.path.join(W, 'moved_in_order.html'))
    return dict(check_red=False, lost=False, note='the fast static steps stay green: only build.py\'s warning and the browser checks can catch an order change (see the cadet_test run on this file)')

@scenario
def content_gen_words(W):
    """A writer changes a .lines file: (a) runs content_gen.py (now writes the piece) and build.py; (b) forgets content_gen;
    (c) an old content_gen (or one pointed at the game file) writes the game file."""
    r = fresh(W, 'content_gen_words')
    f = os.path.join(r.p, 'content/banks/alarm.lines')
    t = open(f, encoding='utf-8').read()
    m = re.search(r'^- (Sleep longer, wake fresher\.)$', t, re.M)
    log(f'    file {os.path.relpath(f, r.p)}; first line: {m.group(1)[:80]!r}')
    rc, o = r.q('python3 content_gen.py --check'); log('    before: ' + o[:80])
    # add a word to a real line: find a line with a quoted text or just append text
    t2 = t.replace(m.group(1), m.group(1) + ' Zebra.', 1); open(f, 'w', encoding='utf-8').write(t2)
    r.sh('python3 content_gen.py --check')
    r.sh('python3 content_gen.py starship-cadet.html')
    r.sh('python3 content_gen.py'); r.sh('python3 build.py'); ok_a = check(r) == 0 and b'Zebra.' in r.read('starship-cadet.html')
    r.q('git commit -qam "words (a)"')
    log('    (c) an old content_gen writes the game file:')
    open(f, 'w', encoding='utf-8').write(t2.replace(' Zebra.', ' Zebra Yak.', 1))
    r.q('git show A:content_gen.py > /tmp/_old_cg.py && cp /tmp/_old_cg.py content_gen_old.py')
    r.sh('python3 content_gen_old.py'); r.q('rm content_gen_old.py')
    red = check(r) != 0
    r.sh('python3 build.py'); ok_c = check(r) == 0 and b'Zebra Yak' in r.read('pieces/content/s22-words.gen.js')
    log(f'    the words piece has "Zebra Yak": {ok_c}')
    return dict(check_red=red, lost=not (ok_a and ok_c), note='(a) content_gen refuses the game file and writes the piece; (c) build.py cut the old tool\'s write into the words piece')

@scenario
def glued_clash_hand_resolved(W):
    """Two seats clash; the build master fixes the clash in the GAME FILE by hand (differently from the pieces)."""
    r = fresh(W, 'glued_clash_hand_resolved')
    for br, tag in (('seatA', 'a'), ('seatB', 'b')):
        r.q(f'git checkout -q -b {br} integration'); r.mark('pieces/js/s15-player-needs.js', 60, tag); r.q('python3 build.py'); r.q(f'git commit -qam {br}')
    r.q('git checkout -q integration'); r.q('git merge --no-edit seatA'); r.sh('git merge --no-edit seatB')
    log('    (the build master fixes the game file by hand, keeping both, and the piece keeping only A)')
    for rel, keep in (('starship-cadet.html', ' // MARK-a // MARK-b\n'), ('pieces/js/s15-player-needs.js', ' // MARK-a\n')):
        t = r.read(rel).decode()
        t = re.sub(r'<<<<<<< HEAD\n(.*?) // MARK-a\n=======\n.*? // MARK-b\n>>>>>>> seatB\n', lambda m: m.group(1) + keep, t, flags=re.S)
        r.write(rel, t.encode()); r.q('git add ' + rel)
    rc, o = r.sh('python3 build.py'); r.survived('a', 'b'); check(r)
    return dict(check_red=True, lost=False, note=f'build.py: {o.splitlines()[-1][:160]}')

@scenario
def reverts(W):
    """(a) git revert of a post-split commit; (b) of a merge; (c) of a commit from before the split."""
    r = fresh(W, 'reverts')
    r.mark('pieces/js/s24-work.js', 10, 'r1'); r.q('python3 build.py'); r.q('git commit -qam r1')
    r.sh('git revert --no-edit HEAD'); check(r); a = r.count('r1') == (0, 0)
    r.q('git checkout -q -b seat integration'); r.mark('pieces/js/s24k-cases.js', 10, 'r2'); r.q('python3 build.py'); r.q('git commit -qam r2')
    r.q('git checkout -q integration'); r.q('git merge --no-ff --no-edit seat')
    r.sh('git revert --no-edit -m 1 HEAD'); check(r); b = r.count('r2') == (0, 0)
    log('    (c) revert A itself (a pre-split commit that made the whole game: too big) -> instead a pre-split edit:')
    r2 = fresh(W, 'reverts_pre')
    r2.q('git checkout -q -b old A'); r2.mark('starship-cadet.html', 12000, 'p'); r2.q('git commit -qam "old edit"')
    r2.q('git checkout -q integration'); r2.q('git merge --no-edit old'); r2.q('python3 build.py'); r2.q('git commit -qam "cut after merging old"')
    r2.sh('git log --oneline -4')
    old = r2.q('git rev-parse old')[1]
    r2.sh(f'git revert --no-edit {old}')
    red = check(r2) != 0
    r2.sh('python3 build.py'); c = r2.count('p') == (0, 0); check(r2)
    return dict(check_red=red, lost=not (a and b and c), note='(a)(b) in step after revert; (c) reverting a pre-split commit touches only the game file: --check red, build.py cut it')

@scenario
def order_both_add(W):
    """Two seats each add a new section as a new piece at the same place in pieces/ORDER."""
    r = fresh(W, 'order_both_add')
    for br, sec in (('seatA', '15c'), ('seatB', '15d')):
        r.q(f'git checkout -q -b {br} integration')
        p = 'pieces/js/s15b-interactions.js'; t = r.read(p)
        new = f'// =====================================================================\n// {sec}. NEW SECTION {sec}\n// =====================================================================\nconst NEW_{sec.upper()} = 1;\n'.encode()
        r.write(f'pieces/js/s{sec}-new.js', new)
        o = r.read('pieces/ORDER').replace(b'js/s15r-rec-activities.js', f'js/s{sec}-new.js                once    1  ^// {sec}\\. NEW\njs/s15r-rec-activities.js'.encode(), 1)
        r.write('pieces/ORDER', o); r.sh('python3 build.py'); r.q('git add -A'); r.q(f'git commit -qm {br}')
    r.q('git checkout -q integration'); r.sh('git merge --no-edit seatA'); r.sh('git merge --no-edit seatB')
    r.sh('git diff --name-only --diff-filter=U')
    t = r.read('pieces/ORDER').decode()
    t = re.sub(r'<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> seatB\n', lambda m: m.group(1) + m.group(2), t, flags=re.S)
    r.write('pieces/ORDER', t.encode()); r.q('git add pieces/ORDER')
    r.sh('python3 build.py'); rc = check(r)
    ok = b'NEW_15C' in r.read('starship-cadet.html') and b'NEW_15D' in r.read('starship-cadet.html')
    return dict(check_red=True, lost=not ok, note='ORDER and the game file clash; keep both lines in ORDER, build.py glues')

@scenario
def rollback(W):
    """Go back to the one-file way: delete pieces/ and the scripts. Then a branch made after the split comes in:
    (a) glued properly; (b) with its last piece edit not glued."""
    r = fresh(W, 'rollback')
    r.q('git checkout -q -b seatA integration'); r.mark('pieces/js/s13-time-save.js', 40, 'ga'); r.q('python3 build.py'); r.q('git commit -qam ga')
    r.q('git checkout -q -b seatB integration'); r.mark('pieces/js/s13-time-save.js', 80, 'gb'); r.q('git commit -qam "gb (not glued)"')
    r.q('git checkout -q integration')
    r.sh('git rm -rq pieces build.py split.py && git commit -qm "rollback: one file again"')
    r.sh('git merge --no-edit seatA'); r.sh('git diff --name-only --diff-filter=U | head -3')
    r.q('git rm -rq pieces 2>/dev/null; git commit -qm "merge seatA"')
    a = b'MARK-ga' in r.read('starship-cadet.html')
    r.sh('git merge --no-edit seatB'); r.q('git rm -rq pieces 2>/dev/null; git commit -qm "merge seatB"')
    b = b'MARK-gb' in r.read('starship-cadet.html')
    log(f'    seatA work in the one file: {a}; seatB (unglued) work in the one file: {b}')
    return dict(check_red=False, lost=not b, note='after a rollback, an unglued piece edit is lost unless every branch passes build.py --check first')

def main(argv):
    W = os.path.abspath(argv[0]); os.makedirs(W, exist_ok=True)
    names = argv[1:] or list(SCEN)
    make_base(W)
    res = {}
    for n in names:
        log(f'\n### {n}\n{SCEN[n].__doc__.strip()}')
        try: res[n] = SCEN[n](W)
        except Exception as e: import traceback; log('    SCENARIO ERROR ' + traceback.format_exc()[-1500:]); res[n] = dict(error=str(e))
        log(f'    RESULT: {res[n]}')
    log('\n## Summary')
    for n, v in res.items(): log(f'- {n}: {v}')
    open(os.path.join(W, 'scenarios.md'), 'w').write('\n'.join(OUT) + '\n')

if __name__ == '__main__':
    main(sys.argv[1:])
