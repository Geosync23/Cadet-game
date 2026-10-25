# CR5 check results

Check runner 5. Share (plans/testing-guide.md, six-way split): `day_check` Days 21 and 27, interactions, events,
career. Own `CADET_WORK=/tmp/work-cr5`, `CADET_CHROME=/opt/pw-browsers/chromium`, one browser check at a time, each
on a copy of the game in `/tmp/work-cr5/new.html` (sha256 checked after copying).

## 0.92.6 full round (2026-10-25, started 15:24 UTC, for BM17 and lead 36)

- Candidate: `claude/staging-0.92.6` b78e1e22 (the final one, with odd jobs). Switches in the file: `ODD_ON = true`
  (20931), `BOARD_TRADE_ON = true` (21139), `STORIES_ON = true` (48484), `PROMO_SIGHT_ON = true` (56665), `PAD_ON =
  false` (61602). Checks run from a worktree of b78e1e22 (its own scripts).
- `starship-cadet.html` sha256 `88f4cc8db099337d1ae61cf05e58be93af6577abea5458ba1449a27733f16fe4`: matches BM17's.
- OLD: 0.92.5 39f7741d (`fddc0ef6...5559`, the file of my 0.92.5 round).
- A first start on defc327f (without odd jobs) was stopped after ~1 minute at BM17's word and thrown away.

| Check | Result | Exit | Time | Key lines |
|---|---|---|---|---|
| `day_check.py BUILD 21` | OK | 0 | 297 s | `DAY CHECK OK` |
| `day_check.py BUILD 27` | OK | 0 | 295 s | `DAY CHECK OK` |
| `interactions_check.py BUILD` | OK | 0 | 2597 s | `INTERACTIONS CHECK OK` (now with the odd jobs) |
| `events_check.py BUILD` | OK | 0 | 645 s | `EVENTS CHECK OK` (slower: 0.92.5 took 522 s) |
| `career_check.py BUILD` | **FAIL (NEW)** | 1 | 140 s | `FAIL busy: "Relied on" before Day 5` |
| `promo_sight_check.py BUILD` (new) | OK | 0 | 17 s | `PROMO SIGHT CHECK OK` |

### The career FAIL

One line, `FAIL busy: "Relied on" before Day 5`: backlog 12's words, but **OLD passes** (the same career_check.py on
39f7741d: `CAREER CHECK OK`), so it is NEW by the rule. The very busy player (part c), Days 1-5:

| Build | Jobs a day | xp and reputation on Day 4 | Relied on |
|---|---|---|---|
| OLD 0.92.5 | 21, 21, 22, 18, 18 | 39, trusted | Day 5 (pass) |
| b78e1e22 | 30, 28, 28, 26, 24 | 41, relied | Day 4 (FAIL) |
| copy, `ODD_ON` false | 22, 20, 23, 22, 19 | 40, relied | Day 4 (FAIL) |
| copy, `BOARD_TRADE_ON` false | 30, 28, 28, 26, 21 | 41, relied | Day 4 (FAIL) |
| copy, `PROMO_SIGHT_ON` false | 30, 28, 28, 26, 24 | 41, relied | Day 4 (FAIL) |
| copy, all four new `_ON` false | 22, 20, 22, 19, 18 | 40, relied | Day 4 (FAIL) |

So odd jobs add about 8 jobs a day, but even with all four new switches off, the busy player ends Day 4 one xp over
OLD (40 against 39) and reaches Relied on a day early: another 0.92.6 change (not one of the four `_ON` switches)
gives that last point. Each copy changes only its switch lines (2 or 8 diff lines); the real file is untouched.

**CR5: FAIL** (5 of 6 OK; career NEW).

**Lead 36's follow-up** (the two suspects together, and an odd job's reputation):
- A copy with `ODD_ON` and `BOARD_TRADE_ON` both false (4 diff lines): still `FAIL busy: "Relied on" before Day 5`;
  Days 1-5 22, 20, 22, 19, 18 jobs; xp 4, 14, 32, **40 relied** on Day 4. The extra point already shows on Day 1
  (xp 4; OLD 3).
- An odd job's reputation: **none of its own**. Every board top-up, odd ones included, is made with `xp: 0`
  (game line 21088, `fixPost`: `extra: true, xp: 0, fix: r.id, fixS: st`), the same as the small repairs; line 21100
  says why (the career's pace waits for the balancing pass, backlog 12 and 17). So odd jobs add jobs (about 8 a day
  for the busy player), not xp directly; with them on the player still gains a point more by Day 4 (41 against 40),
  through what the extra work leads to.
- The calls that give reputation (`worksXp(...)`) are the same in OLD and b78e1e22 (same list, same arguments), so
  the Day 1 point comes from what the busy player gets to do, not from a new reward. Which 0.92.6 change it is needs a
  bisect of the build's other items (not a switch).

## 0.92.5 full round (2026-10-25, started 05:50 UTC, for BM17 and lead 35)

- Candidate: `claude/staging-0.92.5` 53c11f8 (0.92.5: items 1-12, 14-22, the sim bay and the weekend on). Switches in
  the file: `POINT_ON = true` (12892), `GUIDE_ON = true` (16802), `EV_LINE_ON = EVENTS_ON` (41352), `PAD_ON = false`
  (59462). Checks run from a worktree of 53c11f8 (its own scripts).
- `starship-cadet.html` sha256 `fddc0ef61c68ac012409a0f88e4ded2a62098b28377760461d99fb144b595559`: matches BM17's.
- OLD: 0.92.4 ba836359 (`2aa6427f...13a2`, the file of my 0.92.4 round). Not needed: nothing failed.

| Check | Result | Exit | Time | Key lines |
|---|---|---|---|---|
| `day_check.py BUILD 21` | OK | 0 | 275 s | `DAY CHECK OK`; draw calls peak 242 / 201 / 295 / 237 on Decks 1-4 (budget 450; 0.92.4: 204 / 195 / 295 / 236, Deck 1 +38) |
| `day_check.py BUILD 27` | OK | 0 | 255 s | `DAY CHECK OK` |
| `interactions_check.py BUILD` | OK | 0 | 2156 s | `INTERACTIONS CHECK OK` |
| `events_check.py BUILD` | OK | 0 | 522 s | `EVENTS CHECK OK`; Day 0 table 48 of 48 (slower: 0.92.4 took 442 s) |
| `career_check.py BUILD` | OK | 0 | 128 s | `CAREER CHECK OK`; ship.works after 30 busy days 2520 bytes, log 30 |

No FAIL lines in any log. **CR5: OK** (5 of 5).

## 0.92.4 full round (2026-10-24, started 18:58 UTC, for BM16 and lead 34)

- Candidate: `claude/staging-0.92.4` 5bad724d (0.92.4). Switches in the file: `POINT_ON = true` (12690),
  `GUIDE_ON = true` (16585), `EV_LINE_ON = EVENTS_ON` (40512), `PAD_ON = false` (58232). Checks run from a worktree of
  5bad724d (its own scripts).
- `starship-cadet.html` sha256 `2aa6427fde381f3ddf746900ed9e7a62f51aa27f0bb6460f73c557836fa313a2`: matches BM16's.
- OLD: 0.92.3 3866c8f3 (`f18e8540...07853`, the file of my 0.92.3 Round 2). Not needed: nothing failed.

| Check | Result | Exit | Time | Key lines |
|---|---|---|---|---|
| `day_check.py BUILD 21` | OK | 0 | 286 s | `DAY CHECK OK`; draw calls peak 204 / 195 / 295 / 236 on Decks 1-4 (budget 450) |
| `day_check.py BUILD 27` | OK | 0 | 268 s | `DAY CHECK OK` |
| `interactions_check.py BUILD` | OK | 0 | 2371 s | `INTERACTIONS CHECK OK` |
| `events_check.py BUILD` | OK | 0 | 442 s | `EVENTS CHECK OK`; Day 0 table 48 of 48 |
| `career_check.py BUILD` | OK | 0 | 128 s | `CAREER CHECK OK`; ship.works after 30 busy days 2534 bytes, log 30 |

No FAIL lines in any log. **CR5: OK** (5 of 5).

## 0.92.3 full round, Round 2 (2026-10-24, started 10:58 UTC, for BM16 and lead 33)

- Candidate 2: `claude/staging-0.92.3` d9a387b6 (0.92.3 with AC3's m3d fix 4928271f; the game differs from candidate 1
  by one line). Checks run from a worktree of d9a387b6 (its own scripts). Started straight after Round 1 passed, as
  BM16 asked.
- `starship-cadet.html` sha256 `f18e85405e2f18893bb97d10915f3d068a4b02ac66ff74c441353eb22f107853`: matches BM16's.
- OLD: 0.92.2 364c80cb. Not needed: nothing failed.

| Check | Result | Exit | Time | Key lines |
|---|---|---|---|---|
| `day_check.py BUILD 21` | OK | 0 | 252 s | `DAY CHECK OK`; draw calls peak 204 / 195 / 295 / 236 on Decks 1-4 (budget 450) |
| `day_check.py BUILD 27` | OK | 0 | 239 s | `DAY CHECK OK` |
| `interactions_check.py BUILD` | OK | 0 | 2055 s | `INTERACTIONS CHECK OK` |
| `events_check.py BUILD` | OK | 0 | 368 s | `EVENTS CHECK OK`; Day 0 table 48 of 48 |
| `career_check.py BUILD` | OK | 0 | 115 s | `CAREER CHECK OK`; ship.works after 30 busy days 2534 bytes, log 30 |

No FAIL lines in any log. **Round 2: CR5 OK** (5 of 5).

## 0.92.3 full round, Round 1 (2026-10-24, started 10:03 UTC, for BM16 and lead 33)

- Candidate 1: `claude/staging-0.92.3` 0dd4e2e2 (0.92.3). Switches in the file: `POINT_ON = true` (12677),
  `GUIDE_ON = true` (16543), `EV_LINE_ON = EVENTS_ON` (40466), `PAD_ON = false` (58183). Checks run from a worktree of
  0dd4e2e2 (its own scripts).
- `starship-cadet.html` sha256 `4e6538447d13e4c5398fc74844748e1e9d41776afa7bcc83bc99d5eff87cd0a2`: matches BM16's.
- OLD: 0.92.2 364c80cb (`ca2f908d...e7e4`, the file of my 0.92.2 round). Not needed: nothing failed.
- CR6's m3d FAIL (not in this share) led to candidate 2; BM16: finish this one, then Round 2.

| Check | Result | Exit | Time | Key lines |
|---|---|---|---|---|
| `day_check.py BUILD 21` | OK | 0 | 265 s | `DAY CHECK OK`; draw calls peak 204 / 195 / 295 / 236 on Decks 1-4 (budget 450) |
| `day_check.py BUILD 27` | OK | 0 | 252 s | `DAY CHECK OK` |
| `interactions_check.py BUILD` | OK | 0 | 2127 s | `INTERACTIONS CHECK OK` |
| `events_check.py BUILD` | OK | 0 | 387 s | `EVENTS CHECK OK`; Day 0 table 48 of 48 (slower than its usual ~260 s; ran beside other work, not a FAIL) |
| `career_check.py BUILD` | OK | 0 | 120 s | `CAREER CHECK OK`; ship.works after 30 busy days 2534 bytes, log 30 |

No FAIL lines in any log. **Round 1: CR5 OK** (5 of 5).

## 0.92.2 full round (2026-10-23, started 23:49 UTC, for BM15 and lead 32)

- Candidate: `claude/integration-next` ee974894 (0.92.2: team repairs to 98, meals never lost in silence, first solo
  job's arrow, Day 0 diners' own evening, relay shelf glow tap, tray-in-hand seat arrow). Switches in the file:
  `POINT_ON = true` (12657), `GUIDE_ON = true` (16499), `EV_LINE_ON = EVENTS_ON` (38060), `PAD_ON = false` (55638).
  Checks run from a worktree of ee974894 (its own scripts).
- `starship-cadet.html` sha256 `ca2f908d603a53c24c110d26e22b71bc43d26b94d904f2129d9ea494a206e7e4`: matches BM15's.
- OLD: 0.92.1 e03505fd (`2dbb11b8...59b18c`). Not needed: nothing failed.
- BM15's message reached this session at 23:48 UTC (sent ~23:05); started at once.

| Check | Result | Exit | Time | Key lines |
|---|---|---|---|---|
| `day_check.py BUILD 21` | OK | 0 | 284 s | `DAY CHECK OK`; draw calls peak 204 / 195 / 295 / 236 on Decks 1-4 (budget 450; same as 0.92.1) |
| `day_check.py BUILD 27` | OK | 0 | 269 s | `DAY CHECK OK` |
| `interactions_check.py BUILD` | OK | 0 | 2078 s | `INTERACTIONS CHECK OK` |
| `events_check.py BUILD` | OK | 0 | 264 s | `EVENTS CHECK OK`; Day 0 table 48 of 48 before Zeke's goodnight |
| `career_check.py BUILD` | OK | 0 | 136 s | `CAREER CHECK OK`; ship.works after 30 busy days 2664 bytes (0.92.1: 2714), log 30 |

No FAIL lines in any log. **CR5: OK** (5 of 5).

## 0.92.1 full round (2026-10-23, started 16:46 UTC, for BM15 and lead 31)

- Candidate: `claude/integration-next` 51a1bb34 (0.92.1: Crossing the Line ON, save trim, join notices, Day 0 table
  trickle, Zeke's stall fix, ...). Switches in the file: `POINT_ON = true` (12644), `GUIDE_ON = true` (16465),
  `EV_LINE_ON = EVENTS_ON` (38013), `PAD_ON = false` (55565). Checks run from a worktree of 51a1bb34 (its own
  scripts).
- `starship-cadet.html` sha256 `2dbb11b81c6d0da3bcaf32ad0d78ead80e4dcc8fa8b4ea5fc142bf1d2a59b18c`: matches BM15's.
- OLD: 0.92.0 685af944 (`f2329b62...1ebd`). Not needed: nothing failed.

| Check | Result | Exit | Time | Key lines |
|---|---|---|---|---|
| `day_check.py BUILD 21` | OK | 0 | 282 s | `DAY CHECK OK`; draw calls peak 204 / 195 / 295 / 236 on Decks 1-4 (budget 450) |
| `day_check.py BUILD 27` | OK | 0 | 267 s | `DAY CHECK OK` |
| `interactions_check.py BUILD` | OK | 0 | 1788 s | `INTERACTIONS CHECK OK` |
| `events_check.py BUILD` | OK | 0 | 255 s | `EVENTS CHECK OK`; Day 0 table 48 of 48 before Zeke's goodnight |
| `career_check.py BUILD` | OK | 0 | 133 s | `CAREER CHECK OK`; KS1 passes: ship.works after 30 busy days 2714 bytes (was 3001), log 30 |

No FAIL lines in any log. **CR5: OK** (5 of 5).

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

**Re-run, events_check on FX5's Day 0 table fix** (BM14, 11:31 UTC): `claude/integration-next` 4e324417 ("day0-table:
Day 0's kept seat is never cut short by the next walk ..."), game sha256
`f2329b620c113b0a585d6129ef70a3cbb8f8112c6ef9d19a13587fb996271ebd` (matches BM14's), run alone from a worktree of
4e324417 with its events_check.py: exit 0 in 275 s, `EVENTS CHECK OK`, no FAIL lines; `Day 0 table: {'seats': 48,
'free': 1185, 'most': 48, 'before': 48}` (all 48 still seated 5 minutes before Zeke's goodnight; was 45).

**CR5 for 0.92.0 now:** day_check 21 OK, 27 OK, interactions OK (on c2180854), career known KS1 only (on c2180854),
events OK (on f2329b62). BM14 (11:37 UTC): no further re-runs; FX5's change only touches Day 0's kept seat (RV10 checked Days 0-28), so
the c2180854 results stand. Stood down.

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
