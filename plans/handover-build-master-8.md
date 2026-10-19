# Handover: build master 8 (BM8, session_01YGy9FDmcbkySMJpVPYJaAo)

**Role:** combine the seats' reviewed tips into one candidate, run the checks (half with check runner CR2, session_018xWmWkrtNWudZUgXygkW1u), send failures back with evidence, give the lead the green hash. **Lead:** lead 19, session_01FsGspstkG61e9AWadSi36y (reports to it only). **Reviewer:** R7, session_01HCwvy5w432bhz41UYxHYwq (notes claude/reviews-r7). **Scope (lead 19, the user up ~11:45):** finish 0.63.5, then the rec deck combine 0.64.0, then STOP (no ion storm, nothing after).

## Builds
- **0.63.4 final = `claude/p5-cand-s4` aa4f42c** (published by lead 18; game = 92d40d5). Done.
- **0.63.5 = `claude/p5-cand-s5`**: 4e0c385 (my mech_check fix) → 1e70683 (+ crew-pt1 79959ff) → ee9f9ed (+ X3 0.71.7 6a4e153) → 041c473 (+ X3 84fb217, player_check only) → be3d7ee (DEV_NOTES row, mech_check fragility note, plans/cand-0635-results.md). All checks OK except the final player re-run (see loose ends). Game file of be3d7ee = ee9f9ed's.
- **0.64.0 = `claude/rec-cand-s1` 3add6bf** = be3d7ee + RB2 f319ab3 + RA 9dfe971 (0.83.3 = 0.83.2 + RB2's REC_SHOW_CUE/recShowCue rename) + W3 a095799 + RB2 87e3c5f (rec-works' last: 0.84.11 switch REC_DECK = true, 0.84.12 climb fix, two interactions_check fixes). Order and every verdict: the rec queue notes below.

## Tools (container setup)
`pip install playwright`; three r128 in /tmp/cadet-work/three (`npm pack three@0.128.0`); `ln -sfn <scratchpad>/cw /tmp/cw`; BM7's plans/build-master/* into /tmp/cw/bm; mk.sh / q3.sh / teach.py from plans/build-master/bm7 (q3.sh: `WT=<worktree> [OLD=..] [TMO=..] q3.sh HTML TAG check...`, one line per check in /tmp/cw/logs/summary.txt, own CADET_WORK per tag). mk5.sh = mk.sh with BASE/BUILD env. The 0.64.0 resolver: plans/build-master/bm8/rec64.py (copy in this branch).
- **Gotcha:** never `pkill -f` / `pgrep -f` a pattern that also appears in your own command line: it kills your own shell (exit 144). Use `ps aux | grep "[p]layer_check"`.
- **Gotcha:** a `nohup ... &` run died silently once (player, ~12:00, log stopped, no summary line): for long runs use the Bash tool's background mode and check the summary line exists.

## 0.64.0 hand merges (rec64.py; for R7 to see)
1. bd3db3f7/9dfe971 × rec-works, 3 conflicts: REC_MACHINES block vs REC_CREW_PLACES block (keep both), the -svc push vs DECKS[7].gathers (keep both), recTap's Lightdisc court lines: RB2's `recShut().court` refusal first, then RA's Cup/WSO line and RA's recQueue+discAsk(recCourtWaiting()) line (drop rec-works' plain discAsk line).
2. 87e3c5f, 1 conflict, the climbing wall: RA's r0 → free-belay r pick, then RB2's z line with `, sh = recShut()` and its two refusal lines on that r.
- verify_merge: 5 'missing' under f319ab3 = lines RB2 rewrote in later commits (REC_SHOW, REC_OK, the belays line, SYMPTOM_TEXT, the mic stand wrapped in `const ms =`): explained.

## Loose ends
- 0.63.5: player_check on be3d7ee's game re-running (tag s5g, WT=/tmp/cw/wt7, TMO 2700). X3 got PLAYER CHECK OK on the same game + the same player_check. When OK: add the line to plans/cand-0635-results.md, `git push -u origin claude/p5-cand-s5`, send lead 19 the hash (be3d7ee or the results commit on top).
- 0.64.0 round (started ~12:50): mine tag r64 (cadet vs 0.63.5 s5b.html, deck, machine, device, lines, mech, career, disc, interactions) then player; CR2 the rest (day 0-8, 14, 21, 28, events, intro, join, food, clothes, smoke, newgame, leave, bubble, tiles, path, arc). Expected: cadet differs (the rec deck switched on: the lift's R, the deck directory, "Seven decks" texts); explain, don't fail on that. Known pre-existing: events_check day 32 '3-galley-5' double (also on 0.63.4; outside the default 28 days).
- R7 still owes RA 0.83.2's content verdict and a look at the two hand merges on 3add6bf.
- Then: DEV_NOTES 0.64.0 row (pieces, hand merges, results), plans/cand-0640-results.md, push claude/rec-cand-s1, green hash to lead 19 (the lead publishes it as a NEW artifact "Starship Cadet Rec Deck"). Then stop.
