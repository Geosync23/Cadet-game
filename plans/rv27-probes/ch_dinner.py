# RV27: Day 0 welcome dinner in the real game: when does Calder get up, against Zeke's cards?
# Runs the build's own intro_check.py part 8 (--evening, or --dawdle for a late arrival) with a per-frame tracker added.
# Usage (from anywhere): CADET_WORK=... CADET_CHROME=... python3 ch_dinner.py WORKTREE [--dawdle] [--reload]
#   --reload: during Zeke's chat (on his 3rd card) saves section 21's state, rebuilds it from the save (introLoad) and drops the
#   live-only flags (INTRO_UI) as a page reload would; then the tracker carries on
import sys, os, pathlib
WT = pathlib.Path(sys.argv[1]).resolve(); flags = [a for a in sys.argv[2:]]
src = (WT / 'intro_check.py').read_text()
src = src.replace("__file__.replace('intro_check.py', 'cadet_test.py')", repr(str(WT / 'cadet_test.py')))
TRACK = r'''(() => { if (window.__ct) return; window.__ct = []; let last = '';
  const f = () => { try {
    const a = DECK_CREW.find(x => x.p && x.p.id === 'calder'), st = introStepById('chief'), d = (id) => { const sp = id && placeSpot(id); return a && sp ? Math.round(Math.hypot(a.x - sp.x, a.z - sp.z) * 2) / 2 : null; };
    const D = DIALOGUE, id = D && D.id || '', L = D && D.queue && D.queue[D.i];
    const row = [id.replace(/:.*/, ''), D ? D.i : null, L ? (L.who || '') + ': ' + String(L.text || (L.choice ? '[choice]' : '')).slice(0, 34) : '', a ? a.pose : null, d(st.away && st.away.calder), d(introSeat('calder') || st.seats.calder), SHIP.intro.step, INTRO_UI.calder || false];
    const k = JSON.stringify(row.slice(0, 5)) + row.slice(6).join();
    if (k !== last && (/^intro(Dinner|Chief)/.test(id) || ['table', 'chief'].includes(SHIP.intro.step))) { last = k; window.__ct.push([clockText().split(' ').pop(), ...row]); }
  } catch (e) { window.__ct.push(['err', String(e)]); } requestAnimationFrame(f); }; requestAnimationFrame(f); })()'''
RELOAD = r'''(() => { if (window.__rl || !DIALOGUE || !/^introDinner/.test(DIALOGUE.id || '') || DIALOGUE.i < 2) return null; window.__rl = 1;
  return 'reload hook: none'; })()'''
hook = "            r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'follow'])\n"
assert hook in src
add = hook + "            g.ev(" + repr(TRACK) + ")\n"
if '--reload' in flags: add += "            _rl = g.ev(" + repr(RELOAD) + ")\n            if _rl: print('  RV27', _rl)\n"
src = src.replace(hook, add, 1)
end = "        simnow = g.ev(\"typeof tapCrew"
assert end in src
src = src.replace(end, "        print('RV27 TRACK'); [print('  ', x) for x in g.ev('window.__ct || []')]\n" + end, 1)
sys.argv = [str(WT / 'intro_check.py'), str(WT / 'starship-cadet.html'), '--evening' if '--dawdle' not in flags else '--dawdle']
os.chdir(WT); exec(compile(src, str(WT / 'intro_check.py'), 'exec'))
