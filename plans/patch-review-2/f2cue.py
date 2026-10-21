from pp import *
g = start('?nosave&debug'); g.step(5)
for t in ["12*1440-1440+14*60+55"]:
    g.ev(f"skipTo({t})"); g.step(10)
    for i in range(4):
        g.secs(15)
        print(g.ev("({ t: clockText(), ph: SHIP.event && SHIP.event.phase, cues: (SHIP.social.cues || []).filter(c => /^event\\./.test(c.key)).map(c => [c.key, c.at, c.until]) })"))
print(g.errors[:3]); g.close()
