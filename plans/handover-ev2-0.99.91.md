# Handover: EV2, 0.99.91 Sim night in week 1 (2026-11-10, for lead 51)

Role: EV2, events builder for lead 51 (session_01GKuymjp49y3M5hgRLecobm). Reviewer RV36 (session_01GKuymoG8txh1cPvipXz8BW): **PASS** on game 46abc462e68794e0edb15645b3d02251452e45c1dfac6a1e1bed986872779fdd. BM28 merges 6f15a1f. The earlier EV2 notes (events base, storm, visit dinner) are in their own handovers.

## Branch and builds
- `claude/p9991-flightsim` from main bfbcbdf (0.99.9, game 583d99ba...bd16). Commits: 1c46077 (game + words), 6625e41 (records, probe), 23a1085 (phone shots), 6f15a1f (build-table row), f83a19b (DEV_NOTES wording from RV36), then the backlog rows and this note (docs only).
- Switch `EV9991_SIM_ON` (a `var`, Events engineer 2 slot), off on the branch. The build master switches it on. Build-number lines untouched.

## What I built (the user: "Need a flight sim ship tradition week 1 sometime"; EV1's plan)
- Sim night (rec-sim-night) gets a first showing on Wed Day 3, 19:30-20:30: `SIM_NIGHT.when` becomes an any-rhythm alongside its every-other-Thursday run. Plans are cleared after.
- First-time words on Day 3 (content/banks/ev9991-sim.lines): the Mail (in the Wren's evening-before digest, so it has no "I"), ask, here, thanks, and Dev's opener card `join.rec-sim-night.open`.
- Join any sim night: `TRAD_JOIN['rec-sim-night']` (host raman, rec 'sim'), hooked in tradJoin -> `ev9991SimJoin` -> recStart('sim').
- Both pods taken: `ev9991SimGive` has the pilot nearest Dev give you their turn; `EV9991_GIVE` (read via a hook in tradWhere) keeps them off the pod until your run ends. Not saved.
- Details: DEV_NOTES "Sim night in week 1"; design-doc (the first week's traditions).

## Tests (all passed)
Off: cadet_test vs 0.99.9 ALL IDENTICAL; check_fast OK. On (a copy): events_check, day_check 3, weekend_check, devmode_check trad, bigevents_check, and check_fast's parts (deck, machine, leave, device, names) all OK. Probe: `python3 plans/ev2-probes/simprobe.py ON.html [SHOT-PREFIX]`. Shots: plans/ev2-probes/shots/.
Switch-on copy: `sed 's/^var EV9991_SIM_ON = false;/var EV9991_SIM_ON = true; /'` (check with grep -c that it changed).

## Loose ends
- Backlog EV2-2 (four toasts in a row at the hand-over) and EV2-3 (the yielding pilot stands by the full bench): RV36's polish notes, parked by lead 51. (EV2-1 was already an older row, so these start at 2.)

## Gotchas
- *.png is gitignored: use git add -f.
- check_fast tests only the main file, so run its parts on a switched-on copy yourself.
- CADET_CHROME=/opt/pw-browsers/chromium must be set on every command (the shell profile can't be edited here). names_check needs acorn in $CADET_WORK/acorn.
- Crew sim pilots hold both pods for the whole hour on a busy sim night, so without the hand-over the player would wait on the bench all hour.

## Open questions for the user
None.
