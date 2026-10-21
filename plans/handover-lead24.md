# Handover: lead 24

## START HERE (new account, new lead 25)
1. Clone github.com/Geosync23/Cadet-game (the new account needs GitHub access to it). Start your branch claude/lead-25 from claude/lead-24.
2. Read CLAUDE.md, this whole note, TEAM.md (bottom), plans/handover-lead23.md (publishing recipes + standing rules).
3. Every old seat is stopped; their sessions belong to the old account and can't be messaged. Start FRESH seats from each role's handover note (list below). Keep to the user's seat count and watch usage.
4. Republish the game pages from claude/integration (the old pages belong to the old account): a Playtest page (title "Starship Cadet Playtest <build>") and a Dev page (first-line #dev script, recipe in handover-lead23.md). Tell the user the new links.
5. Make your own hourly check-in scheduled task.

**Current build: 0.64.11** = claude/integration 70aa91f (Dev mode Stop 2, Fridays groundwork switched off, new crew Day 21 + Tern ramp both ways, closer camera, food_check fixes). Possibly + DB2's check-only devmode seed fix on top (see BM12's handover).

**Next release (top priority):** storm S10 (claude/storm-update 0b77dfcb, PR6 PASS) + Fridays turn 10 (claude/fridays) switched on TOGETHER. Before it: FR3's `arriving` Day 19 fix and PR8's old-save-on-Friday 18f fix (see handover-fridays-builder-3.md), PR8's final verdict, and check RN1's day_check Day 13 rec-deck note on the combined build.

**Role handover notes (one fresh seat per row as needed):**
- Build master: plans/handover-build-master.md (claude/integration)
- Storm builder: plans/handover-events-builder-6.md (claude/storm-update)
- Fridays builder: plans/handover-fridays-builder-3.md (claude/fridays)
- Line builder: plans/handover-line-builder-2.md (claude/line-update) — next: double-dinner root fix in section 14 (lead's call), ER3 fix 9, Brennan rota line, then ER3 part B, then L6 switch-on
- Line reviewer: plans/handover-event-reviewer-3.md (claude/event-plan-review-3)
- Reviewers: plans/handover-reviewer-5.md, -6.md, -7.md, -8.md (claude/review-5/6/7/8)
- Optimization: plans/handover-opt-render.md (claude/opt-render), plans/handover-test-speed-2.md (claude/opt-tests), plans/handover-review-opt.md (claude/review-opt)
- Events check: plans/handover-events-check-1.md (claude/bigevents-check); food check: plans/handover-food-waits.md (claude/food-waits)
- Crew patch (done, merged): plans/handover-patch-crew.md; Dev mode (Stop 3 when the user asks): plans/handover-devmode-2.md; patch/section owner: plans/handover-patch-builder-b.md

Lead session session_01SDe7z5Nr7u69uH1k4sjZ8r, branch `claude/lead-24` (push only there; started from claude/lead-23). Took over from lead 23 at ~12:43 UTC 2026-10-21. Hourly check-in: trig_01C2doV45RKiUmbkRUeJqZSk (minute 41): a successor disables it and makes its own.

**ACCOUNT MOVE (the user, ~15:31 UTC):** the project is moving to another account. All seats were told: push everything after every step, finish the current turn, no new round over ~60 min without asking, refresh handover notes, reply with stopping point + ETA. Published artifacts (Playtest / Dev pages) belong to the old account: the new lead republishes them from the branches (recipes in plans/handover-lead23.md).

Read first (new lead): CLAUDE.md; this note; TEAM.md bottom; plans/handover-lead23.md (publishing recipes, standing rules); plans/overnight-decisions-lead22.md.

## Standing rules (the user)
- Day mode: up to **14** working seats (the user, 14:21). Future peak ~18-20 with two leads.
- **Push a notification for every question to the user, every new build and every milestone** (the user, 14:06).
- Handover at 500k (warn) / 600k (hand over) for every seat, the lead too. "Identity verification is required" on any seat → tell the user at once.
- **Never change the look of the game** (pixels identical); no texture cache. One exception: player_check may skip drawing in polling/arrive steps nothing reads (14:13).
- Main and the main game link untouched without the user's go. Cut things parked, never deleted.
- 7-day usage limit at allowed_warning (resets 2026-10-24 ~16:00 UTC).

## The user's decisions this shift
- Line supper SEATED sittings (like the lantern supper). Trifold = Samsung Galaxy Z TriFold (derived CSS sizes 412x960 folded, 792x1080 open; Dev Speed card will confirm).
- Opening camera 1.85/1.40 is good. Leavers board the Tern up its ramp (built, T3).
- No CPU-canvas texture option (look must not change). Fix B for player_check: yes.
## Lead calls this shift
- Storm + Fridays switch on in ONE release (Day 12's speech names the storm).
- Dev mode: a calendar tradition in the same room gives way to a Dev start.
- Line volunteer jobs held to 13:45 (was 14:15).
- Line supper bigger: pull 1 + 30-45 min stays (~59 come, peak 40 of 48 seats); bigevents: seated gatherings capped by at-once vs seats, not "60 meaning to go".
- #7 lighter frames and the kit shape cache parked (measured, small). #5 memory fix (unloadDeck detaches old tree, ~80 MB) OK'd.

## Builds
- **0.64.9** claude/integration f782c5d = 0.64.8 + Dev mode Stop 1b + Stop 2. Dev page https://claude.ai/artifact/EWB21cTQnXc8ZT71zCeEzf version 4. Playtest page still 0.64.7 https://claude.ai/artifact/82sEvZTAtj1ezCuv6iAAad.
- **0.64.10** claude/integration c6f665b (Fridays off + food_check fix). Playtest https://claude.ai/artifact/Vx6uXaHnAfZsMQs8DHZJmh ; Dev page v5.
- **Next:** one release with storm S10 (EV6) + Fridays turn 10 (FR3 0dc45624) switched on together → NEW playtest page + Dev page. Then PT1's crew patch (T1-T3 + check fix), opt (#4, #10, #6, perf scenes, #8, #5, TS2 item 2), then the Line (after ER3 round 2 + L6).

## Seats (15:35 UTC) — see TEAM.md for branches
Working: FR3 session_01935gmiyLoy5fgvs3xQd7QC (Fridays; #20 fix) · PR5 session_01Eh4drBZjJ82DjYx6XaTt1F (Fridays 7-9) · PR8 session_01Nrvf1SYaXHTLwssGoBfJ54 (Fridays turn 10 + fixes) · EV6 session_012u45Yq4bSmo6bgqe5phZ9b (storm S10, local) · PR6 session_01LVHLJHrAR5iGJFS7HK9E7i (storm + Line + EC1) · EV7 session_01WeSNWT2a7Fs8HS3j9HWamK (Line L5e + bigger supper + 'everyone' bug) · ER3 session_017jM4m1bcqPHbSesi2kSfLr (Line round 2) · BM12 session_01Pdzb8wT4UA5tPgwQStRoqd · PT1 session_013KBHqs7JLoNRVFCVWdfngN (crew; lift-vs-ramp check) · PR7 session_01LyKAVtCEedL1bP73vqzu9v (PT1) · TS2 session_019Ue76BxEtDwCcqQjJHjFHp (opt tests item 1) · RN1 session_017qkNbUvRUfJqz24bLzTaR3 (opt render; #5 proofs) · OR1 session_015np4rHB2UHzet5Y1zFrBzm (opt reviewer) · FD1 session_01YJhagf6oyF6SeT5XGvrL5H (food_check 4k) · EC1 session_01QgShGXD6P24DDxTp8npN41 (seated-cap rule).
On call: PB session_01FWW2piuXkFYaRRzLXZiqYb (13/14/10), EW2 session_0138EzUAZjAJ3rUMiwyK3m3p (writer). Idle: DB2 (handover plans/handover-devmode-2.md), lead 23.

## Open items / backlog
- #20 Halloran never reaches the tea corner Day 5 (PB's fix, FR3 builds). #21 devmode_check clock flake. #22 cooker fault churn vs late meals (design call). #18 day 12, #12 career, #14 perf memory (old).
- Dev mode Stop 3 (Big events) when the user asks.
- The user to screenshot the Dev Speed card on the TriFold folded + open once #8 is published.

## Later updates (16:15 UTC)
- 0.64.10 published (Playtest https://claude.ai/artifact/Vx6uXaHnAfZsMQs8DHZJmh, Dev page v5). 0.64.11 = crew patch (PT1, all reviewed) + food_check part 2, BM12 running checks.
- Storm S10's 3 FAILs were check problems (EV6); PR6 re-runs them for its verdict. Storm + Fridays release = BM12 merges claude/storm-update (dc0ebe0b+) and claude/fridays (e18844fb + FR3's `arriving` Day 19 fix) together, after PR8's verdict on turn 10/fixes and PR5's mutants.
- Line: L5e pushed, L5f (bigger supper) in its round; then ER3 round 2, then L6 (switch on). Brennan rota clash at the ceremony (EV7). Merge note: keep both food_check changes when food-waits meets line-update (FD1 handover).
- TS2 item 1 (affected-checks runner): batch 1 map done; options (a)/(b)/(c) in plans/handover-test-speed-2.md; TS2 leans (b) (ignore near-universal shared lines, prove by replay with batch 2). Lead leans (b) too; not yet asked of the user.
- Opt in review with OR1: TS2 item 2 (player_check A+B); RN1 #5 memory fix (proofs ~17:00). Passed: #4, #10, #6, perf scenes (+F1-F4), #8 Speed card (DB2 owner OK; nits to RN1).
- Ready for the move: PT1, BM12 (after 0.64.11), ER3, DB2, EC1, FD1, EV6, PR7, TS2, PB, EW2.
- 17:45: 0.64.11 claude/integration 70aa91f (crew patch). Playtest https://claude.ai/artifact/MMoknq9PDzBk264PjmkoLa ; Dev page v6. The 5-hour limit paused all seats 16:20-17:40; resumed.
- 17:45 Line: EV7 idle at claude/line-update 8bfff3b (L5f bigger supper pushed). NEW: day_check 7 fails on L5f: a diner not at the supper eats dinner twice (section 14's double-dinner shape, also on base Day 21), exposed by the fuller mess. **Lead's call: fix the root cause in section 14 (PB's section), not a smaller supper.** Next steps for the Line (after the move): (1) that fix; (2) ER3 fix 9 (Lemaire/Reyes/Yoon skip their ceremony); (3) Brennan rota line in food_check (keep both copies at merge); then ER3 part B, then L6 switch-on. See plans/handover-line-builder-2.md.
- Fridays: PR5 final PASS (7-9 + 11b2220); PR8 turn 10 PASS WITH FIXES: release set = Fridays + storm update together; FR3's `arriving` Day 19 fix + a new 18f fix (old save loaded on a Friday evening gets a false missed-address dip/Mail) pending with FR3.
- 17:51 Opt: RN1 idle (claude/opt-render dfd662d): #4/#10/#6/perf scenes/#8 PASS; #5 memory fix (~78 MB less, all proofs green incl. event branches) with OR1. RN1 note: on a local merge with storm on, day_check Day 13 FAILs "rec deck on but nobody came" (storm Saturday empties the rec deck; same with/without #5). EV6's own S10 round passed day 11-15 and EV4's 4fa198f added a rec skip on storm-shut days, so check this on the real combined build before the storm+Fridays release.
- EV6 idle: storm-update 0b77dfcb (mech m17 check fix). DB2's devmode seed fix 841a9d0 → BM12 pushing to integration (check only).
