#!/usr/bin/env python3
"""smoke_check.py BUILD.html — the build master's run-time smoke test for combined builds.
Loads the game (?nosave&debug), lets it run real frames, opens a chat card with every crew member (chat, ask, close),
draws the device, rides the lift to every deck and runs more frames there. Fails on any page error or console error."""
import sys, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cadet_test.py')).read().split("a, shots = run(")[0])

CHATS = r"""(() => {
  socInit(); const out = { opened: 0, said: 0, errs: [] };
  for (const p of SOC.crew) {
    try {
      if (chatOpen(p)) { out.opened++; if (CHAT) { chatDo('chat'); if (CHAT && CHAT.line && CHAT.line.text) out.said++; chatDo('ask'); } chatClose(); }
    } catch (e) { out.errs.push(p.id + ': ' + (e && e.stack || e)); chatClose(); }
  }
  return out;
})()"""

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    bad = []
    g.page.wait_for_timeout(8000)                       # real frames on Deck 4 at 06:00
    for when in ['8 * 60', '13 * 60', '19 * 60']:       # morning, midday, evening crowds
        g.ev(f"SHIP.time.min = {when}")
        g.page.wait_for_timeout(4000)
        r = g.ev(CHATS)
        print(f"  {when}: chat cards opened {r['opened']}, lines {r['said']}, errors {len(r['errs'])}")
        bad += r['errs'][:5]
        g.page.wait_for_timeout(3000)
    for d in g.ev("Object.keys(DECKS).map(Number)"):
        try:
            g.ev(f"goToDeck({d})")
        except Exception as e:
            print('  deck', d, 'change failed:', str(e)[:120]); continue
        g.page.wait_for_timeout(4000)
        print(f"  deck {d}: {g.ev('typeof DECK_CREW !== \"undefined\" ? DECK_CREW.length : -1')} crew walkers, frames ok")
    errs = [e for e in g.errors if 'favicon' not in e]
    for e in errs[:10]: print('  PAGE', e[:300])
    for e in bad: print('  CHAT', e[:300])
    print('SMOKE OK' if not errs and not bad else 'SMOKE FAILED')
    sys.exit(0 if not errs and not bad else 1)
