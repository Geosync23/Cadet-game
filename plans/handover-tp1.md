# Handover: TP1, tips, the device and HUD words (0.99.7 playtest patch)

Role: build the user's notes 6, 7, 9, 11, 28, 33, 53, 54 (plans/patch-0997.md on claude/lead-49). Lead: lead 49
(session_01GKuymjjreuZtZeDMBX79xn). Reviewer: RV32 (session_01GKuymkDX3gviqiGJcKLWuS). TB6 (session_01GKuymj43WbsuRbKgL2mYc2)
was told about the `join997.*` keys (note 53).

## Branch and builds
- Branch claude/p997-tips, from claude/integration d7ad4c58 (0.99.6, game f6ff5ec1...db8a8).
- 9c7a288: all eight notes (game 0e63713c...5759). Its commit message's Claude-Session line names the lead's session by
  mistake (a force-push to fix it was blocked; left as is).
- The next commit: the two new tip ids shortened to `t:997call` / `t:997trk` (player_check's rule: ids under 12
  characters), and player_check made aware of the switch (see Tests). Sha in the build table row and the message to RV32.

## The switch
`var TP997_ON = false || URL_FLAGS.has('tp997')` (section 13, right after TRAD995_ON), and
`var TP997 = { n6, n7, n9, n11, n28, n33, n53, n54 }` (each defaults to TP997_ON; set one false to drop a note).
Off = 0.99.6: cadet_test vs d7ad4c58 ALL IDENTICAL. Words: content/banks/tp997.lines (new keys only).
DEV_NOTES "Tips, the device and HUD words for 0.99.7" lists where every piece lives.

## What each note does (switch on)
- 6: Day 2, 19:00 (or once your Day 2 call ends) to 22:00: "One call home a day..." (TEACH row `t:997call`); Day 4's
  `t:eve-call` is marked seen.
- 9: Days 1-3 from 06:00: the Schedule tracker tip (TEACH row `t:997trk`).
- 11: `t:devwork` as soon as a work step of 5+ minutes starts (tp997DevWork, from teachTick's first line; tipFront).
- 7: "Nearest bathroom" in the tracker's Places (place:loo): this deck by walking path, else the nearest deck by lift order.
- 28: the rec deck's lift line: "Auditorium, court, pool, rivers, flight sim".
- 33: Pockets app; store snacks and drinks go in SHIP.player.pack (max 4, saved only when not empty); Eat/Drink.
  Lead 49's default; it's an open question in design-doc.md.
- 53: join words for the 50 traditions without any (join997.<id>.tip/.notice), a sentence-shaped fallback
  (tp997Notice), the tip's second sentence (tp997More), the thanks Mail keeps capitals.
- 54: "Mark all as read" at the top of Mail while any is unread.

## Then: the first week's missing arrows (lead 49, RV32's find; TP997.nd1)
Day 1: the arrow to the Works bay from 08:20 for the 08:50 briefing, the time clock's from anywhere after it; 15b's
clockFirstTick holds its early clock arrow until the briefing (it led to a job and a missed briefing). Day 2: queue
entries for the Chief's 08:45 meeting and the 18:00 booths (tp997GuideWeek). Lines touched: introArrowWant (1),
clockFirstTick (1), guideShift (1). MV1 told (it changes the same briefing). Seen with RV32's fresh_walk.py: briefing
08:50, clocked in 09:06, shadow job; Day 2 meeting 08:45, booths 18:08. MV1 may want to know: in the walk, taps on the
time clock just after the briefing opened the Chief's chat a few times before the clock took it.

Then (lead 49, RV32's Day 2 walk: a leisure arrow took over before Zeke's 10:45 meeting): in week 1 the needs arrow
stands aside while a level 1-2 queue entry is live and comes back after (needGoal and needGoalTick, one line each;
introArrowTick may replace a needs arrow); beats with arrows for Days 3-6 too (crew store from 17:00, quiz, Friday tea,
Sowing). fresh_walk to Day 6: every timed beat had its arrow, no errors, nothing stuck.

## Shared lines touched (owners review)
Section 15: teachTick (1 line), actEnd's pay step (1), playerNew (1); section 19: the skin's GLYPH (`pocket`);
section 18: tradWords, tradJoin's notice, tradJoinMinute's ixTip, eventJoin's thanks Mail. The rest is in the
Device engineer, Player engineer, Interactions engineer, Traditions engineer and HUD seat slots.

## Tests
- Probe: `python3 plans/tp1-probes/tp997_probe.py BUILD.html` (its own on copy, 390x844; screenshots to
  $CADET_WORK/test/tp997_*.png). OK.
- On copy: player_check OK (after the check fix below), devmode_check OK, intro_check --firsts OK, --solotap OK,
  interactions_check and player_check --long 60: see the latest message to RV32 and the lead.
- player_check.py, check-side (player engineer's file; for RV32): with TP997.n33 on, the till snack test fills your
  pocket first (so it's eaten as before), the shelf-and-counter run accepts the snack in your pocket, and the tips test
  marks `t:997call`/`t:997trk` seen with the other own-timed tips. With the switch off it runs exactly as before.
- Off: check_fast OK, cadet_test ALL IDENTICAL.

## Open for the user (via the lead)
- Pockets: snacks into your pocket (built) or still eaten at the till (design-doc Open questions).
