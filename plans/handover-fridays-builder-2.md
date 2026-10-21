# Handover: Fridays builder 2 (FR2) → the next Fridays builder

Written 2026-10-21 by FR2 (session_019m7hCEtBsPA3ascA2Bqu9V) at about 520k of memory, after turn 8. Read this, then
`plans/handover-fridays-builder-1.md` (FR1's: turns 1-5, the gotchas, still true) and `plans/fridays-build-brief.md`.
Left to do: turn 9 (perf scenes) and turn 10 (switch on, only after the user's review).

## Role, branch, people

- **Branch:** `claude/fridays`. Push only there. No build number (the build master's).
- **Lead:** lead 23, session_01XXiKm9iPgm565SZ4n1knmU (overnight mode: questions go to the lead). **Turn reviews:** PR5,
  session_01Eh4drBZjJ82DjYx6XaTt1F (lead 23's change; PR4 keeps the storm). PR4's copy of PR3's fill probe:
  claude/review-4 plans/review-4/fr5_fill.py. **Section 14/13/10 owner:** PB, session_01FWW2piuXkFYaRRzLXZiqYb.
  **Storm update (Day 12):** EV4, session_01MqpjPG6mDFe5avrDxcNWTU (claude/storm-update): Marrow released from the
  double shift from 15:30, Vance from 15:45, through 16:50 (EV2 passed this on); EV_OPEN_FOR opens the auditorium.
- **Base:** claude/integration 0.64.7 (6ea5acf) is merged in (4ee3fdc). **Off reference** for cadet_test = claude/integration
  (`git show origin/claude/integration:starship-cadet.html > ref.html`). Every FR2 commit: ALL IDENTICAL against it.

## What FR2 built (all behind `SHORT_FRIDAY`, off)

| Turn | Commit | What | Review |
| --- | --- | --- | --- |
| 6 (C2) | a22d651 | The speech. content_gen.py bakes `content/addresses/*.address` into `FRI_ADDRESSES` (block after TALKS; `ADDRESSES` was taken by section 18). 18f: `friSpeech`, `friFill`, `friCond`, `friAddressTick` (from 18's eventsTick), `friSpeaker` (a bubble's stand-in at the screen edge when Marrow is off a phone's screen: lead's yes), `save.fri` (ring/today/heard/mailed/hu, only when on, about 790 B full) | sent to PR5 |
| fix | 8415d1e | PR3's turn-5 fix: `friLead` (ev.lead in 18's eventPlan) seats people early; 14's leisure join regex + stay end for the address's tag (PB OK). Speech 16:04-16:48 (lead's yes) | PB OK; PR5 |
| 7 (C3+D) | 86d0c80 | Missed it: work -2 (as late) at 16:50 unless `!playerShiftOn(d)`; `friDinner` (14's evening) 17:00-17:50; `recCap` reads `dayShiftEnd` | PB OK; PR5 |
| 8 (E) | see git log (after 86d0c80) | Part E: `friNightKeys`, `friBeatLines`, `flag:shortFriday` (set at load, never saved), `friClock` (clock screen words), the 15:20 toast; EW1's lines in torres-zeke.lines, halloran-emeka.lines, banks/fridays.lines | sent to PR5 |

Seeded keys in use: 1180 (weekly picks), 1181 (you beat), 1182 (trad1), 1183 (lead), 1184 (dinner). Free next: 1185+.

## Turn 9: perf scenes (to do)

- perf_check scenes (the performance engineer's perf_check.py; owner via the lead): the auditorium at 16:10 on a Friday
  (about 50 seated) and the rec lift lobby at 16:52, at zoom 1.5, 0.7 and landscape (budget 450 calls). FR1 measured
  149 / 211 / 128 calls in the full auditorium (Day 5, 16:10). With turn 6 the speech bubble adds DOM, not draw calls.
  Recipe: exec perf_check.py up to `def run(` and run its SCENE_JS / MEASURE_JS for `{'day': 5, 'time': '16:10',
  'deck': 7, 'room': '^Auditorium'}`; the scenes need the switch on, so they run on a test copy (or the scene flips
  it): agree how with the performance owner. Agreed with EV1's F7c: Day 12's address in the storm is theirs.
- Then deck_check.

## Turn 10: switch on (only after the user's review)

`const SHORT_FRIDAY = true;` in section 13, then the full round alone (intro_check in pieces: `--evening`, `--week`,
`--firsts`), design-doc and DEV_NOTES final. Keep it off on claude/integration until the user says so.

## Loose ends and open points (for the lead / the user's review)

- **Day 12:** the lectern is empty until EV4's storm update releases Marrow and Vance; fridays_check notes it.
- **The 15:20 heads-up** is a plain toast (18f), not the device's heads-up queue (section 19's HU_Q, which keeps them off
  meetings and tips). The device engineer may want to move it.
- **Not built:** the brief's "some wash first on Deck 4" after the address (14 plans the evening before the address sits
  in it, so a wash lands before; it made Vance late). In design-doc.
- **Words that never show:** Day 19's night-hand line (no night shifts for you until Pillar 5) and its `{leavers}` line
  (nobody's rota leaves before Day 35). Day 19 also says a new junior arrives "on Sunday" (Day 21), but the first
  rotation is Day 35: for the writers.
- **The save:** `save.fri` adds up to about 790 bytes when on (PB's note; there's no player engineer seat now, so it's in DEV_NOTES and PR5 checks it with player_check).
- food_check fails the same 13 cases off and on (run as `food_check.py BUILD 5`): pre-existing, not Fridays'.
- career_check fails only backlog #12; day_check Day 12 only backlog #18.
- Turnout (decided, ~50), the late gardener's split Friday and the empty garden 15:30-17:00: lead 22 said keep.

## Gotchas (new)

- `CHATTER_AT` held every frame in the auditorium hushes section 20's chatter and section 22's overheard lines: no
  linesHush hook needed.
- Section 14's leisure only joins a gathering already begun for `/^ev-(rec-|captains-address)/` tags, within 10 minutes
  (a host: its first half). `friLead` keeps day workers' starts at workEnd + 8 for that reason; Vance isn't the host
  (Marrow is), so his start is his shift's end.
- The deck-7 walk from the lift to the lectern is about 17 ship minutes in play; the plan doesn't know it.
- Test-page stubs: game functions are lexical in the page's script, so in `g.ev` assign them directly
  (`shipHealthRows = ...`, `toast = ...`), not through `window.`; `window.x` works only for names the game lacks
  (EV1's readers).
- A first cadet_test run in a fresh container showed font-noise differences in the top bar (max 69); a re-run was ALL
  IDENTICAL.
- fridays_check takes about 8 minutes now (paper, the live fill run to 17:11, the speech, reload, missed, leave).

## How to test

1. `python3 fridays_check.py starship-cadet.html` (own off/on copies; FRIDAYS CHECK OK).
2. cadet_test against claude/integration: ALL IDENTICAL.
3. On a test copy (`sed 's/^const SHORT_FRIDAY = false;/const SHORT_FRIDAY = true;/'`): events_check, day_check 5,
   lines_check, the area's own; intro_check `--evening` for part E.
4. `bash check_fast.sh` alone. Then commit, push, send PR5 (and PB for 13/14/10).
