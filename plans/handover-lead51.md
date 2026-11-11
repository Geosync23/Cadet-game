# Handover: lead 51 (session_01GKuymjp49y3M5hgRLecobm), written 2026-11-11 ~02:22 UTC (Nov 10 9:22 PM ET)

## State
- **0.99.9 LIVE** (published on the user's "Publish", 2026-11-08 ~17:44 UTC): Playtest https://claude.ai/artifact/2Uyqpm6jS9dvUW4ML7mb5H
  (slug 0c01401d-1612-4e1c-a69a-5df090589360, v5 1794159823-18ea), Dev https://claude.ai/artifact/JftiS793gzEPhKRekatcon
  (slug 8f197d97-106b-4f75-83f3-37b6695372ad, v5 1794159830-59af). main = claude/integration = bfbcbdf (game 583d99ba...bd16).
  The user's "current save" Dev link (6daNCLCJ...) is untouched; never publish over it.
- **0.99.91 in progress** (plans/patch-09991.md): A TP1-1 shutdown vs night shift (TP2, TP9991_SD_ON), B week-1 Sim night
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
