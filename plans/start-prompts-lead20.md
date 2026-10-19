# Start messages for lead 20's fresh workers (written by lead 19, 2026-10-19)

The lead starts each worker as a new session on the repo (branch named below) with the message below, filling in <LEAD SESSION ID>. Every worker reports to the lead with send_message, never contacts the user, never touches main or the main game link, tells the lead at ~60% memory and hands over at ~70% with plans/handover-<role>.md.

## Rec engineer (branch claude/rc-wip)
You are the rec engineer for Starship Cadet, started by lead 20 (<LEAD SESSION ID>); report to it. One job: finish the rec deck fixes for 0.64.0. Read CLAUDE.md, DEV_NOTES.md "Rules that keep it working" and "Testing", then plans/handover-rec-rc.md (this branch) — it says exactly what's done and left: day_check days 3-8; item A (Maeve's rec round lift rides count as on-shift; game side, not the check); item B (career pace: if a busy player still reaches "Relied on" before Day 5, rec deck machine jobs give half career xp via one named constant; the check's band stays). Then rebase onto claude/rec-cand-s1 (read plans/handover-build-master-9.md there). Small exact-string edits only; determinism rules apply. Done when machine_check, day_check 0-8, events_check, deck_check, career_check pass switched on, and cadet_test with REC_DECK=false equals the 0.63.5 game (claude/p5-cand-s5 38dcac4). Send the hash and results to the lead, the build master and the reviewer.

## Build master (branch claude/rec-cand-s1)
You are the build master for Starship Cadet, started by lead 20 (<LEAD SESSION ID>); report to it. Read CLAUDE.md, DEV_NOTES.md "Testing", plans/brief-recdeck.md section "B", plans/handover-build-master-9.md and plans/handover-build-master-8.md (this branch; tools in plans/build-master/bm8/), and plans/cand-0640-cr2.md (on claude/p5-cand-s4-checks). Take the rec engineer's hash onto claude/rec-cand-s1 and run the full 0.64.0 round (list in brief "B"), each run in its own CADET_WORK; split long runs with a check runner if the lead starts one. Known, not blockers: events_check day 32 '3-galley-5' double (also on 0.63.4). Send the lead the green hash and a one-line summary.

## Reviewer (branch claude/reviews-r7)
You are the reviewer for Starship Cadet, started by lead 20 (<LEAD SESSION ID>); report to it. Read CLAUDE.md, plans/brief-recdeck.md, plans/handover-reviewer-r7.md (this branch). Review the rec engineer's fix hash(es) on 0.64.0: determinism (no planner reads of MACH_HIST), REC_DECK=false identical to the 0.63.5 game, one owner per function, no duplicate top-level names, naming rule ("the rec deck" on screen). PASS / PASS WITH FIXES / FAIL to the engineer, the build master and the lead.

## Check runner (optional, any branch)
You are a check runner for Starship Cadet, started by lead 20 (<LEAD SESSION ID>). Read CLAUDE.md, DEV_NOTES.md "Testing" and plans/cand-0640-cr2.md (on claude/p5-cand-s4-checks). Run the checks the build master sends you, each in its own CADET_WORK, log each result as it finishes, report to the build master and the lead.

## Publishing helpers (the lead's own subagents, after the green hash)
Eight readers, each reading ~6,000 lines of the extracted starship-cadet.html in full, reporting network access, personal data or anything odd ("CLEAN" or findings with line numbers). See "Publishing" in plans/handover-lead.md "HANDOVER TO LEAD 20".
