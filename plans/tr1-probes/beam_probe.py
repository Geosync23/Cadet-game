# TR1 probe, note 8: Name on the beam (Day 1, 17:05). Where you stand to paint vs where your name goes; where the watchers stand
# (their bubbles over their heads) relative to the name. Screenshots while you paint and just after. Usage: beam_probe.py BUILD.html
import sys, json
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
exec(open("/home/user/cadet-game/cadet_test.py").read().split("a, shots = run(")[0].replace("timeout=60000", "timeout=240000"))
build = ARGS[0]; S = '/tmp/claude-0/-home-user-cadet-game/24719ad3-8581-5c0f-8836-4550db8ff7c7/scratchpad/'
GEO = """JSON.stringify((() => { const r = ROOM_BOX['w'], nameX = X0(r.i0) + BEAM.slots[0][0], sp = placeSpot('5-beam-1');
  return { i0: r.i0, nameWorldX: +nameX.toFixed(2), nameSpan: [+(nameX - .6).toFixed(2), +(nameX + .6).toFixed(2)], paintAt: sp && [+sp.x.toFixed(2), +sp.z.toFixed(2)],
    watchers: DECKS[5].places.filter(p => /^5-beam-/.test(p.id)).map(p => { const s = placeSpot(p.id); return p.id + '@' + (s ? s.x.toFixed(2) + ',' + s.z.toFixed(2) : '?'); }) }; })())"""
with sync_playwright() as pw:
    g = Game(pw, build, 390, 844)
    g.ev("(() => { skipTo(17 * 60 + 2); goToDeck(5, null); SHIP.device.settings.tips = false; const sp = placeSpot('5-beam-1'); player.obj.position.set(sp.x + 1, 0, sp.z + 2); player.stop(); })()")
    g.step(10); print('geometry', g.ev(GEO)); print('you in room', g.ev('roomAt(...player.here())'))
    painted = None
    for k in range(400):
        g.step(30)
        st = json.loads(g.ev("JSON.stringify({ m: Math.round(SHIP.time.min), on: typeof beamOn === 'function' && beamOn(), act: ACT && ACT.kind, ready: typeof beamReady === 'function' && beamReady(), at: DECK_CREW.filter(a => a.spot && /^5-beam-/.test(a.spot.id) && a.settled).map(a => a.p.id + '@' + a.spot.id), name: (SHIP.traces || []).some(x => x.id === 'nameYours') })"))
        if k % 15 == 0: print(st)
        if st['on'] and painted is None:
            print('paint tap ->', g.ev("beamPaint()")); painted = st['m']
        if painted and st['act'] and k % 5 == 0: g.shot(S + 'beam_painting.png')
        if st['name']:
            g.step(30); g.shot(S + 'beam_after.png'); g.step(60); g.shot(S + 'beam_after2.png')
            print('name up at', st['m'], 'you at', g.ev("JSON.stringify([+player.obj.position.x.toFixed(2), +player.obj.position.z.toFixed(2)])")); break
        if st['m'] > 17 * 60 + 45: break
    print('errors', g.errors[:3]); g.close()
