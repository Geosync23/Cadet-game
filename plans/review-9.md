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

(That first merge used fridays 6e8e0af; it was rebuilt on f83c8db once FR4's 5b55f84 landed. The round below is on
the rebuilt one, game = f83c8db's = 3bd9b2c's = 951c0cd's.)

**The round on it (each alone):**
- check_fast: QUICK CHECK OK (393 s).
- cadet_test integration 0.64.11 → the combined build with both switches off: ALL IDENTICAL.
- fridays_check: FRIDAYS CHECK OK (1721 s). Day 12 at 16:10: 51 seated, **lectern ['marrow', 'vance']** (PR8's find 1
  closed by the storm update); the storm's lines all fill (only `myshift:night`'s never do); the old save at 18:00:
  `[5, 0, 50, 0, 0]` (mailed, heard, work, count, Mails).
- day_check 5, 12, 13, 19, 21: DAY CHECK OK each. 12 and 13 print "the rec deck is shut for the ship-wide event this
  evening (the storm update): its evening comparison is skipped". The combined day_check.py is storm-update's
  byte for byte; the Day 12/13 FAILs others saw came from an older day_check.py without EV4's 4fa198f.
- events_check: EVENTS CHECK OK, **quiet-watch Day 300 Deck 3: 8/8** even with the old check (PR8's 7/9 knock-on
  doesn't show on the real combined build). The control copy (Fridays off): OK, the same 8/8.
- bigevents_check: BIGEVENTS CHECK OK.

**Live probes (`p9_fri.py`, a real save, 390x844):**
- Day 12 from 15:56: 49 → 54 seated by 16:16, lectern Marrow from 15:56, Marrow + Vance from 16:04, lines 0 → 9 said
  by 16:28 (FRI_SAID). (The 16:30 shot timed out on the software renderer; re-taken on the RC below.)
- Day 19 from 15:55: lectern Marrow + Vance all through, 45 → 49 seated; the 12 lines include "In between, we say
  goodbye to Theo" and "And at dinner a new junior comes up the Tern's ramp", said in order (line 7 at 16:30).
  Shot `shots/rel19_d19_1630.png`: Marrow's named bubble readable. ("cadet, three weeks with us": `{me}` is the
  probe save's default name; real players type one. A game-wide pattern, not Fridays'.)
- An old save (no fri) at Day 5 18:00: at 18:12 `[heard, mailed] [0, 5]`, work 50, address 0, no toasts; the one Mail
  is Pell's "Film night has moved" (the events base), not the Captain's. Shot `shots/relup_up.png`.

## 5b55f84 (FR4: PR8's find 3, an old save on a Friday evening): PASS

Code: `FRI_OLD` = the save's day when it has no `fri` part (cleared by a new game); friAddressTick reads and clears it
on its first frame; after the address's end it sets `FRI.mailed = d` instead of friMissed. A save loaded before 16:50
still misses at 16:50 (a judgement call: an old save loaded at 16:47 gets the dip with no heads-up; the same as a new
save at 16:47, and once).
- fridays_check (FR4's two real localStorage loads): OK on the combined build (above).
- Mutants against FR4's fridays_check (f83c8db): `m14_noold` (the guard gone) **CAUGHT** ("an old save loaded on a
  Friday evening got the missed address [[5, 0, 48, 1, 1, ...]]"); `m15_noclear` (FRI_OLD never cleared) **CAUGHT**
  ("an old save loaded before 16:50 not missed at 16:50").
- Live on the combined build: no dip, no banner, no Captain's Mail (above).

## 3bd9b2c (FR4: events_check's deck walks, backlog #24): PASS

Check only. A walker counts if they settle in the seat `planWhere` gives them at that minute (an `ev-<id>` segment on
that deck), so a re-plan by the week's friendships doesn't count as a miss; a no-show still counts as missing (they stay
in `att`). It is what my own probe (dropped once the combined build showed 8/8) would have counted. FR4's planted
no-show: still FAILs.

## 2078010 (FR4: the #20 hold fix): withdrawn

PB2 failed it (Day 0's arrival dinner); reverted in 951c0cd (game = 3bd9b2c's: `git diff f83c8db 951c0cd --
starship-cadet.html` is empty). Not in the release; the release ships e18844f as reviewed above (its hold doesn't fire;
the fallback gets Halloran to the tea corner). The proper fix is on claude/fridays-20 (PB2: PASS), after the release.

## The release candidate (0.64.12): integration a4a5735 + storm 0b77dfc + fridays 951c0cd

Built locally: sha256 `23fb9118abc3679fd1eea658a072817fd6f2831a9560f1bf86358ada768cb7df`, the same as CR1, CR2 and
CR3's. Against the build of the round above it differs only in the build number and 0.64.12's camera zoom (1.62/1.22).

Lead 25's check runners on it (their notes on claude/checks-cr1 90bc8b3, checks-cr2 37b9383, checks-cr3 5a609c8):
- CR1: player, intro --week (on; and a Fridays-off copy), --firsts, --evening, interactions, clothes, bubble, devmode:
  all OK.
- CR2: talk, social, join, lines (0 errors; 49 warnings, all the storm meetings' "same line also in"), lines --day,
  food_check 1 7, mech: OK. career_check FAIL (backlog #12, the same on integration). food_check 11 4 FAIL (the
  harvest salad: Day 20 is now the farewell supper; the same on plain a4a5735, from the crew patch 0.64.11).
- CR3: arc, path, disc, puzzle, deck OK; perf under 450 everywhere (flags: the Friday scenes, Fridays off on plain;
  memory #14); tiles_check's old FAIL was the check's timing (fixed in the check, after the release).

Mine on it: check_fast QUICK CHECK OK (353 s); fridays_check FRIDAYS CHECK OK (1542 s). events_check (with 3bd9b2c)
EVENTS CHECK OK, quiet-watch Day 300 Deck 3 8/8. Live Day 12 (`p9_fri.py rc d12`): lectern Marrow + Vance from 16:04,
54 seated, the storm's 17-line speech, line 10 ("What I need from you. Stay in when you can...") at 16:30 in Marrow's
named bubble; shot `shots/rc_d12_1630.png`. (The probe's `eventOn('ionStorm')` reads null: eventOn takes a day, the
probe's slip; the storm lines prove the storm is on.)

## FINAL VERDICT: the release (Short Fridays on, with the storm update and EVENTS_ON): PASS

For 0.64.12 = integration a4a5735 + storm-update 0b77dfc + fridays 951c0cd, both switches on as merged, game sha256
23fb9118...cb7df. No blocking finds. PR8's three turn-10 finds are closed: (1) Day 12's lectern (by the storm update:
Marrow and Vance speak, live and on paper); (2) Day 19's welcome (c3b76f4, PASS); (3) the old save's Friday evening
(5b55f84, PASS, mutants caught, live). PR8's quiet-watch knock-on doesn't show on the real combined build (8/8), and
the check is sturdier anyway (3bd9b2c, PASS). Off is identical to integration (cadet_test).

Not blocking, after the release: backlog #20's proper fix (claude/fridays-20, PB2 PASS; e18844f's hold doesn't fire,
the game copes live); backlog 25 (intro beats sharing a stand-in station on Days 1-3); the fridays_check gap for a
welcome said with nobody arriving; the old fails career #12 and food 11 4 (the harvest salad, from 0.64.11).
For BM13: plans/backlog.md conflicts on both merges (keep both sides' rows); take fridays' build-table block (it
already carries integration's rows); day_check.py must be storm-update's.
