# Handover: lead 41 (first lead on the NEW account)

## START HERE (next lead)
Read CLAUDE.md, this note, then the bottom of TEAM.md on **claude/lead-41-e86n0x** from "LEAD 41 started" (every line after). Then plans/overnight-decisions-lead41.md (the user's plan order + the calls made overnight). Older background: plans/handover-lead40.md, plans/handover-lead39.md.
Lead 41 = session_01GKuymjWR1dqfbCw1MyEP9j, branch claude/lead-41-e86n0x, hourly check-in trig_01Bk5Qen4j2ZgBtkLYX1Qwd7 (53 * * * *): disable it when you take over and make your own (copy its prompt).

## The user's plan (in order; see overnight-decisions-lead41.md)
1. 0.94.0: DONE. Published on NEW links (Playtest https://claude.ai/artifact/7hQ14AcwZHCi5EvL1AKiMU , Dev https://claude.ai/artifact/KEyaHvon6ZaVHHFRdAe18m , {downloads}); claude/integration = 6f1915cb (user OK). Step 5, vessel, ending, talk-close all ON; older switches stay OFF (TRAY_TRAVELS, INTRO_ASK_ON, ZEKE_CABIN_MAIL, PAD_ON, END_WAY_BACK).
2. Step 6 (in progress) on claude/staging-p5s6, its own full round, then publish (PUB2 publishes to the same new links or new ones; ask the user).
3. Then the Dev mode update (all new traditions/ship-wide events + career progression).
4. Then the controller update (bring it current with every feature since it was made, then PAD_ON on).
5. Optimization. 6. Playtest patches.

## User rules (all still hold)
- **Questions for the user: always send a push notification** (PushNotification tool) or they won't see it (the user, Oct 27 ~9:40 AM Eastern).
- Live fixes escort-follow-fix (W7) + team-turn-fix (PZ6) ship WITH Step 6, no 0.94.1 (the user).
- CAP: at most **5 seats actively working at once** (idle seats don't count). Count before giving work or hiring.
- Full round of checks before any game change is published (spread over the runners the cap allows; test-only fixes need no game re-run; a words-only fix re-runs the word-related checks: decision 5).
- Tons of arrows, in person first, staged scenes with dialogue, controller, phones first. Times for the user in US Eastern, plain words, no emojis.
- Old account's links can't be updated from here; never publish over 6daNCLCJAcsLCZn27CEthq.

## Seats (new account) — state at ~14:00 UTC Oct 27
- BM19 build master session_01GKuymncYhRTKs8t4byNfdj: merges RV23-passed Step 6 pieces into **claude/staging-p5s6** (last known ce113792+; it was merging: escort-follow-fix cffe8187, promo4 up to 9dcd0b1a, nights 992a4b0; next team-turn-fix 12afb4a on PASS, MA6 db56362e, PZ6 91710ce, W8's turns, DA6's S6-5). Has the seat list; tells builders when staging moves. Then: the Step 6 gate, switch-on (P5_STEP6 true; older switches stay off), the full round, GO.
- RV23 reviewer session_01GKuymoDm1XbC5G8TvaCNLr (~50% memory; will hand over at 60%). Queue: team-turn-fix 12afb4a, N6 992a4b0 cadet, PZ6 91710ce, MA6 db56362e, W7/W8 S6-7 turns 2-4 (promo4 3cb048f2..92e5b38f), DA6 S6-5 turns.
- W8 career engineer session_01GKuymk95u5t4uDsahatkPN (claude/p5s6-promo4; from handover-w7.md): casePoint swap in S6-7, S6-9 the end (Calder's question Day 26 18:40), refit odd job + '2-B' leftovers (24t, 8b, HUD "Visitors' suite"), ALL Step 6 DM_CAREER rows.
- DA6 session_01GKuymjJ4sU5hfdU8bH49UW (claude/p5s6-deck): S6-4 DONE+merged; now S6-5 engine work (turn 1 9332d5a1 PASS w/ 2 shoulds; night 2 next: permit, badge, door, Watch; then controller part night 1).
- MA6 session_01GKuymj1UEDuEYMnG9rmFkc (claude/p5s6-mech-a): S6-2 + S6-6 DONE+merged (db56362e guard in review); now building arrows_check part 'step6' (the arrow-follower through all Step 6 beats, 3 ways).
- N6 session_01GKuymnDA25R2a5yZGYpaBS (claude/p5s6-nights): S6-1 DONE (992a4b0 PASS with the escort fix); idle for round fixes. Backlog N6-1: a let-go save doesn't load (pre-existing, section 20).
- PZ6 session_01GKuymjrmdGE4vaHHHGkvYF: S6-8 DONE+merged; team-turn-fix 12afb4a (LIVE bug MA6-1) in review; casePoint 91710ce in review; QUEUED for it when a seat frees: a check part proving a follow escort reaches a SEATED player (pu3) on top of escort-follow-fix.
- PUB2 publisher session_01GKuymkDxLVyt4rjtcJxdab (idle; handover-publisher-2.md on claude/publish-26). Step 6 publish: ask the user whether to update the new links (7hQ1/KEya) or make new ones (with a push notification).
- Archived: W6, W7, R1, R2, R3.
- Step 6 left to build: S6-5 (DA6), S6-9 + DM rows (W8), arrows step6 (MA6). Then the round + publish.

## Gotchas
- 0.94.0 is the first build with switches set to `true`: many checks looked for the OFF line. BM19 + W6 fixed puzzle, ending, saves, controller, events, promo_beats, mech; watch for more as Step 6 switches go on.
- Several "FAILs" tonight were check-follower gaps (career pick, mech t3, arrows week next to the mysteries board): bisect, then ask "would a real player get stuck?" before changing the game.
- Lead can't push non-lead branches: delegate. Seats sometimes duplicate work (two sweeps): name one owner.
- More than ~3 browsers on one machine gives false timeouts.
