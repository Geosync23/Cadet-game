# Handover: mechanic engineer 3 (E3), Pillar 5 Step 4

Session_01WkkCvj4yxnMALMQYG2DsWM, 2026-10-19 (overnight). Written at about 55-60% memory, before M17, under the user's handover rule. Read it with CLAUDE.md, the brief (`git show origin/claude/lead-pillar1:plans/brief-p5s4.md`), DEV_NOTES rows 0.53.4-0.53.7 and "Places for Pillar 5 Step 4", and the Step 4 pages on `claude/p5-design` (`plans/mechanics/m10-workshop.html`, `off-shift.html`, `m17-lift-roof.html`).

## Role and chain
- Seat E3 for Step 4: the places turn, M10 (24j), cabin touches + star logging (24t), M17 lift roof (24s, not started).
- Lead 16: session_01UMyfd16GqSdgNyz5PE8qSv. Build master BM7: session_01QbuzvT3TwzMwSWRmakzX8Z. Reviewer R4: session_01UGQxniXCxT5TLEE4tgRLfJ. Designer D3 (pages): session_0115ZiGhf9s3oYtFdjs7TgYS. E1 (24 core, ladder rows, Record): session_01AHeKjieg3qWjnEVuHecsHd. E2 (leaks, irrigation, rewiring, favours): session_01Bezat4UU7beoaKsqdSrJBs. Writer W2: session_01866TWKzGRgZmFcxiYRi4db.
- Report each finished piece (hash, build, what, checks, memory %) to the lead, BM7 and R4. Never contact the user; push only to `claude/mech-diagnose`.

## Branch and builds (claude/mech-diagnose, series 0.53.x; next free number 0.53.9)
| Build | Hash | What | Review |
|---|---|---|---|
| 0.53.4 | 9d179e9 | the places turn (on 0.63.3 7a6e137) | R4 PASS WITH FIXES |
| 0.53.5 | b809339 | five leak joints moved; deck_check's leak-joint line | R4 PASS |
| 0.53.6 | 626a907 | M10 workshop + tinkering (24j), merged E1's 0.45.8 7a9a942 | sent to R4 |
| 0.53.7 | 2ce8e9e | 24t cabin touches + star logging | sent to R4 |
| 0.53.8 | see the last commit | R4's two M10 fixes (empty shelf; the made thing in your hands) | sent to R4 |

## What I own and built
- **Places (0.53.4-5):** one block after Step 3's places (search `0.53.4 (Pillar 5 Step 4, seat E3`). All type `event` with `event: 'side'` / `'leak'` / `'leakp'` (inert for the crew). `DECKS[n].leakJoints`, `DECKS[3].growRacks`, `DECKS[4].cabinSpots['4-23']`. Props: the machine shop's order board (`wallFixed`), your bench under the Works bay window. Full list in DEV_NOTES "Places for Pillar 5 Step 4".
- **24j (0.53.6):** orders on the board (Day 12 08:00, then Mondays 08:00), a side job kind `shop` (jobKindAdd, side, crew can't) with the lathe/fab wait + hold, the hand-over on the chat card, lapses, stage 2 parts, tinkering (`TINKER_LIST`, added to `SOC_GIFTS`). Hooks: `shopTap` in 15's jobTap; `shopGiveButton` / `shopGiveSay` in 20's chat. Saved in `SHIP.works.side.shop`.
- **24t (0.53.7):** cabin spots as tap items built by 24t on Deck 4 (`cabinDraw`, each ship minute via WORK_TICKS), `CABIN_FITS` / `CABIN_LOOK`, `cabinMood()`, `cabinPlaced(id)`; star logging at Deck 2's observatory telescope (`starTap`, `starLog`, `starSky`, `starsLogged()`). Saved in `SHIP.works.side.cabin` / `.stars`.
- **Tests:** mech_check parts `m10` and `t24`; deck_check's leak-joint line.

## Shared formats
- `SHIP.works.side.<key>` through 24 core's `worksSide()` (E1); read your own key defensively and clean it on read. Side-job reputation: `worksSideXp(n, why)` (+2 a day cap).
- Ladder rows are E1's table (send changes to E1). m10's row: small, Day 12, by torres-zeke / halloran-emeka / calder. m17's row is in (big, Day 18, by halloran-emeka, stages uses 0 / 2), inert until `WORK_MECH.m17`.
- Writer's keys: M10 on my names (claude/writer-p5 7a5825b); cabin, stars and M17 on W2's names from b00e08b (content/works/keys-p5.md "Step 4", rows E3): M17 = meeting `train.m17.halloran-emeka`; Halloran `work` flags roof.climb | grease | view | done; roof.held, roof.result, roof.resume; crew kind roof.wait.

## Loose ends
1. 24t: `cabinMood()` is not read by section 15 (24t gives +4 leisure at 06:00 itself instead); `cabinPlaced(id)` is not read by `lockerTidy` (one-line hook, if the owner wants it); visitors' remarks (W2's crew kind `cabin.remark`) not built.
2. The Record line for ten stars: asked E1 to append `works.ms.stars` in `worksRecordHead` (24t pushes `['stars', day]` into `SHIP.works.ms`).
3. M10: since 0.53.8 the made thing is in `SHIP.player.carry` (R4 and the lead); main storage refuses to shelve it, and one lost from your hands is waiting by the order board.
4. 5-tool-rack is the existing tool wall (no new rack drawn); D3 had agreed "a wall rack": tell D3 if that matters.

## M17 lift roof (not started): notes from reading
- Page: Thursdays 15:30-16:30 from Day 18; climb on at the top deck (hold), the car rides slowly down the spine stopping at each deck's guide (hold 1 minute each); crew who need another deck wait until 16:30 (no ladder); release at 16:30 always (also if you leave); a save mid-ride loads you on the top deck, lift released. `SHIP.works.side.roof = { rides, last }`. Section 11's lift: `liftHold(on)`, `liftRoofRide(speed)` (E3 on the lift owner's behalf); 14: one typeof-guarded line where crew call the lift (`liftHeld()`); 8b a `grease` pose (falls back to `work`); the camera in the shaft.
- Useful existing code: section 17's `liftStuck(on, until)` / `liftStuckNow()` / `LIFT_STUCK_X` (24f's stuck-lift incident: crew lift rides 3× slower; not saved, 24f re-calls after a load) is the nearest thing to "held"; read how 24f's incident uses it (`INC_LIFT`, around `O.kind === 'lift'`) before writing `liftHold`. "Section 11" in the page means the interaction/lift code: search `liftRide`, `LIFT_AT`, the lift panel (`liftPanel` wall kit), `goToDeck`.
- If it slips it ships after the rest of Step 4 on its own (the summary's lead's call).

## How to test
- Setup: `pip install playwright`; three.js at /tmp/cadet-work/three (DEV_NOTES "Testing"); `CADET_CHROME=/opt/pw-browsers/chromium`.
- `python3 mech_check.py BUILD.html m10 t24` (quick), the whole mech_check, deck_check, `cadet_test.py OLD NEW` from a scratch folder, interactions_check.
- Scratch helpers I used (not committed; easy to rewrite): a tile map of free/blocked/place tiles per room, an EDGES probe for wall edges, a screenshot script (goToDeck, place the player, set `az`/zoom, `document.getElementById('walls').click()`; the address banner can block Playwright clicks), tap walkthroughs calling `playerTap(item, pos, pos)` and `devChosen(k)` for device cards (open a chat and act in the same `ev`: the card closes when you step if the person isn't near).

## Gotchas
- `pkill -f` with a pattern that matches your own shell's command line kills the shell (exit 144): use `[d]eck_check`-style patterns.
- Parallel test runs on the same file name share cadet_test's `_run_<name>` copy: give each run its own file name.
- `type: 'event'` places with no `event` field land in the crew's everyday place list (schedData): always give them an `event` tag.
- `mailSend` unshifts (newest first).
- Gift names are matched in lower case (`giftOf`): keep tinkered item names lower case.

## Open questions for the user
- None of mine. The pages' "lead's calls" stand as built (tinkering from Day 6; orders from Day 12; stars 20:00-23:30).
