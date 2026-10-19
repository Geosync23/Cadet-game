# Rec deck reviews, reviewer R7 (session_01HCwvy5w432bhz41UYxHYwq), from 2026-10-19 ~09:50

Brief: plans/brief-recdeck.md on claude/lead-pillar1 ("R" section). Lead 18 session_01CBur9nrJ411pFkHopF96RL. Build master BM8 session_01YGy9FDmcbkySMJpVPYJaAo. Earlier verdicts: R6's, in plans/reviews-p5-step4.md ("Rec deck activation"). Newest first.

### RB claude/rec-works 3a1cc57 / d9aea96 / 4cfe651 / b899519 (0.84.4-0.84.7, on e4c5da2), R7: PASS WITH FIXES (two small)
Read by hand (the whole game diff, ~260 lines); no code after `//`; no duplicate declarations (whole-build scan vs aa4f42c); nothing new at load calls R() (recMix is a number hash; the float sign's canvas and the belay tags are made lazily on Deck 7, the two crew rope meshes at the first crew climb).
- 0.84.4 `recShutAt`/`recShut`/`recSigns`: pure on the hour record, cached on MACH_REV + hour, REC_OK while dormant; colours through col(); the pool gets its own water material so the river doesn't cloud. Refusal guards in recTap/recStart.
- 0.84.5 the pool leak: an ordinary traced fault (poolfilter `seal` `line: 'pool'`, MACHINE_LINKS.pool only while on), two additive lines in traceSymptom (LINE_SHOWS) and traceGoal (poolDripGoal), 24o's puddleAt reused (no copies). `j.drip` lives on the job (jobs are saved whole), so old saves just lack it (the drip shows again: fine).
- 0.84.6 crew moves: one guarded line in CrewAgent.update (and its talking branch), one in the main loop; recCrewKit keeps a body's full/crowd kind, so it doesn't fight crewDetail. Only reachable from a place with `move` or `anim: 'slump'`, which RA's places will supply: **BM8: check the moves and draw calls on the combine** (RB's probe: +3 calls for 6 movers).
- 0.84.7 still swap: right. scanFitted/caseTry show the `still` of the cause whose part you fitted (`fault.still.<kind>.<that cause>`), so it names its own part and the real fault's symptom.
- **Fix 1 (climbing):** recStart refuses a climb only with both belays out, but recSigns tapes off route `recShut().route` and tags belays 1/2 over routes 1/2, and recStart still lets you climb the taped route or the one under a tagged-out belay ("You clip into an auto-belay on the blue route" under a red tag). Refuse those too (W3's `rec.shut.belay` "That route's auto-belay is tagged out. Try the other one."; a line for a taped route from W3, or the same idea in RB2's draft).
- **Fix 2 (words):** read W3's keys with worksText and keep RB's words as fallbacks: rec.shut.float/net/belays/belay/pool (0.48.121), and SYMPTOM_TEXT.pool now "Water dripping from the ceiling in main storage" (W3 0.48.122), else Maps says "...from the ceiling on Deck 5".
- Note: traceMarks' several-deck branch still prints "Decks 5 and 7" style numbers; not reachable (the pool line is all on R), leave it.
- Checks (mine): dormant: node --check OK, machine_check OK, deck_check OK, interactions_check OK, cadet_test vs aa4f42c ALL IDENTICAL (0 px everywhere). REC_DECK=true copy: machine_check OK (incl. Pool leak), deck_check OK, interactions_check OK, disc_check ALL OK.

### W3 claude/writer-rec f086aec + 4163cfe (0.48.122, symptom.pool reads "... in main storage"), R7: PASS
Text + bake only; keys-rec.md gains the two Works rows. Bake unchanged, lines_check PASS. (SYMPTOM_TEXT.pool in RB's code still has the old words: RB2 to match or read the key.)

### Handover from R6 (~09:51)
R6's last verdicts: RB e4c5da25 PASS, W3 019dcd1 PASS, **RA 22ff1bb6 PASS WITH FIXES** (open, to check on RA's next hash): (1) a lone crew Lightdisc player books the player's 7-disc-1; (2) day_check 1b passes with zero visits; (3) f-string precedence at day_check 131-132; (4) DEV_NOTES "three ways" vs two.

### W3 claude/writer-rec 18cf522 (0.48.121, rec Works texts), R7: PASS (notes)
- Content only + bake: `content/works/rec.lines` (rec.shut.float/net/belays/belay/pool, trace.pool.goal/drip/up, symptom.pool) and their 9 baked LINES entries. No functions, no code. Fresh archive: content_gen leaves the build unchanged; lines_check PASS (the 5 old "(Just listen)" warnings).
- Keys against RB's code (claude/rec-works 33b7738): trace.pool.goal and trace.pool.drip are read by `worksText` with matching fallbacks; trace.pool.up, rec.shut.* and symptom.pool are proposals not read yet (RB2 to wire; `SYMPTOM_TEXT.pool` has the same words). "Up the spine ladder to the rec deck" is right: R sits above Deck 5.
- Note for RB2: the symptom shows as `SYMPTOM_TEXT + ' on ' + deckIn(deck)`, so it reads "Water dripping from the ceiling on Deck 5"; fine, "in main storage on Deck 5" might read better (W3/RB2's eye).
