# Handover: lead 44 -> lead 45

## START HERE (next lead)
Read CLAUDE.md, this note, then plans/roadmap-1.0.md on **claude/lead-44** (the user's road to 1.0 and ALL their Oct 28
decisions), then the bottom of TEAM.md on claude/lead-44 from "LEAD 44 started". Lead 44 = session_01GKuymj3tKpX7xwDZwBh8RM
(~68% memory at handover, 02:15 UTC Oct 29 = 10:15 PM ET Oct 28). Lead 44's hourly check-in trig_01EEPqBFzhAHmVbvZKyhHXWs
(57 * * * *): make your own (copy its prompt, renamed lead 45) and tell lead 44 its id so it disables its own.

## The user said (10:20 PM ET): "You now have everything you need to bring this project to the edge of 1.0."
Drive 0.98 and 0.99 to done. 1.0 = the user's own playthrough notes. They want a FAST pace (they found the earlier ETAs too slow).
ETAs given: 0.98 ready for their OK Thu Oct 29 morning ET; 0.99 Fri Oct 30 morning ET.

## State
- 0.97.0 LIVE: Playtest https://claude.ai/artifact/7hQ14AcwZHCi5EvL1AKiMU v4, Dev https://claude.ai/artifact/KEyaHvon6ZaVHHFRdAe18m v4.
  claude/integration = claude/staging-pad = 610ad7f1 (game 0bd1b5b6...b36f). NEVER publish over 6daN (the user's save link).
- 0.98 (game speed on phones):
  - RB1 session_01GKuymkqMpME5GQvc5vTBqR, claude/opt-098-render: turn 3 one draw per full body, turn 4 colour-only furniture
    materials merged. Pixel-identical or a before/after/difference picture to the user FIRST; only incredibly minor changes, with their OK.
  - OP1 session_01GKuymkG9JWDcSK9pMb28aj, claude/opt-098-plan: walk-estimate fix (sec 14 take(): tradition walks >= 6 min booked;
    FX24-2 + FX12-1; TQ1-1 closed "not seen on 0.96.0"; Deck 4 piano crowding -> backlog). Checks running at handover.
  - SD3 session_01GKuymir9eBj7X6kLtwLRmq: SD3-2 music cache 0b9541c9 on claude/sound-098 = RV25 PASS. Now SD3-1 (room B chime) on claude/sound-099 (0.99).
  - Turn 1 dropped (noise), turn 2 parked, no 60 fps cap, no battery saver.
  - Then BM20 builds the 0.98 candidate (merges RB1 + OP1 + sound-098), build turn 0.98.0, full round in 5 shares
    (plans/round-0970.md pattern; hire fresh runners), then the user's OK, PUB2 publishes, fast-forward integration.
- 0.99 (balance + backlog + title):
  - BAL2 session_01GKuymm7ApobKpq9JW9FJgF, claude/balance-099: sends a table of proposed numbers FIRST -> show the user -> build.
    Decisions: f1 dynamic promotion + much sooner retest; f4/f5/f6 try; social a little more pressure (not a lot); backlog 12 =
    check-expectation fix (calendar pacing kept); the rest keep.
  - BB1 (= BT1) session_01GKuymne2zVMSTZjvCCmXKH, claude/backlog-triage (restarted from 610ad7f1): the 26 backlog fixes
    (plans/backlog-1.0-final.md on that branch), A items first. Leaves V-1/V-2 to the events side, SD3-1 to SD3.
  - Title screen B (crew terminal): plan plans/title-screen-plan.md on claude/title-screen-plan (TS1, archived). No Credits. A music
    track (sound seat makes 2-3 candidates, the user picks). Hire a builder when a seat frees. 3 small questions parked in the roadmap.
  - Events side: V-1 seated formal dinner (no Dev jump needed), V-2 Veyli vessel nod to the visit -> EV1 session_01GKuymmJANJaZkFuhsM9bBt (idle, ~52%).
- Reviewer RV25 session_01GKuymnnpKvNH4Ki69KEzwG (~30%): reviews everything. BM20 session_01GKuymiwDEgkwGmjJ2nokvg (~35%): merges,
  build turns, reach detached on fe11cd66 (no FAIL so far; non-blocking). PUB2 session_01GKuymkDxLVyt4rjtcJxdab publishes only on the user's OK.
- Idle: AS1 session_01GKuymmdgtDvbd8P7URXd4z (good runner), DM2 session_01GKuymoBtAFGaak9qYYXS24 (Dev mode done; good runner).

## Rules
Cap 5 seats actively working (the user). Push notifications for questions and milestones. Times in Eastern. No emojis. Plain words.
Pages that collect answers: check the answers really saved (the backlog page lost them once; fixed with autosave).

## Gotchas
- perf_check is noisy (run spread 1-2 ms; order effects); a perf FAIL = re-measure alone twice; never bisect on single
  cross-container runs. It never starts sound and never measures three.js draw time.
- Builders hired by the lead can only push their own outcome branch: fast-forward trunks yourself (git push origin X:refs/heads/Y).
- Container restarts kill background runs: long checks detached (nohup), no time limits.
- The visit changed a few check assumptions (lamp shelf, p9 clash day, Envoy name): expect event-day ripples in checks.

## Backlog notes from today (not on the user's 1.0 list unless noted)
EV1-1 (double reputation toast; in 0.99 list), DM2-1 (End and keep; dropped), Deck 4 piano crowding (new), DM1-5 (dropped).

## Session chain depth (the user asked, Oct 28 10:20 PM ET)
Lead 44 is depth 3 of a limit of 8; lead 45 is depth 4, its helpers depth 5. Each lead-to-lead handover adds one level.
At lead 45's handover: ask the USER to start lead 46 themselves from claude.ai (short prompt pointing at plans/handover-lead45.md),
which resets the chain to depth 1. Don't create lead 46 from lead 45.
