import sys, json, os
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0])
with sync_playwright() as pw:
    g=Game(pw, sys.argv[1], w=390, h=844)
    for (lab, t) in [('d7 18:35 sunday table', 6*1440+18*60+35), ('d7 14:45', 6*1440+14*60+45)]:
        g.ev(f"skipTo({t})"); g.ev("goToDeck(3)"); g.step(5)
        for (x,z) in [(23.5,12.5),(30.0,9.5),(20,10)]:
            g.ev(f"player.obj.position.copy(cellPos({int(x)},{int(z)})); target.copy(player.obj.position).setY(.7)"); g.step(40)
            print(lab, (x,z), 'calls', g.ev("renderer.info.render.calls"), 'crew on deck', g.ev("DECK_CREW.length"))
    # fake: send all deck crew to plaza spots
    n = g.ev("""(() => { const S = gatherSpots('plaza'); let i=0; for (const a of DECK_CREW) { const s=S[i++%S.length]; if (!s.xy) continue; a.h.obj ? a.h.obj.position.set(...cellPos(s.at[0], s.at[1]).toArray()) : 0; } return DECK_CREW.length; })()""")
    g.step(2); print('fake crowd', n, 'calls', g.ev("renderer.info.render.calls"))
    if g.errors: print(g.errors[:3])
    g.close()
