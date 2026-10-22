# PR9: mutants in the controller build (section 26), each run against its controller_check (caught = exit 1)
# usage: python3 ct_mutants.py BUILD_DIR [names]   (BUILD_DIR holds starship-cadet.html, controller_check.py, cadet_test.py)
import sys, subprocess, pathlib, shutil
H = pathlib.Path(sys.argv[1]); src = (H / 'starship-cadet.html').read_text()
M = {
 'c1_walkflip': ("const wx = rx * x - fx * y, wz = rz * x - fz * y", "const wx = rx * x + fx * y, wz = rz * x + fz * y"),   # up on the stick walks down the screen
 'c2_nostop': ("function padWalkEnd() { if (PAD_DECK.walking) { PAD_DECK.walking = false; if (!steering) player.steer = null; } }", "function padWalkEnd() { if (PAD_DECK.walking) { PAD_DECK.walking = false; } }"),   # letting go keeps walking
 'c3_nodevice': ("['dmSheet', () => DM_UI.open], ['device', () => DEV.open], ", "['dmSheet', () => DM_UI.open], "),   # the device missing from the panel list
 'c4_noback': ("addEventListener('pointerdown', back, true); ", ""),   # a touch doesn't hand back
}
for n in sys.argv[2:] or list(M):
    a, b = M[n]; assert src.count(a) == 1, (n, src.count(a))
    d = pathlib.Path('/tmp/claude-0/-home-user-Cadet-game/c90be8f5-63df-55cd-b247-474233586f38/scratchpad/ctmut/' + n); d.mkdir(parents=True, exist_ok=True)
    for f in ('cadet_test.py', 'controller_check.py'): shutil.copy(H / f, d / f)
    (d / 'starship-cadet.html').write_text(src.replace(a, b))
    r = subprocess.run(['python3', 'controller_check.py', 'starship-cadet.html'], cwd=d, capture_output=True, text=True)
    fl = [l for l in r.stdout.splitlines() if 'FAIL' in l]
    print(n, 'CAUGHT' if r.returncode == 1 else 'MISSED (rc %d)' % r.returncode, fl[:3], flush=True)
