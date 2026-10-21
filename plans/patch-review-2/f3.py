from pp import *
g = start('?nosave&debug'); g.step(5)
for d in (11, 12, 14, 7):
    print(d, g.ev(f"devDay({d}).filter(x => x.kind === 'event').map(x => [hhmm(x.from), hhmm(x.to), x.title, x.where, x.deck, x.room])"))
g.ev("skipTo(12*1440-1440+15*60)"); g.step(10)
print('tracked d12 15:00', g.ev("trkItems().filter(x => /event|^on/.test(x.sec) ).map(x => [x.sec, x.title, x.tag, x.sub, !!x.goal])"))
print('places', g.ev("trkItems().filter(x => x.sec === 'place').map(x => x.title)"), 'closed?', g.ev("eventRoutines(shipNow()).filter(r => r.rule === 'closed').map(r => r.where)"))
print('remind', g.ev("JSON.stringify(SHIP.device.calendarRemind)"))
print(g.errors[:3]); g.close()
