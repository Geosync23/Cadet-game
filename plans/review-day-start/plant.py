# RV6: plant faults in DS1's Start at Day N and run devmode_check part days on each (caught = a FAIL line the clean run lacked)
import sys, subprocess, pathlib, re
D = pathlib.Path(__file__).parent; src = (D / 'ds.html').read_text()
P = {
 'wrongday': [("const rec = DM_DAYS.days[n]; if", "const rec = DM_DAYS.days[n > 1 ? n - 1 : n]; if"), ("|| !sv.time || sv.time.day !== n ||", "|| !sv.time ||")],
 'noundo': [("const kept = devmodeKeep('Start at Day ' + n);", "const kept = null;")],
 'realsave': [("const w = devmodeWrite(SAVE_KEY, save);", "try { localStorage.setItem('starship-cadet-save', save); } catch (e) {} const w = devmodeWrite(SAVE_KEY, save);")],
 'nodecomp': [("if (typeof DecompressionStream !== 'function') return devmodeSay(", "if (false) return devmodeSay(")],
 'trackoff': [("if (sv.player.track === null) delete sv.player.track;", "sv.player.track = null;")],
 'nobusy': [("DM_DAYBUSY = false; devmodeSay('The recorded Day ' + n + ' couldn", "devmodeSay('The recorded Day ' + n + ' couldn")],
}
fails = lambda t: {re.sub(r'[-\d.]+', '#', l) for l in t.splitlines() if l.startswith('FAIL')}
def run(html, tag):
    (D / ('g_' + tag + '.html')).write_text(html)
    r = subprocess.run(['python3', 'devmode_check.py', 'g_' + tag + '.html', 'days'], cwd=D, capture_output=True, text=True)
    (D / (tag + '.log')).write_text(r.stdout + r.stderr); return r.stdout + r.stderr
clean = run(src, 'clean'); base = fails(clean); print('clean', 'OK' if 'DEVMODE CHECK OK' in clean else 'NOT OK', sorted(base)[:3], flush=True)
for name in (sys.argv[1:] or P):
    h = src
    for a, b in P[name]: assert h.count(a) == 1, (name, a); h = h.replace(a, b)
    out = run(h, name); new = sorted(fails(out) - base)
    print(name, 'CAUGHT' if new else 'MISSED', new[:2], flush=True)
