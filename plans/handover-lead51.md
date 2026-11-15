# Handover: lead 51 (session_01GKuymjp49y3M5hgRLecobm), written 2026-11-11 ~02:22 UTC (Nov 10 9:22 PM ET)

## State
- **0.99.9 LIVE** (published on the user's "Publish", 2026-11-08 ~17:44 UTC): Playtest https://claude.ai/artifact/2Uyqpm6jS9dvUW4ML7mb5H
  (slug 0c01401d-1612-4e1c-a69a-5df090589360, v5 1794159823-18ea), Dev https://claude.ai/artifact/JftiS793gzEPhKRekatcon
  (slug 8f197d97-106b-4f75-83f3-37b6695372ad, v5 1794159830-59af). main = claude/integration = bfbcbdf (game 583d99ba...bd16).
  The user's "current save" Dev link (6daNCLCJ...) is untouched; never publish over it.
- **0.99.91 PUBLISHED 2026-11-11 ~14:49 UTC** (Playtest v6 1794408527-c375, Dev v6 1794408531-b0f2; main = integration = cdd9efd). Was: (plans/patch-09991.md): A TP1-1 shutdown vs night shift (TP2, TP9991_SD_ON), B week-1 Sim night
  Wed Day 3 19:30 (EV2, EV9991_SIM_ON), C drills as Calder's talk (TB7, TB9991_DRILL_ON), D Calder results meeting after a
  Dev jump (CR2, CR9991_RESULTS_ON), E (added) rewire Tier fix in 24q (TP2, MC9991_REW_ON, old bug).
- Round 09991 on candidate 1 (staging-09991 4d8869ec, game 475bac86) ended: finds Q1/Q2/Q4 (drill arrows, TB7 fixing:
  direct arrows like the old drill), Q3 (sim pod tagged out, EV2 fixed 6ad4050), E (rewire tier, TP2 fixed dc0ae57).
  Candidate 2 = c1 + those three fixes after their PASSes (RV36: drill + sim; RV35: rewire) + MC9991_REW_ON on; then full
  round 09991b (perf on c2 with R4), BM28 FINAL GO, then ask the user's OK, publish (recipe below), ff main + integration.

## Seats
BM28 session_01GKuymjydss9RxzDw1ftdPf (build master, R5). Runners R1 session_01GKuymkdg7HjAaXfh3NRnBG, R2
session_01GKuymmnJnzWMxP769P9Edd, R3 session_01GKuymo7sJwyufjkoEsCacB, R4 session_01GKuymmDPNyaTSDSCiHCDFj, R6
session_01GKuymjS1cBK12RvWv7L5ka. Reviewers RV35 session_01GKuymm7wiTGz6LA46UHffc, RV36 session_01GKuymoG8txh1cPvipXz8BW.
Builders TP2 session_01GKuymmrDSKcr6yPNqBWPda, EV2 session_01GKuymo8i9kGxDTkGjxNmvn, TB7 session_01GKuymm61PakAiqe965r8d2,
CR2 session_01GKuymo1JQnVN2mdZ5JSdN9. Older seats (TP1, EV1, TB6, CR1, BM27, old R1/R4) handed over, idle.
Hourly check-in trig_01QYwt7yF2Dsfz2JgefUNUAC (lead 51's; delete or reuse).

## Publish recipe (worked for 0.99.9)
tools/publish/build.py on claude/publish-pub3: run in a dir with play/ and dev/ subdirs: python3 build.py GAME.html ->
play/starship-cadet-playtest.html, dev/starship-cadet-dev.html. Check: building the live game reproduces the live shas
(list_files). Phone test: inject "window.__sc = src => eval(src);\n" before the last "})();" in test copies, npm pack
three@0.128.0 (package/build/three.min.js next to phone.js), node phone.js FILE "" tst / dev (tag must not start "play").
Copy the two files into the working folder, publish_files as index.html onto each slug with base_version from
get_artifact, list_files to confirm shas, delete the copies, then push staging tip to main + claude/integration (ff).

## Backlog added
EV2-2/3 (sim toasts busy; yielding pilot by full bench), TB7-1 (Food arrow to a closed servery, old), RV36-1 (shared
card header vs X with long titles), RV36-2 (mech_check partial-row runs fail on 0.99.9 too), BM27-1 (sound_check timing),
EV1 offers (Deck 6 blink softer; notice with the blink).

## Gotchas
Containers restart often (runners resume). *.png is gitignored: git add -f. Messages cross: confirm commits on origin.
A game change after a GO = full round; let the running round finish to batch finds.

## NEW JOB for lead 52 (the user, 2026-11-14 ~9:45 PM ET / Nov 15 02:45 UTC)
The user's words: "Hire 2 Fable 5.2 workers and review the game. Codebase, efficiency, design, playability, performance
and anything else needed thorough review. Create a seperate version with a seperate link for their/ your work."
(The user switched the lead's model to claude-fable-5-2 first; lead 52 and both workers run on claude-fable-5-2.)
Lead 51 was at 61% memory, so by the user's rule it hands this big job to lead 52 before starting.

State: 0.99.91 LIVE (Playtest v6 1794408527-c375, Dev v6 1794408531-b0f2), main = claude/integration = cdd9efd,
game b321a4ec...95f3. All 0.99.91 seats stood down with handover notes on their branches.

Plan (lead 51's reading):
1. Two reviewers, both claude-fable-5-2, from main cdd9efd, hired by lead 51 (ids in TEAM.md):
   - FR1 code, efficiency, performance -> report plans/review-fable-code.md, fixes on claude/fable-review-code.
   - FR2 design, playability, phone feel -> report plans/review-fable-play.md, fixes on claude/fable-review-play.
   Phase 1: review only, ranked findings with evidence, sent to the lead (aim ~3 h). Phase 2: fix what is safe and clearly
   right (bugs, polish, performance), each behind its own switch (off = cadet_test ALL IDENTICAL vs 0.99.91). Changes to
   what the game IS (design decisions) are not built: they go to the user as plain questions.
2. The lead reads both reports, tells the user the main findings in plain words, picks the fix list with the workers,
   and asks the user the design questions.
3. A SEPARATE version: branch claude/staging-fable-review from main, both fix branches merged, switches on, its own
   build label (e.g. 0.99.92-review). Per CLAUDE.md every game change gets the full round of six runners before it is
   published (fresh runners from the handover-rN notes; a fresh BM from plans/handover-bm28.md on claude/handover-bm28;
   each worker's fixes reviewed by the other worker or a reviewer).
4. Publish it as a NEW artifact with its own link (title e.g. "Starship Cadet Review"), NEVER over Playtest, Dev or the
   user's current-save link. The user asked for this link, so no further OK is needed, but the publish step still needs
   their approval tap in the app: ask them to be present. main/integration do NOT move: this version stays separate
   until the user says to adopt it.
5. Also give the user the review itself in plain language (a short report page or message): what's good, what's
   wrong, what was fixed in the review version, what needs their decision.
