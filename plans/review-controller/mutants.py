# RV2: plant mutants in section 26 itself (CT1's code, not beside it) and run CTT's controller_check parts on each copy.
# Caught = a FAIL line the clean run of the same parts didn't have. Usage:
#   python3 mutants.py GAME.html CHECKDIR CLEAN.log name[:parts] ...    (CHECKDIR holds controller_check.py + cadet_test.py)
import sys, subprocess, pathlib, re
GAME, CK, CLEAN = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
src = GAME.read_text()
M = {   # name: (old, new, parts)   turn 3 (0.90.2) first
 't3_noop_crew': ("  if (!s) return true;\n  P.chosen = false; tap(s[0], s[1]);", "  if (!s || t.key.startsWith('crew:')) return true;\n  P.chosen = false; tap(s[0], s[1]);", 'pick'),
 't3_offset':    ("P.chosen = false; tap(s[0], s[1]);", "P.chosen = false; tap(s[0] + 40, s[1] + 40);", 'pick'),
 't3_ringload':  ("padOn('unuse', () => { if (PAD_PICK.ring) padPickShow(false); });", "padOn('unuse', () => { if (PAD_PICK.ring) padPickShow(false); });\nif (PAD_ON) padPickShow(true);", 'idle calls'),
 't3_nounuse':   ("padOn('unuse', () => { if (PAD_PICK.ring) padPickShow(false); });", "", 'touch'),
 't3_rand':      ("  const J = P.job; P.cs = J.cs;", "  R(); const J = P.job; P.cs = J.cs;", 'touch'),
 'pr9_c6_eagerring': ("if (PAD_ON) { addEventListener('gamepadconnected', padHello);", "if (PAD_ON) { const _pr = new THREE.Mesh(new THREE.RingGeometry(.4, .5, 40), new THREE.MeshBasicMaterial({ color: col('#4cc3b5') })); _pr.visible = false; scene.add(_pr); addEventListener('gamepadconnected', padHello);", 'idle calls'),   # PR9's c6_eagerring
 'pr9_c7_mislabel': ("if (a) return 'crew:' + a.p.id;", "if (a && !(want && want.startsWith('place:'))) return 'crew:' + a.p.id;", 'pick'),   # PR9's c7_mislabel
 # P5 (CP5 adffcbe5): run with CP5's controller_check (its a11y part)
 'p5_rmonce': ("  return !!(A.rmq && A.rmq.matches);\n}", "  if (A.v === undefined) A.v = !!(A.rmq && A.rmq.matches); return A.v;\n}", 'a11y'),
 'p5_notoast': ("  if (!toastEl.hasAttribute('aria-live')) toastEl.setAttribute('aria-live', 'polite');", "", 'a11y'),
 'p5_thin': ("body.pad :focus{outline:4px solid #4cc3b5!important", "body.pad :focus{outline:2px solid #4cc3b5!important", 'a11y'),
 'p5_noedge': (",0 0 0 9px #0d1521!important}'", ",0 0 0 9px rgba(13,21,33,0)!important}'", 'a11y'),
 # P3 (CP3 efbe62a): run with CP3's controller_check (its marks, touch, drop parts)
 'p3_markload': ("const padFam = () =>", "if (PAD_ON) setTimeout(() => padMarksSync(), 0);\nconst padFam = () =>", 'marks'),
 'p3_alwaysshow': ("'body.pad .padk{display:inline-flex}", "'.padk{display:inline-flex}", 'touch'),
 'p3_nopause': ("  if (PAD.goneUsed && !PAUSE.on) { PAD_MARK.why = true; pauseSet(true); }", "", 'drop'),
 'p3_pausealways': ("  if (PAD.goneUsed && !PAUSE.on) {", "  if (!PAUSE.on) {", 'drop'),
 'p3_norestore': ("  else if (!on && PAD_MARK.line) { ln.textContent = PAD_MARK.line; PAD_MARK.line = ''; }", "", 'drop'),
 'p3_saidalways': ("  if (!PAD_MARK.said) { PAD_MARK.said = true;", "  if (true) { PAD_MARK.said = true;", 'marks'),
 'p3_ninA': ("nin: { a: ['B', '#e6f0f1', 'B']", "nin: { a: ['A', '#e6f0f1', 'A']", 'marks'),
 'p3_nounuse': ("  if (!padList().length) padUnuse();", "", 'drop'),
 't3_noface':    ("const fx = Math.sin(player.face || 0), fz = Math.cos(player.face || 0);", "const fx = 0, fz = 0;", 'pick'),
}
fails = lambda t: {re.sub(r'[-\d.]+', '#', l) for l in t.splitlines() if l.startswith('FAIL')}
base = fails(CLEAN.read_text())
for arg in sys.argv[4:]:
    name, _, parts = arg.partition(':'); a, b, dp = M[name]; parts = (parts or dp).split()
    assert src.count(a) == 1, (name, src.count(a))
    d = CK / ('mut_' + name); d.mkdir(exist_ok=True)
    for f in ('controller_check.py', 'cadet_test.py'): (d / f).write_text((CK / f).read_text())
    (d / 'game.html').write_text(src.replace(a, b))
    r = subprocess.run(['python3', 'controller_check.py', 'game.html'] + parts, cwd=d, capture_output=True, text=True)
    (d / 'out.log').write_text(r.stdout + r.stderr)
    new = sorted(fails(r.stdout) - base)
    print(name, parts, 'CAUGHT' if new else 'MISSED', new[:3], flush=True)
