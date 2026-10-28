# 0.96.0 full round: R2's share (2026-10-28)

- Candidate: claude/staging-pad **6db1cdd2** (6db1cdd2f7f47e76d4f46ba3f05843ec10900dd6), game sha256
  `c62d63999e6b596d21806d1cb14fa9ab3168a50c5038dfcc1c04f3163d37a74e` (matched BM20's).
- OLD: 0.95.0, claude/integration b5199dc3, game sha256 `b18d2b6487e71ba5b1d806997821b6c11368a92659b8d4f6e97d9ffbb434238a` (matched).
- Later commit (BM20, after the game moved): claude/staging-pad **fe11cd66**, sha256
  `332925003934b49686c080515e154131a07f7fe7a3c14fbe0f6f7684933a129e` (matched): tiles and disc only.
- Setup: CADET_WORK /tmp/work-r2 and /tmp/work-r2b (one per browser), CADET_CHROME=/opt/pw-browsers/chromium,
  `pip install playwright numpy pillow`. Two browsers at most, 4 cores.

## Results

| Check | Commit | Result | Key lines |
|---|---|---|---|
| intro_check (whole) | 6db1cdd2 | OK (exit 0) | `OK`; 74 min (shared the cores with lane B) |
| day_check 0 | 6db1cdd2 | OK (exit 0) | `DAY CHECK OK` |
| day_check 1 | 6db1cdd2 | OK (exit 0) | `DAY CHECK OK` |
| day_check 5 | 6db1cdd2 | OK (exit 0) | `DAY CHECK OK` |
| day_check 7 | 6db1cdd2 | OK (exit 0) | `DAY CHECK OK` |
| day_check 21 | 6db1cdd2 | OK (exit 0) | `DAY CHECK OK` |
| day_check 22 | 6db1cdd2 | OK (exit 0) | `DAY CHECK OK` |
| weekend_check | 6db1cdd2 | OK (exit 0) | `WEEKEND CHECK OK` |
| arrows_check endgo asis (extra, from BM20's share) | 6db1cdd2 | OK (exit 0) | `ARROWS CHECK OK`; offer Day 32, Go Day 34, settled Day 35, ended Day 36; missed 0 |
| arrows_check endgo teachoff | 6db1cdd2 | OK (exit 0) | `ARROWS CHECK OK` |
| arrows_check endgo track | 6db1cdd2 | OK (exit 0) | `ARROWS CHECK OK` |
| perf_check BUILD OLD | 6db1cdd2 vs 0.95.0 | **FAIL (exit 1), twice** | run 1: `14 problem(s)`; run 2 (alone): `15 problem(s)`; all game ms a frame |
| tiles_check | fe11cd66 | OK (exit 0) | `ALL OK` |
| disc_check | fe11cd66 | OK (exit 0) | `ALL OK` |
| cadet_test OLD BUILD, lines, lines --day | - | dropped (lead 44) | BM20 ran them on fe11cd66 |
| path, arc | - | dropped (lead 44) | R3 runs them on fe11cd66 |
| p926 | - | dropped (lead 44) | R1 runs it on fe11cd66 |

endgo note (all three ways, not a FAIL): `(not the ending) stuck from Day 32 16:03 at "Clock in: shift at 09:00" (Deck 5)`, stuck 1. The check counts it as outside the ending.

## The FAIL: perf_check, game time a frame (NEW)

perf_check compares the two builds itself, so the OLD run is inside each run. Logs: `plans/checks-0960-r2-logs/perf-run1.txt`
and `perf-run2.txt`.

- **Same as OLD:** draw calls, triangles, geometries and textures in every scene; memory flat over a week and over
  deck round trips (521/40 -> 521 -> 521: backlog 14's +2 geometries did not show).
- **Different:** JS heap 87 -> 93 MB; game ms a frame.
- Run 1 shared the cores with my other browser (load 10 s -> 14 s). Run 2 was alone (load 10 s both).
- **Repeated on both measures** (so not a one-off spike, backlog 32):
  - Sunday dinner, the mess 18:30, portrait-wide: 2.32 -> 13.66 ms, then 2.43 -> 4.36 ms
  - lantern supper, the mess Sat 18:30, trifold-folded: 2.43 -> 3.78 ms, then 2.30 -> 3.67 ms
- The other problems move between scenes from one run to the next (quiz night, storm party, Bread day, the Line
  supper, the Veyli engine lights, the Captain's address). Each one is about 1 to 2 ms more a frame.
- Over all 127 views: mean 1.90 -> 2.19 ms (run 1) and 1.77 -> 1.99 ms (run 2), about +12%; median 1.68 -> 1.73
  and 1.65 -> 1.70 (+3%). NEW was slower in 76 and 84 of 127 views. The crowded mess scenes are the worst.
- Reading: a small, steady rise in script time a frame, likely from what 0.96.0 switches on (controller, sound,
  the visit). Draw calls and memory are fine. Not on the known-old list (backlog 14 memory, backlog 32 one-off
  spikes), so **NEW**; reported to BM20 and lead 44 at once. Whether it blocks is the build master's and lead's call.
