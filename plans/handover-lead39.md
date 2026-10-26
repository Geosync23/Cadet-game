# Handover: lead 39

## START HERE (next lead)
Read CLAUDE.md, this note, then the bottom of TEAM.md on claude/lead-39 (from "LEAD 39 started", ~17:58 UTC Oct 26, every line after). plans/handover-lead38.md has older background.
Lead 39 = session_019V68fz33UFv4cK5Z4iCDvi, branch claude/lead-39, hourly check-in trig_01AfELgSjcRd9vZXQhCYUS8e (57 * * * *): disable it when you take over and make your own (copy its prompt, update it).
Lead 39 handed over at ~67% memory (~22:00 UTC Oct 26 = 6 PM Eastern).

## User rules from this shift (in TEAM.md too)
- **Keep reducing the workforce**: archive each seat as soon as its piece passes review and its handover is pushed; no new hires unless a seat is the long pole; replace rather than add. "This is not 3 or 4 days of work." Account shows a seven-day usage-limit WARNING.
- Steps 5-6 (and every new piece): **tons of arrows, super obvious progression** (level-1 arrow on the day, forced ring line, notices/Tracked/Schedule, hourly notice if holding another job, in person first, Mail only as record) and **pronounced moments with dialogue** (staged scenes, replies, reactions, close line). Every piece works with a game controller (controller_check).
- Doors: 3 settings (all auto / private rooms tap (DEFAULT) / all tap). Private = the 8 Deck 4 bunk-room doors. An arrow's way opens its doors; free walking stops at a private door with a hint.
- Visit switched ON (EV_SWAP_ON true) in 0.93.3.
- Ship-wide events: only "A Veyli vessel needs help" (Days 27-30) more; answers C1 commendation yes, C2 ship visible yes, C3 Taavek+Calder WAIT at the ramp up to an hour (Calder finds you 09:45, Zeke after 10:30).
- **The ending** (user's design): "Crossing back" as a ship-wide event (Sun Day 35, you lead Basil's oath, Veyli ship alongside, Captain's final address) + a transfer offer to Concord HQ (Thu Day 32, ready room, Captain + Calder; "the Admiral" is the Captain's FISH, never the offerer). STAY = endgame forever (no more promotions or ship-wide events, ~420 new endgame lines). GO = big goodbye Mon Day 36 (~60 crowd in the shuttle bay, Zeke last at the ramp), then the end page. Answers: NO way back (end page = Keep this ending / Start a new game; kept-copy code parked OFF), change mind until the Captain's address, post worded by Calder's answer.
- Steps 5-6 answers: all recommended (early Dev link after S5-2 YES, power safety lesson, mealtime shutdowns allowed w/ grumble, weekly Monday briefing, four answers to Calder).

## Specs (claude/p5-specs; published, db answers saved)
Step 5 https://claude.ai/artifact/9z1tyZ5faB6CPKt94DnN3N, Step 6 https://claude.ai/artifact/VZhNq1rnzRZYwtbjqJvxCo, vessel https://claude.ai/artifact/2myoLxPTGThJHJXiKR7LHp, ending https://claude.ai/artifact/RdFqHF7kBNyTjAvqzwHAVq. Latest spec sha 79c4d275+ (ladder rule) / 696aa679 (ending answers). Planner EP2 archived (plans/handover-ep2.md).
Job slots: 25 t3, 26 t4, 27 vessel, 28/29 P4/P5, 32 m19, 34 m20, 35-37 Step 6, 38 P9, 42/43 m18 (33 free).

## State at handover (~22:00 UTC)
- LIVE 0.93.2 (Playtest 3HqM v6, Dev 9ZWA v6). Never publish over 6daNCLCJAcsLCZn27CEthq.
- **0.93.3 full round RUNNING** since ~21:41 UTC on staging-0.93.3 19400976 (game ec93b94d...d085; doors bdb6f00a + visit on + SW2 words + FX29 check fixes). ~65 min (interactions_check now ~64 min: BM18-1). Next: BM18 GO -> PUB1 publishes BOTH links (keep capabilities {downloads}) -> ff integration ONLY with the user's OK -> tell the user (Eastern time).
- Step 5 (P5_STEP5 off; RV20 reviews): B1 S5-1 DONE (3da2b3a1), finishing small items (ladder rule per EP2, Power safety asked in person, comet Senior line) then retires. B5 (new) builds S5-2 the promotion on claude/p5s5-promo; when RV20 passes it, publish an early Dev link (?p5s5) for the user. B2 M19 (9f49eda0) fixing RV20 musts + **claude/workstep-tap-fix (LIVE bug in 0.93.2: M15 Rewiring jobs play as a generic repair; ships 0.93.4 on its own)**; then B2 hands over. B3 S5-4 shutdowns DONE (5ad090ff) -> then S5-5 M20 from B2's handover. B4 S5-6 puzzles: P4, P5, board done; P9 next (shared hook with B3).
- Vessel (EV_VESSEL_ON off; RV21 reviews): VB1 V-1, V-2 done (73942e8a); V-3 chain, V-4 making the part next. VB2 sky/props/poses done (cfc2dbe3), idle: earmarked as Step 6 deck architect (S6-4).
- Ending (EV_ENDING_ON off; RV21 reviews): combined branch claude/ending-crossing (EN2, da1f8e14 + EN1's later cd4196d5 fixes to merge). EN1 writing a few keys, retires after RV21 PASS. EN2 to finish merge + report events/day 35-36.
- FX30: week-guide FAIL is a CHECK gap (test-only fix in arrows_check.py coming) + stale team-job arrow item.
- Step 6: not started. Build after Step 5 lands, reusing Step 5 seats with memory left (VB2 for S6-4).

## Seats (active)
BM18 01A3S2VBMYmTt2wCZa8ej7XR; PUB1 01GnpjFR6oumvuvTrmcXSqeg (idle until GO); RV20 01PyJwfvfQVu4oXTYDMGkacw (Step 5); RV21 01AmTyMHLr5UuCY9zo3nQcwS (vessel + ending); runners CR1 01CsWNjCsy8u5mrHJgTVgCst, CR2 01DsTDi6xJcpdDVhSkELEm24, CR3 01Pw3EQ24pSz4gjsFcLBMjUF, CR4 01RgnU5d6Um75LNznFSotXYH (fresh), CR5 01UH1U1UpsoL7viYaRRBu2bZ (fresh), CR6 013wLtAmKooMrgGrXF4Ljiof; B1 01GeUbys3v6keTivBrcgHznP (retiring), B2 015mjNkxuGoEZGKA2ksBPz9u, B3 014FBmsiTsA9QymoN2qt4NyL, B4 01LV8Q8UV6aJPTgmQ6ub1z8G, B5 01CgbXRamJJp66pFTP43KYoB; VB1 01UsjGN26E88zwrNPWwef4iT, VB2 01KRBGtugjBpv5iGcV5WDvCP; EN1 01Py28Kh6QV9kk64ri5AzQ5B (retiring), EN2 013er8NqC8eftyZqXBzcSibF; FX30 01HSG9H3UnSNhTDxZtKoACnB.
Archived this shift: lead 38, FX20b, FX24, FX26, FX27, FX28, FX29, EP1, EP2, old CR4, old CR5, SW2, SW3, SW4, SW5, SW6, RV18, RV19.

## Gotchas learned
- **Messages lag badly** to seats in long turns (EN1/EN2/B3 missed several). For must-know corrections use send_message priority "now" and ask for a "got it".
- Lead can't push to non-lead branches (blocked): delegate every branch change.
- Builders sometimes branch from a stale local staging: tell them the exact staging sha.
- Two seats building the same skeleton (EN1/EN2) happened: name ONE owner for shared heads/switch lines/checks.
- Test-only fixes run green on staging can go in without a reviewer (BM18 runs them); note in the build table.
- Backlog this shift: BM18-1 interactions_check ~64 min; RV18-D1 hint title in all-tap mode; B1-1 affected.py day17/day22; live M15 Rewiring tap bug (being fixed); possible stale team-job arrow (FX30); junction-room darkening (later polish); packed cabin + Dev presets Days 32-36 (ending, later).

## Waiting on the user
Tap-test Download my save / Load a save file (said "later").
