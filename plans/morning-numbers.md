# Optimization results for the morning report (performance engineer, 2026-10-17 ~11:26 UTC)

Measured with the computer's CPU slowed 4x to stand in for a mid-range phone, standing in the mess for one ship hour, game code only. 0.60.2 vs 0.60.2 + the overnight speed work (perf 0.27.25-0.27.32). Same crew, same day.

| | Sunday dinner (64 crew) before | after | Tuesday breakfast before | after |
|---|---|---|---|---|
| Average game time per frame | 6.8-6.9 ms | 3.0-3.6 ms | 4.2-4.4 ms | 1.9-2.2 ms |
| Slow frames (over 16.7 ms, i.e. a missed frame) per hour | 54-55 | 7-8 | 24-26 | 4-9 |
| Visible hitches (over 33 ms) per hour | 9-12 | 2 | 1-2 | 0 |
| Worst frame | 90-144 ms | 64-75 ms | 60-61 ms | 28-30 ms |

Plain words: busy meals now need about half the phone's time; visible hitches at Sunday dinner drop from about one every 5-6 minutes to about two an hour. Picture is pixel-identical; routes identical.

Loading: unchanged (about 12 s at 4x slower CPU, about 7 s at normal speed; re-measured 6 runs each, an earlier "0.8 s slower" reading was noise). The shadow stand-ins do add a little to changing decks (Deck 3 most: maybe ~0.7 s on a phone); staggering them is the next optimization (0.27.33).

## 0.60.3 candidate measured (performance engineer, ~12:56 UTC), phone-like (4x slower CPU), one ship hour, two runs

| | 0.60.2 | 0.60.3 (no speed work) | 0.60.3 + speed work |
|---|---|---|---|
| Sunday dinner, average frame | 6.5-6.8 ms | 6.8-7.2 ms | 4.5-4.9 ms |
| Sunday dinner, missed frames/hour | 51-62 | 44-60 | 10-12 |
| Sunday dinner, visible hitches/hour | 6-13 | 9 | 1-2 |
| Breakfast (crew 26 → 45 with the real line), average | 4.1 ms | 5.2-5.4 ms | 3.0-3.2 ms |
| Breakfast, missed frames/hour | 18-20 | 43-48 | 4-6 |
| Breakfast, visible hitches/hour | 2-3 | 4-6 | 0 |

Load time: about the same (~12 s at phone speed; maybe up to 0.5 s slower from the bigger file). Draw calls unchanged (max 430 of 450). Memory flat over a week. File 2.96 → 3.29 MB (new writing).
Decision (lead, 12:57): the speed work goes into 0.60.3 itself (reviewed, identical picture and routes) so the morning build is the smooth one.

## FINAL 0.60.3 (cand-0603 2f7fb2a) vs 0.60.2, phone-like, measured by perf engineer 3 (~14:41 UTC; slower test machine, compare builds with each other)

| | 0.60.2 | 0.60.3 |
|---|---|---|
| Sunday dinner, average frame | 9.5-11.9 ms | 5.2-7.0 ms |
| Sunday dinner, missed frames/hour | 130-260 | 17-37 |
| Sunday dinner, visible hitches/hour | 16-22 | 2-6 |
| Breakfast (27 → 45 crew), average frame | 7.5-8.4 ms | 3.6-4.0 ms |
| Breakfast, missed frames/hour | 91-102 | 21-27 |
| Breakfast, visible hitches/hour | 8-12 | 3-7 |
| Load time | same | same |

Plain words: about twice as smooth on a phone at the busiest meals, same load time. GPU draws about a third fewer. Memory flat over a week of play.
