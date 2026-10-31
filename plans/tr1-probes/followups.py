# TR1 follow-ups on paper: (a) two joinable traditions on one deck at once, Days 1-120 (only the first gets TJ_NOW);
# (b) who goes to Gym club on Day 8 and is Saruth aboard; (c) film night on Day 6 after a skip from Day 0
import sys, json
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
exec(open("/home/user/cadet-game/cadet_test.py").read().split("a, shots = run(")[0].replace("timeout=60000", "timeout=240000"))
with sync_playwright() as pw:
    g = Game(pw, ARGS[0], 600, 500)
    print('(a)', g.ev("""JSON.stringify((() => { const out = [];
      for (let d = 1; d <= 120; d++) { const L = eventsOn(d).filter(e => tradJoinable(e)).map(e => { if (!e.rooms) e.rooms = eventRooms(e.ev); return e; });
        for (let i = 0; i < L.length; i++) for (let j = i + 1; j < L.length; j++) { const a = L[i], b = L[j];
          if (a.from < b.to && b.from < a.to) { const da = new Set([...a.rooms].map(r => r.split('|')[0])), db = [...b.rooms].map(r => r.split('|')[0]);
            if (db.some(x => da.has(x))) out.push(d + ' ' + a.id + ' ' + hhmm(a.from) + '-' + hhmm(a.to) + ' first, hides ' + b.id + ' ' + hhmm(b.from) + '-' + hhmm(b.to) + ' deck ' + db.filter(x => da.has(x))[0]); } } }
      return out; })())"""))
    print('(b)', g.ev("""JSON.stringify((() => { const e = eventsOn(8).find(x => x.id === 'running'), s = schedPeople().find(p => p.id === 'saruth');
      return { goers: tradGoers(e).map(p => p.id), saruth: !!s, aboard: s && typeof aboard === 'function' ? [1, 8, 17, 18].map(d => d + ':' + aboard(s, d)) : null,
        sarPlan8: s ? planDay(s, 8).map(x => hhmm(x.from) + ' ' + (x.tag || x.type || '')).slice(0, 12) : null, rina8: planDay(schedPeople().find(p => p.id === 'rina'), 8).filter(x => x.from > 1100 && x.from < 1220).map(x => hhmm(x.from) + ' ' + (x.tag || x.type)) }; })())"""))
    print('(c) before skip', g.ev("JSON.stringify(eventsOn(6).filter(e => /film/.test(e.id)).map(e => e.id))"))
    g.ev("skipTo(5 * 1440 + 19 * 60 + 50)")
    print('(c) after skip', g.ev("JSON.stringify({ on: eventsOn(6).filter(e => /film/.test(e.id)).map(e => e.id), moved: flag('rec.filmMoved'), allHands: flag('rec.allHands') })"))
    g.close()
