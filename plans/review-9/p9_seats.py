# PR9: e18844f's seat holds on paper. A new game (intro on), then for Days 1-8: every two people planned in one place at
# overlapping minutes (seated places: not 'event' standing spots), and every intro beat's place per person.
# Run from the build's folder: python3 p9_seats.py BUILD.html (cadet_test.py beside it)
import sys, json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    r = g.ev("""(() => { const out = { on: introOn(), clash: [], beats: [] }, byId = schedData().byId;
      for (let d = 1; d <= 8; d++) { const day = shipDay(d), segs = [];
        for (const [id, plan] of day.plans) for (const s of plan) if (s.placeId) segs.push([id, s]);
        for (const [id, s] of segs) if (/^intro/.test(s.tag || '')) out.beats.push([d, id, s.tag, s.placeId, s.from % 1440, s.to - s.from]);
        for (let i = 0; i < segs.length; i++) for (let j = i + 1; j < segs.length; j++) { const [a, s] = segs[i], [b, u] = segs[j];
          if (a !== b && s.placeId === u.placeId && s.from < u.to && u.from < s.to && (byId.get(s.placeId) || {}).type !== 'event' && (/^intro/.test(s.tag || '') || /^intro/.test(u.tag || '')))
            out.clash.push([d, s.placeId, a, s.tag, b, u.tag, Math.max(s.from, u.from) % 1440, Math.min(s.to, u.to) - Math.max(s.from, u.from)]); } }
      return out; })()""")
    print('intro on', r['on']); print('beats', len(r['beats']))
    for b in r['beats']: print('  B', json.dumps(b))
    print('clashes', len(r['clash']))
    for c in r['clash']: print('  C', json.dumps(c))
    print('page errors', g.errors[:4]); g.close()
