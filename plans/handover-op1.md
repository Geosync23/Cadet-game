# Handover: OP1 (0.98 optimization planner, then walk-time builder), 2026-10-29 ~3 AM ET

**Role:** planned the 0.98 optimization pass (game speed on phones only, the user's scope), then built the crew walk-time
fix. Leads: 44, then 45 (`session_01GKuymnu4NeXJhwPe21FWk7`). Reviewer: RV25. Build master: BM20.

## Branches and pages
- `claude/opt-098-plan`: the plan page `plans/opt-098-plan.html` (published privately:
  https://claude.ai/artifact/N6veQ6xkcMh5WTg6E8rCJX, v4; the user's answers are saved on the page's `answers/opt-098`
  store, empty so far: the user answered through the lead), `plans/opt098-notes.md` (all measurements), `plans/opt-098-briefs.md`
  (Brief A: the render builder's turns 3-4; Brief B: OP1's own).
- `claude/opt-098-build`: staging-pad b9b7e3d7 merged in, then:
  - c85781d8: the game change (section 14);
  - de59683f: events_check;
  - 3307e843: day_check;
  - 6b18afe0: records (build-table row 0.98-op1.1, backlog, DEV_NOTES "Walking to a tradition").
  - **RV25: PASS** (2026-10-29 ~06:56 UTC). Not merged yet; BM20 has the list.

## The user's decisions (28 Oct)
- Items 1-2 (render builder) only if pixel-identical, or with a before/after picture and the user's OK for anything
  visible.
- No 60 fps cap. No battery saver.
- Backlog 12 waits for 0.99.
- FX24-2 fixed with "walking time only for long walks to a tradition"; FX12-1 and TQ1-1 folded in.
- SD3-2 went to SD3.

## What happened to the plan's turns
- 1 (shader checks off): **set aside**. Alternating runs showed no gain; the first 0.25-0.3 s came from always measuring OLD first.
- 2 (shadow leftovers): **parked**. About 10 safe draws.
- 3-4 (full bodies as one draw; furniture colours merged): the render builder's, from Brief A. These are the real speed wins.
- 6 (walk time): **done**, RV25 PASS.

## The walk-time fix, in short
- take()'s `o.longLead`. The generic tradition take passes `tradWalkMin()` = 6.
- `ahead(w, hops)` cuts from the previous stay. For traditions it reaches back through lift hops and never cuts a shift.
- `longOk` only fires when the place is free for the walk.
- The stay records `seg.walk`; its arrival is `from + walk`.
- events_check reads arrival that way.
- day_check's rec comparison tolerates only named walk-led people (Day 4: Mori, Tomas).
- Probe: `plans/opt098-probes/walk_probe.py BUILD DECK DAY HH:MM HH:MM [out.json]`.

## Loose ends
- OP1-1 (backlog): Deck 4 late piano fills late from live crowding (section 10), not the plan.
- The full round on the 0.98 candidate runs after the render builder's turns.
- perf_check never measures three.js's own per-frame JavaScript (renderer.render: 4-7 ms here in busy scenes), because it skips drawing. `plans/opt098-probes/render_split.py` and `frame_probe.py` do.

## Gotchas
- Time a frame with a readPixels sync.
- Compare builds alternately (A B A B), never OLD-then-NEW.
- Background bash jobs end at 30 minutes and kill their children. Use nohup for long check lists.
- `cd x && export ... && (a) & (b)`: the `&` backgrounds the whole chain, so (b) runs without the export.
