# TR1: every tradition / event seen on Days 1-N on paper: first days, time, rooms, goers, host, joinable, leader
import sys, json
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
exec(open("/home/user/cadet-game/cadet_test.py").read().split("a, shots = run(")[0].replace("timeout=60000", "timeout=240000"))
build = ARGS[0]; N = int(ARGS[1]) if len(ARGS) > 1 else 35
with sync_playwright() as pw:
    g = Game(pw, build, 600, 500)
    r = g.ev("""JSON.stringify((() => { const out = {};
      for (let d = 1; d <= %d; d++) for (const e of eventsOn(d)) {
        const o = out[e.id] || (out[e.id] = { name: e.name, days: [], trad: evIsTrad(e.ev), join: !!TRAD_JOIN[e.id], act: TRAD_JOIN[e.id] && (TRAD_JOIN[e.id].act || TRAD_JOIN[e.id].pose) || null, host: e.ev.host || (TRAD_JOIN[e.id] || {}).host || null, meal: e.ev.meal || null, src: typeof e.ev.k === 'number' ? 'k' + e.ev.k : '' });
        if (o.days.length < 6) { let g = []; try { g = tradGoers(e).map(p => p.id); } catch (x) {}
          let rooms = []; try { rooms = [...eventRooms(e.ev)]; } catch (x) {}
          o.days.push([d, hhmm(e.from), hhmm(e.to), g.length, (e.ev.host && g.includes(e.ev.host)) ? 'host-goes' : (e.ev.host ? 'HOST-NOT-GOING' : '-'), rooms.slice(0, 3).join(' ')]); }
      } return out; })())""" % N)
    g.close()
r = json.loads(r)
for k, o in sorted(r.items(), key=lambda kv: kv[1]['days'][0][0]):
    print(k, '|', o['name'], '| trad' if o['trad'] else '| EVENT', '| join:' + str(o['act']) if o['join'] else '| NO-JOIN', '| host', o['host'], '| meal', o['meal'])
    for x in o['days']: print('    ', x)
