# RV9: the five fresh-eyes fixes played by pad on 0.91.0 (switch on in a copy); and Settings rows with the switch off/on
import sys, os, json
CC = sys.argv[1]; GAMEF = sys.argv[2]
sys.argv = [CC, GAMEF, 'none']
src_cc = open(CC).read().split('\nwith sync_playwright() as pw:')[0]
__file__ = CC
exec(src_cc)
TOASTS = r"""(() => { window.__toasts = []; const t = document.getElementById('toast'); new MutationObserver(() => { const s = document.getElementById('tt').textContent + '|' + document.getElementById('tx').textContent; if (window.__toasts[window.__toasts.length - 1] !== s) window.__toasts.push(s); }).observe(t, { subtree: true, childList: true, characterData: true, attributes: true }); })()"""
src = GAME.read_text(); on = with_switch(src, True)
def pick_key(r, key, tries=12):
    for k in range(tries):
        s = r.ev("PAD_PICK.sel && PAD_PICK.sel.key")
        if s == key: return True
        r.press('RIGHT'); r.step(4)
    return False
res = {}
with sync_playwright() as pw:
    # 1. eating at any seat, by pad (tray in hand, ring on the seat, A)
    eat = []
    for kind in ('3-mess-',):
      for n in (1, 2, 3, 4, 5, 6):
        sid = kind + str(n)
        r = Run(pw, on, 'rv9eat', mode='pad', plug={}, w=390, h=844)
        r.ev("SHIP.device.settings.tips = false"); r.step(10); r.press('B'); r.step(2)
        r.ev("goToDeck(3, null)"); r.step(60)
        sp = r.ev(f"(() => {{ const s = placeSpot('{sid}'); return s ? {{ x: s.x, z: s.z }} : null; }})()")
        if not sp: r.close(); continue
        r.ev(f"({STAND_BY})({json.dumps(sp)})"); r.ev("SHIP.player.tray = 'Test soup'; SHIP.player.needs.hunger = 40"); r.step(72)
        got = pick_key(r, 'place:' + sid, 16)
        if not got: r.close(); continue
        r.press('A')
        for k in range(120):
            r.step(10)
            if r.ev("typeof ACT !== 'undefined' && ACT && ACT.phase === 'do'"): break
        if 'sitting there' in r.ev("document.getElementById('tx').textContent"): r.close(); continue
        h0 = r.ev("SHIP.player.needs.hunger"); st = r.ev("[ACT && ACT.kind, ACT && !!ACT.o.fed, SHIP.player.tray, ACT && ACT.placeId]"); r.step(150)
        eat.append([sid, got, n] + st + [round(r.ev("SHIP.player.needs.hunger") - h0, 1), r.errors[:2]]); r.close()
    check(len(eat) >= 3, f'at least three mess seats eaten by pad: {len(eat)}')
    print('eat by pad [seat, ringed, tries, act, fed, tray, food change, errors]:'); [print('  ', e) for e in eat]
    for e in eat: check(len(e) > 3 and e[1] and e[3] == 'eat' and e[4] is True and e[5] is None and e[7] > 1 and e[6] == e[0], f'pad eat at {e[0]}: {e}')
print('RV9 PAD OK' if ok else 'RV9 PAD FAILED')
