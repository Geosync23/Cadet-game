# Handover: mechanic engineer 4 (E4), Pillar 5 Step 4

Session_01PtXCwVBprdkJ6AcQisEyJq, 2026-10-19 (overnight). Took over E3's seat (plans/handover-mech3-e3.md: read it too; everything there about 24j/24t/places still holds). Read with CLAUDE.md, the brief (`git show origin/claude/lead-pillar1:plans/brief-p5s4.md`), DEV_NOTES rows 0.53.9-0.53.14 and the hook register rows marked E4, and the page `plans/mechanics/m17-lift-roof.html` on claude/p5-design.

## Role and chain
- Seat E4: M17 the lift roof (24s), then R5's fixes on E3's 24t, the lead's 24t extras.
- Lead 17 session_016bN7x175WBwBL7S9xc2Lpb; build master BM7 session_01QbuzvT3TwzMwSWRmakzX8Z; reviewer R6 session_01CPyuA1o5jgxwQtv7huZTNg (took over from R5 session_01XJyHzg4QvX2nsdtf9zT1TH). The head writer W2 has retired (plans/handover-writer-w2.md on claude/writer-p5): new lines go in our own content files, in W2's style, listed in the DEV_NOTES row.
- Never contact the user; push only to `claude/mech-diagnose`.

## Branch and builds (claude/mech-diagnose, series 0.53.x; next free 0.53.16)
| Build | Hash | What | Review |
|---|---|---|---|
| 0.53.9 | bca66df | M17 lift roof (24s), section 11 liftHold/liftHeld, section 14 whereIs line, mech_check part m17 | R5 PASS WITH FIXES (done in .12-.14) |
| 0.53.10 | f431a79 | R5's five 24t fixes | R5 PASS |
| 0.53.11 | d646e55 (+9e34c98 test) | mug tree (M10 name clash), roof.wait, lockerTidy hook, visitors' cabin.remark | with R6 |
| 0.53.12 | 9d467c5 | R5's M17 fixes: **does not load** (a comment ate a line); never use | R6 FAIL |
| 0.53.13 | f0c41b4 | load fixed, M17 lines in content/works/roof.lines; still one line hidden in a comment | superseded |
| 0.53.14 | 4e6f6bc (+2b5979a results) | the hidden line fixed; m17 tests catch it | R6 PASS (0.53.11-0.53.14) |
| 0.53.15 | 05bcbad (+ results commit) | no "stairs" roof.wait line (lineFor keep); the 4-23 shelf as wood on two dark brackets | sent to R6 |

## What I own and built
- **24s THE LIFT ROOF** (after 24t). Thursdays from Day 18, 15:30 till there's time for the whole spine (`roofLen()` = 17 ship minutes), trained, once a day: tap the lift on Deck 1 (section 11's `enterLift` asks `roofLiftTap` first) → card → `actStart('roofRide')` (PLAYER_ACTS.roofRide, `def.until = roofStep`, per frame). States: climb (1 min) → dark (fade, 0.4 s real) → light → grease/drop per deck → end → section 11's `ride` from its darkest point to the bottom deck. The shaft is built lazily at x+400 (`roofShaft`), near walls hidden per frame in `roofFrame` (its own rAF), which also handles stepping off (drag, time skip: out on the deck the car was at via `ride`) and the fade-only case. `roofDone`: rides/last, worksUse('m17'), worksSideXp(1), lift machine cond +6. Halloran rides with you till stage 2 (a FullPerson on the roof; his lines as toasts, flags roof.climb/grease/view/done).
- **The hold**: `liftHold(on, until)`, `liftHeld(t)`, `var LIFT_HOLD` (section 11, on the lift owner's behalf). Only when you climb on (lead accepted). Section 14's `whereIs` first line → `roofWait(p, t)`: crew whose plan changes deck during the hold wait at a lift-wait place on the deck they were on at the hold's start, till 16:30. `roofTalk`: a waiting crew member near you says a `roof.wait` line once a hold.
- **Ladder**: `WORK_MECH.m17 = { noJob, offer }`: Thursdays only (other days offer returns false and it asks again), Halloran's Mail + meeting at the Deck 1 lift lobby ('+') at 15:30; trained at the meeting. The 24s tick re-points OCCASIONS['works.m17'] to Deck 1 after a reload.
- **Save**: `SHIP.works.side.roof = { rides, last, on? }`; `on` = the day while you're on the roof, so after loading such a save the tick says `roof.resume` once. The hold isn't saved.
- **24t changes**: shelf bracket under the shelf thing; looks for four shelf things; `cabinTap` → approach → `cabinPut`; the tinkered mug rack is now 'mug tree' (old saves migrate on the ledge); `cabinPutAway()` read by 15b's `lockerTidy` (one line; `side.cabinPut = [bought, crafted]`); `cabinRemark` (visitors in 4-23, bank `cabin.remark` by flags, once a day each).
- **Lines**: `content/works/roof.lines` (mine): roof.card, roof.up, roof.free, roof.shut (replaces W2's roof.held, which said "Stairs, please."), works.ask.m17. W2's own M17/24t lines live on claude/writer-p5 (step4.lines, halloran-emeka.lines, workshop.lines bank, train.m17 meeting); BM7 bakes both.
- **Tests**: mech_check parts `m17` (paper: when you can climb, the hold over all crew, roof.wait, saves; live frames: a stop per deck, Deck 6, counted, held till 16:30, draw calls 73, stepping off at Deck 3, stepping off in the fade, ROOF.r/on mid-ride, roof.resume once; restores time/deck/needs after) and `t24` (+ T24B: the real star log, save round trip, looks, mug tree, locker, a visitor's remark).

## Loose ends / notes
1. 8b has no 'grease' pose (the roof uses 'work', the page allows it).
2. Waiting crew stand at lift-wait places; a crowded lobby may send some "elsewhere" (BUSY): fine but untested on phones.
3. Bubbles from roof.wait and cabin.remark need W2's lines baked (no stand-ins on purpose).
4. The shaft's look was checked by screenshots at 900x760 and 390x844 (Day 18); the 0.53.15 wooden shelf only by numbers (R6 eyeballed the earlier slab).
5. cabinRemark/roofTalk "said" sets are not saved (a reload may repeat one).

## Gotchas
- **Comments after code on a line I edit with a script swallowed code twice** (0.53.12): put new comments on their own line; run `node --check` on the extracted script (python: the longest `<script>` block → .mjs) AND the m17/t24 checks before pushing.
- `pkill -f` patterns matching your own shell kill it (exit 144): use `[m]ech_check`-style patterns.
- The full mech_check takes ~25 min; deck/interactions/cadet_test ~10 more. One or two browsers at a time.
- cadet_test's Game: virtual clock (`g.step(n)`); `performance.now` is virtual too.

## How to test
Setup as DEV_NOTES "Testing" (pip playwright; three.js r128 at /tmp/cadet-work/three; CADET_CHROME=/opt/pw-browsers/chromium). `python3 mech_check.py B.html m17 t24 m10 side` (~10 min), the whole mech_check, deck_check, interactions_check, `cadet_test.py OLD NEW` from a scratch folder, `content_gen.py --check`, `lines_check.py`.

## Open questions for the user
- None of mine. Lead's calls taken: the car is held only when you climb on; roof.shut replaces W2's roof.held.
