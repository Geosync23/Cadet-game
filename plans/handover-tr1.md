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

## Re-probes done (2026-10-31, afternoon)
- **TB3 88db900** and **final 4037a26** (claude/p995-traditions, switch TRAD995_ON): Spice, tea corner (standing spot at
  [23,2], doorway clear), beam, the two-on-one-deck fix (`overlap_probe.py`: before/after on Day 6), the milestones,
  Open door and Off the Tern: all PASS. Rough edge sent to RV30: the Spice guess card left open about a minute loses
  the reveal (the wait is 60 real s; the clock runs under the card). Results: `results/tb3-88db900/`, `results/tb3-4037a26/`.
- **TB4 d41e762** (claude/p995-trad926, switch TRAD926_JOIN_ON): the 0.92.6 eight + window-sketch-2 all PASS my sweep
  (`results/tb4-d41e762/`). Day 73 Card night overlaps the tasting table: covered once TB3's fix is merged. RV29 does
  reload, words, the walk and switch-off identity (split agreed).
- `spice_probe.py` takes `TR1_CARD_STEPS=N` (answer the guess card N steps after the tap).
- The user's page: https://claude.ai/artifact/UfwLXgfSzGx7Eic1iyEfPE (file in my scratchpad: rebuild from
  `Artifact read` if needed). Answers in its database: collection `answers` (q-meals, q-rec, q-promise, q-tea) and
  `comments`; empty at the last read. Question (d) = the lead's call: only the standing spot moves.
- Reviewers: RV30 session_014zyJYNFR7ewWJGvEQNUAHr (TB3), RV29 session_014zyJYM3D7UBkZN49CsZVuA (TB4).
