# 0.98.0 builder briefs (OP1 for lead 44, 2026-10-28 ~9:40 PM ET)

The plan: `plans/opt-098-plan.html` (published at https://claude.ai/artifact/N6veQ6xkcMh5WTg6E8rCJX), with the measurements in
`plans/opt098-notes.md` and the probes in `plans/opt098-probes/` (all on `claude/opt-098-plan`).

**The user's answers (28 Oct, through lead 44):**
1. Turns 3-4: show the user a before and after picture first. Only incredibly minor visual changes are accepted. Pixel-identical is preferred, and anything visible needs the user's OK.
2. No 60 fps cap.
3. No battery saver.
4. Backlog 12 stays known-old (balanced in 0.99).
5. FX24-2: book walking time only for long walks to a tradition.

Reviewer for every turn: **RV25**. Build master: **BM20**. Lead: lead 44 (`session_01GKuymj3tKpX7xwDZwBh8RM`).

---

## Brief A: the render builder (a fresh session): turns 3 and 4

**Role:** 0.98 render builder (call yourself RB1). **Branch:** `claude/opt-098-render`. Start from the base BM20 names (claude/integration
fe11cd66 = 0.96.0, or 0.97.0 on claude/staging-pad when it's in). Bring that base into your branch at the start of each turn.

**Read first:** CLAUDE.md, then DEV_NOTES.md sections "Rules that keep it working", "Testing", "Shaders kept across deck changes" and "Machine looks". Then plans/testing-guide.md sections 1 and 8.1, `plans/opt-098-plan.html` items 1 and 2, `plans/opt098-notes.md`, and in `plans/opt-measure.md` the "Faster deck builds (#10)" and "Shadow stand-ins" notes, how mergeMeshes keeps bytes identical.

**What's slow (measured on 0.96.0, 390x844 zoom 0.7, one browser alone):**
- At Sunday dinner in the mess there are 418 picture draws + 216 shadow draws.
- renderer.render's own JavaScript takes 6.5 ms a frame. With the GL calls stubbed, three.js alone is 4.2-4.6 ms.
- The game code is 2.7 ms.
- render() cost grows with the number of draws. `plans/opt098-probes/draw_mix.py` lists the draws by group.

### Turn 3: one draw per full body (plan item 1)
- **What:** you (`player`, a `Walker`, section 10 ~69453) and up to `FULL_MAX` = 3 story crew close to you (`FullPerson`, section 10 ~70147) are each built by `makeCharacter` (section 8 ~67598). `bake` (~67578) turns each joint's parts into one mesh, so each person is about 16 meshes. Each is drawn in the picture and again in the shadow pass: about 128 GPU draws at dinner.
- **The goal:** each person becomes one SkinnedMesh, with the baked per-joint shapes as one geometry and the joints as bones (skin index = joint, weight 1, bind matrices identity in each joint's own space). That's the way the crowd's chunks do it (section 8b `CrowdChunk`, ~68384).
- **Things to keep working:**
  - the player's uniform tint (`playerUniformTint`, `UNIFORM_MAT`, 24b/24p);
  - props in hand (`propMeshes`, `bodyProps`, `recBody`);
  - rank pips and the bar (`promoPip`, `playerRigRebuild` in 24l: they rebuild the rig);
  - taps on you (`userData.walker`, section 15 ~16150 raycasts against walkers, and a SkinnedMesh raycast is not what it was);
  - the crowd's posing code shared by FullPerson (`set`, `update` borrowed from CrowdPerson);
  - `rig.root.rotation.order`.
- **Before you build:** check whether every joint's parts share one material. If they don't (a tinted uniform, a glow), group by material, which gives one draw per material, not one per joint.
- **Expected:** Sunday dinner GPU draws about 638 to about 515; render() JS about 1-1.5 ms less. Measure it with the paired method below.

### Turn 4: furniture that differs only in colour, drawn together (plan item 2)
- **What:** `mergeMeshes` (section 4b, ~3137) merges a deck's still furniture into one bucket per material uuid. Many materials differ only in `color`: Deck 3 has 182 materials but only 65 once colour is ignored; Deck 4 has 106 / 49 (probe: `scratchpad`-style `mats.py`, logic in `plans/opt098-notes.md`).
- **The goal:** materials that are identical in every way but colour go into one bucket that uses `vertexColors`, with each corner carrying its piece's colour. Treat MeshBasic and MeshStandard separately. Leave out anything transparent, alphaTest, noShadow, mapped differently, or with its own side.
- **Keep:** the same triangles, `noMerge`, the shadow stand-ins (`shadowStandIns`, 4b ~3026: buckets by side and tile block, so they don't care about colour), `tallCombine`, `TALL` fading (it changes material opacity: tall pieces must keep their own materials), machine looks that recolour materials (`GD.leaves` wilting on Deck 3 lerps material colour: those materials must stay out), anything that recolours or swaps a material later (search `.material.color` and `.color.set`/`.copy`/`lerp` on deck materials).
- **Expected:** the mess's 142 furniture draws fall to about 55. With turn 3, Sunday dinner's picture calls go from 418 to about 270.

### The look (the user's rule for these two turns)
- Pixel-identical is the goal. Proof:
  - `python3 cadet_test.py OLD.html NEW.html` ALL IDENTICAL;
  - shots of the changed things at the four phone views (portrait 1.5, wide 0.7, landscape 1.15, TriFold folded), day and night: you and a full-body crew member standing, sitting, walking, carrying, tinted; every deck for turn 4.
- **If anything differs, nothing is merged.** Make a before / after / difference picture (enlarged), count the changed pixels and their largest difference (in shades of 255), and send it to lead 44 for the user. Only incredibly minor visual changes are accepted, and only with the user's OK.

### Proving the speed (through the noise)
- Draw counts are exact (`plans/opt098-probes/draw_mix.py`, `render_split.py`).
- Timing: old and new builds in one browser, the same scene, alternated A B A B 15 times. Report the median paired difference and how many pairs went each way (the probes `frame_probe.py` and `render_split.py` give the per-build numbers; pair them).
- Scenes: Sunday dinner, the Line supper, the Veyli engine lights, the Captain's address.
- At most two browsers on the box.

### Each turn
- Small exact-string edits only, in the sections above (section 8/8b/10 code: the Performance engineer's and the sim engineer's; 4b: the deck architect's; RV25 reviews).
- New helpers go in the Performance engineer's slot (section 8b, `// ---- slot: Performance engineer`).
- Don't touch the two build-number lines.
- Add a row to `plans/build-table.md`.
- Run `node names_check.js`, cadet_test, `perf_check.py NEW OLD`, deck_check, bubble_check (full-body crew), player_check (you), then `bash check_fast.sh`. Commit and push.
- Then tell RV25 and lead 44: the commit, the draw counts before/after, the paired timing, the pixel result.
- Update DEV_NOTES (a short section under the render notes) and design-doc only if a design decision is made.
- Handover at about 60% memory (`plans/handover-rb1.md`).

---

## Brief B: OP1's own turns (1, 2 and 6)

Branch `claude/opt-098-plan`, then `claude/opt-098-build` from BM20's base.
1. **Turn 1, shader checks off outside Dev mode:** `renderer.debug.checkShaderErrors = !URL_FLAGS.has('debug') && !devOn` (keep it on with `?debug` so every check still catches shader errors, and with `#dev`). Measured: first frame -0.25 to -0.3 s, 3/3 pairs. Proof: identical pixels by design, cadet_test, devmode_check, the load split paired (`plans/opt-probes/gl_split.py`).
2. **Turn 2, the rest of the still things through shadow stand-ins:** in the mess, 20 merged furniture draws still cast their own shadows. Find why `take()` in `shadowStandIns` (4b) skips them (alphaTest, shadowSide, side mix?). Include the ones that can be included with the same triangles. Proof: cadet_test ALL IDENTICAL, shots with shadows, shadow draw counts.
3. **Turn 6, FX24-2:** the planner books walking time before a gathering at a tradition only when the walk is long (same deck, over a threshold of ship minutes). Sim engineer's section 14, in its slot. Proof:
   - events_check walks reading-corner Day 7 and passes (fails the same way on OLD);
   - day_check on the event days, food_check, bigevents_check;
   - cadet_test shows what moved (only tradition-day plans with long walks), each difference explained.
