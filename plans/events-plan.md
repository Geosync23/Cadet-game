# Ship-wide events plan: summary

Events planner EP1, 2026-10-20, from build 0.64.2, branch `claude/events-plan`. The full page is `plans/events-plan.html`, with screenshots in `plans/events-plan-shots/` and the run log in `plans/events-plan-run-log.json`. Planning only: the game is unchanged.

## When the career ends
- **Day 26 (a Friday), with "Calder's question".** That's from the approved Pillar 5 plan v11:
  - Officer on Day 10
  - Senior Officer on Day 16
  - Engine Specialist on Day 23
- **Steady and busy players get the same days.** Every step has a first possible day, so working harder can't bring it forward. career_check on 0.64.2 confirms the first promotion is on Day 10 for both.
- **A slow player gets there later.**
- **Today's build has only the first promotion.** Tiers 3 and 4 come in Pillar 5 steps 5-6.

## In scope
1. **Ion storm** (main). Built and switched on, Days 10-15 today. Recommended move: Days 11-16 (warning Thu 11, front Fri 12, all-clear and party Sun 14).
2. **Comet viewing** (short). Drafted in `plans/comet-viewing-draft.js`. Sun Day 21 at 21:00.
3. **Diplomatic visit** (main). Built but switched off (`draft: true`). Recommended dates: warning at the first Monday briefing on Day 22, greeting Wed 24, dinners 25 and 27, farewell about Day 29. It runs past Day 26.

**Cut:** everything after Day 26, which is crew rotation day and main events 3-7 with their short events. The rotation traditions that are already built stay.

## The storm audit
**Built:**
- the phases, 4 threads and 3 bands
- the traces
- the machines' wear, blackouts and storm jobs
- storm stew and trays to the bridge
- crew routines
- the jolt, the surge and two addresses
- Calder's briefing and the all-clear meetings
- the party (a full bow lounge, 307 draw calls)
- the commendation, which leads to the ready room, the Captain's table and the bridge invite

**The run:** I ran it at phone size and everything played. Left to itself it came out rough. An earlier run came out bumpy.

**14 updates:**
1. It lands on the first promotion.
2. 89 crew storm lines never fire, because there's no phase note.
3. Calls home still work while comms are down.
4. The device's Schedule, Tracked, heads-ups, Ship status and Record don't show it.
5. A long skip can miss the all-clear and the afterglow.
6. The Works career mostly ignores it: the drill, the inspection, incidents and Pillar 5's undefined "event day".
7. The rec deck stays open and has no blackouts. Pell's Mail arrives at the front, and rec film night clashes with the party.
8. Your briefing choice is usually moot: the crew finish the job first, so there's no commendation.
9. The result flips between bands and needs retuning.
10. On phones, the Captain's banner covers the HUD.
11. Rank-aware parts aren't built.
12. There are two ready rooms and two Captain's tables close together.
13. Supplies run short in skips.
14. Old stand-ins to remove, and the framed menu has no prop.

## The shared base (built once)
- **F1:** an event calendar guard and career-beat guard.
- **F2:** phase notes for crew lines.
- **F3:** the device: Schedule, Tracked, heads-ups, Ship status and Record.
- **F4:** skip-safe phases.
- **F5:** parts by rank.
- **F6:** Dev mode hooks: start any event, even one switched off, at any phase.
- **F7:** one table-driven events check.
- **F8:** a comms-down check.

**Size:** about 26-33 turns in all:
- the shared base: 10-12
- the storm update: 6-8
- the comet: 2-3
- the visit: 8-10

## Order
1. Step 2 (new ways of working).
2. Dev mode.
3. Pillar 5 steps 5-6.
4. The shared base.
5. The storm update: switch it off, test, switch it on.
6. The comet: built off, then on.
7. The visit: built off, then on.

Stop for the user's review after each event.

## Questions for the user (my recommended answers)
1. **Is the list the storm, the comet and the diplomatic visit?** Yes.
2. **Should the storm move off the promotion day?** Yes, by one day, to Days 11-16.
3. **Can the visit run past Day 26, to about Day 30?** Yes.
4. **Should events follow the calendar rather than rank?** Yes: by the calendar, with parts that depend on your rank.
5. **How should the storm turn out if you don't help?** Bumpy.
6. **Should the rec deck close during the storm?** Yes, from the front until the all-clear.
7. **Should the two ready rooms and the two Captain's tables be folded together?** Yes.
