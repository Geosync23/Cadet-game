# Handover: lead 37

## START HERE (next lead)
Read CLAUDE.md, this note, then the bottom of TEAM.md on claude/lead-37 (from "LEAD 37 started", incl. the "CURRENT SEATS" line ~00:12 UTC Oct 26). plans/handover-lead36.md has older background and gotchas.
Lead 37 = session_019GcNZ4GGEqfiuYDYnue7nX, branch claude/lead-37, hourly check-in trig_01Wyf6MPuWdJCXF7DMdQoixq (57 * * * *): disable it when you take over and make your own.

## State (~02:00 UTC Oct 26, 10 PM Eastern Oct 25)
- LIVE: 0.93.1 on Playtest 3HqM5XiXaHXzgrpq7JbesJ v5 + Dev 9ZWAgqiZCvkJvVjjhjVkEr v5 (claude/staging-0.93.1 b957b92d, game 6cd54ab9...8eee). claude/integration = b957b92d. User's current-save link 6daNCLCJAcsLCZn27CEthq (0.92.2): NEVER publish over it.
- 0.93.0 = sound + music (SD1 core, FX20 activities, FX22b music + Music app) + reserved-job fix (FX17). 0.93.1 = promo-arrow fix (RV16).
- Publishing: the user's standing say is BOTH Playtest + Dev after a GO round (PUB1 session_01GnpjFR6oumvuvTrmcXSqeg). Always ask the user before fast-forwarding integration.
- Every game change: full six-runner round before merge/publish (BM18 runs it).

## Next version (0.93.2), being prepared, NOT tested yet
1. Event order swap (user decided): FX22b on claude/event-swap from b957b92d, behind EV_SWAP_ON (off): short visit Days 16-19, comet Fri Day 26 21:30 (both stay draft), Vance memo -> Day 16 08:30, senior briefing -> Day 19 08:00, night shifts Days 19-20 (Kowalczyk crescendo dawn Day 21), new hand's tea retired, Basil 4 = welcome dinner in the mess Day 25 (CS1 abe48f47), Friday address words Days 19/26 drafted by FX22b -> SW2 (session_017dLaLFBnRUQin3PQEQq6so) to polish. design-doc updated in the same commit. Needs a fresh reviewer (RV17 ~52%, RV16 ~43% can do small ones).
2. Traditions: Scone morning (yes), six weekly ones take turns from week 2 (yes), week 1 unchanged, new hand's tea retired; round-2 picks pending: page https://claude.ai/artifact/EFioZPqoM6X6BT7obruTgx (22 ideas; answers in its db: ArtifactData get collection answers doc user). Round-1 page DfXQg3Ff4eX2hfoiTA86Jh (answered). Builder needed for traditions once picks are in (trad_parse needs "every 3/6 weeks" for scones; new key range).
3. The user said "more changes" are coming for the next version: wait for them, batch, then one round.
- Listening pass on sound: user hasn't given feedback yet; route to SD1 (core), FX20 (activities), FX22b (music). Listening list: plans/sound/audio-todo.md (dryer, airlock, shuttle bay not built).

## Seats (see TEAM.md CURRENT SEATS)
EP1 (new) session_01LjeoeX6qpCuwTV5UNVNwV5 (USER: comet ON in 0.93.2; FX22b builds it after the swap): detailed plan page for the visit + comet (claude/events-plan-2) → publish to the user.
RV18 (new) session_01PMfvrCN6StPzwVSPGX7ijH reviews both FX22b and FX24.
FX24 (new) session_017zuWxNJfppnVwkQDtiwnb6 (USER RULE: every tradition = host you tap to join + simple pose/animation for the event + unique dialogue): traditions on claude/trad-0932 (take-turns, 14 new, tasting table rework, tea retired). CS1 writes words. Round-2 answers in: 13 yes + scones; Valo undecided.
BM18 session_01A3S2VBMYmTt2wCZa8ej7XR (fine). Runners CR1, CR2, CR4, CR5, new CR6 fine; CR3 ~59% retired -> hire fresh CR3 from plans/handover-cr3.md (claude/checks-cr3) before the next round. FX17, BM17, old CR6 retired.

## Gotchas
- Messages to helpers can arrive late (FX22b got 18:16-19:24 messages at 19:57). Builders should send shas directly to reviewers and BM.
- Retired sessions still get messages; keep TEAM.md "CURRENT SEATS" current.
- cadet_test pixel noise on a busy machine: rerun alone; must be 0 px.
- Checks that move with a game change (arrows promo, arrows_d S3) were stale, not game bugs; still trace each one.
