# Handover: lead 38

## START HERE (next lead)
Read CLAUDE.md, this note, then the bottom of TEAM.md on claude/lead-38 (from "LEAD 38 started", incl. "CURRENT SEATS (lead 38)" ~04:40 UTC Oct 26 and every line after). plans/handover-lead37.md has older background.
Lead 38 = session_01G2y9crUv6vDiiEB2q6Yo9W, branch claude/lead-38, hourly check-in trig_01DmYmfsujdzynRz5VURoYRP (57 * * * *): disable it when you take over and make your own.
**Session depth:** lead 38 sits at lineage depth 7 of 8. A lead spawned BY lead 38 would be at the limit and may not be able to create helper sessions. Lead 39 should be started by the user directly (a fresh claude.ai/code session on Geosync23/Cadet-game), or from a shallow session.

## Latest (~15:00 UTC Oct 26, 11 AM Eastern)
- LIVE: **0.93.2** (Playtest 3HqM5XiXaHXzgrpq7JbesJ v6, Dev 9ZWAgqiZCvkJvVjjhjVkEr v6, both declare capabilities {downloads: true}; from claude/staging-0.93.2 d9c7e5f0, game c99ea59c...d5d3). claude/integration = d9c7e5f0 (0.93.2; USER OK ~17:47 UTC; ff by BM18 ~17:58 UTC, sha checked). Pending from the user: tap-test Download my save / Load a save file on the live page. User's current-save link 6daNCLCJAcsLCZn27CEthq (0.92.2): NEVER publish over it.
- 0.93.2 = claude/staging-0.93.2 (BM18). In it (all reviewed PASS, switches ON unless noted): event-swap (EV_SWAP_ON OFF), steps-quiet, inspection (INSPECT_ON; incl. 1872153 Day-1 guard + 5793626 "Stand by your berths"), save-slots (SAVE_SLOTS_ON), auto-doors (AUTO_DOORS_ON; lift door always auto), trad-0932 (TRAD_0932_ON), promo-beats (PROMO_BEATS_ON), comet 157d1cfb (EV_COMET_ON), tray-seat-0932, storm-sat 6f19944d (STORM_SAT_ON; storm board never hides your own work), saves_check fix a1df5739 (http route), p926 check fix (CR3 6a527c10).
- Round 1 (41c8a7e0) found: mech m9 (fixed), arrows week (inspection, fixed), workbench tap clash Day 8 (FX24 claude/workbench-tap 484cde7d, with RV18 now), saves migrate (test file:// quirk, fixed in check), p926 (stale check), perf = noise.
- NEXT: (0.93.2 done) hire a fresh CR4 (plans/handover-check-runner-4.md on claude/checks-cr4); then Pillar 5 Steps 5-6 per the v3.1 plan (spec page first).
- 0.93.3 backlog: RV18-C5 (bedtime arrow hides the comet knot arrow), RV18-C6 (lone comet speaker repeats), FX26-1 (join toast twice / "About 44 minutes" after a late join), FX26-2 (only 4 storm-stories asides), FIX_PARKED chores (sh-lamp/press/grinder) can return after the workbench fix, controller audit of 0.93.2's new UI (Saves app, Take a seat, door tap with Auto doors off, join cards).

## The user's roadmap (14:05 UTC Oct 26)
After 0.93.2: Pillar 5 Steps 5 and 6 → 1-2 more ship-wide events (the visit Days 16-19 with EV_SWAP_ON, the Veyli vessel Days 27-30 are planned in EP1's events page 7w7UgrR71rk5VknPhBExSc) → content complete → a full controller pass → optimization → playtest patches.
- Steps 5-6 plan v3.1 (agreed, all answered): https://claude.ai/artifact/5paPxnWk9tMPXg6JwR3NvL (source plans/pillar5-steps56-plan.html on claude/events-plan-2 c827f392; answers in page db answers/user). Key user answers: recommended Q1-4, Q6; Senior Officer's bar in the OBSERVATION ROOM; Senior Officer stays in 4-23; Deck 2 senior quarters at Tier 4 (Thu Day 25 after dinner, Vance walks you). Section 13 lists pieces, switches, owners, checks (incl. controller_check per piece), team: 4-5 builders + deck architect + head writer + 2 reviewers + BM + six runners. Start with each step's spec page. design-doc: update the tier table/laundry line when Step 5 starts.
- User rule (14:16): every new piece works with a game controller as it's built; controller_check in its checks.

## Seats (see TEAM.md CURRENT SEATS + later lines)
BM18 01A3S2VBMYmTt2wCZa8ej7XR; RV18 01PMfvrCN6StPzwVSPGX7ijH (~50%); RV19 01V6FDCQp5Ejidi8Chpo2nJG (~49%); PUB1 01GnpjFR6oumvuvTrmcXSqeg; runners CR1 01CsWNjCsy8u5mrHJgTVgCst, CR2 01DsTDi6xJcpdDVhSkELEm24, CR3 01Pw3EQ24pSz4gjsFcLBMjUF, CR4 01636CfY2MhB3DzrzZ59dhXz (~58%, retire after round 2), CR5 01CHoEsvv7zMPZDr1ir7uAiz, CR6 013wLtAmKooMrgGrXF4Ljiof; writer SW2 017dLaLFBnRUQin3PQEQq6so.
Idle/near-done builders: FX24 017zuWxNJfppnVwkQDtiwnb6 (~60%), FX26 01Mda2GWi1hRm17TjvYmHoED (~57%, handover-fx26), FX27 019Qp5uSM5piXqZXYFENDvkK (low), FX28 01SfsTrhybVq5KEc5AF7Vhqt (~45%), FX20b 01ForKrDZQQCL59hA3yZDfD3 (~35%), EP1 01LjeoeX6qpCuwTV5UNVNwV5 (~60%, handover-ep1.md 3c105d55). Retired: FX20, FX22b, FX25, SD1, CS1, lead 37.

## Gotchas learned this shift
- Messages arrive late (up to ~3 h); builders kept reporting to lead 37. Tell each seat your id directly and repeat shas to reviewer + BM.
- A check run on a builder's own machine under load can mislead (FX26's mech promo FAILs were load/wrong copy): confirm on a runner alone before acting.
- file:// in Playwright can hand a reopened page a fresh storage (saves_check); serve via an http route when a check reopens a page and reads the save.
- Switch-on interactions show up only on the combined staging (inspection Thursday vs dawn swim, arrows week): run arrows_check week + events_check on staging before the round.
- User times always in US Eastern; plain words; no emojis; few messages.
