# Review: being sick (claude/leave b0c0f37, 0.61.5; checked on b097097, 0.61.6)

Reviewer 1d, 2026-10-17. The career engineer's rare sickness. The exam has no script yet (head writer 4's words land in 0.61.7), so the infirmary cures at once.

## Verdict: PASS (lows only)

### What I read (sick* after the career section, and the hooks)
- **When it happens.** A seeded roll at 05:00 (`schedU(7919, day, 901) < 1/28`).
  - Never in the first week, never within 21 days of the last time, never once you've been let go.
  - In a sleep skip, the roll runs from `careerTick(to)` at 06:00.
- **A sick day is excused.**
  - It goes into `c.s`, so it's `careerOff`: no shift, no late note, no miss.
  - The Chief's run neither counts nor breaks, and the bottom count skips it.
  - `careerDue` won't book a talk that day (`playerShiftOn`).
  - A booked leave day comes back.
  - A miss already counted that day is undone (`md`). Both were my notes from 492364d.
- **Worse untreated.**
  - Walking: 0.85, then 0.7 at 08:30, 0.55 at 11:00, and 0.4 and doubled over at 13:30.
  - Energy drains 1.5 times as fast.
  - A toast at each step, and one friend comes to nudge you at the third step.
- **Two cures.**
  - The exam in the Infirmary or Exam room on Deck 3: Rina's if she's at work, else the medic on duty.
  - Or a nap in your bunk by day: skip 180 minutes, then cured.
- **The rest.**
  - The Schedule says "Sick", "seen by Rina" and so on.
  - Chat gives a get-well line, then a glad-you're-better line (none are baked yet, so nothing shows).
  - New game hides the card.
- **Determinism.** No `R()`, no load-time code. The roll is `schedU` on the day.
- **Save.** It adds `md, sd, sh, ss, sc`. leave_check measures 220 bytes at the end of a let-go run and 196 after 280 days. `careerClean` defaults every new field, so older saves load fine.

### What I ran
| Check | Result |
| --- | --- |
| leave_check on b097097 | OK. Sick days 51, 82, 134... (gaps 21-67), never the first week. Excused, the leave given back, no miss, worse through the day to doubled over, both cures, save under 300 bytes. |
| events_check on b097097 (skips past day 51) | EVENTS CHECK OK |
| My probe (sick-b0c0f37-probe.py) | the findings below |

## Findings

### 1. LOW: undoing a miss gives back more than it took
`careerSick` refunds a miss with `repAdd('works', +6, { work: +15 })`. The miss itself was softened below 50 (`x / 50`), but the refund isn't, because climbing is only softened above 50.
- Probe: work 30, then a miss takes it to 21, then a sick day takes it to 36.
- That's 6 points more than before the miss.
- It's reachable only when the roll lands after that day's miss was counted (a skip or a load past 12:30), so it's rare.

**Fix:** keep the work value from before the miss (for example `c.mw = careerWork()` in `careerMissed`) and put it back. Or store the actual drop and add exactly that.

### 2. LOW (design): every game is sick on the same days
The roll only depends on the day and the last sick day. So every fresh game is sick first on day 51, then 82, 134, 169... A second playthrough meets it on the same days.

That's harmless, and it keeps the checks deterministic. If the user wants it to vary, mix a per-save number made at New game into the seed, and have the checks set it.

### 3. LOW: very slow at the worst
Doubled over (×0.4) with low energy and low fitness (×0.64) gives walking at 26%. The infirmary is on Deck 3, a long way from Deck 4's bunks. The bunk cure is always nearby, so you're never stuck, but a phone player may find 26% painful.

It's by design ("worse untreated"). Worth a look in play.

### Notes
- If you walk out of the exam, it plays again the next minute while you're still in the room. That's fine.
- `SICK_SAID` (once a day per person) isn't saved, so after a reload the same person may say the get-well line again. Harmless.
