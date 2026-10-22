# Handover: lead 25

## START HERE (lead 26)
1. Read CLAUDE.md, this note, then the bottom of TEAM.md (lead 25's section, from 2026-10-21 ~18:00 UTC).
2. Branch: start `claude/lead-26` from `claude/lead-25`. Push only there.
3. Make your own hourly check-in scheduled task, then disable lead 25's (trig_01KAvJhBaP2WS636Si64iZ6H, minute 6).
4. Message every seat below with your session id so they report to you.

Lead 25 = session_01J2aTyEohBf8KFHCsTqt3LW, branch `claude/lead-25`. Took over 2026-10-21 ~18:00 UTC on the NEW account (the project moved accounts; old seats and old pages are gone). Handed over at ~475k memory.

## The user's standing rules
- Plain language, no jargon, **no emojis**. Safety of the code is paramount.
- Push a phone notification for every new build, milestone or question.
- Never change the look of the game (pixel-identical regressions); a missing menu word is a bug fix, not a look change.
- main and the published links change only for a passed build. PRs/merges to main only on the user's go.
- Up to **14 active seats**; any number on standby.
- Handover at 500k (warn) / 600k (hand over), every seat.
- Full test round: before every release, whenever the coverage map is remade, and at least once a day. Between those, the test picker on option (a) "Careful".
- Standing crowd limits are set by performance tests, not fixed guesses (the user, 2026-10-21).
- Camera: 1.62 / 1.22 (0.64.12, the user asked 10-15% back from 1.85 / 1.40).

## Game pages (this account)
- Playtest: https://claude.ai/artifact/Wn6mUGcxatoWVqhCNTa1vs (v2 = 0.64.13)
- Dev: https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq (v2 = 0.64.13)
- Publisher PUB1 (session_01GnpjFR6oumvuvTrmcXSqeg) republishes both to the same URLs from a named commit (it made them, so no read is needed). Recipe: plans/handover-lead23.md on claude/lead-24.

## Builds
- 0.64.12 (9654f37): camera. 0.64.13 (a7477a9): storm + Short Fridays ON. Published.
- **0.64.14** (claude/integration 8e239328 + one docs commit; game sha256 94f32868dbe7f27fc744eb834bb6b5f7c335bc15ac1bca86563d8ca4652881e9) = 0.64.13 + opt-render (#4/#10/#6/perf scenes/#8/#5 memory) + tiles_check fix + EC1's bigevents_check + PB2's 4 game fixes cherry-picked (double dinner, harvest salad on farewell days, backlog 18 storm rec gates, section 17 one job per panel) + fridays-20 (#20 Halloran tea seat + #25 stand-in stations). check_fast, day 2/3, cadet_test OK. **Full round running on CR1-CR3** (split below). When all OK: tell PUB1 to republish from that commit, notify the user.
- Full-round split: CR1 player, intro (--week/--firsts/--evening), interactions, clothes, bubble, devmode, events, fridays, day 0/5/7. CR2 talk, social, join, lines, food 11 4 + 1 7, mech, machine, career, bigevents, day 1/12/13/16. CR3 perf (vs a7477a9), arc, path, tiles, disc, puzzle, deck, day 19/21/27. Known old FAIL: career "Relied on before Day 5" (backlog 12).

## Next, in order
1. Publish 0.64.14 after the full round.
2. **Check-only merge** into integration (no build number): claude/opt-tests (TS3: test picker (a), event days, planted faults, plans/testing-guide.md; OR2 must pass its latest tip; take opt-render's perf_check) + claude/fridays-20 169f0b3 and the commit after it (intro_check seat-clash guard, PR9 PASS). Then offer the user the testing guide as a published page.
3. **The Line** (claude/line-update 2ee2724 + c7a092a, PR10 PASS, Line OFF): merge integration into line-update (LB3). Note: patch-b2's be8871d and L5j hit the same tradMeal line: keep L5j's 3-line if, then `e.ate = true;`. line-update's food_check needs integration's copy + EV5's Brennan rota line. Re-review, then L6 switch-on **only on the user's go**.
4. Check gaps from TS3's planted faults: intro_check misses a late day shift and a missing "find you" ask; career_check misses every day being an event day. Assign a check seat.
5. Backlog: 24 (Line, slow Deck 3 door ~(35-36, 9.5), section 10), 22 (cooker fault frequency, design call), 14 (perf memory +2 geometries/lap), PB2-1..3, 27 (PB2's nits on fridays-20).

## Seats (all on this account)
| Seat | Session | Branch | State |
|---|---|---|---|
| BM13 build master | session_01ExFoVfhiFG3wYTFv2QrojC | claude/integration | idle, waiting on the full round |
| PUB1 publisher | session_01GnpjFR6oumvuvTrmcXSqeg | claude/publish-25 | standby |
| CR1 / CR2 / CR3 check runners | session_01CsWNjCsy8u5mrHJgTVgCst / session_01BgMQaB1LQmhfU1rSJ2ATvv / session_016oCbvvzgcqzzCTsBFCkYRB | claude/checks-cr1/2/3 | running 0.64.14's full round |
| PR9 Fridays reviewer | session_01B1FUTc4sJR4Q5FFnx7L6Db | claude/review-8 | idle |
| PR10 storm + Line reviewer | session_01KG4WKkSL57buDyiygrA5tF | claude/review-6 | idle |
| OR2 opt reviewer | session_01AnRKXUUGi8mwREwvt4WbaV | claude/review-opt | reviewing TS3's latest |
| TS3 test speed | session_01QHLjBmVWZLhTVztucsuTeP | claude/opt-tests | planted faults, guide fixes |
| FR4 Fridays builder | session_01YDM1FcnY4nLuD7PN3JMK8R | claude/fridays, claude/fridays-20 | idle |
| PB2 section 14 owner | session_01NWyw8ebj9kTTRiEnAj2bGo | claude/patch-b2 | idle (future integration fixes start from claude/integration) |
| LB3 Line builder | session_01VGHVEQ9kkwqbdcWURcvp1E | claude/line-update | idle, waits for the integration merge |

## Gotchas learned
- Messages cross: always name the exact commit (tip) a seat may take.
- Check which base a branch sits on before merging (patch-b2 sat on line-update; BM13 cherry-picked).
- Release candidates: every runner reports the game file's sha256; the build master's file must match.
- day_check.py must keep EV4's storm skip (4fa198f).
- *.png is gitignored: use git add -f for shots.
- 5 old sessions on this account couldn't be archived (permission check); the user can archive them in the app.
