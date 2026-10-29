# Handover: RB1, the 0.98 render builder (2026-10-29)

**Role:** render builder for the 0.98 optimization plan (plans/opt-098-plan.html items 1 and 2; brief "Brief A" in
plans/opt-098-briefs.md on claude/opt-098-plan). Leads: 44, then 45, then 46 (session_01GKuymiks9CC1WYr2may5nM).
Reviewer RV26 (session_01GKuymjwVsweGh8p9EbTGHU). Build master for 0.99: BM21 (session_01GKuymkAoLNTFXef9RgiYLn).

**Branch:** claude/opt-098-render. Everything below has passed review (RV26).

## What I built

1. **Turn 3, one draw per full body** (8d7a314; in claude/staging-099; missed 0.98.0's 12:30 cut, so it ships in 0.99).
   Section 8's `bake` hands each joint's corners to `bodyBake` (8b's Performance slot): you and each FullPerson are one
   mesh. Pixel-identical by construction: `bodyTick` (scene.onBeforeRender) writes each joint's model, camera x model,
   normal and sun-shadow matrices, worked out the way three does per mesh, into a 16 x 32 float texture that the body's
   shader reads (`bodyShader` replaces project_vertex, defaultnormal_vertex and worldpos_vertex; a customDepthMaterial
   for the shadow). Taps: never-drawn per-joint meshes on BODY_LAYER (1); section 11's ray enables that layer.
   Sunday dinner, wide view: 638 to 516 draws with shadows. DEV_NOTES "One draw per full body".
2. **controller_check fix** (222ec28; in staging-099): bedtime's ring line was hidden by a real-time toast ("Bursting").
   Turn 3's quicker frames made the race show. The check now clears the toast first. The game was fine.
3. **Turn 4, furniture that differs only in colour drawn together** (e7bce5a + the docs commit 24e75b9; with BM21 for
   staging-099). 4b's `mergeMeshes(root, tint)`, plus `mergeTint` / `mergeTwin` / `mergeFlat` in 8b's slot.
   **Not pixel-identical; the user OK'd it** (corner pixels where two surfaces meet at one depth, because draw order goes
   by shader). Expected cadet_test difference: d_wallslow 8 px, i_tap2 1 px. Set: plans/opt098-rb1/. DEV_NOTES
   "Furniture that differs only in colour, drawn together".

## Gotchas

- In turn 4, a furniture material changed while you play must stay out of the tint buckets (the twin is a copy):
  GD.leaves, RK.film and PULSES are excluded by name. Add any new one there, or mark it noMerge.
- Turn 3: if three.js is upgraded, re-check the replaced chunks and renderObject's matrix sums.
- My helper scripts are in my scratchpad, not the repo: shots.py, deckshots.py (every deck x 4 views, day and night),
  ab.py (paired A/B timing in one browser, STUB=1 to stub GL), livemats.py, wilt.py, cmp.py. They are easy to
  rewrite from perf_check's SCENES / SCENE_JS. Ask me while I'm idle.
- Waiting loops: `pgrep -f`, `pkill -f` and `ps | grep` patterns can match the waiting shell's own command line.
  Wait on a log line instead.
- perf_check's game-code times are noisy when other checks run beside it. Run it alone, or use paired timing.

## Open

- perf_check alone on turn 3 was stopped at 76 min (lead's call); the full 0.99 round covers it.
- Turn 3's speed gain was smaller than the plan's estimate: render() JS -0.35 ms (30 of 40 pairs), GL stubbed -0.45 ms.
