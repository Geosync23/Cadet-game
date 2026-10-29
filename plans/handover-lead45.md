# Handover: lead 45 -> lead 46

## START HERE (next lead)
Read CLAUDE.md, this note, plans/roadmap-1.0.md on claude/lead-44 (the user's road to 1.0), then the bottom of TEAM.md on
claude/lead-45 from "LEAD 45 started". Lead 45 = session_01GKuymnu4NeXJhwPe21FWk7 (64% memory at 12:55 UTC Oct 29 =
8:55 AM ET). The user starts lead 46 from claude.ai (session chain depth was 4 of 8). Lead 45's hourly check-in is
trig_016UAJtPjwFezry8dEDiEpBK (53 * * * *): make your own (copy its prompt, renamed), tell lead 45 its id; lead 45 disables
its own. Then tell every active seat you are the lead (one line each, priority "next").

## State at handover
- **0.98.0 LIVE since 8:30 AM ET Oct 29**: Playtest https://claude.ai/artifact/7hQ14AcwZHCi5EvL1AKiMU v5, Dev
  https://claude.ai/artifact/KEyaHvon6ZaVHHFRdAe18m v5. claude/integration = 37b858b4 (= claude/staging-098d; game sha256
  81c07a05...59b1): SD3-2 music cache + OP1 walk-time fix (FX24-2/FX12-1) + join_check 120 s + check fixes (s5cases,
  puzzle p6) + backlog BM20-1. NO RB1 turn 3 (moved to 0.99). NEVER publish over 6daN (the user's save link).
  claude/staging-pad = ba042cf3 (has RB1 turn 3; left as is, merged into staging-099).
- **0.99 (BM21 session_01GKuymkAoLNTFXef9RgiYLn owns claude/staging-099)**: pushed 37346acf; local d0bcfb86 pending its
  checks (= + BAL2 words 6eacbe10 + SD3 title track C febdf8ab + 098d docs). Contents: SD3-1 room B chime, EV2 seated
  formal dinner + vessel words, BB1 26 backlog fixes, TB1 title screen B switched ON with music C (user approved both),
  OP1 nights day-arrow fix (BM20-1 fixed), BAL2 balance (four needs numbers + Friday same-day promotion result kept,
  user's pick: slow players Engine Specialist Day 26/27, steady 23), RB1 turn 3 (one draw per body).
  Still to merge, both via RV26 PASS: (1) RB1 222ec28 controller_check.py only (bunk-ring FAIL = real-time toast race,
  proved OK on 8d7a314); (2) RB1 turn 4 (furniture colours merged; USER APPROVED the corner-pixel changes; cadet differences
  expected = those reviewed pixels only). Then: 0.99.0 build turn (header/GAME_BUILD, build table, DEV_NOTES, backlog
  closes), full round in 5 shares (plans/round-0970.md pattern; OLD = 0.98.0 37b858b4), user OK, PUB2 publishes over
  7hQ1 + KEya, lead fast-forwards claude/integration. ETA told the user: 0.99 OK ~4-6 PM ET today if the round is clean.
- All user questions for 0.99 are answered. Title preview (for reference): https://claude.ai/artifact/GLSzgGfn55Kk9LFCaoGevR.
  Title music page (pick C saved): https://claude.ai/artifact/XwWvqkL7EdMouqrJ3cRHYm.
- After 0.99: 1.0 = the user's own playthrough notes only (roadmap).

## Seats
Working: BM21 (0.99 build master, ~13%), RV26 session_01GKuymjwVsweGh8p9EbTGHU (reviewer, ~49%), RB1
session_01GKuymkqMpME5GQvc5vTBqR (turn 4 + 222ec28, ~33%).
Ready runners for the 0.99 round: R1 AS1 session_01GKuymmdgtDvbd8P7URXd4z, R2 session_01GKuymmiqCTVdUwF2rf5qBM,
R3 DM2 session_01GKuymoBtAFGaak9qYYXS24 (controller + devmode); hire a fresh R4 (BB1 handed over).
Idle, can answer questions: PUB2 session_01GKuymkDxLVyt4rjtcJxdab (publisher), BAL2 session_01GKuymm7ApobKpq9JW9FJgF,
SD3 session_01GKuymir9eBj7X6kLtwLRmq (~50%), TB1 session_01GKuymo2ikX7y7GA88GPXQP, EV2 session_01GKuymn7YSDpEbeNYGxup6N.
Handed over (notes pushed, don't reuse for big work): BM20 (handover-bm20), RV25 (handover-rv25), OP1 (handover-op1),
BB1 (handover-bb1), EV1.

## Gotchas learned
- *.png is in .gitignore: builders must git add -f screenshots.
- A planner change (walk timing) moves machine wear, so which case/fault happens on a day changes; checks that hardcode a
  day's machine or case break. Fix the check, not the game. Run case + arrows checks before merging planner changes.
- Render speed-ups change real-time frame pace; checks that race real-time timers (toasts 5.6 s) can flake. Clear the
  timer in the check (DEV_NOTES "Real time in a check").
- join_check reload ~28.5 s on busy boxes (now 120 s). Max two browsers per container; perf_check alone.
- Seats misreport memory; check get_session context_usage yourself.
- Don't switch a worktree's checkout while a check runs in it.

## Backlog notes from today
BM20-1 (fixed in 0.99), EV2-1 (Dev mode formal dinner jump label stale), RV26 note: whole-day-off Day 22 gets the sleep
arrow from 05:30 (p5nDayBed rule, OP1's call), two water-line head-scratchers can be open at once (pre-existing),
BAL2 notes: Saturday badge kept.
