# Review: ship events 0.34.50 (2ffff6f), a New game resets section 18

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS.**

## Tests (trial merge: claude/cand-0603 eb75e1a (0.60.3) + device 24f1920 (0.35.39) + ship-events 2ffff6f;
build-label conflicts only, `node --check` OK)
- events_check (2ffff6f's, its new part 11 included): **EVENTS CHECK OK**; part 11: occasions [], commendations 0,
  traces [], old Mail keys [], votes [], occasion meetings [].
- **Two New games in one page** (the button, tapped twice each time). Before each I played forward: day 6 with the
  ready-room summons and the Captain's table booked (2 device appointments, 3 meetings, 11 traditions Mailed, a
  one-off, the framedMenu trace). After New game 1 and again after New game 2, everything matches a fresh start:
  occasions [], appointments 0, meetings [], traces [], sent/joined/oneOffs 0, no ship event, Mail back to the 1
  welcome message, no dialogue open. Between the two, the second game books and Mails again as normal (day 4: the
  summons, 6 Mailed), so nothing is left switched off.
- Read: the listener runs after section 19's (file order: device ~9041, lines ~23306, section 18 ~24634, Tiles
  later), and none of the earlier ones books occasions or meetings, so nothing a fresh game adds is wiped.

## FYI for the build master (not this build)
On the 0.60.3 candidate, device_check fails "Mail: From home, Play on a recorded message" (play False) with its own
device_check and with 24f1920's; it fails the same without 2ffff6f, so it predates this review. 0.60.3's own
device_check also fails four heads-up cases, which 0.35.39's device_check fixes.
