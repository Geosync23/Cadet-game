# Review 9: Short Fridays (reviewer PR9, after PR8)

PR9 (session_01B1FUTc4sJR4Q5FFnx7L6Db), branch `claude/review-8`, from 2026-10-21 ~18:00 UTC. Lead 25
(session_01J2aTyEohBf8KFHCsTqt3LW); Fridays builder FR4 (session_01YDM1FcnY4nLuD7PN3JMK8R, claude/fridays).
PR8's results and finds are in `plans/review-8.md`. Tools: `plans/review-9/` (runner, mutants, probes); logs in
`plans/review-9/logs/`, shots in `plans/review-9/shots/`. Every check run alone, CADET_CHROME=/opt/pw-browsers/chromium.

## 208581c (FR3: PR5's turn-6 fixes): PASS

PR8's two open runs, now done:
- `player_check.py` with Fridays on: **PLAYER CHECK OK** (1817 s). The job loop gets past the auditorium seats.
- Mutants against its fridays_check (PR8's `mutants.py`): `m11_nohook` (no SIM_ADVANCE path) **CAUGHT**
  ("a jump across Friday 16:50 without the banner, Mail or dip [[5.95, 1, True], [5.95, 1, 33, 0, 0]]");
  `m12_mailnow` (the jump's Mail stamped at the jump's end) **CAUGHT** (`[5.71, 3, 40, 1, 0]`: no Mail at 16:50).

With PR8's runs (fixes 2 and 3 verified, check_fast OK, cadet_test identical), PR8's provisional verdict stands as a
full **PASS**. (Turn 10's open find 3, the old-save Friday dip, is FR4's and is reviewed below when it lands.)

## e18844f (FR3: backlog #20, section 14): PASS WITH FIXES (not blocking)

Checks (each alone):
- intro_check `--week`, Fridays on: OK; **d5-mug (Day 5 13:01, plan [5, intro, 5-tea-1]): heard 3/3**.
- intro_check `--week`, Fridays off (a copy): OK (d5-mug has no lines with the switch off, so it isn't tested).
- intro_check `--firsts`: OK (52 s). `--evening`: OK (414 s).
- day_check 1: DAY CHECK OK. day_check 5: DAY CHECK OK.

My probe (`p9_seats.py`, a new game with the intro on, Days 1-8 on paper: two people planned in one place at once,
where one of them is on an intro beat): 208581c 8, e18844f 10. The two new ones are both on Day 5:
`5-tea-1` Halloran (intro-d5-mug, 13:00-13:45) with Soto (tea 13:15-13:30) and with Calder (tea 13:30-13:45).

**Find 1: the hold never happens.** `introPlan` always sets `placeId` to the room's first place (`pl = ... near[0]`)
as well as `alts`, so shipDay's new hold (`!e.placeId && e.alts`) and introLay's matching dedupe
(`!e.placeId && e.alts && e.alts[0] === id`) are never true. `p9_tea.py`: Halloran's introPlan for Day 5 is
`{from 780, to 825, placeId "5-tea-1", alts [5-tea-1, 5-tea-2, 5-tea-3]}`, and Day 5's `occ.res` on the tea seats
holds only the evening's new-hands-tea (18:35-19:30). So the tea rota does **not** plan round Halloran, as the
commit says it does. Halloran reaches the corner only through the new fallback (`e.alts.find(free) || e.alts[0]`:
all three are booked at some point in his 45 minutes, so he takes 5-tea-1 anyway).

Live (`p9_tea_live.py`, 390x844, Day 5): the runtime copes. At 13:24 Soto is planned on 5-tea-1 but walks to
5-tea-2; at 13:39 Calder is planned on 5-tea-1 and stands with no goal (-1.53, -0.53) for his tea. Nobody stacks
on one seat, and Halloran sits and says his lines (shot `shots/e18_tea_1335.png`). So it works for the player, but
not as designed, and the plan has two people on one seat.

Fix for FR4 / PB (section 14, small): key the hold and the dedupe on `e.alts && e.alts.length` (an alts beat),
not on `!e.placeId`; then re-run my probe (the two Day 5 clashes should go) and intro --week. Before turning it on,
check that no two people have alts beats in one room at once (today none do: the beat list in `logs/seat_e18.log`;
Torres's d2-tea uses the same corner on Day 2, alone). Not blocking the release: the player sees the beat.

**Older, not e18844f's (backlog row suggested):** in both builds, on Day 1 Torres (his intro-d1-briefing, shadow,
lead and end beats, 08:50-16:45) is planned on `5-stool-1` while Halloran's ordinary plan has the same stool, and on
Day 3 Salo and Torres (intro-d3-pick) share it; on Day 2 Rina (intro-d2-health) and Oduya share `3-infirmary-6`.
Probably the same cause: an alts beat's seat is chosen in introLay after others are booked, and nobody else's plan
knows about it. day_check doesn't see it (test URLs start with the intro off).

## c3b76f4 (FR3: Day 19's welcome only with an arrival): PASS

Code: the bare condition `arriving` (content_gen's ADDR_KEYS; 18f's `friCond`): true when a rotation on Day d+1..d+2
brings anyone in; Day 19's "And at dinner a new junior comes up the Tern's ramp" line takes `? arriving`; the Mail
says "...and the weekend ahead" (the Mail takes no conditions).

Probe (`p9_arriving.py`, paper, the welcome line 1tvwp26, the leavers line vwvwab, `arriving` on Day 19 and 26):

| Rotation | arriving 19 | welcome | leavers | arriving 26 |
| --- | --- | --- | --- | --- |
| as built at c3b76f4 (first Day 35) | false | none | none | false |
| first on Day 20 / 21 | true | said | "goodbye to Theo" | false |
| first on Day 22 | false | none | none | false |
| Day 21, out only | false | none | said | false |
| Day 21, in only | true | said | none | false |
| combined build (integration 0.64.11: first Day 21) | true | said | said | false |

Nit (check gap, not blocking): fridays_check only fails a line that never fills; nothing fails the welcome being said
with nobody arriving (a mutant `arriving` always true would pass it). A two-line case in fridays_check (Day 19 with the
first rotation on Day 35: no 1tvwp26) would cover it.

## The release build (local): integration 0.64.11 + storm-update 0b77dfc + fridays 6e8e0af

`git merge` on claude/integration 70aa91f: storm-update conflicts only in `plans/backlog.md` (both sides' rows kept);
then fridays conflicts only in `plans/backlog.md` and `plans/build-table.md` (both kept). No conflict in the game or
the checks. Both switches on as merged (`SHORT_FRIDAY = true`, `EVENTS_ON = true`, `EV_STORM_ON = EVENTS_ON`); first
rotation Day 21. content_gen `--check`: up to date. names_check: OK. (For BM13: the backlog numbers 18b/20-23 come from
three branches; renumber when merging.)

Round: running (results below when done).
