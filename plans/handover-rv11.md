# Handover: RV11 (reviewer), 2026-10-24

Role: reviewer for the patch builds. I read a fix's diff, run its new check lines on the build before (they must FAIL) and on the fix (they must PASS), plant faults to prove each line bites, run the area's checks plus check_fast and cadet_test, and judge what else a player could see. Verdicts go to the fixer, the lead and the build master.

Branch: `claude/review-rv11` (notes only). Everything I reviewed is in `plans/review-rv11.md`, with every run's exit code and last line in `plans/review-rv11/runs.txt` and the probes I wrote in `plans/review-rv11/`.

## Builds reviewed

| Build | Fix | Final commit | Verdict |
|---|---|---|---|
| 0.92.2 | FX3 relay shelf glow | p5-fix3 04c38a76 | PASS (after: glow tap moved after tapCrew) |
| 0.92.2 | FX6 team repairs to 98 | team-restore 28bcc102 | PASS |
| 0.92.2 | DV1 Day 2 solo job tap | d2-solo-tap e81ef301 | PASS |
| 0.92.3 | FX4 items 2, 12, 14, 20, 26 | p923-fx4 97251620 | PASS (after: HUD button text; lift badge at 320 px) |
| 0.92.3 | FX8 items 22, 28 | p923-fx8 9fd5b500 | PASS (after: occasions skipped; person must be there) |
| 0.92.3 | DS1 items 1, 7-10 | p923-ds1 872d3c2b | PASS |
| 0.92.4 | FX4 B dirty clothes | p924-fx4 177bcc37 | PASS (after: laundry wording when out of clean clothes) |
| 0.92.4 | FX8 C crew glide | p924-fx8 69356d11 | PASS (after: day_check reads the drawn body) |
| 0.92.5 | FX9 items 6, 7 | p925-fx9b f67dd971 | PASS |
| 0.92.5 | FX13 item 5 | p925-fx13 04a9385d | PASS |
| 0.92.5 | FX11 items 2, 3, 14, 17 | p925-fx11 23432122 | PASS (after: seat hold after a move; a deterministic test) |

Cancelled: DS1 goodnight-words afc5e7a4 ("Breakfast from six"; breakfast is 07:00).

## Loose ends for the lead and the user
- The Day 1 10:00 double message (old toast plus new tip) is settled: 0.92.4 dropped the toast.
- Long crew get-ups (over 1.2 tiles, about 1 in 10 on Deck 3, plus the rec stands) still hop, by lead 34's choice. Backlog FX8-1: a swimmer leaving a lane jumps 5.2 tiles (old).
- The auditorium piano's tiles stay blocked on nights without talent night.
- intro_check part 12's new-game click flaked twice for me (it also hangs on 0.92.2 in a repro). Watch it in rounds.
- The bedtime tip is a long code stand-in until the writers add tip.bedtime.

## How I test (gotchas)
- Setup: `pip install playwright numpy pillow`; three.js r128 and acorn under `/tmp/cadet-work`; `CADET_CHROME=/opt/pw-browsers/chromium`. Each parallel run gets its own `CADET_WORK` (a lane script that symlinks three and acorn).
- One worktree per commit (`git worktree add --detach`). Plants are copies of the game with one exact-string change, run with the fix's own check file.
- Keep to about 3 browsers at once; interactions_check takes about 50 minutes under load, about 30 alone.
- A copy of intro_check.py or interactions_check.py must keep its file name (it finds cadet_test.py by replacing its own name).
- Don't use `pgrep -f`/`pkill -f` with the pattern in the same command; use `ps -eo pid,args | grep '[x]...'`.
- To test a crew or player state frame by frame, loop `window.__step(1, 1000/30)` inside one evaluate with `__skip` set; Game.step(n) runs n frames in one call.
- Read what is drawn (a.h.pos, isShown, getBoundingClientRect), not what the code computes; three fixes here passed their own checks until I looked at the screen.
- A check that sets up a crewmate once can lose to their plan within a frame; hold the state for the one synchronous call (FX11's stub) or re-set it every frame.
- Memory: my "3-4%" figures early on were the wrong counter; estimate from context instead.
