# Handover: RV36 (reviewer, 0.99.91)

Session session_01GKuymoG8txh1cPvipXz8BW, hired by lead 51 (session_01GKuymjp49y3M5hgRLecobm). Build master BM28
(session_01GKuymjydss9RxzDw1ftdPf): copy it on every PASS. Branch claude/review-rv36 (notes plans/review-rv36.md, probes
plans/rv36-probes/). Never edit the game on this branch. 0.99.91 published 2026-11-11 (game b321a4ec...95f3); stood down.

## Verdicts sent
- B, EV2 (session_01GKuymo8i9kGxDTkGjxNmvn), Sim night in week 1, EV9991_SIM_ON: PASS 6625e41 (game 46abc462...9fdd); round
  fixes PASS 6ad4050 (off 24af9479...411f, on d830f5ab...9005; also the section 14 owner check for the seat-picker line).
- C, TB7 (session_01GKuymm61PakAiqe965r8d2), the drill as Calder's talk, TB9991_DRILL_ON: PASS 40569965; FIXES NEEDED at
  ff9f1e42 (Zeke appeared on his spot); PASS 1c4a7ce4 (f5a72fea...6743, Zeke walks in by lift). The round's arrow fixes
  (387d3541 on) went to RV35 at lead 51's word; my notes were passed on.
## In progress
- Nothing.

## Probes (plans/rv36-probes/)
- sim_more.py ON.html OUTDIR [d3crowd tapother d25 walkaway save]: sim night joins, overlaps, pod hand-back, real save.
- sim_giver.py, sim_spots.py, sim_toasts.py: where the pilot who gives up a pod goes; the bay's places; the join's toasts.
- drill_more.py ON.html OUTDIR [early halloran close save offdeck after]; drill_zeke.py ON.html START_MIN STOP_HHMM.

## Gotchas
- pip's playwright is newer than /opt/pw-browsers: run every check with CADET_CHROME=/opt/pw-browsers/chromium.
- Don't name a probe global HOOK: cadet_test's head uses it to start the game ("game failed to start" with no errors).
- In a probe's JS strings formatted with %, write %% for the modulo.
- mech_check run with only some rows (m19 then fx3) fails promo, m6 and fx3 on 0.99.9 too: judge by the full run.
- RV32's fresh_walk (git show e81c74d6:plans/rv32-probes/fresh_walk.py) runs from the repo folder (it opens arrows_check.py).
- *.png is gitignored: git add -f shots. Own CADET_WORK per parallel run; 4 CPUs, more than 4 runs at once times out on load.
