# Backlog: small known bugs

Started by the ways-of-working engineer WW1 (2026-10-20) from the roadmap's list (`plans/roadmap-after-recdeck.md`), START-HERE.md's "Things for the user to look at later", lead 20's notes and the reviewers' notes. **Anyone who finds a small bug in passing adds a row here** instead of fixing it outside their brief or losing it. Fixing one is a normal piece of work: the owner's seat (`plans/owners.md`), a brief from the lead, the usual checks. When one is fixed, move it to "Fixed" with the build.

Lines are at 0.64.2 (rec-cand-s1 1eeb99c); `python3 tools/section.py --where LINE` names the section today.

| # | Bug | Where | Owner seat | Found by | Notes |
|---|---|---|---|---|---|
| 1 | **An unclosed CSS comment swallows two rules.** The comment that ends line 181 (`/* 0.72.0 (the user's playtest): a little smaller ...`) has no `*/` until the end of line 183's own comment, so `.device .app i{...}` (line 182, the app icons' size and colour) and `.device .app span{...}` (line 183, long labels wrapping inside their tile) never apply. | `page`, lines 181-183 | HUD seat | the 0.63.5 publish read (lead 19) | Fixing it changes how the device's app tiles look (icon size 26 px, labels wrap): needs screenshots and the user's eye, so it is a look change, not a silent fix. |
| 2 | **A `//` comment hides the small door gear.** In `doorGear(g)` (Deck 5's bay door gear), line 1732: `... small.position.set(-1.0, 1.55, -.5);   // pitch circles touch small.castShadow = true; g.add(small);`: the `g.add(small)` is inside the comment, so the small gear is never added (it still spins in `SPINS`, unseen). | `4b`, line 1732 | Deck architect | the 0.63.5 publish read (lead 19) | Fixing it adds a mesh on Deck 5 (draw calls, Deck 5's screenshots change): cadet_test differences expected on Deck 5's bay only. |
| 4 | **Rec talent night only moves off the yearly talent night,** not other busy days. `rec-talent-night`'s `skip: d => Math.abs(shipYearDay(d) - 152) < 7` (line 34008) stands it down within a week of day 152, as lead 18 asked; lead 17's call 7 (it moves off a busy career day) isn't done. The 152 is also written in by hand: if the writers move the yearly one (`content/`, `dayOfYear: 152`), the two can land in the same week. | `18`, line 34008 | Traditions engineer (rec side: Rec engineer) | R7's review (`plans/reviews-rec-r7.md` on claude/reviews-r8), START-HERE | For the user to decide whether "busy days" matter. |
| 5 | **The Tracked panel fills almost the whole screen on a small (320 px) phone.** | `page` CSS, `trkPlace` (15b) | HUD seat | lead 19, START-HERE | |
| 6 | **On phones the tip card lies over the needs strip, Tracked and the activity bar** while it shows (`#devTip`, fixed at top 128 px). Pre-existing, not changed in 0.64.x. | `page` CSS, 19's `tipShow` | HUD seat (device engineer for the card) | RE20, lead 20 (told the user) | Not changed unless the user asks. |
| 7 | **"Seven decks" Deck 4 texts aren't gated on `REC_DECK`.** The deck directories (lines 4367, 5313, 6446, 6713, 7142) and the spine ladder (line 4404) say "Seven decks" even with the rec deck switched off. | `4d` | Deck architect (words: writers) | R6/R7 on W3's 0.48.117, BM9 | Harmless while the rec deck ships switched on; matters only for a build with `REC_DECK = false`. |
| 8 | **`REC_HABIT_TEXT` is declared and never read** (line 9783), so its "rec dec" texts never show. | `14` | Sim engineer (words: writers) | R7's review | Either use it or remove it (removal: check nothing else reads it; cadet_test identical). |
| 9 | **Lightdisc's older toast "The rec dec's closed till six."** is written text, which the naming rule (lead 18: mid-sentence "the rec deck") would make "The rec deck's closed till six." | `23b` | Games engineer (words: writers) | R7's review | |
| 10 | **Seed key 1039 is used twice:** Maeve's rec round (Fridays, line 10095) and the Cup's draw (Sundays). Harmless today, but a separate key is tidier. | `14`, `18` | Sim engineer | R7's review | Changing a key changes the crew's random rolls: cadet_test and day_check differences expected. |
| 11 | **Breakfast seat share on day 3:** day_check day 3 finds two crew settled in one seat ('3-mess-42 walsh-esme/kovac-zainab from 07:38'; 0.60.6a also '3-mess-16 dlamini-lukas/silva-bea from 18:24'). | `14` / `16` | Sim or galley engineer | the traditions engineer at 0.34.56 (DEV_NOTES "Known issues") | Not held for 0.60.7 (lead 11). |
| 12 | **career_check fails 'busy: Relied on before Day 5'** (a busy player's career pace). | `24` | Works career engineer | BM9/BM10 | **Known and accepted** by the user (2026-10-20): waits for the big balance pass. Not a bug to fix now; listed so nobody "fixes" it by changing the check. |
| 13 | **mech_check's parts share the game:** M8, M13, M14, M15, FC and FF run machinesNew/machinesNow before they rebuild the works, so their catch-up reads the last run's works. They pass today. | `mech_check.py` | Works career engineer | build master 8 (DEV_NOTES "Testing") | If one fails only on its first run, this is why. |

## Dropped

| Bug | Why |
|---|---|
| (was #3) "The double clock hold in the evenings" | Dropped 2026-10-20 (lead 20, the user): no record anywhere, probably a typo for the Day 0 evening's two designed clock holds (17:30 manifest until you sign; lead 13's call A while Zeke talks before dinner). |

## Fixed

| Bug | Fixed in |
|---|---|
| Two wall faults at once could leave you queued for a climb that never comes (`recBelaysUsable`) | 0.64.1 (RE20, item C, the user's) |
