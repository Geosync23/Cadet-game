# Handover: lead 44 (draft, kept current)

## START HERE (next lead)
Read CLAUDE.md, this note, then the bottom of TEAM.md on **claude/lead-44** from "LEAD 44 started", then plans/roadmap-1.0.md
(the user's road to 1.0 and all their Oct 28 decisions). Lead 44 = session_01GKuymj3tKpX7xwDZwBh8RM; hourly check-in
trig_01EEPqBFzhAHmVbvZKyhHXWs (57 * * * *): make your own (copy its prompt) and tell lead 44 its id so it disables its own.

## State (~02:00 UTC Oct 29 = 10 PM ET Oct 28)
- 0.97.0 LIVE (Playtest 7hQ1 v4, Dev KEya v4). claude/integration = claude/staging-pad = 610ad7f1. Never publish over 6daN.
- 0.98 (game speed on phones): RB1 render turns 3-4 (pixel-identical or picture to the user first); OP1 walk-estimate fix
  (sec 14 take(): tradition walks >= 6 min booked; FX24-2 + FX12-1; TQ1-1 closed not reproduced); SD3 SD3-2 music cache.
  Turns 1 (shader checks) dropped, 2 (shadow stand-ins) parked. No 60 fps cap, no battery saver. Backlog 12 -> 0.99.
- 0.99: balance (user's answers on the balance report pending) + 26 backlog fixes (BB1 on claude/backlog-triage) + title
  screen B (TS1's plan; no Credits; a music track; 3 small questions parked in the roadmap).
- 1.0: the user's own playthrough notes (they do the whole-game real-phone run + controller test themselves).
- ETA given to the user: 0.98 OK Thu Oct 29 morning ET; 0.99 OK Fri Oct 30 morning ET. The user wants a fast pace.

## Rules today
Cap 5 working. Day/evening: push notifications for questions and milestones. Pages that collect answers: check they save
(the backlog page lost answers once: fixed with autosave). Times in Eastern. No emojis. Plain words.

## Gotchas
- perf_check is noisy (run spread 1-2 ms; order effects); never bisect on single cross-container runs; it never starts sound
  (?nosave&debug) and never measures three.js draw time (OP1 found the real cost there).
- Builders created by the lead can only push their own outcome branch: fast-forward trunks yourself (git push origin X:refs/heads/Y).
- Container restarts kill background runs: long checks detached with nohup, no time limits.
