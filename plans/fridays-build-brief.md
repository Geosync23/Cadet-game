# Short Fridays and the Captain's address: the build brief (turn 0)

FR1 (the Fridays builder), session_01FXFdUaCbBurQbdY9E58HKs, branch `claude/fridays` (from claude/integration 0.64.6,
675588c). Lead: lead 21 (session_01KYPEbF745ZQ9g9kr4XJgre). Turn reviews: PR3 (session_01EtHMLLsjDYDHPG3JgCMbGi).
Owner hooks: PB (session_01FWW2piuXkFYaRRzLXZiqYb) for sections 13, 14 and 10; OR1 (session_01W7AHxrcgBM3rJNtCFKwp9W)
for the unstaffed sections. Written 2026-10-21 for the lead's go; nothing is built yet.

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
  without a temporal-dead-zone risk; one line in the sim engineer's section, owner review PB).
- **Off = identical game.** Every new function is defined when off (names_check sees it) and returns what today's code
  returns. Every turn: cadet_test ALL IDENTICAL against claude/integration with the switch off, and events_check,
  day_check and food_check's output unchanged off.
- The words are baked but silent while off. **The tradition is gated by the const at load, never a story flag**
  (PR3's fix 1: `flag()` reads the saved `SHIP.flags`, and `eventsOn` feeds the planner): `captains-address` is taken
  out of `SHIP_TRADITIONS` at load when `SHORT_FRIDAY` is off (as `REC_TRAD_ON` gates `REC_TRADS`). The breakfast
  lines' `flag:shortFriday` is set from the const at load, never saved. The address lines go in their own generated block, read only by code that's switched off.
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
- `eventFree` (section 18, line 35291): **part A doesn't change it.** It already reads `schedFrame`'s `workEnd`, so a 15:30
  Friday end frees the day shift for 16:00 by itself (with its 15-minute margin and a strict
  overlap, so the workaholics' tail stops at 15:45 at most, or they'd miss the address). EV1's note (neither side changes eventFree alone) is kept.
- EV1's answer is folded in here before turn 5. If EV1 prefers otherwise, the brief changes, not the code.

## The turns

Each turn: small exact edits; a row in `plans/build-table.md` under "Short Fridays"; my area's checks off and on;
cadet_test off (ALL IDENTICAL); `bash check_fast.sh` alone; commit; push to claude/fridays; send to PR3 (and OR1 for
hooks); design-doc.md in the same commit as the decision it depends on. No build number (the build master's).

| Turn | Part | What | Sections touched (owner) | Checks besides check_fast and cadet_test off |
|---|---|---|---|---|
| 1 | A1 | The switch; section 18f; the crew's Friday: `WEEK_SHAPE[4]` gains `end: 930`, read by `schedFrame` only when `SHORT_FRIDAY` (day shift's `workEnd` 15:30, workaholics to 15:35-15:45); the skeleton keeps 17:00 | 13 (switch), 14 `schedFrame` and `dayReport` (sim: PB) | day_check Days 5 and 12 on and off; events_check |
| 2 | A2 | The skeleton list (made at load from the roster, no `R()`: helm and watch ratings on the bridge, one medic, the dinner cooks; fp-q2); the night shift sleeps on (they come at 50%, from their own schedule); garden (already to 15:30), store and galley hours checked; the bridge staffed 15:30-17:00 | 14 (sim: PB), 16 read only | day_check 5/12 (nobody stuck, bridge never empty), food_check, events_check |
| 3 | B1 | Your clock: a shared `dayShiftEnd(d)` (1020, or 930 on a Friday when on) in section 14 beside `playerShiftOn`; `DAY_SHIFT`'s readers that mean "your shift ends" read it (about 27 reads of `DAY_SHIFT[1]`; each listed); `CAREER` clock-out from 15:30 and auto sign-out 16:00 on Fridays (fp-q7); early-out 15:00, the 12:30 miss line and leave unchanged | 14 (sim: PB), 17 `DAY_SHIFT` (systems: OR1), 20 `CAREER` (social / Works career: OR1): `dayShiftEnd` **asked of PB at turn 0** (a new shared function) | leave_check, career_check (a steady player 09:00-15:30 on Fridays), machine_check, mech_check |
| 4 | B2 + F | Friday team jobs (`TEAM_FRI`, 14:00 in even weeks) fit by 15:30; the device's Schedule row and the time clock screen say 15:30 on Fridays; Dev mode's Clock tab gets "To 15:25" on Fridays (part F); the address can be started from Dev's tradition list | 24h (Works career), 19 (device), 25 (Dev mode): OR1 | mech_check, device_check, interactions_check, devmode_check |
| 5 | C1 | The tradition: `content/traditions/captains-address.trad` (EW1's draft moved in, its `k:`; gated by the const at load), weekly Friday 16:00-16:50 from Day 5, the auditorium's `rec:seat`, Marrow at `rec:lectern` with Vance; who: Marrow and Vance always, the skeleton never, night shift 50%, everyone 90%; Thursday 18:00 Mail (Day 4's first-week words); `recShow('allhands')` for the room's lights; the hold assert | content (baked by content_gen), 18 (`recShow` call: rec engineer, OR1) | events_check on and off, join_check, content_gen --check, day_check 5/12 (about 60-70 in the auditorium), one draw-call reading in the full auditorium at phone size (deck_check on, or a single perf scene) |
| 6 | C2 | The speech: content_gen bakes `content/addresses/*.address` into a new generated block `ADDRESSES` (section 22: the dialogue engineer's tool, OR1); the player in 18f: line *i* at 16:00 + *i*·(48/n) ship minutes, by the clock (a reload, a late arrival or a skip lands on the right line, never a replay), bubbles over Marrow and Vance while you're in the auditorium, the chatter hushed (`linesHush` hook, section 22); the banner and a Mail for anyone not there; conditions and placeholders read when she speaks, never by the planner; Day 12 keeps the storm (`keep`); Days 33+ play EW1's `friday-weekly.address` (pools, below) | 22 (content_gen.py, `linesHush`: OR1), 18 (storm `keep`: EV1) | events_check, lines_check, content_gen --check, bubble_check (the auditorium, phone size), player_check (the whole-save budget) and devmode_check (Dev's save and Undo) for the ring, a reload mid-speech; off: nothing new in the save |
| 7 | C3 + D | Missing it (defined exactly in the turn and in design-doc.md: proposed, never in the auditorium 16:00-16:50; the 16:00 auto sign-out never counts against you): a work-reputation dip the size of being late (set with the Works career engineer: OR1), none on leave, sick, a rota day off, a Dev excuse or nights; dinner: each attendee's dinner time spread over 17:00-17:50 (seeded keys), some wash first on Deck 4; the rec lift queue clears by about 17:10 | 20 (career: OR1), 14 (dinner: sim, PB), 16 read | career_check, leave_check, food_check (a Friday case: Day 12), day_check 5/12 (the lift) |
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
- EW1's answers (2026-10-21): a `?` line holds until the next `?` (comments don't break it); poses nod, gesture,
  laugh, sigh, listen, play; tones funny, warm, serious (after the pose); speakers only marrow and vance; the `mail:`
  header may hold {me}; count lines drop when the count is 0. The only two-term condition is Day 12's
  `? done:stormBatteries !done:stormBatteries.you`.
- The .trad Mail's `? week1:true` (Day 4's first Mail): a tradition's Mail reads plain lines only, so turn 5 adds a
  small rule (or a `mail.week1` key) in 18f; to agree with the dialogue engineer's content_gen (OR1).
- **After Day 26: `content/addresses/friday-weekly.address`** (EW1, claude/events-lines d15803c; the lead: fold into
  C2). Each `== <beat>` is a pool, played in order: open, hello, headline, behind (pick 2), people (pick 2), nod, you,
  ahead, thought, close; one line a pool, seeded by the week, never a line used in the last 6 weeks (a small saved
  ring, in SAVE_EXTRA: PB); a beat with nothing that fits is skipped; the `you` beat about one week in three; lines
  with no speaker are marrow's; 9-12 lines spread over 16:00-16:48. New slots, read in 18f when she speaks:
  `nod:<dept>` and `{dept}` (the week's department, rotating Works, galley, watch, survey, infirmary, garden: a
  function of the week number), `health:good|ok|poor` (the ship health boards, section 17: OR1), `{arrivals}` and
  `{leavers}` (`ROSTER_ROTATIONS`), `{trad1}` and `{day1}` (one of next week's traditions, from `upcomingTraditions`),
  `{winner}` (`tallyLast`); existing `season:`, `cue:repair.you`, `cue:tradition.<id>.you`. If C2 gets too big, the
  weekly pools are their own half-turn (6b) right after it.

## PR3's review (2026-10-21): PASS WITH FIXES

Fix 1 is in "The switch"; fixes 2-5 are in their turns (eventFree's section and the 15:45 tail; turn 6's save checks;
turn 7's "missed it"; a draw-call reading at turn 5). The hold assert lives in my check, typeof-guarded, until EV1's
F0a is in claude/integration.

## Owners' answers so far

- **PB (13/14/10), 2026-10-21: OK** to the switch, `WEEK_SHAPE[4].end`, `dayShiftEnd(d)`, the saved ring and the
  dinner spread, with: turn 1 also moves **`dayReport`'s "shift short" interval** (end of section 14) to the person's
  own Friday end (else day_check flags everyone off at 15:30), and greps every other crew read of `SHIFTS.day[1]`;
  `dayShiftEnd`'s comment states its contract (d = ship day, 1 = the first Monday; minutes after midnight; Friday =
  `weekday(d) === 4`; night shifts not covered); `DAY_SHIFT` stays; only readers meaning "your shift ends today" move,
  each outside 14 to its owner; the ring's load accepts missing or junk, its bytes told to the player engineer;
  seeded keys unused today (not the 30s, 60s-110s or 1030s).
- **EW1:** `friday-weekly.address` now at claude/events-lines c053470: pools open, hello, headline, behind (pick 2),
  arrivals, leavers (each one line, skipped when empty, since the last address), nod, you, ahead, thought, close; a new
  condition `week:tradition.<id>` (that tradition ran since last Friday's address); `{winner}` as words (the tasting
  table's dish or the cup's team); the nod rotation is 7 weeks (Works, galley, watch, survey, infirmary, bridge,
  garden).

## Checked: nothing else on a Friday afternoon

- PR3 first flagged `cook-along` and `tiles-ladder`, then corrected it: both are `weekday: 5`, Saturday (0 = Monday).
  No tradition overlaps Friday 15:30-17:00 today; my check still asserts that with the switch on.

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

Answered by the lead (2026-10-21): (1) yes, the new section 18f with its own slot; (2) `dayShiftEnd(d)` asked of PB
(section 14's live owner) now; (3) the dip's size measured and reported in turn 7. PR3 reviews this brief; turn 1
starts when PR3 passes it.
