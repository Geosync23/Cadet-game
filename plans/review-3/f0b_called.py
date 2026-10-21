# PR3: EV2's F0b. With EVENTS_ON on in a copy: the all-clear (Day 14 10:00, Deck 1 observation room): the named cast
# planned there for the whole meeting; the called-in notes sent; and whether section 20 makes the cue calledIn (and
# calledIn@me for the one called in). Run: python3 f0b_called.py ON.html
import os, sys
os.environ.setdefault('CADET_WORK', '/tmp/work-RV3')
exec(open('/tmp/rv/pp.py').read())
g = PGame(sync_playwright().start(), sys.argv[1], '?nosave&debug'); g.step(20)
print(g.ev("""(() => { const d = 14, out = {}; for (const g of evMeetsOn(d)) { out[g.id] = { at: g.at, len: g.len, cast: evMeetCast(g, d).map(c => { const p = c.p, B = (d - 1) * 1440;
  const segs = planDay(p, d).filter(s => s.from < B + g.at + g.len && s.to > B + g.at);
  return [p.id, c.named, eventCalledIn(p, d), segs.map(s => [s.act, s.tag || null, s.deck, s.from - B, s.to - B])]; }) }; } return out; })()"""))
g.ev("skipTo(13 * 1440 + 9 * 60 + 50)"); g.step(10)
for k in range(45):
    g.shipmins(2)
    if g.ev("SHIP.time.min") >= 11 * 60 + 5: break
print('notes', g.ev("simNotes('calledIn').map(n => [n.who, n.meeting, n.day, n.at])"))
print('cues', g.ev("(SHIP.social && SHIP.social.cues || []).filter(c => /calledIn/.test(c.key)).map(c => [c.key, c.who])"))
print('hears calledIn?', g.ev("typeof SOC_HEARS !== 'undefined' && SOC_HEARS.includes('calledIn')"))
print('errors', g.errors[:3]); g.close()
