# Handover: adversarial reviewer 1c

- **Role:** adversarial reviewer for Pillar 4, added to share reviewer 1b's queue (session_018XY1NbMBxo2SLDPxooe5yx). Report to the lead (session_01KPJMYjXAPkNUcrQ8VRkhLE) with send_message; send each verdict to build master 2 (session_01F8ph7FKqViF3heRn94YgBr) too, and fixes to the owning seat (ids in TEAM.md on claude/lead-pillar1). Never contact the user. Never change game code.
- **Branch:** `claude/reviews-3`, notes only, under `plans/reviews/`. Style: verdict PASS / PASS WITH FIXES / FAIL, a severity per finding, a concrete fix, proven on a merge where it matters (1b's notes on claude/reviews are the model).

## Done (2026-10-17)
| Item | Note | Verdict |
| --- | --- | --- |
| Roster claude/deck-plans-1-2-6 d53cf40 (0.16.15 kin/lost/hobbyNoun) | roster-d53cf40.md | PASS WITH FIXES: talent-theme hobbyNoun for quist-ilse, jovanovic-petra, juarez-nell |
| Arrival claude/arrival 0ea5048 (0.42.20-21 tour, dinner, bed arrow) | arrival-0ea5048.md (+ arrival-0ea5048-tour_probe.py) | PASS WITH FIXES: HIGH, a follower hears 19/61 tour lines (overlapping places, out of order, pacing); MEDIUM, leftover lines over the dinner and the Chief |
| Player claude/player-needs 4776216 (0.28.29-0.28.35) | player-4776216.md | PASS WITH FIXES: MEDIUM, joining the line at tap time stalls the counter; lows on the tray, lie-to-sleep, the strip |

**Open loose ends:**
- The onboarding seat (session_01KaHzfqSqF8B4bkNFrH1tsx) was inactive, so the arrival fixes went to the lead to route.
- **Galley 40166d6 + sim bfcd864 fail player_check's job loop (5) and food_check (4) together**, with or without the player branch; each alone is OK. Reported to the lead, the build master, galley engineer 3 and sim engineer 4.
- Reviewer 1b never answered my first message. Check that they didn't also review these three.

## How I test (fresh container)
- `pip install playwright`; three r128 unpacked at /tmp/cadet-work/three (DEV_NOTES "Testing"); `CADET_CHROME=/opt/pw-browsers/chromium`.
- Merge the way the build master does: start from a branch that already carries the latest ship-integration (e.g. galley), merge the others in, resolve build lines by keeping either.
- **Gotchas:**
  - Run one browser test at a time: two at once made page loads time out (60 s).
  - Never wait with `pgrep -f "<pattern>"` in a loop: it matches its own command line and never ends. Use `pgrep -f "[p]attern"`.
  - In a probe that `exec`s cadet_test.py, don't name anything `HOOK` (it replaces cadet_test's own, and the game never starts).
  - player_check skips its real-line test when `lineSpot` exists, so walk the real line with a probe on a combined build.
- Probes live in the scratchpad; the tour one is saved next to its note.
