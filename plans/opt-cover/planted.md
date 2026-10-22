# Planted faults for the test picker (TS3, 2026-10-21/22; `tools/affected_planted.py`)

Why: most known failures (failures.md) come from commits where option (a) picks nearly every check, so "23 of 23"
proves less than it sounds (OR2, lead 25). These are small faults in **one** section each, each aimed at a check that
section's rules **don't** name, so only the coverage map can pick it. Each was then run for real: a fault counts only
if its check, on the faulty copy, prints a FAIL or error the game as it is doesn't (its known FAILs don't count), or
exits 1 where the game as it is exits 0. Game: claude/integration a4a5735 (0.64.12); map: tools/check_map.json (37
entries, the event days included).

## Result: 6 of 6 picked by (a) and (b), and each fails its check; the rules alone miss all 6

| # | Fault (one line) | Section | Check | Rules alone | (a) | (b) | The check on the faulty copy |
|---|---|---|---|---|---|---|---|
| 1 | an escort to a tile goes nowhere (`escortGoal`) | 10 | intro | miss (3 checks) | picks (7, 41 min) | picks | exit 1 (as is: 0); 12 new FAILs: "Torres never said goodnight", "following Torres, some core tour lines are never heard", ... |
| 2 | a typo in the seek chip (`seekEl` for `seekEl()`) | 20 | intro | miss (4) | picks (5, 19 min) | picks | exit 1 (as is: 0); `TypeError: el.appendChild is not a function` |
| 3 | a due tool no longer slows a look step (`workStep`) | 15 | mech | miss (3) | picks (4, 22 min) | picks | exit 1 (as is: 0); "FAIL side: a look step with a due tool takes a quarter longer" |
| 4 | a typo in `eventDay` (`fals`) | 18 | career | miss (10) | picks (14, 84 min) | picks | exit 1 (as is: 1, its known FAIL); new: `ReferenceError: fals is not defined` |
| 5 | a typo in the health check booking (`pls.id`) | 21 | player | miss (3) | picks (4, 27 min) | picks | exit 1 (as is: 0); `ReferenceError: pls is not defined` |
| 6 | your tasting vote isn't kept (`tallyVote`) | 18 | food | miss (10) | picks (11, 71 min) | picks | exit 1 (as is: 0); 2 new FAILs: "tasting with the tally", "your tastes" |

**What they prove** (OR2): the three crash typos (2, 4, 5) prove coverage (a check catches a typo only by running its line, which is what the map claims), not that a check notices wrong behaviour; the three behaviour faults (1, 3, 6) are the stronger evidence.

Run: `CADET_CHROME=/opt/pw-browsers/chromium python3 tools/affected_planted.py --run --out DIR` (about an hour, one
browser check at a time; the base run of each check once, then each fault); 2026-10-22 00:45-01:30 UTC, fault 4
again with the error rule at 01:31. On paper only: `python3 tools/affected_planted.py` (under a minute).

## Faults the checks did not notice (a finding about the checks, not the picker)

Tried first and replaced, because their check passed (or showed only its known FAIL) with the fault in:

| Fault | Section | Check | What the check missed |
|---|---|---|---|
| `seekArrive` never shows the chip | 20 | intro | a crew member who comes to find you never says anything |
| `socialSeekAsk` never records the ask | 20 | intro | Pell's "find you" ask on Day 3 never made |
| `wsOf` starts a work step afresh every time | 15 | mech | multi-visit work steps losing their progress |
| `eventDay` true on every day (guard off) | 18 | mech, career | every day treated as an event day |
| `crewGather` finds no tiles | 14 | career | the promotion's gatherings standing nobody anywhere (only career's known FAIL showed) |
| `DAY_SHIFT` 09:00 → 10:00 (a table) | 17 | intro | the day shift starting an hour late in the first week |

These are gaps worth a look by each check's owner (the picker did pick each of them; it's the checks that stayed green).
