# RV2: plant mutants in section 26 itself (CT1's code, not beside it) and run CTT's controller_check parts on each copy.
# Caught = a FAIL line the clean run of the same parts didn't have. Usage:
#   python3 mutants.py GAME.html CHECKDIR CLEAN.log name[:parts] ...    (CHECKDIR holds controller_check.py + cadet_test.py)
import sys, subprocess, pathlib, re, os
CHECK = os.environ.get('MUT_CHECK', 'controller_check.py')   # another check: MUT_CHECK=arrows_check.py (parts '' runs it whole)
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
 # P4 (CP4 db80eb0): run with CP4's controller_check (its settings part)
 'p4_savealways': ("SAVE_EXTRA.push(s => { const d = padSetDiff(); if (d) s.pad = d; });", "SAVE_EXTRA.push(s => { s.pad = padSetDiff() || {}; });", 'settings'),
 'p4_showalways': ("const padSetSeen = () => PAD_ON && (PAD.live || !!PAD.id || !!padSetDiff());", "const padSetSeen = () => PAD_ON;", 'settings'),
 'p4_noclash': ("  [phy[n], phy[other]] = [k, phy[n]];", "  phy[n] = k;", 'settings'),
 'p4_noflip': ("PAD.rs[1] * (PAD_SET.flip ? -1 : 1)", "PAD.rs[1]", 'settings'),
 'p4_oddsave': ("if (new Set(all).size !== all.length) S.map = {};", "", 'settings'),
 'p4_nogentle': ("if (PAD_SET.walk === 'gentle' && PAD_DECK.walking", "if (false && PAD_DECK.walking", 'settings'),
 'p4_noeat': ("  for (const n of PAD_BTN) for (const e of [n, n + ':up']) (PAD.on[e] = PAD.on[e] || []).unshift(() => PAD_SET_UI.listen || PAD_SET_UI.eat ? true : undefined);", "", 'settings'),
 # P3 47d71ff (CP3's five fixes)
 'p3b_saidalways': ("  if (!PAD_MARK.said) PAD_MARK.say = true;", "  PAD_MARK.say = true;", 'marks'),
 'p3b_overtoast': ("  if (PAD_MARK.say && PAD.used && !toastEl.classList.contains('show')) {", "  if (PAD_MARK.say && PAD.used) {", 'marks'),
 'p3b_nounuse': ("  if (!padList().filter(g => g.index !== PAD.goneIdx).length) padUnuse();", "", 'drop'),
 'p3b_saynow': ("  if (!PAD_MARK.said) PAD_MARK.say = true;", "  if (!PAD_MARK.said) { PAD_MARK.said = true; toast('Controller connected', 'x'); }", 'marks drop'),
 # P5 4892a0b (CP5's five fixes)
 'p5b_keepattr': ("  if (!PAD_A11Y.toast) return; for (const a of PAD_A11Y.toast) toastEl.removeAttribute(a); PAD_A11Y.toast = false;", "", 'a11y'),
 'p5b_glyphname': ("if (/\\p{L}/u.test(t)) return t;   // a mark alone", "if (t) return t;   // a mark alone", 'a11y'),
 'p5b_nomaps': ("  ['#device button', el => DEV.app === 'maps'", "  ['#nothing', el => DEV.app === 'maps'", 'a11y'),
 # arrows piece B (AR1 c0ab64c): MUT_CHECK=arrows_check.py, parts '-' (the whole check)
 'ar_levels': ("return out.sort((a, b) => a.level - b.level ||", "return out.sort((a, b) => b.level - a.level ||", '-'),
 'ar_track': (".filter(e => SHIP.player.track !== null || e.level <= 2);", ";", '-'),
 'ar_direct': ("  if (IX_GOAL && e.level > 1) return null;", "", '-'),
 'ar_body': ("  if (e.level >= 5 && jobGoal) return null;", "", '-'),
 'ar_nocount': ("    if (guideLimit(e)) SHIP.guide.seen[e.id] = (SHIP.guide.seen[e.id] || 0) + 1;", "", '-'),
 'ar_tqmin': ("const TQ_MIN = 2500, TQ_MAX = 3;", "const TQ_MIN = 500, TQ_MAX = 3;", '-'),
 'ar_nomerge': ("  if (shown === t + '|' + x || GUIDE.tq.some(q => q[0] === t && q[1] === x)) return true;", "", '-'),
 'ar_saveoff': ("SAVE_EXTRA.push(s => { if (!GUIDE_ON) return;", "SAVE_EXTRA.push(s => {", '-'),
 'ar_throwkeeps': ("catch (err) { done = true; }", "catch (err) { done = false; }", '-'),
 # arrows piece C (AC1 47e55bb4): MUT_CHECK=arrows_pointer_check.py, parts '-'
 'ac_showrow': ("const teachShown = () => { let g = false;", "const teachShown = () => true, _ts0 = () => { let g = false;", '-'),
 'ac_nocount': ("  if (show && !show.e.shown) { show.e.shown = true; pointCount(show.e.id); }", "  if (show && !show.e.shown) { show.e.shown = true; }", '-'),
 'ac_offlets': ("return m === 'off' ? 0 : m === 'all'", "return m === 'off' ? 1 : m === 'all'", '-'),
 'ac_nocover': ("const hit = document.elementFromPoint(x, y); if (!hit || hit !== el && !el.contains(hit)) return null;", "", '-'),
 'ac_tapkeeps': ("  if (st && st.press && st.el === POINT.aim) pointDrop(c.id);", "", '-'),
 'ac_firststep': ("    const s = e.path[i]; if (s.open && s.open()) continue;", "    const s = e.path[i];", '-'),
 # arrows B 5dd6b6f (AR1's tip with RV2's points)
 'ar2_direct': ("  if (IX_GOAL && e.level > 1) { GUIDE.shown = null; GUIDE.covered = e.id; return null; }", "", '-'),
 'ar2_body': ("  if (e.level >= 5 && jobGoal) { GUIDE.shown = null; return null; }", "", '-'),
 'ar2_nomerge': ("  if (GUIDE.tq.some(q => q[0] === t && q[1] === x)) return true;", "", '-'),
 'ar2_norecheck': ("  if (fin) { guideDrop(e.id); e = guidePick(); if (!e) { GUIDE.shown = null; return null; } }", "", '-'),
 'ar2_retime': ("  if (shown === t + '|' + x && !GUIDE.tq.length) return false;", "", '-'),
 't3_noface':    ("const fx = Math.sin(player.face || 0), fz = Math.cos(player.face || 0);", "const fx = 0, fz = 0;", 'pick'),
 # arrows piece E (AR1 14cffba): MUT_CHECK=arrows_check.py, parts queue (or 'week guide')
 'ae_from': ("from: r.at - 15, until: r.at + r.len,", "from: r.at - 45, until: r.at + r.len,", 'queue'),
 'ae_level': ("guideAsk({ id: 'train:' + c.id + ':meet:' + c.d, level: 2,", "guideAsk({ id: 'train:' + c.id + ':meet:' + c.d, level: 4,", 'queue'),
 'ae_meetdone': ("      done: () => guideStage(c.id, 'meet') });", "      done: () => false });", 'queue'),
 'ae_meetroom': ("goal: () => ({ deck: r.deck, room: r.room, crew: c.by,", "goal: () => ({ deck: r.deck, room: 'w', crew: c.by,", 'queue'),
 'ae_nowatch': ("  } else if (c.st === 'watch') {", "  } else if (c.st === 'watchx') {", 'queue'),
 'ae_watchcrew': ("goal: () => ({ deck: s.deck, crew: c.by, at: s.tile,", "goal: () => ({ deck: s.deck, at: s.tile,", 'queue'),
 'ae_watchlevel': ("guideAsk({ id: 'train:' + c.id + ':watch', level: 3,", "guideAsk({ id: 'train:' + c.id + ':watch', level: 6,", 'queue'),
 'ae_dodone': ("      done: () => guideTaken(c.j) || guideStage(c.id, 'do') });", "      done: () => guideStage(c.id, 'do') });", 'queue'),
 'ae_nodo': ("  } else if (c.st === 'do' && c.j) {", "  } else if (c.st === 'dox' && c.j) {", 'queue'),
 'ae_notick': ("try { guideTrain(); } catch (e) { /* 24 core not ready */ }", "", 'queue'),
 'ae_throw': ("const row = ladderRow(c.id); if (!row) return;\n  const now", "const row = ladderRow(c.id); if (!row) return; null.x;\n  const now", 'queue'),
 # arrows E fixes (AC1 d99a9e50)
 'ae2_level': ("guideAsk({ id: 'train:' + c.id + ':meet:' + c.d, level: 2,", "guideAsk({ id: 'train:' + c.id + ':meet:' + c.d, level: 4,", 'queue'),
 'ae2_crewalways': ("...(guideTeacherIn(c.by, r.deck, r.room) ? { crew: c.by } : {}),", "crew: c.by,", 'queue'),
 'ae2_nowatch': ("  } else if (c.st === 'watch') {", "  } else if (c.st === 'watchx') {", 'queue'),
 'ae2_watchcrew': ("goal: () => ({ deck: s.deck, crew: c.by, at: s.tile,", "goal: () => ({ deck: s.deck, at: s.tile,", 'queue'),
 'ae2_watchday': ("id: 'train:' + c.id + ':watch:' + c.d,", "id: 'train:' + c.id + ':watch',", 'queue'),
 'ae2_dodone': ("      done: () => guideTaken(c.j) || guideStage(c.id, 'do') });", "      done: () => guideStage(c.id, 'do') });", 'queue'),
 'ae2_overjob': ("return m && m.id !== c.j ? null :", "return false ? null :", 'queue'),
 'ae2_offer': ("} else if (c.st === 'do' && c.j && !(WORK_MECH[c.id] || {}).offer) {", "} else if (c.st === 'do' && c.j) {", 'queue'),
 'ae2_notick': ("try { guideTrain(); } catch (e) { if (!GUIDE.trainWarned)", "try { 0; } catch (e) { if (!GUIDE.trainWarned)", 'queue'),
 'ae2_emptyshown': ("  if (!g || !g.deck) { GUIDE.shown = null; return null; }", "  if (!g || !g.deck) return null;", 'queue'),
 # arrows F3/F4 (AC1 bd18997): MUT_CHECK=arrows_f_check.py, parts '-'
 'af_follownow': ("  const g = q.g; if (!q.by ||", "  const g = q.g; return g; if (!q.by ||", '-'),
 'af_valve0': ("pointCard(line.length - 1, worksText('inc.point.valve'", "pointCard(0, worksText('inc.point.valve'", '-'),
 'af_track': ("  return g => { SHIP.player.track = tk; ", "  return g => { ", '-'),
 'af_scanhs': ("if (!j || !j.scan || j.picked || caseOf(j)) {", "if (!j || !j.scan || j.picked) {", '-'),
 'af_call2': ("else if (can.length === 1 && !c.long", "else if (can.length <= 2 && !c.long", '-'),
 'af_nextdone': ("x.got.includes(k.id) || x.calls.length > calls; } });", "x.got.includes(k.id); } });", '-'),
 'af_stopoff': ("  if (!incGuide() || j.inc !== 'burst' || j.walk) return null;", "  if (j.inc !== 'burst' || j.walk) return null;", '-'),
 'af_nowait': ("{ open: () => performance.now() - F3P.scanT > 3000,", "{ open: () => true,", '-'),
 'af_inclevel': ("guideAsk({ id: 'inc:m6', level: 1,", "guideAsk({ id: 'inc:m6', level: 3,", '-'),
 'af_incclear': ("  if (INC_GOAL.q) { INC_GOAL.q = null; if (typeof guideDrop === 'function') guideDrop('inc:m6'); }", "", '-'),
}
fails = lambda t: {re.sub(r'[-\d.]+', '#', l) for l in t.splitlines() if l.startswith('FAIL')}
base = fails(CLEAN.read_text())
for arg in sys.argv[4:]:
    name, _, parts = arg.partition(':'); a, b, dp = M[name]; parts = (parts or dp).split()
    assert src.count(a) == 1, (name, src.count(a))
    d = CK / ('mut_' + name); d.mkdir(exist_ok=True)
    for f in (CHECK, 'cadet_test.py'): (d / f).write_text((CK / f).read_text())
    (d / 'game.html').write_text(src.replace(a, b))
    r = subprocess.run(['python3', CHECK, 'game.html'] + [x for x in parts if x != '-'], cwd=d, capture_output=True, text=True)
    (d / 'out.log').write_text(r.stdout + r.stderr)
    new = sorted(fails(r.stdout) - base)
    print(name, parts, 'CAUGHT' if new else 'MISSED', new[:3], flush=True)
