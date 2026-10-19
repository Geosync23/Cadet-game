# Rec deck reviews, reviewer R7 (session_01HCwvy5w432bhz41UYxHYwq), from 2026-10-19 ~09:50

Brief: plans/brief-recdeck.md on claude/lead-pillar1 ("R" section). Lead 18 session_01CBur9nrJ411pFkHopF96RL. Build master BM8 session_01YGy9FDmcbkySMJpVPYJaAo. Earlier verdicts: R6's, in plans/reviews-p5-step4.md ("Rec deck activation"). Newest first.

### 0.64.0 candidate claude/rec-cand-s1 50d55ef (BM9: the closed toast), R7: PASS
Game file: the two strings only (discAsk's toast at 41180 and the 15017 comment now say "The rec deck's closed till six."); no "rec dec's closed" left. The rest is BM8's notes and scripts under plans/. Closes my 3add6bf note.

### 0.64.0 candidate claude/rec-cand-s1 3add6bf (BM8/BM9, on the 0.63.5 final be3d7ee), R7: PASS (merges; the full round is the build master's)
- Order: f319ab3 (rec-works to 0.84.10, the switch not yet) -> 9dfe971 (rec-crew) -> a095799 (writer-rec) -> 87e3c5f (rec-works with 0.84.11's switch and 0.84.12): **the switch comes last**. `const REC_DECK = true;`, GAME_BUILD 0.64.0. No conflict markers left; node --check OK; no duplicate declarations (whole-file scan vs aa4f42c); the combined-diff lines are each branch's own, already reviewed.
- Court tap (15044-15046): RB2's net-down refusal first, then RA's Cup / WSO, then RA's queue and discAsk(recCourtWaiting()): right order.
- Climbing (15133-15138): RA's pick (the free belay route nearest your tap; recBelaysFree already leaves out a tagged-out belay and the taped route) then RB2's two refusals, which now only back it up. The crew side (10056) leaves out the same belays. Consistent.
- **Lead 19's question: yes, the old toast can still show.** In 3add6bf, recTap's three court lines (15044-15046) come before its own opening-hours check (15051, "The rec deck's closed till six."). So tapping the Lightdisc court or "Ask someone to play" between midnight and 06:00 reaches `discAsk`, whose guard (41180, section 23b) says **"The rec dec's closed till six."** Small fix before publishing, one string at 41180: `'The rec dec\'s closed till six.'` -> `'The rec deck\'s closed till six.'` (the 15017 comment can match).
- Note (rare, no fix needed now): with two faults at once (one belay tagged out and the other's route taped) recFreeFor('climb') is false with nobody on the wall, so a tap queues you for a turn that never comes; a refusal there (like "Both auto-belays...") would be kinder. For the next rec engineer.

### RA claude/rec-crew bd3db3f (0.83.1-0.83.2: the traditions engine, R6's four fixes, events_check days 92/99; +9dfe971's rename), R7: PASS (notes)
- Read: the rec traditions (REC_TRADS: rules in one place, the writer's .trad brings the words; deck-7-only ones load only with REC_DECK), WSO/Cup/regatta on paper via ldPaper (keys 1035-1039, RA's block), the talks' rota and cards, film's move and the first all-hands (on the first ship-wide event's address), the show cue to RB2's recShow (renamed in 9dfe971: the only cross-branch clash, now gone), Maeve's round, crew pick-ups and the lone player at 7-disc-2 (R6's fix 1). Every time in REC_TRADS matches the agreed list. No R()/Math.random in the added lines; no duplicate declarations; no code after `//` (8 comment hits read).
- SHIP.rec: `recClean` reads save.rec defensively (old saves start empty), SAVE_EXTRA writes it, newGame resets it.
- R6's fixes: (1) lone crew player waits at 7-disc-2, your tap plays them; (2) day_check 1b fails when the rec deck gets no evening visits; (3) the print fixed; (4) it really runs three ways (off / on without traditions via REC_TRAD_ON / on), the strict Commons rule on everyday use (lead 18's call). All closed.
- Notes (no fix needed): key 1039 is used for both Maeve's round (Fridays, her seed) and the Cup's draw (Sundays): harmless, but a separate key would be tidier; `REC_HABIT_TEXT` is declared and never read (its "rec dec" texts never show); Lightdisc's older toast "The rec dec's closed till six." (40228, base code) is written text that the naming rule would make "the rec deck's"; lead 17's call 7 (talent night moves off a busy career day) is only the day-152 skip in code: lead's eye.
- Checks (mine): REC_DECK=true copy: events_check OK, day_check OK (Day 1: Commons 40.4 mean / 69 peak with and without; the rec deck 4.9 mean, peak 11, under the cap 15), deck_check OK. Dormant: events_check OK, cadet_test vs aa4f42c ALL IDENTICAL.

### RB2 for RA claude/rec-crew 9dfe971 (0.83.3, rename REC_SHOW/recShowTick -> REC_SHOW_CUE/recShowCue) and RB2 claude/rec-works 2f0eea6 (interactions_check: the Tracked test's tap outside the panel), R7: PASS
- 87e3c5f (rec-works, check only): three more fallback points in the margins round a panel that fills the screen; PASS.
- 9dfe971: the three sites renamed, nothing else left by the old names (one comment). Whole-file scan, rec-crew 9dfe971 against rec-works 2f0eea6 (vs aa4f42c): no name both branches add. A trial `git merge` of the two has 6 text conflicts (header, the auditorium's dress around 8511-8577 and 8775, the REC_LANES area, 15r) for BM8 to resolve; afterwards node --check and a duplicate-name scan on the combine.
- 2f0eea6: check only; the tap moves to the first point clear of the Tracked panel that lands on the canvas (falls back to the old spot). Sound.

### RB2 claude/rec-works 2387479 (0.84.12: climb refusals, the talk's ring of chairs and stool, pool symptom words), R7: PASS (closes my fix 1)
- recStart refuses the taped route (`sh.route === r`, W3's rec.shut.route) and route 1/2 under a tagged-out belay (`belayOff`, rec.shut.belay), the same reading the signs use; REC_OK carries `belayOff: [false, false]`. SYMPTOM_TEXT.pool matches W3's words.
- The ring and stool: RB's kit (the auditorium's dress) for RA's places 7-ring-1..8 / 7-stool-1, one owner each; KIT.chair/stool don't call R(); shown only for 'talk', the mic stand hidden then (merged, noMerge). Note: the hidden microphone keeps its IT, so a tap there during a talk may still say "Microphone" (cosmetic).
- No code after `//`, no duplicate declarations. Checks: deck_check OK (Deck 7 178 calls), interactions_check OK, cadet_test vs 32f7710 ALL IDENTICAL (noise).

### RB2 claude/rec-works f319ab3 + 32f7710 (0.84.10 checks loop over DECK_ORDER; 0.84.11 the switch, REC_DECK = true), R7: PASS (merge the switch last, as the brief says)
- 0.84.10: device_check and machine_check walk `DECK_ORDER` (falls back to the DECKS keys for older builds); device_check's room-name fit now writes the HUD line with deckWord. Check code only.
- 0.84.11: the one line, `REC_DECK = true` (DECK_ORDER puts R between 4 and 5). Grep of the switched-on build: no "Deck 7" literal outside comments; every `'Deck ' + n` goes through deckWord/deckIn except Maps' goal, which has its own "the rec deck". The `{deck}` fills (rounds, team Mail, 24o leaks, the p2 case title) can't see 7 today: rounds and the logbook skip the rec deck (lead 17's call 5), leaks and team jobs are fixed machines on Decks 1-6, and p2 needs 3+ causes (rec kinds have 2 at most). **Keep that true:** a future rec fault with 3 causes would read "Deck 7" in a p2 card.
- Checks (32f7710 as is): device_check OK (Maps R), machine_check OK, deck_check OK (Deck 7 178 calls, 74 items, memory flat), cadet_test vs 11fb633 ALL IDENTICAL (noise only). RB2's: disc_check, interactions_check, the save on R reloading there.
- My fix 1 (climb refusals) is still open; W3's rec.shut.route is ready for it.

### W3 claude/writer-rec ef1fc0b + a095799 (0.48.127, rec.shut.route; W3's handover note), R7: PASS
One Works text for the taped route (my fix 1 to RB2) + notes; bake unchanged, lines_check PASS.

### RB2 claude/rec-works 0ab43cd + 11fb633 (0.84.8 recShow, W3's keys; 0.84.9 stage poses, crew perform/address, juggling balls, mic stand, piano side-on), R7: PASS (my 0.84.7 fix 1 still open)
- Read by hand; no code after `//`; no duplicate declarations; load-time adds are plain tables, two scratch objects and col() colours (no R()). Kit on R only: the music room's micStand/pianoBench (MUS, shared, no R()), the piano moved; the light pools' quad sits 3 cm over the stage top (.58 vs .55: not coplanar), additive, hidden with no show; the film cloth on its own noMerge pivot.
- `recShow(state)` (null/film/talk/allhands/talent), RB's to own, RA only calls it. House lights: applyLight sets intensities fresh each frame, so the `*= (1 - dim)` doesn't compound; it dims only in the auditorium (lastRoom 'A'). Ticks only while a show, a dim or the screen is on.
- 0.84.9: perform { act } loops the act + a 3 s bow; piano sits (`sit:play`, which exists); one juggler's balls at a time (one InstancedMesh, 3 instances, made at the first juggle). Fix 2 of my 0.84.7 verdict done (rec.shut.float/net/belays, trace.pool.drip + .up through worksText).
- **Still open, fix 1:** a climb on the taped route or under a tagged-out belay isn't refused yet.
- Checks: dormant cadet_test vs aa4f42c ALL IDENTICAL (0.84.8 and 0.84.9), machine_check OK (0.84.8); REC_DECK=true copy: deck_check OK (Deck 7 178 calls by the lift, unchanged; 74 items with the microphone), interactions_check OK (both).

### W3 claude/writer-rec 2cc8056 (0.48.126, mail.rec.talk.you names the day), R7: PASS
One Mail text ("It's on {weekday}, at seven.") + keys notes; bake unchanged, lines_check PASS. **RA: pass {weekday}** when you send it, or "{weekday}" shows as written.

### X3 claude/crew-pt1 6a4e153 (0.71.7, the 17:00 clock-out take waits 20 min, not 6), R7: PASS (forwarded by lead 18)
One number in section 14 `shiftWithBreaks` (the evening clock-out; the morning one stays 6); no code after `//`. On BM8's 0.63.5 WIP (p5-cand-s5 1e70683): leave_check FAILS unpatched ("the Works crew don't use the clock: [2, 1, 2, ...]") and is OK with the one line. On crew-pt1 alone: cadet_test vs 6a4e153^ ALL IDENTICAL; leave_check there fails "the reputation chip: None", the branch's older HUD, not this line (OK on the combine).

### W3 claude/writer-rec 4f2dcdc (0.48.125, talk.open/answer/listen and talent.* for RA's panels), R7: PASS
Content + bake: banks/talks.lines (anyone's fallback) and own talk lines for 9 speakers (the brief's four plus five for later talks); Lucia Ferreira (talent night's host) has talent.ask/tune/joke/trick/watch. In voice, short. Bake unchanged, lines_check PASS. Keys for RA to read when its panels land.

### W3 claude/writer-rec 3b96ca3 (0.48.124, symptom.pool -> trace.symptom.pool with {deck}), R7: PASS
Matches S2's traceTitle key (`trace.symptom.<line>`, {deck} = the drip's Deck 5, like air/heat). Bake unchanged, lines_check PASS.

### W3 claude/writer-rec ef14088 (0.48.123, the 13 rec .trad files), R7: PASS (W3's part); events_check needs RA's fix before BM8 merges it
- Content + bake: 13 `content/traditions/rec-*.trad` (k 486-498, the next free numbers after 485; no duplicate k; trad k's are their own number space, not the 1030-1049 code keys), trad-words/rec folded in, reactions/news on the new ids, Slow stretch 08:00 (lead 18). Every one has `flag: rec.on` (film night: `rec.film.moved`), and eventsOn skips a flagged-off tradition before anything else (eventPools only builds place lists, no R()), so nothing happens until RA sets the flag. Fresh archive: bake unchanged; lines_check PASS.
- Days and times against the agreed list (Day 1 a Monday): WSO Sun 11:30-16:30 from 7; Cup 4-weekly Sun (28, 56...); dawn swim Tue+Thu 06:15 from 2; paddle club Wed 18:30 from 3; regatta 4-weekly Sun 09:30 (21...); wall night Tue 18:30 from 2; float hour Wed 21:30 from 3; slow stretch Sun 08:00-08:45 from 7; small talks Mon+Thu 19:00-19:40; chiefs' 2-weekly Thu 19:00-19:45 (18, 32...); film night Sat 20:00; talent night 4-weekly Sun 19:30 (14...); all-hands first Monday of a season 17:45-18:10 (from Day 2, so Day 92; Day 1's is the first ship-wide event's). All right.
- What the format can't say is in each file's "FOR RA" comment (talks' career-day skips, the Day 8 Sato talk, WSO yielding to the Cup, the talent-night clash rules, film night's move): RA's engine work. Also for RA: lead 18's call that WSO "runs with whoever comes when Pell is on shift" vs the file's `pell always` + `host: pell`.
- **events_check FAIL (dormant):** "rec-all-hands and its flag rec.on: 0 days without, 0 with": the check wants each flagged tradition seen in its window, and the all-hands' first day is 92. events_check is RA's: list (not fail) a flagged tradition with no due day in the window, or step to its first due day. **BM8: merge ef14088 only with RA's events_check fix** (or the full run goes red).
- cadet_test: vs W3's 4163cfe ALL IDENTICAL; vs aa4f42c only `items` (the "Seven decks" directory texts from 8bb9823, R6's note: ship with the switch on) and 1-level noise.

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
