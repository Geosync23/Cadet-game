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

## Update, 2026-10-29 ~7 AM ET (after the 0.98.0 round)
The walk-time fix moved some crew plans, so the week's machine wear moved, so later checks met different faults. Three new FAILs in the 0.98.0 round traced to that.
- **controller_check s5cases** (check only): the suspects now come from the case's own `c.sus`.
- **puzzle_check p6's first save size** (check only): the size counts this case plus the shared record.
- Both are on `claude/s5cases-fix` 34adecc7 and 10865180. RV26 PASS; they went into 0.98.0.
- **arrows step6 p5n:bed:22** (a real 28a gap, AS1's find): if you never clock in on Day 22, the day-sleep arrow was never asked. Fixed on `claude/nights-dayarrow` 79a87eac **for 0.99** (lead 45). Its fields:
  - p5nGuide's day-sleep block also runs when there's no day part;
  - `from` is a whole minute, because the queue skips entries with now < from;
  - it never runs the morning after a night.
  - Proof: step6 in all four ways OK, step5 OK, day 22 OK, cadet ALL IDENTICAL, check_fast OK. RV26 is reviewing, AS1 is running the whole arrows_check, and BM21 has it for 0.99.
- Also done: join_check's real reload now waits up to 120 s (`claude/join-timeout` c27ebb88, RV26 PASS). The owner read of EV2's apptWhere a.early: OK.
- **Lesson:** a planner change moves wear and faults, and so which case and machine every later check meets. Before merging one, run the case and arrows checks: controller s5cases/s6cases, puzzle, arrows step5/step6.
