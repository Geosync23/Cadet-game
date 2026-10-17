# Review: claude/leave 0af21bf..c08342c (0.61.13-0.61.16, the career engineer): the time clock, the reputation chip, the Works crew clocking in and out

Reviewer 1e, 2026-10-17. In-depth review, because it changes behaviour and the save. The probe is `leave-6f5bc37-clock-probe.py`; the game code at 6f5bc37 and c08342c is the same, and the later commits change only deck_check and the handover.

## Verdict: PASS WITH FIXES

There is one MEDIUM: with the clock, section 14's shift note and the career disagree about a late clock-in. Otherwise the clock, the chip, the crew stops and the save all work, and every check passes.

## Checks (on c08342c)
| Check | Result |
| --- | --- |
| leave_check | LEAVE CHECK OK (280 casual days, career save 212 bytes with `ci`/`co`/`rm`) |
| deck_check | DECK CHECK OK (Deck 5 with the clock place) |
| day_check day 1 | DAY CHECK OK (the Works crew's shifts are full length after 0.61.16) |
| The clock probe, every ship minute of a Tuesday past the grace | See below |

| The player | Section 14's `shiftStart` note (section 20 scores this) | Career miss |
| --- | --- | --- |
| clocks in 07:55 | late 0 | no |
| clocks in 09:30 | late 90 | no |
| **clocks in 10:30** | **missed (sent at 10:00)** | **no** |
| **clocks in 12:00** | **missed** | **no** |
| clocks in 03:00 | late 0 | no |
| clocks in 07:01, out 07:02 | late 0 | no |
| no clock-in, a repair at 09:00 | missed | **no** |
| nothing | missed | yes |

### MEDIUM 1: a clock-in between 10:00 and 12:30 is "missed" for reputation but "worked" for the career
`shiftTick` (section 14) still gives up at **10:00** (`if (!here && m < 600) return;`). It then sends `{ late: 120, missed: true }`, which section 20 scores as a missed shift. The career counts a miss only after **12:30** (`CAREER.missBy` 750), and `careerStarted` counts any clock-in before then.

So a player who clocks in at 10:30:
- gets the reputation hit for a missed shift;
- is counted as having worked by the career;
- may hear a crew member's `clock.late` remark.

DEV_NOTES 0.61.13 says "missed if not clocked in by 12:30", which is what players would expect from a clock. The mismatch was there before the clock (with "being in the bay"), but the clock makes it visible: it's now a deliberate act with a time on it.

**Fix (the career engineer and the sim's section 14 owner):**
- `shiftTick` waits until `CAREER.missBy` when it exists: `m < (typeof CAREER !== 'undefined' ? CAREER.missBy : 600)`.
- When you're clocked in, it takes `late` from the clock-in time (`SHIP.career.ci % 1440 - 480`), not the minute it happens to tick. That's the same thing in play, but robust to skips.

**Test:** this probe's 10:30 and 12:00 rows should read `late 150` / `late 240`, not missed.

### LOWs
1. **A repair without clocking in:** `onSim('repair')` → `careerStarted` still counts the day as worked for the career, but `shiftTick` says missed. Either a repair should clock you in (with a toast), or it should stop counting once the first week is over.
2. **Clocking in at night counts as on time.** `careerClock` takes a clock-in at any hour on a shift day. 03:00 counts, and the toast says "Clocked in at 03:00." The comment says "from 07:00". A "Too early. The clock opens at 07:00." toast before 07:00 (or 06:00) would match the design.
3. **Clocking in and straight out counts as a full day.** 07:01 in and 07:02 out is a worked day with no lateness. That's a design question for the user (the old rule, "be in the bay once", was just as loose). If it should matter, a clock-out before, say, 16:00 could count as "left early".
4. **`CLOCK_SAID` isn't saved,** so after a reload the day's remark can come again. That's harmless.

## The code
- **The clock kit:** made at load, no `R()`, existing materials. The place `5-timeclock-1` at [20,0] faces north. deck_check now knows the type.
- **`careerClock`:**
  - it refuses on leave, sick and days off, and after 17:00;
  - it shows the hours worked on clock-out;
  - `careerClockedIn`/`Out` are day-scoped.
- **Auto clock-out:** at 18:00 the same day with a toast, or silently when the day has rolled over. It only ever writes `co` = 17:00 of the clock-in day.
- **The reminder and the tip:** once a day (`rm`) and once ever (`k & 8`), and only in the Works bay on a shift day, from 07:00 to 17:00.
- **`careerRemark`:** deterministic (`schedU` on `clockSeed`), about one time in two, the nearest Works crew member within 5 m. The order is back > late > Monday > in, and Friday > out.
- **The crew's clock stops (`shiftWithBreaks`, called once a day):** a 1-minute `work` stop at the clock before and after the shift (wait 6, min 1) for day-shift Works crew on Deck 5. day_check shows full shifts.
- **The reputation chip (`careerJobIn`):**
  - one chip per 8 real seconds, none during a dialogue or chat;
  - jobs with no machine add `repAdd(dept, 1, { work: 1 }, 'jobs')` (always Works);
  - the Record badge is set once.
  - Repairs are still scored only by section 20, so nothing is counted twice.
- **The save:** `ci`, `co` and `rm` go through `int()` like the rest. Old saves load with 0s, which means "not clocked in".
- **The first week:** `careerAtWork` still accepts being in a Works room until `CAREER.grace` (day 7), so a new player isn't punished while they learn the clock. The tip and reminder only start from 07:00 on a shift day. That answers the engineer's question about first-week players: fine.
