# Handover: TR1, ship traditions reviewer

- **Role:** review only (the user: "a reviewer whose sole task it is to analyze ship traditions, especially their
  starts and triggers"). Lead 47, session_014zyJYM4mt9ZDCD5H9JZDtN. I don't change the game; a traditions builder fixes.
- **Session:** session_014zyJYMx26ZwoJgqt2dLUYL. **Branch:** claude/p995-tr1 (from claude/staging-0994 8976965e, game
  a01d1a4c...bc4a). Only `plans/review-tr1-traditions.md`, `plans/tr1-probes/`, this note.
- **Done (2026-10-31):** the findings page (every tradition, ranked, causes with lines, fixes, the user's open
  questions); reports to the lead: Spice (note 19), notes 8, 10, 16, the full summary.

## Probes (plans/tr1-probes/, each runs on any build: `python3 plans/tr1-probes/X.py BUILD.html`)
- `sweep.py BUILD SHARD NSHARDS [ids]`: one visit per tradition (env `TR1_DAYS=36-365` for the later ones); JSON lines.
  `sweep_read.py` makes one line each; `table.py` the page's table (the verdicts are a dict in it).
- `spice_probe.py BUILD [days]`, `tea_probe.py BUILD [day]`, `beam_probe.py BUILD`, `inventory.py BUILD [N]`,
  `followups.py` (overlapping joinable traditions, Saruth, film), `followups2.py` (rec-wso, quiet watch), `calendar.py`.
- Raw results of the base in `results/`.

## Gotchas
- Setup: `pip install playwright==1.63.0 numpy pillow`, three r128 in /tmp/cadet-work/three, `CADET_CHROME=/opt/pw-browsers/chromium`.
- The probes exec cadet_test.py's top half: never name a variable `HOOK` (it replaces the game's eval hook: "game failed
  to start"). They lift the load timeout to 240 s (4 cores: two browsers at once are slow).
- `pgrep -f name` in a wait loop matches the loop itself; use `ps aux | grep "[t]r1-probes/..."`.
- `skipTo` from Day 0 runs the days in between (flags such as rec.filmMoved get set: Film night on Day 6 becomes the
  rec deck's after a skip); a skip also ends your own activity.
- Some speakers are drawn through `a.h` (birthday): count bubbles by text, not by `who.p`.
- Saruth is posted aboard all game (not a bug).

## Next, if asked
- Re-probe the traditions builder's branch: `spice_probe.py` (star from 18:15, the tap, Brennan stays at the shelf, the
  card), `sweep.py` on the changed ids, `followups.py` part (a) (no hidden stars), `tea_probe.py`, `beam_probe.py`.
