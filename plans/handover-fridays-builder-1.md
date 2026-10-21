# Handover: Fridays builder 1 (FR1) → the next Fridays builder

Written 2026-10-21 by FR1 (session_01FXFdUaCbBurQbdY9E58HKs) at about 430k of memory, after turn 5, because turn 6
(the speech) is big enough to fill the rest. Read this, then `plans/fridays-build-brief.md`, then build turn 6.

## Role, branch, people

- **Role:** builds Short Fridays and the Captain's Friday address (plan `plans/fridays-plan.md` rev 4 on
  claude/patch-plan cdeb1ff; the agreed turn-by-turn brief `plans/fridays-build-brief.md` on this branch).
- **Branch:** `claude/fridays`, head 78112ef (pushed, check_fast OK). Push only there. No build number (the build
  master's).
- **Lead:** lead 22, session_01BGQCZLK6gYTnqu6mwZ61jB (overnight mode on: questions to the lead, who takes the
  recommended answer). **Turn reviews:** PR3, session_01EtHMLLsjDYDHPG3JgCMbGi (send: commits, base, parts, checks,
  probes). **Owner hooks:** PB (session_01FWW2piuXkFYaRRzLXZiqYb) for sections 13, 14, 10; PR3 for the rest (OR1 has
  handed over). **Events base:** EV1, session_014ckxYgG3KA6eHksEMi6Eru (claude/events-base). **Words:** EW1 has handed
  over (plans/handover-events-writer-1.md on claude/events-lines); bigger writing goes to the next writer via the lead.

## Base and merges

- Built on claude/integration 0.64.6 (675588c), with **claude/patch-a efba55a and claude/patch-b 319f541 merged in**
  (lead 22's order: they are what 0.64.7 merges, apart from the cocoa-name bake and three switches). When 0.64.7 lands
  in claude/integration, merge it in (should be trivial) before the next hook into 15/20/21.
- **The off reference** for cadet_test ("off = identical"): 675588c + efba55a + 319f541 without the Fridays work. Make
  it with a worktree: `git worktree add --detach /tmp/x 675588c; cd /tmp/x; git merge efba55a; (take theirs for
  plans/build-table.md); git merge 319f541; cp starship-cadet.html ref.html`. After 0.64.7: use claude/integration.

## What's built (all behind `const SHORT_FRIDAY = false;`, section 13 beside DEVMODE)

Off = identical every turn (cadet_test ALL IDENTICAL against the reference). Reviews: PR3 PASS on turns 1-4, PB OK on
1-3, OR1 PASS on 3 (with the toast fix) and 4. Turn 5 is with PR3.

| Turn | Commit(s) | What |
| --- | --- | --- |
| 1 (A1) | ffb3b98 | `SHORT_FRIDAY`; new section **18f** with its slot (`// ---- slot: Fridays builder (section 18f)`); `friShort(d)`, `friSkeleton(p, d)`, `friCrewEnd(p, d)`; `WEEK_SHAPE[4].end = 930`; `schedFrame`'s day `workEnd` and `dayReport`'s interval read `friCrewEnd` |
| 2 (A2) | 37b7eb2, 3ae4bec | `friHours(p, d, hrs)`: 15:30-17:00 out of the hours rotas (gardeners; the storekeepers are off by then anyway); the dinner rush waits for 17:00 (`Math.max(F.workEnd, MEALS.dinner[0])`) |
| 3 (B1) | 4d270ac | `dayShiftEnd(d)` (section 14's sim slot, PB's contract comment); the skeleton per day from who's aboard; `friAutoOut(d)` (16:00 Fri); your clock in 15/17/20 reads them (clock out from 15:30, auto sign-out 16:00, jobs held to 15:30) |
| 4 (B2+F) | 6b6abae, 56fbd2b | the 24 mechanics' held-for-you ends → `dayShiftEnd`; `friHaulUntil` (Friday haul held to 14:30); `friTeamSlot` (Friday team job 13:30); the device's On shift row; Dev's "To 15:25" (`friDevTimes`); `clock.auto.friday` toast words |
| 5 (C1) | 1d780b7, 4ce9613 | the tradition: `content/traditions/captains-address.trad` (k 499), `content/banks/fridays.lines` (`fri.mail.week1`), 18f's `FRI_ADDRESS` + `friText` + the load IIFE (takes the baked one out; on with `SHORT_FRIDAY && REC_TRAD_ON` puts the rules entry in with the file's words, `baked: true`); storm `keep`; `recShow` 'allhands'; events_check skips it off; new `fridays_check.py` |

The skeleton: the lowest-ranked non-story helm, watch and infirmary day crew aboard and on shift that Friday
(strand-erik, shah-dara, larsen-hamid at the start), plus the galley on its rota. The watch rating's desk is on
Deck 2 (the plan said "on the bridge"; say so to the user in the summary).

## Next: turns 6-10 (as in the brief)

- **First, PR3's fix from turn 5's review (PASS WITH FIXES, 78112ef; full verdict with lead 22):** in real play the
  crew set off at 16:00 and arrive late: Marrow at the lectern 16:12, Vance 16:27, 49 seated only by 16:36
  (plans/review-3/fr5_fill.py on claude/review-3). Plan the trip ahead so people are seated by about 16:00 (patch
  #9's walk lead, `walkLead` in section 14, or an earlier crew segment for the address: a deck 7 ride from Deck 3/4
  takes several minutes), and add a live part to fridays_check (step the day on the deck from 15:45 and count who is
  seated at 16:00 and 16:05, Marrow and Vance at the lectern by 16:00). The rest of turn 5 passed: off identical, the
  gate right, 140-172 draw calls in the full room.

- **Turn 6 (C2), the speech.** The big one.
  - **Bake:** content_gen.py (the dialogue engineer's tool) learns `.address` files into a new generated block
    `ADDRESSES` (add `// ---- BEGIN ADDRESSES ...` / `// ---- END ADDRESSES ----` markers in section 22's generated
    area and a `blocks()` entry). Words: claude/events-lines `content/addresses/` (friday-d5/d12/d19/d26 and
    friday-weekly; README f869a07 has the format). Copy them into `content/addresses/` on this branch (the drafts'
    `.draft` and `part-e.draft` stay out; part E is turn 8).
  - **Format** (EW1's answers): header `day:`, `from:`, `mail:` ("Subject | body", may hold {me}); `== lines`;
    `who: text [pose] #tone`, `who > you:`; `? a b` = AND, `!x` = NOT, `x|y` in a term = OR, a bare `?` clears it,
    comments don't break it; poses nod/gesture/laugh/sigh/listen/play; tones funny/warm/serious; speakers only
    marrow and vance. **Weekly file:** each `== <beat>` is a pool, in order open, hello, headline, behind (`pick: 2`),
    arrivals, leavers, nod, you, ahead, thought, close; one line a pool (two where `pick: 2`), seeded by the week,
    none used in the last 6 weeks (a small saved ring via SAVE_EXTRA: PB OK'd it; load must accept missing/junk;
    tell the player engineer its bytes); a beat with nothing that fits is skipped; arrivals/leavers skipped when
    empty; the `you` beat about one week in three; lines with no speaker are marrow's; 9-12 lines a week.
  - **Readers** (when she speaks, never by the planner): EV1's `eventBandOf(id)` (band:), `eventJobDone(jobId, you, t)`
    (done:x / done:x.you), `!!SHIP.commendations.length` (commended), `eventJobsCount('ionStorm')` ({stormjobs}),
    `eventJobsCount(id, true)` ({myjobs}) — on claude/events-base bb285a0, not in integration yet: typeof-guard them
    (a line whose reader is missing is dropped); drop a count line when the count is 0. **myrank:** yours, from
    `SHIP.works.rank` (`playerRank()`); `myshift:night` never matches until Pillar 5's night shifts. Weekly extras:
    `nod:<dept>` / `{dept}` (7-week rotation Works, galley, watch, survey, infirmary, bridge, garden: a function of the
    week number), `health:good|ok|poor` (the ship health boards, section 17), `{arrivals}` / `{leavers}`
    (ROSTER_ROTATIONS, since the last address), `{trad1}` / `{day1}` (next week's traditions: upcomingTraditions),
    `{winner}` (tallyLast, as words), `week:tradition.<id>` (that tradition ran since last Friday), and the existing
    `season:`, `cue:repair.you`, `cue:tradition.<id>.you`.
  - **The player** (18f): line i of n at 16:00 + i·48/n ship minutes, by the clock (a reload, a late arrival or a skip
    lands on the right line, never a replay); bubbles (section 8b's `bubbleSay(a.h, text, secs)`) over Marrow or
    Vance's walker while you're in the auditorium; hush the chatter (set `CHATTER_AT = simNow()` each line; section
    22's overheard player stops on `linesHush`, ask PR3 before hooking it); for anyone not there by 16:50, a banner
    (toast) and a Mail with the file's `mail:` (mailSend, section 15). Tick from section 18's `eventsTick` (one
    typeof-guarded line) or the main loop. Checks: events_check, lines_check, content_gen --check, bubble_check in the
    auditorium at phone size, player_check (save budget), devmode_check (Dev's save and Undo), a reload mid-speech;
    off: nothing new in the save. Extend fridays_check: every line of all five files fills or drops, never shows `{`
    or a stray `?`.
  - Day 12: the rec deck is open for the address's hour during the storm (EV1's `EV_OPEN_FOR`, F3a on events-base);
    Marrow and Vance's release from the storm's double shift is EV1's storm update. fridays_check notes Day 12's empty
    lectern until then.
- **Turn 7 (C3 + D):** missing it = a small work-reputation dip "the size of being late" (measure and report the
  number; set with the Works career owner = PR3 now); define "missed" exactly (proposed: never in the auditorium
  16:00-16:50; the 16:00 auto sign-out never counts against you) and put it in design-doc; no dip on leave, sick, a
  rota day off, a Dev excuse (`devmodeExcused(d)`) or nights. Dinner: each attendee's dinner time spread over
  17:00-17:50 (seeded schedU keys nobody uses: not the 30s, 60s-110s or 1030s; grep first); some wash first on
  Deck 4; the rec lift queue clears by about 17:10. PR3's note: about 2 days in 5 the dinner rush puts half the day
  shift at the servery 17:03-17:13; recCap (14) and deck3Full (14) treat Friday 15:30-17:00 as working hours: check
  the rec deck and Deck 3 caps with 60+ free then. food_check gains a Friday case.
- **Turn 8 (E):** EW1's `part-e.draft` (claude/events-lines content/addresses/part-e.draft): Zeke's two goodnight
  lines on Day 0 (keys walk.goodnight.friday.1/2), Halloran's three after the mug at 13:00 Day 5 (beat.d5-friday.1-3),
  the Friday breakfast bank (`flag:shortFriday`, set from the const at load, never saved; `weekday:fri`, `act:breakfast`,
  `week1:true` already exist); the 15:20 heads-up and the Friday time clock screen. intro_check alone, in pieces
  (`--evening`, `--week`, `--firsts`; it's >2 h whole).
- **Turn 9 (G):** perf_check scenes: the auditorium at 16:10 on a Friday (about 50 seated now) and the rec lift lobby
  at 16:52, at zoom 1.5, 0.7 and landscape (budget 450). My probe (/tmp, gone with the container) read 149 / 211 /
  128 calls in the full auditorium on Day 5 at 16:10; recreate it by exec'ing perf_check.py up to `def run(` and
  running SCENE_JS / MEASURE_JS for `{'day': 5, 'time': '16:10', 'deck': 7, 'room': '^Auditorium'}`.
- **Turn 10:** switch on only after the user's review; the full round alone.

## Gotchas

- **Load order:** section 14 plans before 18f runs. Anything the planner calls in 18f must be a function declaration
  or a `var` (I had a `const` arrow once: a temporal-dead-zone crash waiting to happen). Consts in 18f are fine only
  for code that runs after load.
- **Rec deck traditions follow `REC_TRAD_ON`**, not just `REC_DECK`: day_check flips `REC_TRAD_ON` to measure the
  deck's everyday use alone, and a rec tradition that ignored it broke its Commons comparison.
- events_check fails on a baked tradition the game didn't load: tell it when a switch gates one (as for first-light
  and captains-address).
- day_check Day 12 fails at 0.64.6 already (backlog #18, the rec deck's evening guard): not yours. join_check fails
  first-light with FLC_ON off (backlog #19): not yours. career_check fails only backlog #12: known.
- Test copies: `sed 's/^const SHORT_FRIDAY = false;/const SHORT_FRIDAY = true;/'`. Parallel checks need their own
  CADET_WORK each (`/tmp/w-a` etc. with `three` and `acorn` linked); check_fast alone, never alongside others.
- A container restart can kill a long check mid-run (exit 137): just run it again.
- The stop hook nags about unpushed commits: never push before check_fast says OK.

## How to test (each turn)

1. Your area's checks on a test copy with the switch on, and off where they could change.
2. cadet_test reference → off: ALL IDENTICAL.
3. `python3 fridays_check.py starship-cadet.html` (makes its own off/on copies).
4. `bash check_fast.sh` alone (`CADET_CHROME=/opt/pw-browsers/chromium`). Then commit, push, send PR3 (and PB for
   13/14).

## Open questions for the user (through the lead)

- Turnout: about 50 sit in the auditorium on Day 5 (the plan guessed 60-70). It follows from the rules (skeleton,
  galley, half the night shift away, everyone else 90%). Fine, or raise the chances?
- The late gardener's Friday is split (13:00-15:30 and 17:00-21:00) so she can go: OK?
- The garden has nobody on it 15:30-17:00 on Fridays: OK?
