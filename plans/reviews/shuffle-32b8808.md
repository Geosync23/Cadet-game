# Review: claude/player-needs-shuffle 32b8808 (0.28.70, player engineer 9): walking into people shuffles them aside

Reviewer 1g, 2026-10-18. In-depth review, because it changes behaviour (crew positions, section 10's player push). There's no save change: `SHUFFLE` and `SHUFFLE_SAID` aren't saved and last under a second, or a minute for the polite word. The probes are `shuffle-32b8808-probe.py` (busy play: the player keeps walking into crew, every frame checked) and `shuffle-32b8808-toast-probe.py` (ordinary walking: how often the polite word comes, and a need warning). Run them next to a `cadet_test.py`.

## Verdict: PASS WITH FIXES

The step aside itself is sound. Nobody steps into a wall, a wall edge, furniture or a closed tile, the player never stalls, and crew carry on with their plans. One MEDIUM: the polite word is a full toast, which in a crowd comes in bursts, replaces other toasts and holds back the need warnings. One LOW: a short side-to-side wobble when you follow someone closely.

## Checks (on 32b8808)
| Check | Result |
| --- | --- |
| Busy play, the player walking into the nearest crew on their feet, head-on and from behind (a tapped path 2 tiles past them), every frame, about 5 min each | Deck 3 18:05: 58 walks, 62 steps aside (33 people). Deck 4 21:30: 36 walks, 31 steps (17). Deck 3 07:10: 46 walks, 126 steps (52). **Nobody stepping aside on a closed tile or inside a wall or furniture: 0. Player stalls: 0.** Step sizes only 0.5 and 0.25. No console errors. |
| Ordinary walking across Deck 3 (far tiles, not chasing anyone), about 200 s | 07:15: 8 polite words. **18:10: 20 polite words, three within 0.2 s of each other** (gaps 0.1, 0.0, 0.1 s). |
| A hunger warning due from about 3 s, the same walk | with shuffling: shown at **~32 s (07:15) and ~59 s (18:10)**; a copy with `shuffleable` returning false: ~32 s and **~33 s** |
| cadet_test | not re-run. PE9's result (only i_tap3 differs, a crew member who stepped aside, and a copy with shuffling off ALL IDENTICAL) matches what the change does. |

## MEDIUM 1: the polite word crowds out other toasts and holds back the need warnings
`shuffleTick` calls `toast()` for every person who steps aside, at most once a person a minute. Nothing limits it across people, though, so a busy mess at dinner gives about one every 10 s, in bursts, each replacing the toast before it (a job toast, "Your turn. You take a tray", a warning). `toast()` stamps `TOAST_AT`, and the need warnings wait 5.6 s + `WARN_GAP` (8 s) after any toast, so in the probe the hunger warning at dinner came about 26 s late (59 s against 33 s). The tips wait too (`TEACH_TOAST`). These are the user's warnings (0.28.41).
**Fix (small):** say it only when no toast is up, and at most once every 20-30 s across everyone, for example `if (id && !(at - SHUFFLE_SAID.get(id) < SHUFFLE_SAY) && at - TOAST_AT > 5600 && !(at - SHUFFLE_LAST < 20000))`, setting `SHUFFLE_LAST = at` when it speaks. Better still, a speech bubble or the floating note instead of a toast, which doesn't stamp `TOAST_AT`; that's PE9's call. The step aside itself stays as it is.

## LOW 1: a side-to-side wobble when you follow or meet someone closely
Once a step ends, the person can be stepped aside again the next frame if you're still touching them and they're ahead of you. The probe saw 3 to 7 steps within 3 s for a few people: janssen-hugo stepped +z, −z, +z within 0.4 s (Deck 3, walking to the lift with you behind), and jovanovic-petra and nandakumar likewise. On screen it's a quick wobble. You're never held up, so it's cosmetic.
**Fix:** after a step, leave that person alone for about 1.5 s, or until you're more than `SHUFFLE_NEAR + .3` away (keep a `SHUFFLE_DONE` time per agent next to `SHUFFLE`).

## Notes (no change asked)
- Crew walking up the servery line or the lift queue aren't `settled` between their places, so they're `shuffleable` and can be stepped aside there too. They walk back to their place, so it's harmless.
- With nowhere to step, you pass through them, because the push skips `shuffleable` crew. That's by design (the design doc: "nobody on their feet holds you up").
- No `R()`. `SHUFFLE_SAID` uses `performance.now()` (virtual in tests), and only for the toast.
