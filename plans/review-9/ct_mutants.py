# PR9: mutants in the controller build (section 26), each run against its controller_check (caught = exit 1)
# usage: python3 ct_mutants.py BUILD_DIR [names]   (BUILD_DIR holds starship-cadet.html, controller_check.py, cadet_test.py)
import sys, subprocess, pathlib, shutil
H = pathlib.Path(sys.argv[1]); src = (H / 'starship-cadet.html').read_text()
M = {
 'c1_walkflip': ("const wx = rx * x - fx * y, wz = rz * x - fz * y", "const wx = rx * x + fx * y, wz = rz * x + fz * y"),   # up on the stick walks down the screen
 'c2_nostop': ("function padWalkEnd() { if (PAD_DECK.walking) { PAD_DECK.walking = false; if (!steering) player.steer = null; } }", "function padWalkEnd() { if (PAD_DECK.walking) { PAD_DECK.walking = false; } }"),   # letting go keeps walking
 'c3_nodevice': ("['dmSheet', () => DM_UI.open], ['device', () => DEV.open], ", "['dmSheet', () => DM_UI.open], "),   # the device missing from the panel list
 'c5_anoop': ("P.chosen = false; tap(s[0], s[1]); P.n = 0;", "P.chosen = false; P.n = 0;"),   # A does nothing
 'c6_eagerring': ("if (PAD_ON) { addEventListener('gamepadconnected', padHello);", "if (PAD_ON) { const _pr = new THREE.Mesh(new THREE.RingGeometry(.4, .5, 40), new THREE.MeshBasicMaterial({ color: col('#4cc3b5') })); _pr.visible = false; scene.add(_pr); addEventListener('gamepadconnected', padHello);"),   # a hidden mesh made at load
 'c7_mislabel': ("if (a) return 'crew:' + a.p.id;", "if (a && !(want && want.startsWith('place:'))) return 'crew:' + a.p.id;"),   # a seat ringed where the tap reaches a person
 'p1_devbackno': ("device: () => { if (DEV.app && DEV.app !== 'home') deviceShow('home'); else deviceClose(); },", "device: () => {},"),   # B does nothing in the device
 'p1_nolanding': ("if (L !== F.layer || L && L !== PAD_HUD && !L.contains(document.activeElement)) { F.layer = L; if (L) padFocusIn(L); }", "if (L !== F.layer) { F.layer = L; }"),   # opening a panel puts the highlight nowhere
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
