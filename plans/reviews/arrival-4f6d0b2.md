# Re-review: claude/arrival 7abf466..4f6d0b2 (0.42.16-0.42.17: Monday in play, the shadow shift, dinner seats)

Reviewer 1, 2026-10-17. Section 21, plus one direct write into section 19's data (see 3). name_check OK.

Tested on my full merge of arrival 4f6d0b2 + sim 2f6d8dd + crew 98df62f + social 945c447 + social B 31f8aea + player-needs (tip), conflicts kept on both sides: intro_check parts 0-9 OK (the name now survives a reload: "name Sam", with section 15's save in), and part 10's jobs, shadow shift and turn-in OK. But **part 10 FAILS: "the Monday briefing did not play"**.

**Verdict: PASS WITH FIXES** (one fix in section 21, one in the sim's section 14).

## 1. SHOULD FIX (section 21): the briefing starts before its cast is in the room, and drops whoever isn't there yet
- `introWeekMeetings` plays a week meeting as soon as **you** are in its room (`inMeeting(m)` looks at the player), then `introScriptHere` cuts the lines of anyone in the cast who isn't in the room, except the step's own speaker.
- Proven (`?debug`, New game, sign, skip to Monday 07:40, stand in the Works bay): at 07:52, `DIALOGUE.id` is `introBriefing~here`. Calder is still in **Main storage** and Torres in the **Main corridor**, both walking to it. The script played is Calder × 3 (Torres's "Properly. Always." cut), and Calder speaks though she isn't in the room. That's also why part 10 fails (it expects `introBriefing`).
- Fix: start a week meeting only once its speaker (`b.who`) is in the room, or at most a few minutes after `at` (then cut whoever's still missing). Let part 10 accept the trimmed id only when someone really is away.

## 2. SHOULD FIX (the sim engineer, section 14 `introPlan`): two cast members are planned on the same place
- For a week beat (`{ deck, room }`), `introPlan` takes `cand[0]`, the first place in the room by id that isn't anyone's own or a desk, without checking whether another intro beat already holds it (it isn't given `occ`). For the briefing, Calder and Torres are both planned at **`5-stool-1`** (`whereIs` at 07:52: `calder: 5/5-stool-1/intro`, `torres-zeke: 5/5-stool-1/intro`).
- day_check can't see it (its URLs run with the intro off). Fix: pass `occ` to `introPlan` (or skip places already booked by `introLay` for the same time), and add an intro-on day_check case for Monday.

## 3. Low (seat line): section 21 writes section 19's data directly
- On the shadow shift's `take`, `introJobNote` sets `SHIP.device.tipsSeen[k] = true` for board, machine and turnin. That's the device's state, written from section 21 with no hook. Use a section 19 call (e.g. `tipSeen(k)`, typeof-guarded), or add the line to the hook register and tell the device engineer.

## Checked, fine
- The week's three jobs are reserved at Monday 05:00 (not on skip, once only, saved with the jobs). Unclaimed ones go to the crew at the intro's end (`jobRelease`).
- Torres follows on the shadow shift (2 tiles from you), the turn-in ticks "Shadow a job" and sends the d1-shadow note. His walking and job lines go through `lineFor` (week1, `walk.<step>` flags) with the stand-ins as fallback, in try.
- Calder comes to your table by `crewComeTo` (until 19:00 on Day 0, again after a reload). Torres sits when he waits at his seat.
