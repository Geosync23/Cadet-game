#!/usr/bin/env python3
"""section.py: find your way round the one-file game by its sections (the file's own "// 19. DEVICE" headings).

    python3 tools/section.py                      list every section: id, first and last line, size, heading
    python3 tools/section.py 19                   print section 19 with game line numbers (also: 24a, 15b, ...)
    python3 tools/section.py DEVICE               the same, by a word of the heading (must name one section)
    python3 tools/section.py 19 --head 40         only the first 40 lines of it
    python3 tools/section.py --where 23456 ...    the section a game line is in (browser errors, grep hits)
    python3 tools/section.py --diff [A [B]]       which sections a change touches, with the owner from plans/owners.md:
                                                  no A: your uncommitted changes; A: A to now (with uncommitted);
                                                  A B: A to B (e.g. --diff origin/claude/shared HEAD, or a branch's
                                                  merge base: --diff $(git merge-base origin/claude/shared HEAD) HEAD)
    --game FILE                                   another copy of the game (default starship-cadet.html)

A heading is a line at column 0: "// " then a number with an optional letter, an optional dot, a space and a word in
capitals ("// 1. SETUP", "// 15b. PLAYER INTERACTIONS", "// 24a ROUNDS"). Lines before the first heading are "page"
(HTML and CSS); the last section runs to the end of the file. names_check.js names sections by the same rule.
Section ids are not unique forever: if two headings share an id, both are listed and --diff names each by its line.
Changes nothing; exits 1 on a bad argument.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD_RE = re.compile(r"^// (\d+[a-z]?)\.? ([A-Z][A-Z&'()-]+\b.*)$")


def sections(lines):
    """[(id, first line, last line, heading)] in file order; 1-based, inclusive."""
    out = [['page', 1, None, 'the page: HTML head, CSS, body (before section 1)']]
    for i, l in enumerate(lines, 1):
        m = HEAD_RE.match(l)
        if m:
            out[-1][2] = i - 1
            out.append([m.group(1), i, None, m.group(2).strip()])
    out[-1][2] = len(lines)
    return [tuple(s) for s in out]


def where(secs, n):
    for s in secs:
        if s[1] <= n <= s[2]:
            return s
    return None


def owners():
    """{section id: owner} from plans/owners.md's table rows that start | `19` | ... | owner |."""
    o = {}
    try:
        for l in open(os.path.join(ROOT, 'plans', 'owners.md'), encoding='utf-8'):
            m = re.match(r'^\|\s*`([0-9a-z]+)`\s*\|(.*)\|\s*$', l)
            if m:
                o[m.group(1)] = m.group(2).split('|')[-1].strip()
    except OSError:
        pass
    return o


def short(h, n=60):
    return h if len(h) <= n else h[:n - 3].rstrip() + '...'


def git(*a):
    return subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')


def diff_sections(game_rel, a, b):
    """Changed line counts per section: removed lines placed by the old file's sections, added by the new file's."""
    rng = [a, b] if b else ([a] if a else [])
    d = git('diff', '-U0', '--no-color', *rng, '--', game_rel)
    if d.returncode:
        sys.exit('section.py: git diff failed: ' + d.stderr.strip())
    old_text = git('show', f'{a}:{game_rel}').stdout if a else git('show', f'HEAD:{game_rel}').stdout
    new_text = git('show', f'{b}:{game_rel}').stdout if b else open(os.path.join(ROOT, game_rel), encoding='utf-8').read()
    olds, news = sections(old_text.split('\n')), sections(new_text.split('\n'))
    hits = {}   # (id, heading) -> [removed, added, first new line]
    for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', d.stdout, re.M):
        o0, oc, n0, nc = int(m.group(1)), int(m.group(2) or 1), int(m.group(3)), int(m.group(4) or 1)
        for k in range(oc):
            s = where(olds, o0 + k)
            h = hits.setdefault((s[0], s[3]), [0, 0, None]); h[0] += 1
        for k in range(nc):
            s = where(news, n0 + k)
            h = hits.setdefault((s[0], s[3]), [0, 0, None]); h[1] += 1
            h[2] = h[2] or n0 + k
    return hits


def main(argv):
    game = os.path.join(ROOT, 'starship-cadet.html')
    if '--game' in argv:
        k = argv.index('--game'); game = os.path.abspath(argv[k + 1]); del argv[k:k + 2]
    head = None
    if '--head' in argv:
        k = argv.index('--head'); head = int(argv[k + 1]); del argv[k:k + 2]
    lines = open(game, encoding='utf-8').read().split('\n')
    secs = sections(lines)
    if not argv:
        for s in secs:
            print(f'{s[0]:>5}  {s[1]:>6}-{s[2]:<6} {s[2] - s[1] + 1:>6} lines  {short(s[3], 80)}')
        return 0
    if argv[0] == '--where':
        for a in argv[1:]:
            s = where(secs, int(a))
            print(f'line {a}: ' + (f'section {s[0]} ({short(s[3])}), lines {s[1]}-{s[2]}' if s else 'past the end of the file'))
        return 0
    if argv[0] == '--diff':
        rel = os.path.relpath(game, ROOT)
        a = argv[1] if len(argv) > 1 else None
        b = argv[2] if len(argv) > 2 else None
        hits = diff_sections(rel, a, b)
        if not hits:
            print('no change to ' + rel); return 0
        own = owners()
        print(f'{rel}: {"uncommitted changes" if not a else a + " to " + (b or "now")} touch {len(hits)} section(s):')
        for (sid, h), (rm, ad, first) in sorted(hits.items(), key=lambda kv: (kv[1][2] or 0)):
            who = own.get(sid, 'no owner listed')
            print(f'  {sid:>5}  -{rm:<5} +{ad:<5} {short(h, 50):<50}  owner: {who}' + (f'  (first new line {first})' if first else ''))
        return 0
    q = ' '.join(argv)
    hit = [s for s in secs if s[0] == q] or [s for s in secs if q.lower() in s[3].lower()]
    if not hit:
        print(f'section.py: no section "{q}"; run with no arguments for the list'); return 1
    if len(hit) > 1:
        print(f'section.py: "{q}" names {len(hit)} sections; give its id:')
        for s in hit:
            print(f'  {s[0]:>5}  line {s[1]}  {short(s[3], 80)}')
        return 1
    s = hit[0]
    end = s[2] if head is None else min(s[2], s[1] + head - 1)
    for n in range(s[1], end + 1):
        print(f'{n:>6}  {lines[n - 1]}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
