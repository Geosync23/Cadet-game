# CR5 check results

Check runner 5. Share (plans/testing-guide.md, six-way split): `day_check` Days 21 and 27, interactions, events,
career. Own `CADET_WORK=/tmp/work-cr5`, `CADET_CHROME=/opt/pw-browsers/chromium`, one browser check at a time, each
on a copy of the game in `/tmp/work-cr5/new.html` (sha256 checked after copying).

## 0.92.0 full round (2026-10-23, started 08:38 UTC, for BM14 and lead 31)

- Candidate: `claude/integration-next` 4147f03d (0.92.0: teaching arrows ON, Pillar 5 fixes, breakfast at 07:00,
  Zeke's Day 0 tour, the dinner spread, ...; controller and Crossing the Line off). Checks run from a worktree of
  4147f03d, except interactions_check.py, which is 3d729dd7's (FB1's test-only garden fix, BM14's instruction; file
  sha256 cbf23b84...). The game at 3d729dd7 is the same file.
- `starship-cadet.html` sha256 `c2180854a780936c21cbac0ba9e7932fb491759f740e1d5ac3b4d4494a4f1286`: matches BM14's.
- OLD: 0.91.0 989fd566 (`da9f1d08...dc94aee`).
- First start stopped after ~3 min of Day 21 (BM14's correction about which interactions_check to use); restarted
  clean. Only the restarted run is reported.

| Check | Result | Exit | Time | Key lines |
|---|---|---|---|---|
| `day_check.py BUILD 21` | OK | 0 | 283 s | `DAY CHECK OK`; draw calls peak 204 / 195 / 293 / 236 on Decks 1-4 (budget 450) |
| `day_check.py BUILD 27` | OK | 0 | 279 s | `DAY CHECK OK` |
| `interactions_check.py BUILD` (3d729dd7's) | OK | 0 | 1894 s | `INTERACTIONS CHECK OK`; neither known item (garden pin, Cart dock 1) failed. Slow: 0.91.0 took 486 s |
| `events_check.py BUILD` | **FAIL (NEW)** | 1 | 287 s | `FAIL Day 0's Sunday table not full 5 minutes before Zeke's goodnight: {'seats': 48, 'free': 1185, 'most': 48, 'before': 45}` |
| `career_check.py BUILD` | **FAIL (NEW)** | 1 | 128 s | 12 FAIL lines (below) |

### The FAILs

Both repeat exactly when run alone (events: the same line; career: the same 12 lines, `diff` empty). Neither is on
the known list (backlog 14, 23, 32; controller_check day x2; interactions' two items).

**events_check**: one line, quoted in the table: on Day 0, 45 of the Sunday table's 48 diners are still seated at
19:40 (5 minutes before `free` = 1185 = 19:45, Zeke's goodnight); the check wants all of them. This part is new
(ed7f5318, "Day 0's table full till Zeke's goodnight"), not in 0.91.0's events_check, so OLD can't show it. With
the arrows switched off in a copy (`POINT_ON`, `GUIDE_ON` false, 4 lines changed) it fails the same way: not the
arrows.

**career_check**: 12 FAIL lines; 0.91.0's career_check passed (the arrows were off there).
1. Toasts (3): the check reads the Day 0 wake toast ("You wake in Bunk 1, in the junior wing. Tap to walk
   somewhere...") instead of the one it expects: `a reminder never covers a toast on screen, nor in the gap after
   it`; `its word going up is said`; `a missed shift: said and in Mail` (the Mail is there, the toast read is the
   wake one). Likely BM14's note: with the arrows on, toasts queue.
2. Meeting and call arrows (8), each finding no arrow (None): `an ask made during a sleep is told (toast) when you
   are up; its arrow comes 15 minutes before the meeting`; `bug 2: the meeting arrow is up 14 minutes before`;
   `bug 2: in the room it says wait here ...`; `bug 2 (PR9): another arrow borrows it ...` (Food, None); `(p2) a job
   taken inside the window should not keep the meeting's arrow away`; `(p3) the call's arrow is up at 10:30`; `(p3)
   coming into her office before the meeting starts, the call's arrow should stay`; `(p3) the meeting plays, then
   her walk to the pipe takes the arrow`.
3. Save size (1): `ship.works over 3 KB by Day 30, or the log not cut to 30`: 3001 bytes after 30 busy days (limit
   3000), log 30.

With the arrows off in a copy: only line 3 fails (the 3001-byte save); the 11 others pass. So 1 and 2 come with the
arrows on; 3 doesn't.

Logs (this container): `/tmp/work-cr5/logs-new7/` (`events.txt`, `career.txt`, `*-rerun.txt`, `*-arrowsoff.txt`).

**CR5: FAIL** (3 of 5 OK; events and career NEW).

**Re-run, career_check with AC3's test-only fix** (BM14, 09:45 UTC): `claude/integration-next` 7ac605e4's
career_check.py (file sha256 9d38bdd2...), the same game (7ac605e4's starship-cadet.html is still c2180854...).
Exit 1 in 137 s, one FAIL line, as BM14 expected: `FAIL ship.works over 3 KB by Day 30, or the log not cut to 30`
(`ship.works after 30 busy days: 3001 bytes, log 30`). Lead 31 made it known item **KS1** for this round (old slow
growth; trimmed in the next build). So career: **known (KS1)**. events_check waits for FX5's game fix (new sha).

## 0.91.0 full round (2026-10-22, started ~21:30 UTC, for BM14 and lead 29 / lead 30)

- Candidate: `claude/integration-next` 989fd566 (0.91.0: CP1's controller 0.90.9 on 0.64.16, PAD_ON off, + fresh-eyes
  batch 1; breakfast not in it). Checks run from a worktree of this commit (its own check scripts).
- `starship-cadet.html` sha256 `da9f1d0851efa06a307e2fafe9eef9ff4d867d625c2f5c2d3e584aa79dc94aee`: matches BM14's.
- OLD: 0.64.16 b9f053ba (`70f94273...42e6a5c7`). Not needed: nothing failed. Known-old this round: backlog 14, 23,
  32, controller_check touch and day (none in this share).

| Check | Result | Exit | Time | Key lines |
|---|---|---|---|---|
| `day_check.py BUILD 21` | OK | 0 | 275 s | `DAY CHECK OK`; draw calls peak 220 / 207 / 258 / 233 on Decks 1-4 (budget 450; the same as 0.64.16) |
| `day_check.py BUILD 27` | OK | 0 | 266 s | `DAY CHECK OK` |
| `interactions_check.py BUILD` | OK | 0 | 486 s | `INTERACTIONS CHECK OK` |
| `events_check.py BUILD` | OK | 0 | 252 s | `EVENTS CHECK OK` |
| `career_check.py BUILD` | OK | 0 | 45 s | `CAREER CHECK OK` |

No FAIL lines in any log. **CR5: OK** (5 of 5).

## 0.64.17 full round, second candidate (2026-10-22, started ~16:40 UTC, for lead 29 and BM14)

- Candidate: `claude/integration-next` 1498dbf4 (0.64.17 with SC1's tradMeal Line supper fix 7f07d035 and CP4's
  bubble slide cap 36f8abf7). Checks run from a worktree of this commit (its own check scripts).
- `starship-cadet.html` sha256 `ff45b427d65d543ab8dfe10f289b49653f0102af8ef513b960dd2e2ecbfac306`: matches lead 29's.
- OLD: 0.64.16 b9f053ba (`70f94273...42e6a5c7`). Not needed: nothing failed. Known-old this round: backlog 14, 23,
  32 (none in this share).

| Check | Result | Exit | Time | Key lines |
|---|---|---|---|---|
| `day_check.py BUILD 21` | OK | 0 | 236 s | `DAY CHECK OK`; draw calls peak 204 / 195 / 293 / 235 on Decks 1-4 (budget 450; same as 8193458e) |
| `day_check.py BUILD 27` | OK | 0 | 221 s | `DAY CHECK OK` |
| `interactions_check.py BUILD` | OK | 0 | 381 s | `INTERACTIONS CHECK OK` |
| `events_check.py BUILD` | OK | 0 | 234 s | `EVENTS CHECK OK` |
| `career_check.py BUILD` | OK | 0 | 45 s | `CAREER CHECK OK` |

No FAIL lines in any log. **CR5: OK** (5 of 5).

## 0.64.17 full round (2026-10-22, started 15:50 UTC, for lead 28 and BM13 / BM14)

- Candidate: `claude/integration-next` 8193458e (0.64.17, breakfast at 07:00). Checks run from a worktree of this
  commit (its own check scripts).
- `starship-cadet.html` sha256 `225836918e5a70cad2a9809b2aea8febc21837617f3dee907b49a07655a4c4b5`: matches BM13's.
- OLD: `claude/integration` b9f053ba (0.64.16), sha256 `70f94273...42e6a5c7`. Not needed: nothing failed.
- The round is held for SC1's m12 fix (CR6's mech_check FAIL, not in this share; lead 28).

| Check | Result | Exit | Time | Key lines |
|---|---|---|---|---|
| `day_check.py BUILD 21` | OK | 0 | 300 s | `DAY CHECK OK`; draw calls peak 204 / 195 / 293 / 235 on Decks 1-4 (budget 450; 0.64.16: 220 / 207 / 258 / 233, the earlier breakfast moves the busy moment) |
| `day_check.py BUILD 27` | OK | 0 | 291 s | `DAY CHECK OK` |
| `interactions_check.py BUILD` | OK | 0 | 458 s | `INTERACTIONS CHECK OK` |
| `events_check.py BUILD` | OK | 0 | 264 s | `EVENTS CHECK OK` |
| `career_check.py BUILD` | OK | 0 | 46 s | `CAREER CHECK OK` |

No FAIL lines in any log. **CR5: OK** (5 of 5).

## 0.64.16 full round (2026-10-22, started 14:06 UTC, for lead 27 / lead 28 and BM13)

- Candidate: `claude/integration-next` b9f053ba ("0.64.16: the Zeke patch (ON1's claude/patch-zeke ce2f77bc)").
  Checks run from a worktree of this commit (its own check scripts).
- `starship-cadet.html` sha256 `70f9427354a398ef25e355e7428f10ba6f0800b4c83a83945c8c950a42e6a5c7`: matches BM13's.
- OLD: `claude/integration` 2b4a05db (0.64.15), sha256 `0c1f6fb4...8259d2e` (the 0.64.15 re-run's file). Not
  needed: nothing failed.

| Check | Result | Exit | Time | Key lines |
|---|---|---|---|---|
| `day_check.py BUILD 21` | OK | 0 | 284 s | `DAY CHECK OK`; draw calls peak 220 / 207 / 258 / 233 on Decks 1-4 (budget 450) |
| `day_check.py BUILD 27` | OK | 0 | 277 s | `DAY CHECK OK` |
| `interactions_check.py BUILD` | OK | 0 | 449 s | `INTERACTIONS CHECK OK` |
| `events_check.py BUILD` | OK | 0 | 258 s | `EVENTS CHECK OK` |
| `career_check.py BUILD` | OK | 0 | 47 s | `CAREER CHECK OK` |

No FAIL lines in any log. **CR5: OK** (5 of 5).

## 0.64.15 full re-run (2026-10-22, started 08:46 UTC, for lead 26 and BM13)

- Candidate: `claude/integration-next` 31c44cb9 ("Merge claude/patch-play1-d 836db6c7 (CJ1: part 14 takes fetch or
  make ...)"). Checks run from a worktree of this commit (its own check scripts).
- `starship-cadet.html` sha256 `0c1f6fb487d6f7f7a47ab3f4f20a475f0ded2b53107030bdd4dbfb6ef8259d2e`: matches the
  lead's.
- OLD: `claude/integration` 32b699a6 (0.64.14), sha256 `94f32868...881e9`: matches. Not needed: nothing failed.

| Check | Result | Exit | Time | Key lines |
|---|---|---|---|---|
| `day_check.py BUILD 21` | OK | 0 | 224 s | `DAY CHECK OK`; draw calls peak 220 / 207 / 258 / 233 on Decks 1-4 (budget 450) |
| `day_check.py BUILD 27` | OK | 0 | 202 s | `DAY CHECK OK` |
| `interactions_check.py BUILD` | OK | 0 | 364 s | `INTERACTIONS CHECK OK` |
| `events_check.py BUILD` | OK | 0 | 229 s | `EVENTS CHECK OK` |
| `career_check.py BUILD` | OK | 0 | 43 s | `CAREER CHECK OK` |

No FAIL lines in any log. **CR5: OK** (5 of 5).

## 0.64.15 full round (2026-10-22, started 06:43 UTC, for lead 26 and BM13)

- Candidate: `claude/integration-next` c5c43293 ("0.64.15: playtest patch 1 ... the Line merged switched off;
  breakfast (F) not in it").
- `starship-cadet.html` sha256 `e955d667fe946b3e1e0a21c0b1f3049694460096f675dad5019c328e5d7d4a25`: matches the
  lead's.
- OLD (for any FAIL): `claude/integration` 32b699a6 (0.64.14), sha256
  `94f32868dbe7f27fc744eb834bb6b5f7c335bc15ac1bca86563d8ca4652881e9`: matches. Not needed: nothing failed.

| Check | Result | Exit | Time | Key lines |
|---|---|---|---|---|
| `day_check.py BUILD 21` | OK | 0 | 271 s | `DAY CHECK OK`; draw calls peak 220 / 207 / 258 / 233 on Decks 1-4 (budget 450); worst stuck 0.0 ship min |
| `day_check.py BUILD 27` | OK | 0 | 266 s | `DAY CHECK OK` |
| `interactions_check.py BUILD` | OK | 0 | 425 s | `INTERACTIONS CHECK OK` |
| `events_check.py BUILD` | OK | 0 | 247 s | `EVENTS CHECK OK` |
| `career_check.py BUILD` | OK | 0 | 43 s | `CAREER CHECK OK` (backlog 12's `busy: "Relied on" before Day 5` doesn't show) |

No FAIL lines in any log. The one warning is Python's `SyntaxWarning: invalid escape sequence '\|'` at
interactions_check.py:498 (the check's own source, not the game; harmless).

**CR5: OK** (5 of 5).
