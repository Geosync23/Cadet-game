# Handover: lead 24

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
