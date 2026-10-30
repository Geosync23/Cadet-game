#!/usr/bin/env python3
"""add_slots.py: put one labelled, empty append slot per seat into the game file (comment lines only).

    python3 tools/add_slots.py [GAME.html] [OUT.html]     default: starship-cadet.html in place

Each slot goes at the end of its seat's main section, just before the next section's heading (the blank line and the
"// =====" rule above it stay where they are):

    <the section's last line>

    // ---- slot: Sim engineer (section 14). New code of this seat's goes here, above the end line (plans/owners.md) ----
    // ---- end of slot: Sim engineer ----

    // =====================================================================
    // 19. DEVICE

Two seats then never add lines at the same spot, so git merges their additions without a clash (SR2's option d; the
split rehearsal counted 260 of 606 remaining clashes as same-spot additions). Refuses (changes nothing) if a heading is
missing or found twice, if a slot is already there, or if a slot would land inside a statement (it must sit between two
top-level statements of the game's script; acorn from $CADET_WORK/acorn/package, via node). Afterwards it proves that
removing exactly the added lines gives back the original file, byte for byte.
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# (seat, its main section, the heading of the section that follows it in the file)
SLOTS = [
    ('Deck architect', '4d', '// 4e. '),
    ('Rec engineer', '4e', '// 5. LIGHTING'),
    ('Sim engineer', '14', '// 19. DEVICE'),
    ('Device engineer', '19', '// 15. PLAYER NEEDS'),
    ('Player engineer', '15', '// 15b. '),
    ('Interactions engineer', '15b', '// 15r. '),
    ('Galley engineer', '16', '// 17. MACHINES'),
    ('Systems engineer', '17', '// 22. LINES'),
    ('Dialogue engineer', '22', '// 18. SHIP EVENTS'),
    ('Traditions engineer', '18', '// 20. SOCIAL'),
    ('Social engineer', '20c', '// 21. ARRIVAL'),
    ('Onboarding engineer', '21b', '// 23. TILES'),
    ('Games engineer', '23b', '// 24. WORK'),
    ('Puzzles seat', '24k', '// 24e TUNING'),
    ('Works career engineer', '24p', '// 6. CAMERA'),
    ('Performance engineer', '8b', '// 9. CREW DATA'),
    ('HUD seat', '11', '// 12. MAIN LOOP'),
]


def slot_lines(seat, sec):
    return ['',
            f'// ---- slot: {seat} (section {sec}). New code of this seat\'s goes here, above the end line (plans/owners.md) ----',
            f'// ---- end of slot: {seat} ----']


def top_level_gaps(text):
    """Offsets (in the file) of the ends of the game script's top-level statements, from acorn via node."""
    acorn = os.path.join(os.environ.get('CADET_WORK', '/tmp/cadet-work'), 'acorn/package/dist/acorn.js')
    js = r'''
const fs = require('fs'), acorn = require(process.argv[1]); const html = fs.readFileSync(0, 'utf8');
const a = html.indexOf('<script>\n') + 9, src = html.slice(a, html.lastIndexOf('</script>'));
const ast = acorn.parse(src, { ecmaVersion: 2022, sourceType: 'script' });
const iife = ast.body.find(s => s.type === 'ExpressionStatement' && s.expression.type === 'CallExpression' && s.expression.callee.type === 'ArrowFunctionExpression');
console.log(JSON.stringify(iife.expression.callee.body.body.map(s => [a + s.start, a + s.end])));'''
    r = subprocess.run(['node', '-e', js, acorn], input=text, capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        sys.exit('add_slots: the game does not parse: ' + r.stderr.strip()[-300:])
    return json.loads(r.stdout)


def main(argv):
    src = argv[0] if argv else os.path.join(ROOT, 'starship-cadet.html')
    out = argv[1] if len(argv) > 1 else src
    text = open(src, encoding='utf-8', newline='').read()
    if '// ---- slot: ' in text:
        sys.exit('add_slots: STOPPED, the file already has slots; nothing changed')
    lines = text.split('\n')
    stmts = top_level_gaps(text)
    offs = [0]
    for l in lines:
        offs.append(offs[-1] + len(l) + 1)
    inserts = []   # (index of the line to insert before, lines)
    for seat, sec, head in SLOTS:
        hits = [i for i, l in enumerate(lines) if l.startswith(head)]
        if len(hits) != 1:
            sys.exit(f'add_slots: STOPPED, heading "{head}" found {len(hits)} times; nothing changed')
        i = hits[0] - 1                                   # the rule line above the heading
        while i > 0 and lines[i - 1].strip() == '':      # and the blank line(s) above it
            i -= 1
        at = offs[i]
        inside = [s for s in stmts if s[0] < at < s[1]]
        if inside:
            sys.exit(f'add_slots: STOPPED, the {seat} slot (line {i + 1}) would sit inside a statement; nothing changed')
        inserts.append((i, slot_lines(seat, sec)))
    new = list(lines)
    for i, add in sorted(inserts, reverse=True):
        new[i:i] = add
    result = '\n'.join(new)
    # proof: removing exactly the added lines gives back the original, byte for byte
    added = {l for _, add in inserts for l in add if l}
    # (each slot brings a blank line right before its slot line: drop those too)
    back2, k = [], 0
    while k < len(new):
        if new[k] == '' and k + 1 < len(new) and new[k + 1].startswith('// ---- slot: '):
            k += 1; continue
        if new[k] in added:
            k += 1; continue
        back2.append(new[k]); k += 1
    if '\n'.join(back2) != text:
        sys.exit('add_slots: STOPPED, the proof failed (removing the slots does not give back the original); nothing written')
    open(out, 'w', encoding='utf-8', newline='').write(result)
    print(f'add_slots: {len(inserts)} slots added ({3 * len(inserts)} lines, comments and blank lines only); '
          f'removing them gives back the original byte for byte. Wrote {out}')


if __name__ == '__main__':
    main(sys.argv[1:])
