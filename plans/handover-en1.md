# Handover: EN1, the ending engineer (lead 39)

**Role:** the ending engineer: E-2 (the offer and your answer, section 29a) and E-3 (the goodbye, the end page, section 29b) of
`plans/ending-spec.html` on claude/p5-specs (EP2). Session session_01Py28Kh6QV9kk64ri5AzQ5B.
**Branch:** `claude/ending` from claude/staging-0.93.3 d9c7e5f0 (SW6's claude/ending-words-a merged in). Build-table rows ending-1 to ending-9. Last: 319b7739 (game sha256 0f5866f3...); RV21 PASS on cd4196d5 (review fixes); 319b7739 adds only words. EN2 merges claude/ending into claude/ending-crossing (the combined ending). All behind
`EV_ENDING_ON` (section 13, `URL_FLAGS.has('ending')`, off; `?ending` / `#ending` previews). Off: cadet_test ALL IDENTICAL
against d9c7e5f0 on every turn, check_fast OK.

## What's built (details in DEV_NOTES "The ending")
- **Section 29 core** (after section 27, before the main loop: a spot no other branch adds to): the week's times `END_T`,
  `endWeek()` (Day 32 offer, 34 answer due, 35 settled at the Captain's address, 36 the goodbye; with Step 6 on, the first
  Thursday from Day 32 after `SHIP.works.end.day`), the post by Calder's answer (`endPostKind`), `SHIP.end` (saved only when on),
  `endingChoice()`, `endOpen()`, the user's question constants `END_WAY_BACK` (false: answered, no way back), `END_CHANGE`
  ('address'), `END_POST_BY` (true).
- **29a:** the ready room offer (an occasion, `moment:ending.offer`), Calder's search and walk, "About the transfer" on the
  Captain's and friends' chat cards, Stay / Go / Not sure, changing your mind, the 19:30 search, settled at the address,
  `endingAsk()` for E-1's address, Friday's friends, Zeke's Friday talk, the call home, Schedule rows, the Record.
- **29b:** the Monday goodbye (last morning, ~60 in the shuttle bay with an aisle, farewells in turn, Zeke at the ramp, aboard
  the Tern, fade), the end page (`endPage`, `endTheEnd`, ended save), the end page as a pad panel. The kept copy and "Back to
  before my choice" are CUT (the user, 2026-10-26) and parked off in 29b.

## Hooks outside section 29 (owners to review)
- Section 13: the switch line after `P926_APPT` (the vessel's `EV_VESSEL_ON` goes there too: keep the vessel's first).
- Section 20 (social engineer): one line in chatShow (`endChatButton`), one in chatDo (`endChatDo`).
- Section 19 (device engineer): one line in devDay (`endItems`), one in the Record app (`endRecord`).
- Section 26 is only called (`padPanelAdd`); section 18 is not touched (the booths: 29a watches `ACT.kind === 'call'`).

## For the other pieces
- **E-1 (crossing back, section 18):** at the address call `endingAsk()` when it returns true it plays the Captain's Stay/Go
  ask at the front; give the address minute with `crossBackAddressAt()`; read `endingChoice()` / `endSaid()` for the address's
  two versions. 29a settles at Day 35 15:00 itself, and if nothing's firm she finds you 15 minutes after.
- **E-4 (endgame):** `flag('end.stay')` is the day it settled as Stay (`end.go` for Go).
- **Writers:** SW6's words are merged and wired (ending-7). EN1 wrote the last few keys in SW6's files (ending-9): ending.breakfast.fetch, ending.bay.fetch, ending.btn.bye, ending.endpage.kept.<id>, ending.notice.go.ends. SW6 keys not yet used: ending.rumour, ending.friend.told, ending.friend.settled, ending.breakfast.here (chatter bubbles), ending.status.*, ending.saves.ended, ending.endpage.btn.new.sub (ending.works.* are EN2's).
- **EN2's API (agreed):** `endAnswer()`, `endSettle(now, answer)` -> the choice (calls EN2's `endStaySet(leave day)` on Stay; end.stay is EN2's), `end.cb.stay` / `end.cb.go` final, `END_ITEMS` rows through `endItems`. Zeke's Sunday 21:00 talk is EN1's (29a, `endZekeSunTick`).

## Loose ends
- Owner review still owed: the one line in section 20's careerOff (`endOffDay`, the career engineer), the two chat-card lines (section 20) and the devDay/Record lines (section 19).
- The packed cabin on Monday (24t's touches shown boxed) is not built: a display change in 24t, its owner's.
- The end page's "What you kept" humanises `SHIP.traces` ids ("line plaque") until the writers name them.
- The slower-career week settles on its own Sunday at 15:00 (judgement call; the crossing back stays Day 35).
- Dev mode presets for Days 32-36 (spec section 8) are not built: Dev mode's section 25 would need them.
- Not run on this branch: the full six-runner round (the switch is off), day_check Days 31/35/36 with the switch on.

## How to test
`python3 ending_check.py starship-cadet.html [off offer answers week endpage pad goodbye reload keep]` (about 6 minutes; the
on parts run in copies with the switch on, `pad` with PAD_ON on too, `reload`/`keep` from a web address). Then check_fast and
cadet_test against the build before. Screenshots: `plans/ending-shots/`.

## Open questions for the user
None. All three ending questions are answered (2026-10-26): no way back (the kept copy parked off, END_WAY_BACK false); change your
mind until the Captain's address; the post worded by your answer to Calder.
