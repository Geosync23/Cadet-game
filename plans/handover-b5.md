# Handover: B5 (the Works career engineer for Pillar 5 Step 5, S5-2 the Senior Officer promotion)

- **Role:** Works career engineer for Step 5 after B1, hired by lead 39; now owner of 24 core / 24u for Step 5 (lead 40,
  session_01NXybH7NNqM8M4ngiyidq6m). My session: session_01CgbXRamJJp66pFTP43KYoB. Reviewer RV20 (session_01PyJwfvfQVu4oXTYDMGkacw).
- **Branch:** `claude/p5s5-promo` (from claude/p5s5-career 3da2b3a1 + SW3's words claude/p5s5-words 277b9c15; then B1's
  51b1a9c6 and VB2's kit 69eb706d merged in). Build-table rows `0.93.4-s.5` to `0.93.4-s.8` (B1 has s.4). The two
  build-number lines are never touched.
- **Spec:** `plans/p5-step5-spec.html` on claude/p5-specs, "The beats" and piece S5-2. DEV_NOTES "The Senior Officer
  promotion (S5-2 ...)" has the map of what's where; design-doc "The Senior Officer promotion, as built".

## What's built (24u, behind `P5_PROMO3`; off: cadet_test ALL IDENTICAL)
- Turn 1: the offer in person (Calder seeks you from Day 14; the storm party's evening from 19:05; scenes pu3.offer /
  .monday / .party), notice + Mail, `SHIP.works.pu.t3` set only then; Schedule/Tracked, Training tab, What's next,
  reputation toasts, friends' luck Mail, crew talk.
- Turn 2: the test (`WORK_MECH.t3`, job kind `tier3`, slot 25, the worse Deck 6 junction): breaker, plan, warn two
  (chat card "About the shutdown"), off (vetoed until both know), breaker, back; passed at turn-in; delayed two workdays.
- Turn 3: result 08:15 (`pu3Result`; you sit in VB2's visitor chair `5-office-visit-sit`), `puPromote`, the bar
  (`pu3Bar`, guests on the ceremony spots, `spec.bar` on your collar via 24p's promoPip asking `puRank`), the cake,
  the toast (`pu3Toast`), keepsakes (pushed by the Captain's name: giftKeepsake keeps one a person).
- Turn 4: Dev mode's promotion list (`puDevSteps`) and career arrow (`puDevNext`); checks.

## Checks (on a copy with `P5_STEP5 = true` unless noted)
- `promo_beats_check.py ON t3before t3pointer t3passed t3result t3bar t3toast`; `t3off` on the build as shipped.
- `arrows_check.py ON step5` (about 40 min; `teachoff`, `track` for the other two ways).
- `dev_arrow_check.py ON pu3`; `saves_check.py BUILD promo3`; `controller_check.py BUILD promo3` (in ALL_PARTS).
- `day_check.py ON 15` and `16`.

## Gotchas
- `__tick` in promo_beats_check runs WORK_TICKS only: the ladder and trainTick need `worksCareerTick` / `trainTick`.
- Meetings register through section 18's occasionsTick: call it before meetingsTick on paper.
- A scene shown where you are (not in its room): set `r.f['met:' + r.key]` or its gist comes by Mail too.
- 15b's board takes registered kinds only if they're in its BOARD_KINDS (I added 'tier3'; B2's relayswap/battcell?).

## State at the stopping point (lead 40's call, 2026-10-26 ~23:40 UTC)
- **Latest sha: claude/p5s5-promo 5703dfb6** (S5-2 all four turns + the teacher fix e7ff9253 + the test-morning arrow fix 5703dfb6). I own 24 core and 24u for Step 5 now
  (B1 retired). RV20 has 762d9cb5, e7ff9253 and 5703dfb6 to review; no verdict yet.
- **Teacher fix (e7ff9253):** `p5TeacherWait` in 24u via B1's `p5Escort`: for ps/m19/m18/m20 the teacher goes to the
  meeting's place from 30 min before (`P5_TEACH_LEAD`; the appointment's place, else a place in the room), and a self-led
  lesson's teacher follows you during 'do'. RV20's probes (claude/review-rv20 plans/rv20-m19-live.py, rv20-sd-live.py) on a
  scratch merge with mech-a + mech-b: Calder in the relay room from 10:50 for 11:00 (B2's own early booking was in that
  merge too, so this one alone doesn't prove the fix), at the port junction from 08:49 for 09:15 (no workaround there).
  Not seen directly: Calder staying beside you on M18's screen (the probe saw her in the lift lobby at 09:18).
  B2's and B3's own early appointments can go once merged.

## The arrow-follower's three ways (`arrows_check.py ON step5 [teachoff|track]`)
- As is: **OK** on 762d9cb5 (offer in person, test Day 15 first try, result, bar, cake, toast met).
- Teaching arrows Off first **FAILED** on 762d9cb5 and found two real bugs, both fixed in 24u's `puTestGuide` (build
  table 0.93.4-s.10): (1) `pu3:testday` gave no goal once you were in the bay, so a Deck 3 arrow took over and the
  follower rode the lift Deck 5 <-> 3 from 09:00 to 09:14: now it points at the board in the bay and is gone once the
  test is on the board; (2) holding another job when the test went up (a ticket case held for you from 08:00) made the
  test's arrow yield all day and it lapsed: now a level 1 arrow "Your Tier 3 test is waiting: drop this job at the board"
  with that job's Drop it rung (forced). The follower now prefers the board row the arrow names. **On 5703dfb6's code the
  Off run met the whole promotion** (test Day 15 first try, result, bar, cake, toast); its one FAIL was the check's own
  expectation (pu3:drop led instead of pu3:test), fixed in the check.
- Tracking another job: **OK on 5703dfb6** (the whole promotion met; only the known-old "hold it steady" stucks, not Step 5).
- **All three ways OK on 5703dfb6** (run one after another, 00:16-00:32 UTC): as is, Teaching arrows Off, tracking another job.
- Run them one after another (side by side they slow each other and page loads time out).
## RV20's verdict (00:08 UTC) and after
- e7ff9253: FIXES NEEDED, one must (M1); 5703dfb6's arrow fix PASSED. **M1 fixed** (build table 0.93.4-s.11): `ladderBigP5`
  leaves trained rows out (machine_check "traced faults" was not the same twice: a trained-but-unopened Tracing was asked
  again, and the check's two runs share SHIP.occasions). machine_check on the on copy OK twice.
- Shoulds S1-S4 **done** (build table 0.93.4-s.12; promo_beats_check part t3shoulds): friends' Mail from 12:30; no "reputation down" toast at the promotion (15b's guideShiftWords, P5_STEP5); the visitor chair's toast has words (`pu3.result.sit`, a stand-in for the writer); Dev presets Days 17-18 follow the ladder (no m17).
- RV22's MUST on cbca3e3e (build table 0.93.4-s.13): the M1 comment had been put mid-line and disabled ladderBigP5's sort; moved to the line above, order re-checked (m19 before m17), machine_check twice OK.
- RV22 PASSED f00d93c1 (01:49 UTC) with one should: the friends' Mail filed at 08:30 dated 12:30; fixed in s.14 (`puFriendsTick`: filed at 12:30, dated then). Also from RV22/RV20 for lead 40: the ladder fix must reach B2's and B3's branches (they carry 51b1a9c6).
- Note for the systems engineer: machine_check's traced run keeps SHIP.occasions between its two runs (an isolation gap).

## Open
- Known old: the team job's "hold it steady" arrow (FX30) shows as "stuck" in the follower; not Step 5's.
