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
- **Latest sha: claude/p5s5-promo e7ff9253** (S5-2 all four turns + the teacher fix). I own 24 core and 24u for Step 5 now
  (B1 retired). RV20 has 762d9cb5 + e7ff9253 to review; no verdict yet.
- **Teacher fix (e7ff9253):** `p5TeacherWait` in 24u via B1's `p5Escort`: for ps/m19/m18/m20 the teacher goes to the
  meeting's place from 30 min before (`P5_TEACH_LEAD`; the appointment's place, else a place in the room), and a self-led
  lesson's teacher follows you during 'do'. RV20's probes (claude/review-rv20 plans/rv20-m19-live.py, rv20-sd-live.py) on a
  scratch merge with mech-a + mech-b: Calder in the relay room from 10:50 for 11:00 (B2's own early booking was in that
  merge too, so this one alone doesn't prove the fix), at the port junction from 08:49 for 09:15 (no workaround there).
  Not seen directly: Calder staying beside you on M18's screen (the probe saw her in the lift lobby at 09:18).
  B2's and B3's own early appointments can go once merged.

## The arrow-follower's three ways: redo on e7ff9253
- As is: **OK** (on 762d9cb5): offer in person, test Day 15 first try, result, bar, cake, toast all met.
- **Teaching arrows Off: FAILED** (on 762d9cb5), a real bug to fix next. On the test morning the follower ping-pongs
  Deck 5 <-> Deck 3 from 09:00 to 09:14 ("walk to: Your Tier 3 test, 09:00: the Works bay", then "lift to Deck 3", over and
  over: some other arrow pointing to Deck 3 alternates with pu3:testday, which stays up till 09:15 even once the job is
  on the board); at 09:15 it takes another job (filter bank) and works it all morning; pu3:test never leads (by design it
  yields while you hold another job), so the test lapses at 15:00 and is set again (Day 17, then 19). Fix ideas: end
  pu3:testday as soon as the job is on the board; find what points to Deck 3 at 09:00 (scratch: arrows_check internals,
  real_game(pg, 15), puSet(15), Follower.run to 13:00, print f.acts from 08:20); give the test's Take it priority over
  other jobs on its morning.
- Tracking another job (`track`): not run (stopped).

## Open
- Known old: the team job's "hold it steady" arrow (FX30) shows as "stuck" in the follower; not Step 5's.
