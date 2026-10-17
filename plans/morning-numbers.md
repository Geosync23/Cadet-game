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
