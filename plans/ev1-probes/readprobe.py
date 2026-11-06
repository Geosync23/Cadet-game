import sys
exec(open("/home/user/Cadet-game/cadet_test.py").read().split("a, shots = run(")[0])
path = sys.argv[1]; days = [int(x) for x in sys.argv[2].split(',')]; pick = int(sys.argv[3]) if len(sys.argv) > 3 else 0
with sync_playwright() as pw:
    g = Game(pw, path, 390, 844); g.step(3)
    g.ev("window.__B = []; const bs = bubbleSay; bubbleSay = (w, t, s) => { window.__B.push([(w && w.p ? w.p.id : (w && w.id) || String(w)), t, SHIP.time.min, (() => { const a = DECK_CREW.find(c => c.p && c.p.id === 'walsh-esme'); return a ? [a.tag, a.settled, !!a.h, a.spot && a.spot.id] : null; })()]); return bs(w, t, s); }")
    if g.ev("typeof GUIDE_ON !== 'undefined' && GUIDE_ON"): g.ev("GUIDE.tq.length = 0; guideToast = () => false")
    for d in days:
        g.ev(f"skipTo(({d} - 1) * 1440 + 15 * 60 + 50); goToDeck(3)"); g.step(30)
        g.ev("window.__B.length = 0")
        g.step(30*20)   # to about 16:02
        J = g.ev(f"""(() => {{ const e = eventsOn({d}).find(x => x.id === 'reading-corner'); if (!e) return 'no rc';
           tradJoinMinute(shipNow()); const a = DECK_CREW.find(c => c.p && c.p.id === 'walsh-esme'); const at = DECK_CREW.filter(c => c.p && evTagId(c.tag || '') === 'reading-corner').map(c => c.p.id + (c.settled ? '*' : ''));
           return [!!a && tradJoin(e, a), at, SHIP.time.min]; }})()""")
        print('Day', d, 'join', J)
        card = None
        for k in range(80):
            g.step(30*2)
            dl = g.ev("DIALOGUE ? [DIALOGUE.id, DIALOGUE.queue.length, DIALOGUE.i] : null")
            if dl and not card:
                card = dl; v = g.ev("JSON.stringify(dialogueView())"); print('  card', dl, v[:300])
                if pick:
                    for j in range(6):
                        vv = g.ev("(() => { const v = dialogueView(); return v ? (v.choices ? 'c' : 'n') : null; })()")
                        if vv == 'c': g.ev(f"dialogueChoose({pick - 1})"); break
                        if vv == 'n': g.ev("dialogueNext()")
                        g.step(3)
                    for j in range(6):
                        if g.ev("!!DIALOGUE"): g.ev("dialogueNext()"); g.step(3)
                    print('  after card', g.ev("Object.keys(SHIP.flags || {}).filter(k => /^read\\./.test(k))"), g.ev("!!DIALOGUE"))
            if g.ev("SHIP.time.min") >= 17*60+2: break
        for b in g.ev('window.__B'): print('  ', int(b[2]//60), int(b[2]%60), b[0], '|', b[1][:40], b[3])
    print('errors', g.errors[:5])
    g.close()
