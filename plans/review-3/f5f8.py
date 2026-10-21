# PR3: EV2's F5 (parts by rank) and F8 (comms down), a copy with EVENTS_ON. Calls home at points through the storm, and
# each meeting's ranks, invite and script at your rank (junior, then as an officer). Run: python3 f5f8.py ON.html
import os, sys
os.environ.setdefault('CADET_WORK', '/tmp/work-RV3')
exec(open('/tmp/rv/pp.py').read())
g = PGame(sync_playwright().start(), sys.argv[1], '?nosave&debug'); g.step(20)
for d, m in [(11, 12 * 60), (12, 13 * 60), (12, 15 * 60), (13, 12 * 60), (13, 20 * 60), (14, 9 * 60), (14, 12 * 60)]:
    g.ev(f"skipTo({d - 1} * 1440 + {m})"); g.step(3)
    print('D%d %02d:00' % (d, m // 60), 'phase', g.ev("(eventNow() || {}).phase || null"), 'commsDown', g.ev("eventCommsDown()"), 'callable', g.ev("homeCallable().length"))
print('rank', g.ev("playerRank()"))
print(g.ev("SHIP_EVENTS.ionStorm.meetings.map(m => [m.id, m.ranks || null, m.scriptBy || null])"))
print('junior', g.ev("SHIP_EVENTS.ionStorm.meetings.map(m => [m.id, evInvited(m), evScriptOf(m)])"))
g.ev("(() => { try { SHIP.works.rank = 'officer'; } catch (e) {} })()")
print('as', g.ev("playerRank()"), g.ev("SHIP_EVENTS.ionStorm.meetings.map(m => [m.id, evInvited(m), evScriptOf(m)])"))
print('errors', g.errors[:3]); g.close()
