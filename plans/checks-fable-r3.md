# Round fable, share R3 (check runner R3, session_01GKuymjwGjfNXnjezjs87rS)

- Candidate 1: claude/staging-fable-review c4999dae, label 0.99.92-review.
- Game file starship-cadet.html sha256 d6b9ce81a5254ab089f07afad01ed20edbd05e38d12a6043092f0578f9efa1c0 (matches the GO).
- Check files: c4999dae's own. Each check run once, on the candidate. No FAIL, so OLD (0.99.91) was not run.
- Order: controller_check first, two lanes at once and nothing else on the machine (4 cores); then sound_check
  alone; then the other six in two lanes. Script: plans/r3-scripts/roundf.sh. 2026-11-15, 09:12 to 10:42 UTC.

**Result: R3: OK**

| Check | Result | Key lines |
|---|---|---|
| controller_check G1 (idle save calls touch walk pick lift door day games unplug odd) | OK | exit 0, 1396 s, CONTROLLER CHECK OK, 12 parts, skipped 0 |
| controller_check G2 (shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words) | OK | exit 0, 2408 s, CONTROLLER CHECK OK, 26 parts; tiles passed first time; skipped 1 (see below) |
| controller_check G3 (m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3) | OK | exit 0, 2305 s, CONTROLLER CHECK OK, 13 parts, skipped 0 |
| controller_check G4 (nights mentor props jobs2 beam court) | OK | exit 0, 394 s, CONTROLLER CHECK OK, 6 parts, skipped 0 |
| sound_check (alone) | OK | exit 0, 568 s, SOUND CHECK OK, skipped 0 |
| promo_sight_check | OK | exit 0, 17 s, PROMO SIGHT CHECK OK, skipped 0 |
| arrows_d_check | OK | exit 0, 81 s, arrows_d_check: OK, skipped 0 |
| arrows_f_check | OK | exit 0, 38 s, arrows_f_check: OK, skipped 0 |
| ending_check | OK | exit 0, 142 s, ENDING CHECK OK, skipped 0 |
| devmode_check (all parts) | OK | exit 0, 866 s, DEVMODE CHECK OK, skipped 0 |
| dev_arrow_check | OK | exit 0, 180 s, DEV ARROW CHECK OK, skipped 0 |

Notes
- controller_check: all 57 parts but reach (the four groups together are the check's whole list less reach). No
  "not yet", no timeout, no FAIL line. This is its first clean run with FRP_PINTAP_ON and FRP_LEAD_ON on.
- The one "skipped" line (controller G2, log line 38) is game screen text inside a printed focus dump in the clock
  part ("Clock in, A again 1 s later"), not a test that was skipped.
- No flakes this round: sound's timing parts and controller's tiles each passed on their one run.
