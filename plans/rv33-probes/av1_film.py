import sys, json, base64, pathlib
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
on, out = sys.argv[1], sys.argv[2]
R3_AT = r"""(([t, deck, room]) => { skipTo(t); goToDeck(deck); const R = DECKS[deck].rooms, k = R[room] ? room : Object.keys(R).find(x => R[x].name === room);
  const tl = ROOM_TILES[k]; if (!tl || !tl.length) return 'no tiles for ' + room; player.obj.position.copy(cellPos(...tl[(tl.length / 2) | 0])); return k; })"""
with sync_playwright() as pw:
    g = Game(pw, on, w=390, h=844)
    g.ev("flagSet('rec.filmMoved', 1); flagSet('rec.allHands', 1)")
    print(g.ev(f"({R3_AT})({json.dumps([5 * 1440 + 20 * 60 + 10, 7, 'A'])})")); g.step(60)
    g.ev("if (typeof dialogueClose === 'function') try { dialogueClose(); } catch (e) {}")
    # stand about 6 m in front of the screen, camera turned so the screen faces us
    sp = g.ev("(() => { const v = new THREE.Vector3(); REC_SHOW.piv.getWorldPosition(v); return [v.x, v.y, v.z]; })()"); print('screen at', sp)
    for k, wait in enumerate([3, 9, 17, 31, 45, 59]):
        g.page.wait_for_timeout(0); g.step(int(30 * (wait - (0 if k == 0 else [3, 9, 17, 31, 45, 59][k - 1]))) )
        url = g.ev("REC_FILM_CV.cv.toDataURL('image/png')"); pathlib.Path(out + f'/film_canvas_{k}.png').write_bytes(base64.b64decode(url.split(',')[1]))
        print(k, g.ev("[REC_SHOW.state, REC_FILM_CV.n, lastRoom, renderer.info.render.calls]"))
    for a in range(8):
        g.ev(f"az = azT = {a} * Math.PI / 4"); g.step(20); g.page.screenshot(path=out + f'/film_az{a}.png')
    print([e for e in g.errors if 'pageerror' in e][:3])
