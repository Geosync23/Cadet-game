# Handover: lead 20

Written 2026-10-20 ~13:55 UTC, after the user pointed out lead 20 had been auto-summarized without a handover. Kept current from now on: refreshed at 600k memory or before any big task. A fresh lead reads this, then `TEAM.md`, `plans/roadmap-after-recdeck.md`, CLAUDE.md, DEV_NOTES.md.

## Role
Lead session (session_019UJSCUCdtC1kTpYiABWKhs). Starts and briefs helper seats (`create_session` + `send_message`), routes reviews, publishes pages and builds as artifacts, keeps `TEAM.md` current, talks to the user in plain words (new to git; no jargon). Branch: `claude/start-here-review-3qoht9` (push only there). Lead also created `claude/whole-file-0.64.2` (frozen copy) and `claude/integration` (5dd740c, where all seats start and builds merge).

## Standing user rules
- CLAUDE.md "How we work" (one deck/stop at a time then review; plan pages before building; small exact edits; tests; determinism; phones first).
- **Handover before auto-summarizing, every seat.** Helpers tell the lead at 500k of 1,000,000, write `plans/handover-<role>.md` at 600k (or before a job big enough to reach it), push, report, stay idle. The lead warns the user at 500k and hands over at 600k. Check with `get_session` (`context_usage.used_tokens`). The hourly check-in (trig_015zr2FPnqC1CV3XuMfyr35L, minute 9) does this check first.
- Notify (PushNotification) when: a build is published, a decision is needed, results of a test/investigation. Never in overnight mode. "Identity verification is required" on any seat → tell the user at once.
- Every published plan/survey/results page has places to answer and comment (save script: `div.q[data-qid]`, radios named by qid, `<qid>-comment` textareas → db collection `answers`).
- Cut things are parked on record, never deleted. Aim 3-4 working seats, 5 max.
- Overnight mode: no notifications, log calls in `plans/overnight-decisions-lead20.md`; user questions don't end it; the user says when it's over.
- main and the main game link untouched without the user's go. Repo is PUBLIC.

## Agreed order (the user)
1 Dev mode → 2 playtest patch (30 items) → 3 Talk a while pack wired in → 4 ship-wide events chronologically (shared base F0-F8, ion storm, Crossing the Line, comet, visit) → 5 Pillar 5 steps 5-6 → 6 character arcs → 7 optimization → 8 balancing & polish. No file split (the user's call after split testing).

## State right now
- **Dev mode (step 1):** DB1 (session_01R4RFu3mPaq4qj1L2TXEoza) building Stop 1a on `claude/devmode`. D1 fffb8e2, D2 c0bf421, D3 78b4985 done (cadet_test ALL IDENTICAL each; devmode_check, check_fast OK). D4 (Take me to, Mark/Back) in progress. DR1 (session_01WfFmjT31bVcy4mvsNVi5Mz) stands in as owner reviewer (no live owner seats): D1 hooks c9cc785 (13), 55add3f (21) PASS WITH FIXES (4 fixes sent to DB1, see claude/devmode-review-1 68618fa); now reviewing 58d63a4 (13), e02c085 (20), b1de9f6 (15), 9d96a16 (11). When D4 + reviews pass: start a build master to merge into `claude/integration` (check_fast + relevant checks, set build number), publish Stop 1a as a NEW artifact with the `#dev` link, notify the user.
- **Patch plan (step 2):** final once PP1 (session_01QfLuMmrJSgMQ3A4tBtXAmf) marks rev 3 answers (pp-v3-q1 bar-only, pp-v3-q2 20 min). Rev 3 = claude/patch-plan b8865a9: 30 items incl. #26 First Light Cocoa (first Monday 20:00-20:45 bow lounge; Dev Raman at the windows; tips from 3 of 5 old hands; Tomas; pick a reply; no pin), #29 cocoa at the bar, #30 the mug in your hands. ~21 turns. Page https://claude.ai/artifact/BrEniitA4gGKf1wFMvwy2s (scratch file `scratchpad/pp/plans/patch-plan.html`, save script appended before `</body>` plus `savestate`/`savestate2` paragraphs around `form#answers`; PP1's file has neither).
- Next after Dev mode: staff the patch build (owners per `plans/owners.md`).

## Links
Rec Deck 0.64.2 https://claude.ai/artifact/7ZHXGUSvgJzAc1mYmfPt1K · Playtest 0.63.5 https://claude.ai/artifact/9m3jP4HBL8ix3oyZaJoo9p · Events plan (complete, claude/events-plan f6996d86) https://claude.ai/artifact/Qi1Uvev6p4TbPwYFQvRB1P · Dev mode plan (v3.1 ff25dda, all answered) https://claude.ai/artifact/2ugbTkkAFkEsgTZa3bbFdH · Talk pack lines (claude/talk-pack 8692459; 160 talks, 1,476 lines; pool strictly once per save) https://claude.ai/artifact/BEWR9Y2uywFZ7FjNDwuJE4 · Patch plan https://claude.ai/artifact/BrEniitA4gGKf1wFMvwy2s · Split plan (shelved) https://claude.ai/artifact/9v7C1oRCJUUTGkAujsAoUt

## Seats (session ids)
DB1 01R4RFu3mPaq4qj1L2TXEoza (working) · DR1 01WfFmjT31bVcy4mvsNVi5Mz (working) · PP1 01QfLuMmrJSgMQ3A4tBtXAmf (finishing) · idle: PR1 01J7kHfFrG8Syjmz8XYK9USU, DP1 01HvjJKxBhqXwvnVKUfFQCLq, DR2 012GxodCR3fkT9KyQCeLTd4D, EP1 0183vbQyL2CzMHAS3AZ9kivj (handed over), ER1 01CU43dzWJe5PGBQWTtKH4C3, TW1 019ek4xmi5Yp9xijbzuAo2kN, TR1 01T93VUcBukQwhBLu8vCNUhV, WW1 0192KVdPtywdv7sp3mXUXGHU, R8 01GdhqdLeZuGFQSTX7RL92U5, BM10 01KpcQGJvrAz57dmKp6AFg4w. All prefixed `session_`.

## Gotchas
- START-HERE.md and the roadmap originally lived on origin/claude/lead-pillar1.
- `git archive | tar` fails on a missing path; use `git show branch:path`.
- Section owners for 11/13/15/20/21 have no live seats; DR1 stands in. Shared-function input/table-shape changes go to the owner first.
- Dev mode switch is `DEVMODE` (`DEV` is already used).

## Update ~14:17 UTC
- Patch build started in parallel (the user: "Hire extra helpers"): PA session_01Jka314UJ2Yto5XxbcQnB8H (claude/patch-a, batches A-C), PB session_01FWW2piuXkFYaRRzLXZiqYb (claude/patch-b, D then F; PB now owns 13/14/10 and OKs PA's #1 formats), BM11 session_01W7NHRM4JjqaNEJQUWNxgcE (build master, next build 0.64.3 = Dev mode). PP1 reviews patch turns. Batch E waits for DB1.
- Talk pack wiring started alongside (the user: ship it with the patch): TE1 session_01MnQHVrsK5wnTwfEi2QFm4W (claude/talk-wire).
- Dev mode Stop 1a built (bb6e78a); DB1 doing DR1's round 1+2 fixes; then DR1 final pass, BM11 merge, publish a NEW page with #dev, notify. Check on the published page: #dev shows the DEV tag in the Claude app and a phone browser; Back to mark keeps the tag; the plain link shows the real game.

## Update ~16:15 UTC (lead memory 41%)
- Published: Dev mode 0.64.3 https://claude.ai/artifact/EWB21cTQnXc8ZT71zCeEzf (scratch file scratchpad/dev/starship-cadet-dev.html = integration build + a first-line script forcing #dev; title "Starship Cadet Dev"). Work pools plan https://claude.ai/artifact/42zY17Rc3ePiKZEVHVv8KZ (answered: all recommended).
- claude/integration: 0.64.3 da5e2aa (Dev mode), 0.64.4 5d6ee1c (Talk a while, 280 talks incl. nine work pools; TALK_PACK_ON committed ON, the user's call).
- Patch: PA (patch-a, A-C) and PB (patch-b, D then F) slow, nothing pushed yet at 16:12 (asked to push WIP). PE (session_01H7weuTSkTfuSAqhxvdx1EK, patch-e): #25 #21 #6 #24 done (2e2575d, PP1 PASS WITH FIXES, DR1 owner review asked), #5 ladder next (Deck 5 hatch at v,19,9). DB1 builds #30 #29 on claude/devmode (its only push branch), maybe #26; else a fresh builder for #26.
- Idle/done: TE1, TW1 (talk), TR1 stopped (handover on claude/talk-pack-review cb6dd07). BM11 build master ready (next build 0.64.5).
- Usage: 5-hour limit showed "allowed_warning" at 16:11 (resets 16:40 UTC).

## Update ~17:10 UTC (lead memory 50%: user warned)
- 16:12-16:47 every seat stopped on the 5-hour usage limit; resumed at 16:48 on the user's "Resume". Asked the user: full team with pauses, or 3-4 seats steady (no answer yet).
- Branch heads: patch-a e9d9022 (batch A: #1 #2 #28 done; PP1 reviewing, PB owner-reviewing hooks 47b3dba/6e9e86d; next batch B), patch-b 5baa5b8 (WIP batch D, check_fast pending), patch-e 2e2575d (#25 #21 #6 #24: PP1 PASS WITH FIXES, DR1 PASS; ladder #5 next), devmode 05314b6 (#30 mug behind MUG_ON; PP1 reviewing; #29 next, then DB1 may hand over before #26).
- Merge plan: BM11 merges each reviewed branch into claude/integration (next 0.64.5), then the full round of checks from Day 1, then publish the patch build as a new page (Dev page can be republished too) and notify.
- Answered for the user: first big gathering = Day 6 Crossing the Line (plaza ~50) per the events plan; then ion storm all-hands Days 9-11; Founders' Day festival (70+) after the phone test.
