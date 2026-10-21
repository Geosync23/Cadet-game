# Short Fridays and the Captain's address: the build brief (turn 0)

FR1 (the Fridays builder), session_01FXFdUaCbBurQbdY9E58HKs, branch `claude/fridays` (from claude/integration 0.64.6,
675588c). Lead: lead 21 (session_01KYPEbF745ZQ9g9kr4XJgre). Turn reviews: PR3 (session_01EtHMLLsjDYDHPG3JgCMbGi).
Owner hooks: OR1 (session_01W7AHxrcgBM3rJNtCFKwp9W). Written 2026-10-21 for the lead's go; nothing is built yet.

**What it builds:** the plan as decided, `plans/fridays-plan.md` rev 4 (claude/patch-plan cdeb1ff), with the user's
answers: the day shift stops at 15:30 on Fridays; the Captain's address 16:00-16:50 in the rec deck auditorium, every
Friday from Day 5; dinner at 17:00 as now. A skeleton keeps working (helm and watch ratings on the bridge, a medic on
call, the dinner cooks). Bubbles over the crowd plus a banner and a Mail for anyone not there. Missing it is expected:
a small work-reputation dip, but none on leave, sick, a rota day off, a Dev-mode excuse or nights. The weekly shape
with parts that change. An event on a Friday: both happen. Your auto sign-out at 16:00 on Fridays. The normal clock
(revision 3's slowed clock stays parked, not built). The words are EW1's (claude/events-lines: `content/addresses/`,
`part-e.draft`; the user: keep 16-19 lines a speech, spread evenly over 16:00-16:48).

## The switch

- One switch, `const SHORT_FRIDAY = false;`, in section 13 next to `DEVMODE` (so every section can read it at load
  without a temporal-dead-zone risk; one line in the sim engineer's section, owner review OR1).
- **Off = identical game.** Every new function is defined when off (names_check sees it) and returns what today's code
  returns. Every turn: cadet_test ALL IDENTICAL against claude/integration with the switch off, and events_check,
  day_check and food_check's output unchanged off.
- The words are baked but silent while off: the tradition carries `flag: fri.on` (the trad format's existing gate, as
  `rec-all-hands` uses `rec.on`), set only when `SHORT_FRIDAY` is on; the new banks and lines use new flag keys
  nothing sets while off. The address lines go in their own generated block, read only by code that's switched off.
- On: a test copy with the line flipped (`sed 's/const SHORT_FRIDAY = false/const SHORT_FRIDAY = true/'`) for my area
  checks every turn. Switching it on in the real build is its own reviewed step after the user's review (turn 10).

## Where the code goes

- **A new section `18f SHORT FRIDAYS`** right after section 18 (the plan's own feature, as Dev mode got section 25),
  with its own slot `// ---- slot: Fridays builder (section 18f) ----`. It holds everything that's mine: the
  skeleton list, the address's player, its readers for the words' conditions, the missed-it rule, the dinner spread.
  The new section's heading and slot lines: `tools/section.py` and `plans/map.md`/`owners.md` rows in turn 1 (the
  build master's tools, asked of the lead).
- **Hooks into other sections** are one-line, `typeof`-guarded or `SHORT_FRIDAY`-guarded calls, each in DEV_NOTES'
  Hook register, each reviewed by OR1 before PR3's turn review. A change to a shared function's inputs or result, or
  a shared table's shape, is asked of OR1 (standing in for the owner) *before* the turn that needs it. The ones I
  know of now are listed per turn below.
- Integration moves to 0.64.7 (the playtest patch) within hours: I merge it in when it lands, and always before my
  first hook into sections 13, 14, 15, 20 or 21 (patch-a and patch-b edit those).

## One table for the Friday hold (to agree with EV1 before part C; asked 2026-10-21)

- **EV1 owns `EV_BEATS`** (section 18, F0a 835ab24) and its `fridayAddress` row: Friday 15:30-17:00 from Day 5, held
  whether or not `SHORT_FRIDAY` is on. That row is the only hold. I never add a second one.
- **I own the address itself**: the tradition `captains-address` (16:00-16:50) and the Friday shift end. My check
  asserts the address sits inside EV_BEATS' row, so the two can't drift apart.
- Day 12, "both happen": the storm's `pause` lists `captains-address` in `keep` (whoever builds second adds it; key
  agreed with EV1).
- `eventFree` (section 14): **part A doesn't change it.** It already reads `schedFrame`'s `workEnd`, so a 15:30
  Friday end frees the day shift for 16:00 by itself. EV1's note (neither side changes eventFree alone) is kept.
- EV1's answer is folded in here before turn 5. If EV1 prefers otherwise, the brief changes, not the code.

## The turns

Each turn: small exact edits; a row in `plans/build-table.md` under "Short Fridays"; my area's checks off and on;
cadet_test off (ALL IDENTICAL); `bash check_fast.sh` alone; commit; push to claude/fridays; send to PR3 (and OR1 for
hooks); design-doc.md in the same commit as the decision it depends on. No build number (the build master's).

| Turn | Part | What | Sections touched (owner) | Checks besides check_fast and cadet_test off |
|---|---|---|---|---|
| 1 | A1 | The switch; section 18f; the crew's Friday: `WEEK_SHAPE[4]` gains `end: 930`, read by `schedFrame` only when `SHORT_FRIDAY` (day shift's `workEnd` 15:30, workaholics to 15:35-15:45); the skeleton keeps 17:00 | 13 (switch), 14 `schedFrame` (sim: OR1) | day_check Days 5 and 12 on and off; events_check |
| 2 | A2 | The skeleton list (made at load from the roster, no `R()`: helm and watch ratings on the bridge, one medic, the dinner cooks; fp-q2); the night shift sleeps on (they come at 50%, from their own schedule); garden (already to 15:30), store and galley hours checked; the bridge staffed 15:30-17:00 | 14 (sim: OR1), 16 read only | day_check 5/12 (nobody stuck, bridge never empty), food_check, events_check |
| 3 | B1 | Your clock: a shared `dayShiftEnd(d)` (1020, or 930 on a Friday when on) in section 14 beside `playerShiftOn`; `DAY_SHIFT`'s readers that mean "your shift ends" read it (about 27 reads of `DAY_SHIFT[1]`; each listed); `CAREER` clock-out from 15:30 and auto sign-out 16:00 on Fridays (fp-q7); early-out 15:00, the 12:30 miss line and leave unchanged | 14 (sim), 17 `DAY_SHIFT` (systems), 20 `CAREER` (social / Works career): **asked of OR1 before the turn** (a new shared function) | leave_check, career_check (a steady player 09:00-15:30 on Fridays), machine_check, mech_check |
| 4 | B2 + F | Friday team jobs (`TEAM_FRI`, 14:00 in even weeks) fit by 15:30; the device's Schedule row and the time clock screen say 15:30 on Fridays; Dev mode's Clock tab gets "To 15:25" on Fridays (part F); the address can be started from Dev's tradition list | 24h (Works career), 19 (device), 25 (Dev mode): OR1 | mech_check, device_check, interactions_check, devmode_check |
| 5 | C1 | The tradition: `content/traditions/captains-address.trad` (EW1's draft moved in, its `k:`, `flag: fri.on`), weekly Friday 16:00-16:50 from Day 5, the auditorium's `rec:seat`, Marrow at `rec:lectern` with Vance; who: Marrow and Vance always, the skeleton never, night shift 50%, everyone 90%; Thursday 18:00 Mail (Day 4's first-week words); `recShow('allhands')` for the room's lights; the hold assert | content (baked by content_gen), 18 (`recShow` call: rec engineer, OR1) | events_check on and off, join_check, content_gen --check, day_check 5/12 (about 60-70 in the auditorium) |
| 6 | C2 | The speech: content_gen bakes `content/addresses/*.address` into a new generated block `ADDRESSES` (section 22: the dialogue engineer's tool, OR1); the player in 18f: line *i* at 16:00 + *i*·(48/n) ship minutes, by the clock (a reload, a late arrival or a skip lands on the right line, never a replay), bubbles over Marrow and Vance while you're in the auditorium, the chatter hushed (`linesHush` hook, section 22); the banner and a Mail for anyone not there; conditions and placeholders read when she speaks, never by the planner; Day 12 keeps the storm (`keep`); Days 33+ use the weekly shape (if EW1 writes it; else banner and Mail only) | 22 (content_gen.py, `linesHush`: OR1), 18 (storm `keep`: EV1) | events_check, lines_check, content_gen --check, bubble_check (the auditorium, phone size) |
| 7 | C3 + D | Missing it: a work-reputation dip the size of being late (set with the Works career engineer: OR1), none on leave, sick, a rota day off, a Dev excuse or nights; dinner: each attendee's dinner time spread over 17:00-17:50 (seeded keys), some wash first on Deck 4; the rec lift queue clears by about 17:10 | 20 (career: OR1), 14 (dinner: sim, OR1), 16 read | career_check, leave_check, food_check (a Friday case: Day 12), day_check 5/12 (the lift) |
| 8 | E | Explaining it: Zeke's two goodnight lines on Day 0; the Captain's Thursday Mail on Day 4 (turn 5's); Halloran's three lines after the mug at 13:00 Day 5; the 15:20 heads-up and the Friday time clock screen; your name in Day 5's address (turn 6's); Friday breakfast lines (`flag:shortFriday`). EW1's `part-e.draft` moved into its files | 21 (onboarding: OR1), 19, content | intro_check alone in pieces (`--evening`, `--week`, `--firsts`), lines_check, device_check |
| 9 | G | perf_check scenes: the auditorium at 16:10 on a Friday with about 65 seated, and the rec lift lobby at 16:52, at zoom 1.5, 0.7 and landscape (budget 450); agreed with EV1's F7c (Day 12's address in the storm's onset is theirs) | perf_check (performance engineer: OR1) | perf_check, deck_check |
| 10 | switch on | Only after the user's review: `SHORT_FRIDAY = true`; the full round alone (intro_check in pieces); design-doc and DEV_NOTES final | 13 | everything |

About 9 build turns, as the plan said. Order: A and B, then C and D, then E, F and G (F rides with turn 4 since it's
a quarter-turn in section 25 next to B's clock).

## The words (EW1; questions sent 2026-10-21)

- `.address` format: header `day:`, `from:`, `mail:` ("Subject | body"); `== lines` written like a `.meet`
  (`who: text [pose] #tone`, `who > you:` for a line to you); `? terms` above lines (AND of space-separated terms,
  `!x` NOT, `a|b` OR inside a term), a bare `?` clears it; a line whose condition fails or whose placeholder can't be
  filled is left out. Lines at most 90 characters.
- Conditions and placeholders I read in 18f (when she speaks, never by the planner): `{me}`; `myrank:` (Works
  career's `SHIP.works.rank`: OR1); `myshift:night` (Pillar 5, not built: reads false until it is); `done:<job>` and
  `.you`, `band:`, `commended`, `{stormjobs}`, `{myjobs}` (EV1's section 18 readers, F0a); `{leavers}` (this week's
  leavers from `ROSTER_ROTATIONS`). Each gets a check case in events_check's Friday part: every line of all four
  speeches fills or drops, never shows a `{` or a stray `?`.
- Day 12's line 3 ("I've borrowed this room for an hour") needs the code's matching exception: the rec deck opens for
  the address's hour while the storm keeps it shut (the user's yes to the addresses page q2). Agreed with EV1 in turn 6.
- After Day 26 the weekly shape takes over: I won't write words; if EW1 hasn't written a weekly speech by turn 6,
  Fridays after Day 26 have the tradition, the banner and the Mail only, and that's said in the turn's summary.

## Rules I keep

- Shared kit at load never calls `R()`; the skeleton list and dinner spread use `schedU` seeded keys (new key numbers
  listed in the turn's notes and checked for clashes with `grep`).
- The crew's planner never reads anything built while the game runs: who comes, the skeleton and the dinner spread
  come from the roster, the day and seeded rolls only. The speech's slots are filled when she speaks.
- Checks never assume a free slot: my Friday cases look for free seats and say which they used.
- check_fast alone before every push; never push when it says FAILED. intro_check alone, in pieces.
- Memory: `get_session` after each turn; the lead hears at 500k; at 600k `plans/handover-fridays-builder-1.md`, push,
  idle.
- Found a small bug outside the brief: a row in `plans/backlog.md`, not a side fix.

## Open (for the lead)

1. The new section `18f` and its slot: OK, or should 18f's code live in the Traditions engineer's slot (section 18,
   EV1's working area too)? I recommend 18f (no two seats adding lines at one spot).
2. Part B's `dayShiftEnd(d)` in section 14 (beside `playerShiftOn`): OK to ask OR1 now, so turn 3 isn't held up?
3. The dip's size: "the size of being late" (CAREER's late hit). I'll measure it in turn 7 and say the number.
