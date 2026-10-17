# Handover: Pillar 5 designer (puzzles)

- **Role:** design only, no game code. Reports to the lead (named at the top of TEAM.md; at the time of writing session_01KPJMYjXAPkNUcrQ8VRkhLE).
- **Branch:** `claude/pillar5-plan`.
- **What I own and built (2026-10-17):** Part 6 of `plans/pillar5-plan.md` ("Added: deductive repair puzzles", the head-scratchers), the "Added: puzzles" section of `plans/pillar5-plan.html` (plus small pointers: header, rule 3, risks, questions 8-16), `plans/pillar5-puzzles-mockup.html` (three phone screens) and `plans/shots/p5-puzzle-{when,line,rig}.png`, and the user's ask recorded in `plans/pillar5-notes.md`.
- **The user's rule for this work:** keep the whole existing plan; add, never remove or shrink.
- **Status:** waiting for the user's answers to questions 8-16. Nothing is built. design-doc.md is unchanged on purpose: on approval, its "Work is physical" ground rule, the job loop's "Diagnose" step and the Works progression's tools list get a line each (in the same commit as the first work that depends on them).
- **Next, if approved:** in Step 1, a spec page for the case engine and for P3 and P1 (`plans/mechanics/<id>.html`, in the style of `plans/pillar5-plan.html`), then the fault tables' causes in plain words per machine kind (Tier 1 kinds first).
- **Mock-up shots:** re-made with `NODE_PATH=$(npm root -g) node shot.js` (a short Playwright script screenshotting `#m1`, `#m2`, `#m3` of the mock-up page at 2x; Chromium at `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`).
- **Gotchas:** hash keys 880-894 are a suggestion inside Pillar 5's 850-899 (F4 hands keys out); the build ranges 0.55.x/0.56.x for the new seats are not yet confirmed free by the build master. Crew names used: Calder (she), Zeke Torres, Brennan (she), Tomas, Pell, Rina, Yara Esposito; the machine shop tech and the laundry hand are unnamed.
