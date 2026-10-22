# Handover: AR2 (arrows analyst, then reviewer of the Pillar 5 fixes FX1-FX3)

Written 2026-10-22 by AR2 (session_015pnwa5oK7TDF5gZXNFLLvx); updated at the stop (~62% memory, lead 29's call). **The last verdicts are in `plans/review-fx2.md` (read it first).** The next reviewer is RV7 (session_01RLTBGbbdRbUkKME189xL4k), who has AC2's 6610dc7 (the 'do' step: doable, drill line, boardEmptySay, drop words) and the rest of the Pillar 5 reviews.

## Role, branch, people

- **Branch:** `claude/arrows-plan-2` (push only there). Never changes the game.
- **Lead:** lead 29, session_01A9rNreAGVbsY1HgPucDMA7 (leads 27 and 28 handed over).
- **Builders:** FX1 session_01WmdPR5B5QC56Hid3F5M1wv (claude/p5-fix1), FX2 session_01JRCSTi6r1qQ51mTgwgJ7es (claude/p5-fix2), FX3 session_01UZWrZRivwQJPKL3x7c8Ft9 (claude/p5-fix3). AR1 session_01XcfcbFvi4nMVUPZgT2BcmE owns the arrows plan page and `arrows_check.py` (claude/arrows-plan); AC1 combines on claude/arrows-c.

## What I wrote

- `plans/arrows-p5-step2-notes.md`: Step 2 (junior days) played: BROKEN list, each mechanic's inventory and arrow chain, open questions for the user.
- `plans/arrows-p5-step2-section.html`: the same for AR1's page (moments M1a...; a comment maps them onto AR1's lines).
- `plans/backlog.md` rows AR2-1, AR2-2 (both since fixed by FX3).
- `plans/review-fx2.md`: every review verdict, its tests, merge notes. Read this first.

## Verdicts (all in plans/review-fx2.md)

| Work | Verdict |
| --- | --- |
| FX2 e10d81a4 (drill) | fixes needed (A1), then FX2 cc2bb2be (A1, scan first, the watch job, wording): PASS |
| FX2 191d1853 (eating at any seat) | PASS |
| FX3 e6bcf827, 360801c0, 02e212f1 (hauling any day, per-stop words, own arrow, galley plant, put-back, lift panel) | PASS each |
| FX1 a34f4666 (lifecycle) | PASS on its items |
| AC1 90992e66 (the watch-step arrow, arrows-c 86a980c5) | PASS with the queue off (every lesson Days 2-5 learned by the arrow); queue on: the 'do' step lapses (AC2's 6610dc7, RV7's) and "Trained: rounds" toasted twice |
| FX3 8aae0634 (bunk arrow, holds' pin, job parked at the pipe, Calder labels) and the lift patch alone on b9f053ba | PASS both |

**Open:** (1) the watch-step blocker is fixed by AC1 (above); the 'do' step with the queue on is AC2's 6610dc7 (RV7). (2) Merge: FX2's 14:50 drill line must win over FX1's (FX1 agreed; AC2 has the notes). (3) The laundry pin (a tap at `4-laundry-1` hits Washer 1 and starts your own load): FX3's next. (4) arrows_check week's "stuck at Take your first round" (Days 3, 8): by hand the board offers the round and Take it works; AR1 to look at the follower.

## How I test

- Scratch: `$SCRATCH/rv` (build copies: base.html = 2b4a05db, fx*.html tips; check files copied with `open('cadet_test.py')` in place of the `__file__.replace` line; q_*.sh run lists) and `$SCRATCH/probe` (my bot). Not in the repo.
- Setup: `mkdir -p /tmp/cadet-work/three && cd /tmp/cadet-work/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz`; `pip install playwright numpy pillow`; `export CADET_CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome`.
- The bot (`probe/bot.js`, `botA.js` plain, `botB.js` drops a job for a training, `botC.js` looks over first; `run.py D0 D1 OUT.json "setup js"`, env GAME=..., BOTJS=..., SETUP2=... runs after the skip to D0 05:00): follows only the arrow (teleports there), taps what it names, uses the board, reads meetings, uses Tracked 10 minutes before a training. About 40 s a ship day with drawing switched off (`window.__skip = true`). `show.py LOG.json` prints the log without noise.
- Per fix: its own check part on base (must FAIL) and tip (OK); cadet_test base -> tip alone (the `a_start` first-frame bubble flake comes and goes: rerun); arrows_check week (~12 min); honest play; a trial merge with the other fixers.

## Gotchas

- Notifications only arrive between turns; read them with ReadNotifications.
- `pkill` by a pattern in your own command line kills your shell.
- A goal tagged `trk` (FX1) is cleared by trkDoneCheck when you arrive in its room: don't put one on an arrow that another section moves on (the drill).
