# PR3: FR1 turn 1 (A1). On vs off copies: every non-Friday day plans identically; on a short Friday who is at work
# 15:30-17:00 by department and deck; nobody's plan has a hole. Run: python3 fr1_t1.py OFF.html ON.html
import sys, json
sys.argv, files = [sys.argv[0], sys.argv[1]], sys.argv[1:3]
exec(open('/tmp/rv/ec/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
PLANS = """(days => { const o = {}; for (const d of days) for (const p of schedPeople()) o[d + ' ' + p.id] = planDay(p, d).map(s => [s.from, s.to, s.act, s.placeId || null, s.tag || null]); return o; })"""
AT = """(d => { const B = (d - 1) * 1440, out = {}; for (const m of [920, 935, 960, 1000, 1015]) { const w = {}; for (const p of schedPeople()) { const s = planDay(p, d).find(s => s.from <= B + m && B + m < s.to); if (s && s.act === 'work') { const k = p.dept + '@' + (s.deck != null ? s.deck : '?'); w[k] = (w[k] || 0) + 1; } } out[m] = w; } return out; })"""
SK = "(() => [...(friSkeleton(schedPeople()[0]), FRI_SKEL)].map(id => { const p = ROSTER.find(q => q.id === id); return [id, p.dept, p.rank]; }))()"
with sync_playwright() as pw:
    res = {}
    for f in files:
        g = Game(pw, f)
        res[f] = { 'plans': g.ev(PLANS + "([4, 5, 6, 11, 12, 13])"), 'at5': g.ev(AT + "(5)"), 'at12': g.ev(AT + "(12)") }
        if 'on' in f: res[f]['skel'] = g.ev(SK)
        g.close()
    a, b = res[files[0]]['plans'], res[files[1]]['plans']
    for d in [4, 5, 6, 11, 12, 13]:
        diff = [k for k in a if k.startswith(f'{d} ') and a[k] != b[k]]
        print(f'Day {d}: {len(diff)} plans differ on vs off', diff[:6])
    print('skeleton', res[files[1]].get('skel'))
    for f in files:
        for d in ('at5', 'at12'): print(f, d, json.dumps(res[f][d]))
