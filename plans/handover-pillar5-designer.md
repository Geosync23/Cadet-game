# Handover: Pillar 5 designer (seat D: D2, then D3)

**Latest (D3, session_0115ZiGhf9s3oYtFdjs7TgYS, 2026-10-19 ~03:20, standing by idle on lead 16's word).** Lead: **lead 16, session_01UMyfd16GqSdgNyz5PE8qSv**; report only to it with send_message. Never contact the user, never start sessions, push only to `claude/p5-design`, stay inside `plans/` and `design-doc.md`.

## D3 did (all FINAL, all in design-doc's Ship traditions paragraph "Rec dec traditions" and two Answered bullets)
| Piece | Files | Artifact | State |
| --- | --- | --- | --- |
| Rec dec traditions | `plans/rec-traditions-plan.html` (src `plans/mechanics/src/rectrad.body`) | https://claude.ai/artifact/4f8hTNDsaF9CdSiCMgy6xF (v3 → final, Version 4; v1/v2 were D2's JFMgkWEYAhoEa2HphtN4im) | FINAL: court Winner Stays On + Cup; pool Dawn swim; river Paddle club + regatta (Glow paddle out); wall Wall night (Ring the bell retired; a note for the rec owner on the page); float Float hour + Slow stretch; Wren talks small Mon+Thu 19:00 (stage ring, 4-10) + a chief's talk every 2 weeks (seats, 20-40), first Days 8, 18, 25, then every Mon/Thu |
| Traditions survey | `plans/rec-traditions-survey.html` | https://claude.ai/artifact/KxGGxgHgDvJMCpA8HfJbbn (db collection `answers`, one doc) | answered 03:01 |
| Rec dec mini-games | `plans/rec-minigames-plan.html` (src `minigames.body`) | https://claude.ai/artifact/Ubn2MJvidnuK1awcx2gKMP (Version 2) | FINAL: Reach, Lengths, White water (no gates, currents + stamina); rec deck phase, kayaks → wall → pool, each prototyped standalone, then integrated |
| Mini-games survey | `plans/rec-minigames-survey.html` | https://claude.ai/artifact/UhfG1mAAFfLXPWMob71eaM (db `answers`) | answered 03:15 |
| Step 4 side jobs (lead 16, overnight) | `plans/mechanics/` m10-workshop, m11-tool-upkeep, m12-logbook, m13-leak-hunting, m14-irrigation, m15-rewiring, m17-lift-roof, favour-cases, off-shift, step4-stages (srcs m10/m11/m12/m13/m14/m15/m17/p-favours/offshift/stages.body), index #s4, `step4-summary.html` (src s4sum.body) | https://claude.ai/artifact/A5z6YJqf5psGgUYDzrGU3Y (the summary with the ten pages as files) | DRAFTS for the user's morning review; small team E1/E2/E3 + B, R, W; 4 rounds; keys 1010-1026 (checked: 1000-1004 are H2's, 1005-1009 H2's spare); lead's calls listed on the summary |

## How the surveys work
A plain page with a `CARDS` list (id, options, rec) that writes one doc per Send to collection `answers` (`{survey, sentAt, by, answers:{id:{pick,recommended,note}}}`), published with `capabilities: {db:{}, user:{}}`. Read answers with ArtifactData `list` on the artifact's url. To make a new one, copy `rec-minigames-survey.html` and replace `CARDS`, the title, the plan link, the draft key and the `survey` name. The user writes important changes in the notes: read every note.

## Loose ends
- The rec deck plan (`claude/recdeck-plan`, not ours) still lists Ring the bell and "No practice, no times"; the lead was asked to pass the changes to the rec owner (session_013LcEsgjMTDMMeiACKLj2bB).
- Proposed seed keys 833-838 for the mini-games are unchecked against the key list.
- design-doc's Pillar 4 line "talent night only once a year" disagrees with the rec plan's every four weeks (not mine; flag if asked).

---


**D2's latest (2026-10-19 ~02:40, session_01VAVLL8kQNeQwiZ7TJZ6GMF, stopping at ~65% memory as the user's rule says).** Report to **lead 16, session_01UMyfd16GqSdgNyz5PE8qSv**: only finished pieces (with hashes), blockers and design calls; builders may ask directly. Never contact the user; never start sessions; stay inside `plans/` and `design-doc.md`; push only to `claude/p5-design`. Approval is the user's, relayed by the lead.

## Where everything stands (this session)
| Piece | File(s) | State |
| --- | --- | --- |
| Tier 2 fault tables | `plans/mechanics/fault-tables.html` (src `ft.body`) | APPROVED (7e4c17b); a `Line` column (water/heat/air), damper table |
| Step 3 pages | promotion-officer, m8, m9, p1, p2, case-engine#t2 | APPROVED with changes (e6b6601): M8 2-3 team jobs a week (rota on the page), stage 2 in Step 4; P2 gated on `SHIP.works.said.p2`; the full air line in Step 3 |
| Air line for the deck architect | `plans/mechanics/architect-air-line.html` (src `air.body`) | sent to DA5 (session_01CHRbUTZc18m7eBck8eWhXj, branch claude/deck-p5s3) |
| Plan v11 | `plans/pillar5-plan.md` + `.html` | the Step 3 survey answers |
| Holidays | `plans/holidays-plan.html` (src `holidays.body`) | ON HOLD (user); 7 questions unanswered; design-doc untouched for it |
| Ship-wide events | `plans/events-plan.html` (src `events.body`), artifact https://claude.ai/artifact/5fAouaAV1K1qptqPYez9rt (v5 = plan v4 approved) | APPROVED 2026-10-19 and written into design-doc "Ship-wide events" (71fe06b). Phase 1 = the nine in Days 1-26 (comet 2, storm 4-5, Space Creature 8, visit 12-15, surge 17, Echo 18, distress 21, Loss of Power 24 07:40-11:40, inspector 25); Phase 2 = the other eleven. Remaining open questions: the recommendations stand as the plan |
| TNG pitch | `plans/events-pitch-tng.html` (src `pitch.body`), published as a second file of the events artifact | matches events v4 |
| Rec dec traditions | `plans/rec-traditions-plan.html` (src `rectrad.body`), artifact https://claude.ai/artifact/4f8hTNDsaF9CdSiCMgy6xF (FINAL, Version 4); survey https://claude.ai/artifact/KxGGxgHgDvJMCpA8HfJbbn | FINAL (the user's survey 2026-10-19 03:01), written into design-doc's Ship traditions: court Winner Stays On + Cup; pool Dawn swim only; river Paddle club + regatta (Glow paddle out); wall Wall night only (Ring the bell retired); float Float hour + Slow stretch; Wren talks small Mon+Thu + a chief's every 2 weeks |
| Rec dec mini-games | `plans/rec-minigames-plan.html` (src `minigames.body`), artifact https://claude.ai/artifact/Ubn2MJvidnuK1awcx2gKMP; survey `plans/rec-minigames-survey.html` https://claude.ai/artifact/UhfG1mAAFfLXPWMob71eaM (db collection `answers`) | FINAL (the user's survey 2026-10-19 03:15, Version 2): Reach, Lengths, White water with no gates (currents + stamina meter); built in the rec deck phase, kayaks → wall → pool, each a standalone prototype first; in design-doc |

## Next
1. When the user picks the rec dec's last five: update `rectrad.body` (mark approved, drop the rest, refresh the week view), rebuild, republish to the same artifact (`Artifact` publish of `plans/rec-traditions-plan.html`; it keeps the URL), then write the approved rec traditions into design-doc's traditions section (and the rec dec answers) in the same commit.
2. Builders' questions on Step 3 pages: answer, and record each in the page's "Builders' questions" section.
3. Step 4 pages (side jobs, Step 2's optional stages, M8 stage 2, favours, fault-finder tickets, cabin touches, star logging) when the lead asks; then Step 5.

## How pages are made
Edit `plans/mechanics/src/<name>.body` directly (4 header lines TITLE/H1/SUB/NAV, then sections), then `python3 mk.py X.body ../OUT.html base.css` (pages outside mechanics/: `../../OUT.html`), then check `NODE_PATH=$(npm root -g) node chk.js $(realpath OUT.html)` (390 px, no sideways scroll). The scratchpad generator scripts used for events v1-v3 are gone: edit the bodies by hand now. Republishing an artifact from another session needs an `Artifact` read of it first (and a read of each extra published file you replace).

## Gotchas found this session
- The newest game file is on `claude/p5-cand-s2` (0.63.1), not this branch; `lead-pillar1` is old (0.41.4).
- `ROSTER_ROTATIONS` already has crew rotations on Days 35, 77, 119; `bridgeInvite` is due the day before bridge hour (Day 22 now); events need a fixed-day `earliest` with `spread: 0, gap: 0`.
- Bridge hour: every 4 weeks, Tuesday of week 4 (Day 23 first); talent night every 4 weeks from Day 14 (the rec plan).
- Deck 5's air plants are `5-scrubber-1/-2` (kind airplant); `5-fan-1` is a stand-in inside the locked Fan hall.

---


- **Role:** design only. Reports ONLY to the lead (TEAM.md names it; from 2026-10-18 ~15:53 lead 13, session_015UkCGSS9FyGoBdkePhrKbC (report only finished pieces, blockers, design calls; Step 3 paused by the user until Step 2 is out); on 2026-10-18 ~10:14 lead 12, session_01GjWhU9Z9V8RNoR8yyELA9V; before that lead 11, session_01YKC3CGA9VS4b7wuqLbPT7V) with send_message: one line when starting, one per finished page with its commit hash, at once if blocked. Never contacts the user. Never starts sessions. Stay inside `plans/` and `design-doc.md`.
- **Branch:** `claude/p5-design` (made from `claude/pillar5-plan` 93a5a7f). Predecessor: session_01FDy4na3u2FS8L8vEjR6gAR (archived), then session_01VXENaUt4vdyYtr3KjVZk9z (this note's writer, 2026-10-18).
- **Messaging rule (lead 12):** send the lead only design calls beyond the pages, finished pages (hash), or blockers; answer builders directly. (lead 11's rule, ~09:00, was the same:) answer builders' questions directly (no cc to the lead); message the lead ONLY for a design call beyond the approved pages or a real blocker. Record every answer in the page's "Builders' questions" section.
- **Seats (2026-10-18):** C Works career session_01LgTgzjeqLNrjeCa2iRzbYx; H cases session_013nqpqRFX4hh3cLPhhpZirJ; S systems session_01KxfsfBWkCGcncuuH2n1hFB; R reviewer session_01MSLjUdmeVJetxFhh9PqzLt; seat A's branch is claude/deck-0607.
- **Authority overnight (2026-10-18):** the lead approves or rejects each page against the approved plan; nothing waits for the user (`plans/overnight-decisions.md` on `claude/lead-pillar1`, last section).

## Done (2026-10-18)
| Commit | What |
| --- | --- |
| 8a50917 | Plan v9 (`pillar5-plan.md` + `.html`): P3 on Day 5 with the scanner, M2 uniform Day 8, puzzle rates 1/10 (Days 5-9), 1/5 (10-15), 1/4 (16-22; 1/3 own tier), 1/3 (23+), a T1 band; the case engine in Step 1 (seat H joins Step 1), P3 in Step 2; 24g scanner moved from M3 to H so Step 2 stays at 6 seats (D, B, M1, M2, H, A); M5's stale question fixed. `design-doc.md` taken from `claude/lead-pillar1` (newest) plus two bullets (Day-2 dates; puzzles from Day 5) |
| 46f10be | `plans/mechanics/foundation.html` (17 playerTier, jobs by rank, real faults, causes, job kinds with steps, reserved training/test jobs; 15 work steps, careerSpeed; 24 core: ladder, training, tools, reputation bands, Works app, save; hooks; tests; build and key ranges; the name clash) |
| 29904c1 | `case-engine.html` |
| 374dc66, 9b94208, 7c860ad, 3c6e396, c481db1, 62a9ae4, 0a99c09 | `m1-rounds`, `m2-uniform`, `m3-drill-inspection`, `m4-hauling`, `m5-tuning`, `m6-incidents`, `m7-scanner` + `p3-whats-been-tried` |
| 9cca2dc | `fault-tables.html` (Tier 1 complete, Tier 2 draft), `plans/mechanics/index.html`, plan notes on the corrections |

## How the pages are made
`plans/mechanics/src/`: each page's source is a `.body` file (four header lines TITLE/H1/SUB/NAV, then the sections), `mk.py BODY OUT base.css` wraps it in the plan page's style; `chk.js` (`NODE_PATH=$(npm root -g) node chk.js FILE...`) checks no sideways scroll at 390 px. Edit the body, rebuild, commit the html (and the body).

## Facts found that the plan didn't have (all on the pages)
- **Name clash:** `SHIP.career`, `ship.career`, `CAREER`, `career…` functions are the 0.61.x leave/missed-shift/time-clock system (section 20). Pillar 5 uses `SHIP.works` / `ship.works`; `CAREER_LADDER`, `careerSpeed` keep their names. Seat C is a different seat from the 0.61.x career engineer.
- **Builds:** systems next 0.33.43+ (0.33.42 is 0.60.7's Wednesday delivery), player 0.28.71+; 0.44, 0.45, 0.47, 0.49-0.59 (but 0.48 is the content writer's), 0.63+ free on every branch (checked 2026-10-18).
- **Hash keys:** 850-899 free (split on the foundation page: 850-854 core, 855-859 section 17, 860-879 mechanics, 880-894 cases, 895-899 spare). 900-949 is NOT free (901 sick, 920+k and 930 galley); 951-952 (time clock) are inside Pillar 6's 950-999. Suggested second range 1000-1049.
- **Deck 4 has no light-relay machine with a panel** (4-lights-1 is a dropped stand-in); real machines list is in the game's `DECKS[n].machines`. P3's first case is `4-washer-2` leaking.
- **Tiers in code:** junction Tier 3, doorgear Tier 2, valve Tier 2 (so a burst pipe's fix is a Tier 1 joint job).
- 0.60.7 builds clothes in 15c (`player.clothes`, the onboarding engineer's), the Wednesday delivery as crates (0.33.42), right-shelf parts (0.33.41), `HOLD_MAX` 3 and `shareOut` (0.33.40). Details: `plans/plan-0607.md` on `claude/plan-0607`.

## Since the first pages (all approved; FAQs record the builders' answers)
- Day 5's teacher is Emeka Halloran (Torres off Thu+Fri), by-lists first-on-shift; the work-step field is `how`; real faults are made by finding worn machines already at the top of faulty (S, key 856); lift machine 5-mainlift-1; galley alarm on 3-galleyplant-1; worksTabAdd; a case kind is open when its ladder row opened; P3 borrows the scanner lesson's escort at Washer 2.

## Step 3 (2026-10-18 afternoon; approval is the USER's again, through lead 12; send the lead each hash)
Done and sent: plan v10 (9e26a58: Step 2's optional stages into Step 4, the cold-case board into Step 5), `promotion-officer.html` (bc1171c), `m8-team-jobs.html` + `m9-tracing.html` (0e84ab7), `p1-when-does-it-happen.html` + `p2-who-saw-what.html` (445f63f), the T2 band on `case-engine.html#t2` and the index (b6d6534).

## Since (2026-10-18 afternoon, session_01VAVLL8kQNeQwiZ7TJZ6GMF)
- adc12e2 + 1083c85: Tier 2 fault tables complete (`Line` column: water/heat/air causes can be traced). e6b6601: the user's Step 3 survey applied (plan v11): pages approved; M8 2-3 team jobs a week (rota on the page), stage 2 in Step 4; P2 gated on `SHIP.works.said.p2`; the full air line now: `architect-air-line.html` (src `air.body`), M9 and the damper table. Fault tables' Tier 2 still awaits the user's approval.

- 33587e7: `plans/holidays-plan.html` (src `plans/mechanics/src/holidays.body`), for lead 13; the user put holidays ON HOLD (2026-10-18 ~16:54); its 7 questions are unanswered; design-doc.md not edited for it.

- 2c49900 (v1) and 69d076e (v2): `plans/events-plan.html` (src `plans/mechanics/src/events.body`, generated from a data script: edit the body directly now), the ship-wide events plan for lead 14 (session_01RHtJv7GJDi4qosgU8Gb2b8, the lead from 2026-10-18 ~23:20). v2 has the user's answers; its 7 open questions await the user.

- c28ea3f: `plans/events-pitch-tng.html` (src `pitch.body`); 7034c2d: events plan v3 (nine events in Days 1-26; pitch re-timed). With the user for approval (9 questions). Lead 15 (session_01TfFnwP88RmL4MhCWAMdSGn) from 2026-10-18 ~23:57 passes on the answers. Edit `events.body` / `pitch.body` directly now (the scratchpad generator scripts are gone with the session).

- 563dc35: events plan v4 (artifact https://claude.ai/artifact/5fAouaAV1K1qptqPYez9rt Version 4). The user OK'd Space Creature on Day 8: mark that question answered next time the page is touched (no new version just for it). Awaiting overall approval.

- 71fe06b: events plan v4 APPROVED (2026-10-19), written into design-doc's Ship-wide events. Lead 16 (session_01UMyfd16GqSdgNyz5PE8qSv) from ~02:15: Step 3 seats route page questions via the lead or directly. Standing by.

- 5f25fbd: `plans/rec-traditions-plan.html` (src `rectrad.body`), artifact https://claude.ai/artifact/JFMgkWEYAhoEa2HphtN4im: twelve rec dec traditions for the rec deck's activation phase (after Steps 3 and 4), for the user's approval (6 questions).

## Next (in order)
1. ~~**Finish the Tier 2 fault tables**~~ (done, adc12e2) (`fault-tables.html`, `src/ft.body`): each Tier 2 kind's causes in the Tier 1 format (card, up close, when, how common, still, from), parts from `STOCK` only, same card needs different signs. Needed by: M9's lines (water: recycler, filter, uv, pump, valve; heat: heater, heatpump, manifold), P1's first case (3-pump-1 `peak`; filter `always`; membrane; valve), P2's first case (scrubber: filter `always`, bearing `warm`, a new `panel` cause, part seal, `touched`). Air plant and main fan are stand-ins without panels (no tracing for air yet).
2. Whatever the user sends back on the Step 3 pages (fix, re-push, one line to the lead each).
3. Step 4 pages when asked (side jobs, Step 2's optional stages, favours, fault-finder tickets, cabin touches, star logging), then Step 5.

## Gotchas
- Line numbers on the pages are from `claude/cand-0607`'s game file; builders match by text.
- Every cause in a fault table needs a part already in `STOCK` (listed on `fault-tables.html`), and causes sharing a card need different signs.
- The solver's rule "no single clue solves it" catches plan examples (P3's did); check each later kind's example against it.
- Day 2 has only one new thing (rounds): 0.60.7's laundry and health check fill it.
