# Handover: lead 23

Lead session session_01XXiKm9iPgm565SZ4n1knmU, branch `claude/lead-23` (push only there; started from claude/lead-22). Took over from lead 22 at 05:13 UTC 2026-10-21. Hourly check-in: trig_014tZ4QHeyDbh7qhmpbd1s76 (minute 20): a successor disables it and makes its own. Read CLAUDE.md, this note, TEAM.md (bottom = newest), plans/overnight-decisions-lead22.md (all overnight calls, leads 22 + 23), plans/handover-lead22.md, plans/handover-lead21.md + plans/handover-lead20.md (standing rules, links), plans/roadmap-after-recdeck.md (newest sections).

## Standing rules (unchanged)
- Handover at 500k (warn the user, by day) / 600k (hand over) for every seat, the lead too. Notify the user only by day: published build / decision / results. "Identity verification is required" on any seat → tell the user at once. Every published plan page has answer + comment boxes. Cut things parked, never deleted. Main and the main game link untouched without the user's go. Overnight: max 5 working seats; recommended answers, logged.
- Helpers never set the build lines (the build master does); they name each turn in the build-table row.
- The test machines have 4 cores: one browser check at a time; a reviewer takes ~25-40 min a turn.

## Publishing recipes (scratch files are in lead 23's scratchpad, not available to a successor)
- **Patch/game page:** `git show origin/claude/integration:starship-cadet.html`, change the `<title>` to "Starship Cadet Playtest X", scan it (no fetch/XHR/WebSocket/eval/iframe; only cdnjs three.js), publish as a NEW page (icon game).
- **Dev page** https://claude.ai/artifact/EWB21cTQnXc8ZT71zCeEzf: the integration file with, right after `<meta charset="utf-8">`, the first-line script `<script>/* published Dev page: Dev mode always on (not in the repo) */try{if(!location.hash.slice(1).split(".").some(t=>(t.includes("-")?t.slice(0,t.indexOf("-")):t)==="dev"))history.replaceState(null,"",location.pathname+location.search+"#dev");}catch(e){}</script>` and title "Starship Cadet Dev". Read the URL first (action read) before republishing to it.
- **Plan pages with answers:** the planner writes `form#answers` with `div.q[data-qid]`, radios name=qid, textareas `qid-comment`, `#savebtn`. The lead adds `data-collection="answers" data-doc="<doc>" onsubmit="return false"` to the form, a `<p id="savestate"></p>` after the button, and the save script (copy the second `<script>` block at the end of any published plan page, e.g. read https://claude.ai/artifact/LK2gXYXbnTqRhjt7k28Q5N with path index.html), then publishes with capabilities `{db:{}, user:{}}`. Answers: ArtifactData list collection `answers`.

## Pages and builds published by lead 23
- **Playtest 0.64.7** https://claude.ai/artifact/82sEvZTAtj1ezCuv6iAAad (claude/integration 6ea5acf: patch-a + patch-b + cocoa names + LADDER/MUG/FLC on). The user's build to play.
- **Dev page** v2 = 0.64.7, v3 = **0.64.8** (claude/integration 0ca6a58 = 0.64.7 + events base + bigevents check, every event switch off; plays the same as 0.64.7).
- **Optimization plan** https://claude.ai/artifact/LK2gXYXbnTqRhjt7k28Q5N (claude/opt-plan acadf6e, OP1, ER2 PASS round 2; db answers/opt-plan, opt-q1..q8 + opt-general). Unanswered: for the user in the morning.

## State (keep current; see FINAL STATE when handing over)
- **Ion storm:** S1-S9 built on claude/storm-update f32d901 (EV4; S4/S8 by EV2). ER2's adversarial build review of f32d901 in progress. PR4 turn reviews: S1, S3-S7 (with fixes, folded), S4 PASS; S8, b9aa775, props 96bb2c6 (4d + 8b stand-in), f32d901 queued. S10 (switch on) after ER2 PASS + PR4. S2 (Captain/Vance off the double shift for the Day 12 address: Marrow 15:30, Vance 15:45 to 16:50) after Fridays reaches claude/integration.
- **Fridays:** FR2 on claude/fridays, turns 1-7 built (turn 7 86d0c80); reviewer PR5 (turns 5-fix, 6, 7 on); PB owner-reviews s13/14/10 (all OK so far). Turns 8-10 left. FR2 ~440k: handover note at 500k → a fresh FR3.
- **Build master:** BM11 handed over (plans/handover-build-master.md, claude/integration 3a48846). Start a fresh BM12 from that note when Fridays is ready to merge (then the storm).
- **Crossing the Line:** not started. Plan decided (claude/event-plan-line ee590ed; lines on claude/events-lines-2). Needs a builder (L1-L6 behind EV_LINE_ON, after the storm update) + a turn reviewer + ER2 build review.
- **Optimization pass:** plan published; team of 4 + the build master after the events (test-speed, render, game code, reviewer); TS1's notes on claude/test-speed bd7d61f.

## Seats (lead 23)
Working: EV4 session_01MqpjPG6mDFe5avrDxcNWTU (storm builder, ~420k, handover plans/handover-storm-builder-2.md) · FR2 session_019m7hCEtBsPA3ascA2Bqu9V (Fridays) · PR4 session_014WyaZtasY32m5fnkBxuR9d (storm reviewer, ~410k) · PR5 session_01Eh4drBZjJ82DjYx6XaTt1F (Fridays reviewer) · ER2 session_01S8pboNujAzZgMSWFK84CxD (adversarial reviewer, ~400k).
On call / idle: EC1 session_01QgShGXD6P24DDxTp8npN41 (bigevents_check owner) · PB session_01FWW2piuXkFYaRRzLXZiqYb (s13/14/10 owner reviews, ~58%) · OP1 session_01RxxLLT9jpvagqJpCW99dop (opt planner, done, ~25%) · EV2 session_017S7eVMgX34nSt8fxZ5kat9 (~440k, S4/S8 fixes only) · EV3, BM11, lead 22 (done).

## Backlog notes from lead 23's shift
- 18b perf_check scenes stand you in the wrong room (6 of 8) → optimization item 0.
- 18c join_check first-light FAIL (old, off too).
- save.fri adds ~790 bytes to the save with SHORT_FRIDAY on (no player-engineer seat).
- "Old placeholder code" in the storm S9 plan: nobody knows what it meant: ask the user.
- With the storm on, other mess meal gatherings' crowd spots get no tray (old rule, PB).

## Morning summary for the user (when they write)
Short and plain: what was built (0.64.7 published; 0.64.8 events base; storm S1-S9 + review; Fridays turns 1-7+; optimization plan), the overnight decisions (plans/overnight-decisions-lead22.md, the lead-23 rows), test results, links to play (0.64.7 page, Dev page), and the open questions (standing diners with trays, opt-plan questions, placeholder code). Then notify.
