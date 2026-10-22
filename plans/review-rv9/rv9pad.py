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
    for kind in ('3-longtable-', '3-lounge-'):   # (mess seats: the ring offers the long-table seat on the same spot, as on 0.90.8; eating there predates the fix)
      for n in range(1, 13):
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
        h0 = r.ev("SHIP.player.needs.hunger"); st = r.ev("[ACT && ACT.kind, ACT && !!ACT.o.fed, SHIP.player.tray]"); r.step(150)
        eat.append([sid, got, n] + st + [round(r.ev("SHIP.player.needs.hunger") - h0, 1), r.errors[:2]]); r.close(); break
      else: eat.append([kind, 'no free seat the ring reached'])
    print('eat by pad [seat, ringed, tries, act, fed, tray, food change, errors]:'); [print('  ', e) for e in eat]
    for e in eat: check(len(e) > 3 and e[1] and e[3] == 'eat' and e[4] is True and e[5] is None and e[6] > 1, f'pad eat at {e[0]}: {e}')
    # 2. Settings rows: switch off (no pad), switch on (no pad, pad seen); New game by pad: Keep playing, then Start over
    def rows(r): return r.ev("deviceView('settings').blocks.map(b => b.text || (b.items || []).map(i => i.label).join('|'))")
    r = Run(pw, src, 'rv9set0'); v0 = rows(r); r.close()
    r = Run(pw, on, 'rv9set1'); v1 = rows(r); r.close()
    print('settings, switch off:', v0[-6:]); print('settings, switch on, no pad:', v1[-6:])
    check(v0 == v1, 'settings differ with the switch on and no pad')
    check('New game' in v0 and 'Controller settings' not in v0, f'switch off: New game row, no Controller row: {v0}')
    r = Run(pw, on, 'rv9set2', mode='pad', plug={}, w=390, h=844); r.ev("SHIP.device.settings.tips = false"); r.step(10); r.press('B'); r.step(2)
    r.ev(TOASTS); v2 = rows(r); print('settings, pad seen:', v2[-6:])
    check('New game' in v2 and v2[-1] == 'Controller settings', f'pad seen: both rows: {v2}')
    r.ev("deviceShow('settings')"); r.step(3)
    B = "[...document.querySelectorAll('#devBody button')].find(b => b.textContent === '%s')"
    seq = []
    for lab in ('New game', 'Keep playing', 'New game', 'Start over'):
        f = r.ev(f"({MARK})({json.dumps(B % lab)})")
        ok_to = f and pad_to(r, '[data-ctt]'); r.press('A'); r.step(6)
        seq.append([lab, bool(ok_to), r.ev("devNewSure"), r.ev("DEV.open"), r.ev("DEV.open && DEV.app")])
        if lab == 'Start over': r.step(30)
    after = r.ev("[SHIP.time.day, SHIP.time.min, player.deck, DEV.open]")
    print('new game by pad [button, highlighted, asking, device open, app]:', seq, 'after:', after)
    check(seq[0][1] and seq[0][2] is True, f'New game by pad should ask: {seq[0]}')
    check(seq[1][1] and seq[1][2] is False and seq[1][3], f'Keep playing by pad: {seq[1]}')
    check(seq[3][1] and seq[3][2] is False and seq[3][3] is False, f'Start over by pad: {seq[3]}')
    # the Controller row still works after New game (pad seen): open the Controller page and back with B
    r.ev("deviceShow('settings')"); r.step(3)
    f = r.ev(f"({MARK})({json.dumps(B % 'Controller settings')})"); okc = f and pad_to(r, '[data-ctt]'); r.press('A'); r.step(6); app1 = r.ev("DEV.app")
    r.press('B'); r.step(6); app2 = r.ev("DEV.open && DEV.app")
    print('controller settings page by pad:', okc, app1, app2, 'errors', r.errors[:3])
    check(okc and app1 == 'padsettings' and app2 == 'settings', f'Controller settings by pad: {okc} {app1} {app2}')
    r.close()
    # 3. bunk words by pad: your bunk by day (too early), another bunk in your room (which is yours)
    bunk = []
    for which in ('own', 'other'):
        r = Run(pw, on, 'rv9bunk', mode='pad', plug={}, w=390, h=844); r.ev("SHIP.device.settings.tips = false"); r.step(10); r.press('B'); r.step(2)
        r.ev("SHIP.time.min = 600"); r.ev(TOASTS)
        t = r.ev("""((own) => { const id = playerBed(), bed = PLACE_OF.get(id), b = cellPos(...bed.at), rm = roomAt(...bed.at), w = new THREE.Vector3();
          if (deckDef.num !== deckOf(id)) goToDeck(deckOf(id), null);
          const L = ITEMS.map((i, k) => [i, k]).filter(([i]) => i.hit && /^bunk$/i.test(i.t)).map(([i, k]) => { i.hit.getWorldPosition(w); return [i, k, w.clone()]; })
            .filter(([i, k, p]) => own ? p.distanceTo(b) <= 1.2 : p.distanceTo(b) > 1.2 && roomAt(...cellAt(p.x, p.z)) === rm).sort((m, n) => m[2].distanceTo(b) - n[2].distanceTo(b));
          if (!L.length) return null; return { k: L[0][1], x: L[0][2].x, z: L[0][2].z, label: L[0][0].x || '' }; })(%s)""" % ('true' if which == 'own' else 'false'))
        if not t: bunk.append([which, 'none']); r.close(); continue
        r.step(30); r.ev(f"({STAND_BY})({json.dumps(t)})"); r.step(72)
        got = pick_key(r, 'item:' + str(t['k'])); hint = r.ev(HINT); r.press('A'); r.step(200)
        bunk.append([which, got, hint, r.ev("typeof ACT !== 'undefined' && ACT ? ACT.kind : null"), r.ev("window.__toasts"), t['label'], r.errors[:2]]); r.close()
    print('bunk by pad [which, ringed, hint, act, toasts, label]:'); [print('  ', b) for b in bunk]
    check(bunk[0][1] and bunk[0][3] == 'lie' and any('Too early to sleep: you can turn in from 20:00.' in x for x in bunk[0][4]), f'own bunk by pad: {bunk[0]}')
    check(bunk[1][1] and any(x.endswith('Yours is the next one.') for x in bunk[1][4]), f'other bunk by pad: {bunk[1]}')
    # 4. (RV5 via CP1) the seek chip at z-index 2: the pad's focus outline on it shows and nothing covers it (phone and wide)
    from PIL import Image
    for (w, h) in ((390, 844), (1280, 800)):
        r = Run(pw, on, 'rv9seek', mode='pad', plug={}, w=w, h=h); r.ev("SHIP.device.settings.tips = false"); r.step(10); r.press('B'); r.step(2)
        shown = r.ev("(() => { const a = DECK_CREW.find(a => a.x !== undefined); if (!a) return null; seekShow(a.p, SHIP.time.min); const e = document.getElementById('seek'); return !!e && !e.hidden; })()"); r.step(5)
        r.press('UP'); r.step(4); okf = pad_to(r, '#seek'); r.step(3)
        info = r.ev("""(() => { const e = document.getElementById('seek'), b = e.getBoundingClientRect(), cs = getComputedStyle(e);
          const pts = [[b.left + 4, b.top + 4], [b.right - 4, b.top + 4], [b.left + 4, b.bottom - 4], [b.right - 4, b.bottom - 4], [(b.left + b.right) / 2, (b.top + b.bottom) / 2]];
          const cover = pts.map(([x, y]) => { const t = document.elementFromPoint(x, y); return t === e || e.contains(t) ? null : (t ? (t.id || t.className || t.tagName) : 'none'); }).filter(Boolean);
          return { focus: document.activeElement === e, outline: cs.outlineStyle + ' ' + cs.outlineWidth, body: document.body.className, z: cs.zIndex, rect: [b.left, b.top, b.right, b.bottom], cover }; })()""")
        p = r.shot(f'rv9seek_{w}'); im = Image.open(p).convert('RGB'); L, T, Rr, Bt = info['rect']; my = int((T + Bt) / 2)
        ring = [im.getpixel((max(0, int(L) - 5), my)), im.getpixel((min(w - 1, int(Rr) + 4), my)) if Rr + 4 < w else None, im.getpixel((int((L + Rr) / 2), max(0, int(T) - 5)))]
        teal = [px for px in ring if px and abs(px[0] - 76) < 30 and abs(px[1] - 195) < 30 and abs(px[2] - 181) < 30]
        print(f'seek chip by pad at {w}x{h}: shown {shown}, highlighted {okf}, {info}, outline pixels {ring}, shot {p}')
        check(shown and okf and info['focus'] and not info['cover'] and len(teal) >= 2, f'seek chip outline at {w}x{h}: {info} {ring}')
        r.close()
print('RV9 PAD OK' if ok else 'RV9 PAD FAILED')
