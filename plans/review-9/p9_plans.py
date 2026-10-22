# PR9: claude/fridays-20 on paper. A new game (intro on); Days 0-8: every plan as [person, day, from, to, act, tag, place],
# written to OUT.json, plus the seat clashes of p9_seats.py and occ.res holds marked 'alts'. Compare two builds' files.
import sys, json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    r = g.ev("""(() => { const out = { plans: [], clash: [], alts: [], unused: [] }, byId = schedData().byId;
      for (let d = 0; d <= 8; d++) { const day = shipDay(d), segs = [];
        for (const [id, plan] of day.plans) for (const s of plan) { out.plans.push([id, d, s.from, s.to, s.act, s.tag || null, s.placeId || null]); if (s.placeId) segs.push([id, s]); }
        for (const [id, rs] of day.occ.res) for (const [x, y, w, k] of rs) if (k === 'alts') { const who = w.slice(6), used = (day.plans.get(who) || []).some(s => s.placeId === id && s.from < y && x < s.to);
          out.alts.push([d, id, w, x % 1440, y - x, used]); if (!used) out.unused.push([d, id, w]); }
        for (let i = 0; i < segs.length; i++) for (let j = i + 1; j < segs.length; j++) { const [a, s] = segs[i], [b, u] = segs[j];
          if (a !== b && s.placeId === u.placeId && s.from < u.to && u.from < s.to && (byId.get(s.placeId) || {}).type !== 'event' && (/^intro/.test(s.tag || '') || /^intro/.test(u.tag || '')))
            out.clash.push([d, s.placeId, a, s.tag, b, u.tag, Math.max(s.from, u.from) % 1440, Math.min(s.to, u.to) - Math.max(s.from, u.from)]); } }
      return out; })()""")
    json.dump(r['plans'], open(sys.argv[2], 'w'))
    print('plans', len(r['plans'])); print('clashes', len(r['clash']))
    for c in r['clash']: print('  C', json.dumps(c))
    print('alts holds', len(r['alts']))
    for c in r['alts']: print('  A', json.dumps(c))
    print('unused alts holds', r['unused']); print('page errors', g.errors[:4]); g.close()
