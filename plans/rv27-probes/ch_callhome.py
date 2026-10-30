# RV27: the Day 0 call-home card in the real evening (the build's intro_check part 8, --evening or --dawdle), with a per-frame
# tracker from 18:00 to 22:00: your action and its phase, the tray, ate:sat / ate:meal / call:tip, the dialogue and the device card.
# Usage: CADET_WORK=... CADET_CHROME=... python3 ch_callhome.py WORKTREE [--dawdle]
import sys, os, pathlib
WT = pathlib.Path(sys.argv[1]).resolve(); flags = sys.argv[2:]
src = (WT / 'intro_check.py').read_text().replace("__file__.replace('intro_check.py', 'cadet_test.py')", repr(str(WT / 'cadet_test.py')))
TRACK = r'''(() => { if (window.__ch) return; window.__ch = []; let last = '';
  const f = () => { try { const D = SHIP.intro.done, m = ((Math.floor(shipNow()) % 1440) + 1440) % 1440;
    if (m >= 1080 && m < 1320) { const dc = document.getElementById('devDlg'), card = dc && !dc.hidden ? (dc.textContent || '').slice(0, 30) : '';
      const row = [ACT ? ACT.kind + ':' + ACT.phase + (ACT.o && ACT.o.fed ? ':fed' : '') : '-', SHIP.player.tray ? 'tray' : '-', D['ate:sat'] ?? '-', D['ate:meal'] ?? '-', D['call:tip'] ?? '-', D['chief:met'] ?? '-', D['chief:end'] ?? '-', DIALOGUE ? (DIALOGUE.id || '').replace(/:.*/, '') : '-', card, SHIP.intro.step];
      const k = JSON.stringify(row); if (k !== last) { last = k; window.__ch.push([clockText().split(' ').pop(), ...row]); } }
  } catch (e) { window.__ch.push(['err', String(e)]); } requestAnimationFrame(f); }; requestAnimationFrame(f); })()'''
hook = "            r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'follow'])\n"; assert hook in src
src = src.replace(hook, hook + "            g.ev(" + repr(TRACK) + ")\n", 1)
end = "        simnow = g.ev(\"typeof tapCrew"; assert end in src
src = src.replace(end, "        print('RV27 CALL [t, act, tray, ate:sat, ate:meal, call:tip, chief:met, chief:end, dialogue, card, step]'); [print('  ', x) for x in g.ev('window.__ch || []')]\n" + end, 1)
sys.argv = [str(WT / 'intro_check.py'), str(WT / 'starship-cadet.html'), '--dawdle' if '--dawdle' in flags else '--evening']
os.chdir(WT); exec(compile(src, str(WT / 'intro_check.py'), 'exec'))
