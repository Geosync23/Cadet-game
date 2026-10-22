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

## claude/fridays-20 db001aa + 378e82b (FR4 with PB2: backlog #20 and #25): PASS

Code (section 14, not behind a switch; only with the intro on, so test URLs and every other check are unchanged):
- **#20:** a second pass in shipDay, in planning order, after every named seat is held: a beat with `alts` whose first
  place is a seat (SEAT_SOCIAL) holds the first seat of its alts not held for another intro beat then, unless a seat is
  already held for that person then (the escort's arrival dinner). The hold is marked `'alts'`, so introLay doesn't
  turn it into an `intro-seat` sitting (2078010's Day 0 break).
- **#25:** a spare station that one of the day's intro beats uses gets no stand-in that day; the person the draw picks
  stays at their own desk and leaves the draw for later stations (deterministic; it reshuffles later stations' picks).

My runs against the release's fridays (951c0cd), new game with the intro on, Days 0-8 on paper (`p9_plans.py`):
- Intro seat clashes (`p9_seats` rule): **10 → 0**. Three new holds (Day 2 5-tea-1 Torres, Day 2 3-bench-17 Eklund,
  Day 5 5-tea-1 Halloran), **all used** by their beats.
- Whole plans: **Day 0 identical** (the arrival dinner), Days 4, 6, 7, 8 identical. Changed: Day 1 (Halloran off
  5-stool-1, Volkov), Day 2 (Oduya 3-infirmary-6 → 3-infirmary-2), Day 3 (10 people: the stand-in reshuffle), Day 5
  (Calder, Kovac, Soto off Halloran's seat). Two people in one place at once (any place, standing spots included), per
  day: never more than before (Day 1 51 → 45, Day 2 46 → 45, Day 3 65 → 64, Day 5 42 → 40, the rest equal). Work
  minutes on Day 3 move by 1-3 at most.
- Live Day 5 (`p9_tea_live.py`): Halloran at 5-tea-1 through the beat; Soto sits at 5-tea-2 as planned; **Calder now
  gets a seat** (5-tea-2) instead of standing for his tea. No page errors.
- intro_check (full, the arrival evening in the real game included): OK. cadet_test 951c0cd → fridays-20: ALL IDENTICAL.
- FR4's own: intro --week (d5-mug 3/3), day_check 0/1/2/3/5, fridays_check, check_fast OK; PB2 PASS (section 14).

Nits, not blocking (PB2's two in backlog 26, plus one):
1. The alts hold ignores an event's holds (only intro holds are tested); none clash in Days 0-8.
2. introLay's `held` lookup wants the held seat within 2.5 of `alts[0]`; a hold on a later alt further away would be
   left unused (none is today: all three are used).
3. No check in the repo guards #20 or #25: day_check runs with the intro off, and intro --week passes with and without
   the fix. A small intro_check case (no two people on one place at once Days 0-8 with the intro on, my p9_seats rule)
   would.

## claude/fridays-20 169f0b3 (FR4: intro_check's seat-clash guard, check only): PASS

intro_check `--week` part 12 now runs my p9_seats rule first, on paper, Days 0-8 (Day 0 included): two people planned
in one seated place at overlapping minutes, one of them on an intro beat, FAIL (each named, the first 8; the count of
all). Run alone (`--week --beats=none`): on 951c0cd's game **FAILED**, "10 shared", the 8 named are exactly my list
(Day 1 Torres/Halloran 5-stool-1 x6, Day 2 Rina/Oduya 3-infirmary-6, Day 3 Salo/Torres 5-stool-1); on fridays-20 0,
**OK**. Nit: with `--beats=none` it also prints "not yet: the writers' beat lines are not in this build", which is
misleading there (the beats are only filtered out), harmless.

8d88993 (the nit): with `--beats` filtering every beat out it now says "no beats walked: none match --beats"; otherwise unchanged. One line, check only: OK.

# Controller support (CT1, claude/controller): reviewer PR9 (lead 25's ask, 2026-10-22 ~01:56)

Plan: `plans/controller-plan.html` (7dcfab05). The user's answers (the page's db `answers/controller-plan`, saved
2026-10-22 01:46): Q1 confirm by position (bottom button) with a swap in Settings; Q2 pause on disconnect if used in
the last 30 s; Q3 walk with the stick (no walk-to-goal button); Q4 vibration built, off; Q5 keyboard later; Q6 the
system keyboard, else a suggested name; **Q7 no tester page** ("I export and play outside of claude"); Q8 a
reviewer every two turns; and "Make this a separate branch". Review every two turns, adversarially. The hard rule: no
pad, the game is pixel-identical (cadet_test ALL IDENTICAL), no save or R() change.

## What I'll hold the turns to (sent to CT1 before turn 1)

1. **No pad = nothing.** With PAD_ON on and no pad: cadet_test ALL IDENTICAL; no new DOM node, style or listener that
   changes behaviour (a `gamepadconnected` listener only); no mesh made at load (the ring and any material are made on
   the first pad press, not made-and-hidden: scene children and draw calls unchanged); no `R()` call ever (the pad's
   repeat timers use real time, never the game's random numbers); the save byte-identical (no `pad` key unless a
   setting differs from normal).
2. **A pad seen but never pressed** behaves like none (the fake pad must mimic browsers: `getGamepads()` empty until
   the first press, then the connect event).
3. **Touch after pad = exactly as before**: the screenshot after a pad press then a tap must match the no-pad one,
   including no leftover `:focus` / `:focus-visible` outline on the last highlighted button (blur on touch), no
   button marks, no ring.
4. **The ring on the floor is not coplanar** (the phones rule: lift it off the floor), its colour through `col()`,
   one draw call, and it never shows in a no-pad screenshot.
5. **The reachability proof must not be circular.** For each panel, the check must list the clickable things from
   the page itself (visible buttons, inputs, `[onclick]`, `role=button`, and elements with click listeners or
   `cursor: pointer`), not from the controller's own panel list, and show each one can be highlighted, pressed with A
   (the same result as a click) and the panel closed with B. Any visible clickable the highlight can't reach fails. I'll
   plant mutants: a panel dropped from the helper's list, a div-with-a-click-handler button, a B that doesn't close.
6. **A on the deck = the tap.** The check compares A's result with the regression test's own tap on the same thing (a
   crew member, a seat, a machine, a sealed door, the lift) by the game's state after, not by the ring's label.
7. **Stick walking in all four view turns** (up the screen is up every time), and a let-go stops at once, through
   `player.steer` only (no second walking path).
8. **Keyboard unchanged** (Q5 later): arrow keys, Enter, Escape and Lightdisc's arrows do exactly what they do now.
9. **Disconnect**: stops walking; pauses only if the pad was used in the last 30 s; touch keeps working; no pause
   from a pad that was never pressed.
10. The usual: off-switch identical, check_fast before every push, names_check, phones-first draw calls.

## Controller turns 1 + 2 (CT1: c99acf4f 0.90.0 the base, ef59c61a 0.90.1 the deck): PASS

Code read (section 26 + one line in section 12's loop, `if (PAD.live) padTick(dt)` with the real clamped frame time):
- With PAD_ON off: only consts, the PAD object and padOn registrations (inert). With it on and no pad: two window
  listeners (`gamepadconnected`/`disconnected`) and nothing else; the hand-back listeners (pointerdown, wheel,
  mousemove, capture, passive, no preventDefault) are added only at a hello. No `R()`, no save, no DOM, no mesh in
  section 26 (grep).
- Walking sets `player.steer` (the touch walk's own shape), never while a touch is steering (`steering`); a let-go or a
  panel ends it. Turns are `azT ± π/2` (what the Rotate button does), zoom goes through `setZoom` (pinch's clamp).
  Menu = pauseSet (a hidden tab pauses at any time too, so pausing over anything is the game's own behaviour); Y and
  View press their own buttons (`click()`), so the device's lock etc. apply.
- All 15 ids in PAD_PANELS exist in the game. A queue (ACT kind queue) shows qAsk, which is in the list, so the stick
  walk ends the next frame and qAsk is asked once (Stay by pad needs turn 4's highlight).

Runs (each alone):
- cadet_test integration 0.64.14 → 0.90.1 (switch off): ALL IDENTICAL. → a copy with `PAD_ON = true`: ALL IDENTICAL.
- controller_check: CONTROLLER CHECK OK (161 s).
- Mutants (`plans/review-9/ct_mutants.py`), all **CAUGHT**: c1 walking flipped (view 0 "asks to walk the wrong way");
  c2 a let-go that doesn't stop (views 0-3); c3 the device dropped from PAD_PANELS ("with the device open the stick
  walked or RB turned"); c4 no pointerdown hand-back ("a touch did not hand back").

Nits for later turns (not blocking):
1. A worn stick drifting past the dead zone (.22) keeps the controller "in use" and walking; turn 7's dead-zone setting
   covers it, but a stick that never returns to centre could also be ignored until it does once.
2. controller_check has no "pad already there at load" case and no screenshot-after-touch case yet (none needed while
   nothing is drawn; both are due with turn 3's ring and RV2's check review).
3. Walking's "moved in >= 2 of 4 directions" is loose; the steer direction test (> .999 in all four) is the strict one.

## Controller turn 3 (CT1: 1ec16129 0.90.2, picking): PASS for the game, WITH FIXES for the check

Code read: the ring (one RingGeometry mesh, colour through `col()`, y .035, clear of rugs at ~.012 and under the touch
marker at .06) and the bottom line `#padHint` are made at the first use only (`padPickShow`, when the pad is in use and
nothing is open), hidden with a touch, a panel or a toast. A presses section 11's own `tap()` at a screen point where a
finger would hit the thing (`padFind` asks `padWhat`, a read-only copy of tap()'s order: crew, walker, item / lift,
lift door, lock, shut door, then the floor's job / crate / hamper / wardrobe / place). The search is spread over frames
(6 screen points a frame). Reduced motion keeps the ring still. Small label nit: a `youLock` door is always named a door,
but tap() only treats it as one when `youLockTap` answers (else the tap walks you there); A still does what the tap does.

Runs (each alone):
- cadet_test turn 2 → turn 3 (switch off): ALL IDENTICAL (renderer noise only). Switch on, turn 2 → 3: ALL IDENTICAL.
  integration 0.64.14 → turn 3 on: ALL IDENTICAL.
- controller_check: OK; pick: 25 things pressed, kinds crew, item, lift, place (A and a finger's tap in lockstep give the
  same outcome every time).
- Mutants: **c5** A does nothing: CAUGHT. **c6** a hidden ring mesh made at load (inside `if (PAD_ON)`): **MISSED**.
  **c7** a seat ringed where the tap actually reaches a person (padWhat skips the crew when looking for a place):
  **MISSED**.

Fixes for the check (CTT / CT1; not the game):
1. c6: the `quiet` part (switch on, no pad) should also compare the 3D scene with the no-pad page: `scene.children.length`
   and `renderer.info.memory` (geometries, textures), and after a press-then-touch, `renderer.info.render.calls`.
2. c7: the lockstep compares A with a tap at the same point, so a wrong point passes. Also check that the outcome fits
   the ringed thing's kind: crew → the chat opens with that person; lift → the lift panel; place → you go to that place
   (ACT / goal at its spot); item → its toast or activity; door → you walk to that door.
3. My bar 6: the kinds pressed should include a shut door and a machine (a job stop or a FLOOR_ACTS machine), not only
   "lift or crew" plus an item.

## RV2 on turn 3 (for the record)

RV2 (claude/review-controller) gave turn 3 PASS WITH FIXES against CTT's newer check (claude/controller-tests 049aff56):
a ring made at load (my c6) is CAUGHT there (its idle/calls compare the scene count); A 40 px off and R() in the search
CAUGHT; "A ignores crew" caught only via a sleeping person's toast (CTT's OUTCOME doesn't read #chat); "facing ignored"
MISSED (CTT to add one thing ahead, one behind). My c6/c7 against CTT's check (RV2): **c6 CAUGHT** (idle's scene count, pad modes a and b); **c7 MISSED**: CTT's pick finds no lone seat on Deck 4, so a seat ringed where the tap reaches a person is never tried. Open for CTT: a seat case, with a person in front of a seat, on a deck that has one.

## Controller P1, panels (CP1: claude/controller-p1 86d45aba, on CT1's turn-4 WIP a2c80df6): PASS WITH FIXES

Code read: while a panel is open the highlight is the page's real focus; the D-pad (or the left stick past half way)
moves to the nearest button that way, the same scrolling list first; A = `click()` (a text box only takes the focus);
B = the panel's own way out (PAD_BACK, else Escape; PAD_MUST on a card you must answer); the right stick scrolls, the
triggers page; LB/RB are the device's Back/Home; D-pad up on the deck reaches the screen's edge (PAD_HUD); X presses the
showing action button. The outline CSS (`padCss`) is added only once the pad is used and a panel opens, and only applies
under `body.pad`. The API for P2-P5: padPanelAdd, padOwn, padStep/padPress/padBack, PAD_FIRST, PAD_BACK.

Runs (each alone):
- cadet_test integration 0.64.14 → 86d45aba: switch off ALL IDENTICAL; switch on ALL IDENTICAL.
- controller_check: OK (panels: 30 swept, 17 device apps; api; lists).
- Mutants: `p1_devbackno` (B does nothing in the device) CAUGHT; `p1_nolanding` (opening a panel puts the highlight
  nowhere) CAUGHT.
- My page-derived sweep (`p9_reach.py`: every visible element with cursor:pointer, an onclick, role=button or a form
  control, not in padItems): only disabled buttons (the lift's and ladder's "You are here", the alarm's "−" at its limit,
  the device's Back on its home screen: a tap does nothing there either) and the Maps app's SVG map, whose room taps
  run the same `maps pick` as its Rooms list rows (only service rooms are on the map but not in the list; the map's
  person dots have no action in Maps). Nothing a tap can use is out of the pad's reach today.

**Fix (game, small): a touch after the pad leaves an outline** (`p9_focus.py`). The pad focuses the device's Calendar
tile; after a pointerdown hands back (body.pad off, PAD_FOCUS_CSS off) the tile keeps the focus and still matches
`:focus-visible`, so the game's own `.device button:focus-visible{outline:2px solid var(--crt-hot)}` (and
`button:focus-visible` at line 23) draws a 2px outline a touch-only player never sees. Fix: remember what the pad focused
and on 'unuse' blur it if it still has the focus (never a focus the game set itself); add a check case.

**Fix (check): the panels sweep is circular.** REACH starts from `padItems(L)`, the controller's own list, so a clickable
`div` with an onclick (not focusable) would never be found missing. Add the page-derived cross-check (as `p9_reach.py`).

## Controller P2, mini-games and special screens (CP2: claude/controller-p2 e62efcc, on P1 86d45aba): PASS

Code read (section 26's slot only, all on P1's padOwn / padPanelAdd / PAD_FIRST; no hooks elsewhere):
- Tiles: the board's own buttons by the helper's nearest-button move; A is the board's own click; the highlight lands on
  How to play's Next, else your last square, else a tile you can move; Again when it ends; kept across redraws.
- Lightdisc: the left stick's full range writes `DISC.inp.kx/kz` (the arrow keys' own path; a let-go zeroes it once, and
  a keyboard player's arrows are untouched when the stick is idle); padOwn frame returns true while playing, so the stick
  never moves the highlight; A never presses Leave unless you moved onto it; B = Leave.
- Question cards (deviceChoose): land on the first answer; the same button when a turn card asks again; B = the ×.
- Alarm: Set alarm first; − and + across (CP1's same-row padNearest makes this padOwn redundant: CP2 to drop it).
- The arrival manifest: an id set from section 26 once the pad is in use; A on Sign with the box empty fills in
  PAD_NAME 'Alex Morrow', A again signs; B only leaves the box (PAD_MUST).

Runs (each alone): cadet_test integration 0.64.14 → e62efcc: off ALL IDENTICAL; on ALL IDENTICAL (renderer noise only).
controller_check: OK (tiles, disc, screens). Mutants, all **CAUGHT**: `p2_ldnostick` (Lightdisc ignores the stick),
`p2_ldleave` (A can press Leave), `p2_noname` (no suggested name), `p2_tilesnoland` (the highlight never lands on the
board).

**For the user (via the lead):** the plan's Q6 answer says the suggested name "can be changed later", but the game has no
rename (the name is set only on the manifest, and it's on your cabin plate and the beam). Add a rename (P5's settings
could) or drop the promise. "Alex Morrow" is close to Captain Marrow; another name would avoid the echo.
Not covered (CP2's note): Dev mode's sheet by pad (needs #dev). P2 inherits P1's focus-after-touch fix when it takes
cff5bab7.

## Controller P1 re-review (CP1: cff5bab7, with 1afcaca4 + 825378d2): PASS

The two fixes: (1) `PAD_FOCUS.el` is what the pad focused; on 'unuse' it is blurred if it still has the focus (a focus
the game set itself stays), and the tabindex the helper gave tap-cards is removed (PAD_FOCUS.tabs). (2) The panels
sweep first runs a page-derived CLICKY cross-check (allowed: disabled buttons, Maps' svg); the api part plants a div
with an onclick and checks CLICKY finds it. Also read: padNearest prefers a button overlapping on the cross axis (same
row/column), and after a redraw of the same screen the highlight returns to the same-named button (else the same index).

Runs (each alone): cadet_test integration 0.64.14 → cff5bab7 off ALL IDENTICAL, on ALL IDENTICAL. My focus probe: after a
touch the focus is on the body, outline none (was 2px). My page sweep: nothing unreachable. controller_check OK (30 panels,
17 apps). Mutants, all **CAUGHT**: p1_devbackno; p1b_nolanding; **p1_noblur** (the blur line removed: "a touch should
take the focus off the pad's highlighted button"). The frame-cost probe (`p9_cost.py`) can't time anything in the test
page (the harness fixes the clock): the per-frame `padItems` over a 152-row Roster is left to turn 8's frame-time check.

## Controller P2 follow-up (CP2: 67df90a): PASS

Merges P1 cff5bab7 (drops CP2's alarm padOwn: P1's same-row move does it), and the user's answer: PAD_NAME 'George', no
rename promised. One word: the cabin plate shows the whole name, the beam `firstName` ('George'). cadet_test cff5bab7 →
67df90a (switch off): ALL IDENTICAL. CP2's own: controller_check OK, tiles/disc/names/check_fast OK.

## Controller P4, the Controller settings page (CP4: claude/controller-p4 7631ab6 = P1 cff5bab7 + e73b7b0, db80eb0, 7631ab6): PASS WITH FIXES

(Taken over from RV2, whose code read is in plans/review-controller.md "P4"; RV2 passed the section 19 hook.) Code read:
a hidden device app 'padsettings', reached from a button that ends Settings; PAD_SET saved as `s.pad` only when it
differs from normal (`padSetDiff`); `padSetLoad` keeps only valid values and drops a button map that isn't one action per
button; rebinding swaps clashes and the pressed button is "eaten" until let go; 10 s or Cancel stops waiting. Edits
outside the slot: padTick's PAD_MAPK / PAD_PHY / stick swap (CP1 agreed), turn 2's zoom line (flip, speed), section 19's
one hook, and four typeof-guarded `padBuzz` hooks in sections 15/15b beside their messages (no-ops unless vibration was
turned on and a pad is live).

Runs on 7631ab6 (each alone): cadet_test integration 0.64.14 → 7631ab6 off ALL IDENTICAL, on ALL IDENTICAL.
controller_check: OK, all 9 parts (settings included). RV2's P4 mutants (`plans/review-9/rv2_mutants.py`), all
**CAUGHT**: p4_savealways, p4_showalways, p4_noclash, p4_noflip, p4_oddsave, p4_nogentle, p4_noeat.
My save probe (`p9_padsave.py`, saveGame's own build-up): no pad, Settings has no Controller button; the pad used and the
page opened with nothing changed: the save equals the no-pad save, no `pad`; a swap + dead .32 + Y on X saves exactly
`{"map":{"x":"y","y":"x"},"swap":true,"dead":0.32}` and loads back; Everything back to normal (twice) leaves no `pad` and
the save equals the no-pad one; odd saves (null, 5, "x", [1,2], a non-permutation map, out-of-list values, "yes" for true)
load as normal, keeping only valid parts.

**Fix 1 (the hard rule, mode b; RV2's find, confirmed by `p9_modeb.py`): a pad connected but never pressed shows the
"Controller settings" button in Settings** (`padSetSeen = PAD.live || PAD.id || diff`; PAD.live is true at a hello).
Gate it on the pad having been used this session (`PAD.lastUse > -1e9`) or a saved change; add a check case (plug + hello,
no press: Settings unchanged).
**Fix 2 (small; RV2's find): a trigger moved to another action presses at the browser's own `pressed` threshold** (a light
squeeze can press A); treat the physical triggers by their half-way rule whatever action they carry.
For P5 (RV2's note): the left-hand preset leaves no way to zoom.

## Controller P4 re-check (CP4: f904532): PASS

Fix 1: `padSetSeen = PAD_ON && (PAD.lastUse > -1e9 || !!padSetDiff())`; my `p9_modeb.py` (plug + hello, no press): Settings
has no Controller button (it did on 7631ab6). Fix 2: physical buttons 6/7 count as pressed only past half way
(`padTrig(value) > .5`), whatever action they carry. (Note: `lastUse` is also set by a stick past its dead zone, so a stick
drifting at connect counts as a use; that is turn 2's drift nit, for turn 7's dead zone.) Runs (each alone): cadet_test
integration 0.64.14 → f904532 off ALL IDENTICAL, on ALL IDENTICAL; controller_check settings OK. Mutants undoing each fix,
both **CAUGHT** by CP4's new cases: `pr9_p4_seenlive` ("a pad connected but never pressed changed Settings"),
`pr9_p4_trigpressed` ("a light squeeze of LT (bound to confirm) pressed it").
