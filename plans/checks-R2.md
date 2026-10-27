# R2's checks: 0.94.0 full round

- Commit: `9faaee80` (claude/staging-0.94.0), Step 5, the Veyli vessel and the ending switched on, talk-only-when-close.
- Game sha256: `04cc0cb65f2272c8f7afbeb438b94d972d80a8f59d42580515b86a1a380e0dbf` (matches BM19's).
- OLD: 0.93.3, `git show 19400976:starship-cadet.html` (sha256 `ec93b94d...d085`).
- Share: old CR2 + old CR3 (without controller, which BM19 ran). `CADET_WORK=/tmp/work-R2`, at most two browser checks at once; perf_check alone.

| Check | Result | Key lines |
|---|---|---|
| intro_check (whole) | OK | `OK` (printed only when every part passes; 0 FAIL lines) |
| perf_check BUILD OLD | OK (noise, backlog 32) | exit 1 twice, each time different one-off frame-time spikes, none repeated (below). Memory: week 521 -> 522 geometries, round trips 521/521/521; draw calls unchanged |
| cadet_test OLD BUILD | OK (run by R1, handed over) | rc 0, `ALL IDENTICAL (apart from renderer noise: some pixels 1 level off)`; only j_steer1, 6 px, max 1 level |
| path_check | OK | exit 0, `PATH CHECK OK` |
| arc_check | OK | exit 0, `ARC CHECK OK` |
| lines_check | **FAIL (NEW, known to BM19: W6 words fix coming)** | exit 1, `lines_check: FAIL (4 errors, 105 warnings)` |
| lines_check --day | OK | exit 0, `lines_check --day: PASS (0 errors)` |
| p926_check | OK | exit 0, `P926 CHECK OK` |
| day_check Day 21 | OK | exit 0, `DAY CHECK OK` |
| day_check Day 0 | OK | exit 0, `DAY CHECK OK` |
| day_check Day 1 | OK | exit 0, `DAY CHECK OK` |
| day_check Day 5 | OK | exit 0, `DAY CHECK OK` |
| day_check Day 7 | OK | exit 0, `DAY CHECK OK` |
| weekend_check | OK | exit 0, `WEEKEND CHECK OK` |
| arrows_d_check | OK | exit 0, `arrows_d_check: OK` |
| arrows_f_check | OK | exit 0, `arrows_f_check: OK` |
| promo_sight_check | OK | exit 0, `PROMO SIGHT CHECK OK` |
| sound_check | OK | exit 0, `SOUND CHECK OK` |

## FAILs

### lines_check: NEW (no backlog row; reported to BM19 and lead 41 at once)

```
ERROR bank [event.veyliVessel.tap.sketch.shelf] "Taavek's sketch of you at the foot of the Tern's r": 145 characters (at most 90)
ERROR bank [event.veyliVessel.notice.roundOne.missed] "Taavek showed Calder and Zeke the round one at the": 113 characters (at most 90)
ERROR bank [event.veyliVessel.notice.home.missed] "Taavek went home on the Tern. They left a sketch f": 95 characters (at most 90)
ERROR bank [event.veyliVessel.signed] "You sign the sheet: Sunday, 13:00, Main storage to": 107 characters (at most 90)
lines_check: FAIL (4 errors, 105 warnings)
```

All four are in `content/banks/event-veyliVessel.lines`. Proof it is new: 0.93.3 checked out whole (19400976, its own
`content/`) gives `lines_check: PASS (0 errors, 69 warnings)`, exit 0. BM19 replied that W6 has a words fix coming.

### perf_check: noise (backlog 32)

Run 1 (alone, 62 min): one problem, `the Line supper, the mess Sun 18:30 trifold-open: js 2.11 -> 3.3 ms a frame`.
Run 2 (alone, re-measure, 62 min): that scene is not flagged; three other scenes are, each one not flagged in run 1:

```
PROBLEM Friday dinner, the mess 17:20 portrait: js 1.7 -> 2.73 ms a frame
PROBLEM lantern supper, the mess Sat 18:30 portrait: js 1.74 -> 3 ms a frame
PROBLEM weekend: Bread day, the galley Sun 07:25 trifold-open: js 1.73 -> 3.65 ms a frame
```

Four different one-off spikes over two runs, none repeated: backlog 32's pattern. No memory growth (backlog 14 not
seen), draw calls and triangles the same in both runs.

## Notes

- The background queue for intro_check was split mid-run to keep two browser checks going; intro's exit code was not
  kept, but its last line is `OK`, which intro_check prints only on the success path (`print('OK' if ok else 'FAILED')`).
- perf_check here takes about 62 minutes a run (15 in the guide).
