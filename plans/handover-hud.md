# Handover: U, the HUD engineer (session_01FcMPTX7mMTHkyr4pxDfNcS)

**Branch:** `claude/hud-pt1` (push only there). **Build series:** 0.72.x (last: 0.72.6). Report to the lead (lead 16, session_01UMyfd16GqSdgNyz5PE8qSv at the time of writing); hashes to the build master (BM7 session_01QbuzvT3TwzMwSWRmakzX8Z) and the reviewer (R4 session_01UGQxniXCxT5TLEE4tgRLfJ). Lines come from the head writer W2 (session_01866TWKzGRgZmFcxiYRi4db), who bakes them; my code always carries a stand-in.

## What I built (all merged up to 0.63.3 unless marked)
| Build | What | Where in starship-cadet.html |
|---|---|---|
| 0.72.0 | **Tracked** button `#trkBtn` + panel `#trkPanel` (`.lift` dialog): your job, the rest of today + tomorrow morning from devDay, then `TRK_PLACES` (job board, your bunk, call booths). Tap = goal arrow (`setGoal({...goal, trk: key})`; your job via `SHIP.player.track`), tap again = stop. `tradGoal(x)` (traditions seat) first for a tradition, else `devItemGoal`. `trkPlace`: on phones right-aligned under the needs strip, else after the Device button | section 15b, right after `requestAnimationFrame(ixFrame)` |
| 0.72.0 | Device app labels 13px/.03em | `.device .app` CSS |
| 0.72.1 | **Watch a film** hobby (`HOBBIES.film`, `label` field for the button) | section 15's HOBBIES, the Hobbies app |
| 0.72.2 | Tiles "⏸ The ship's clock is paused while you play" (`.tl-pz`, shown while `PAUSE.tiles()`; W2's `tiles.paused`) | section 23's tilesDraw |
| 0.72.3 | **Turn-in gains** chips in the "Job complete" toast: rep in words only (the user's 0.61.15 rule), then "+N <system>" per meter. `turnInSnap`/`turnInGains`/`turnInShow`; data `j.gains` (C2's careerJobIn) then S2's `j.meters`, else a before/after diff; one chip per dept/system | after the Tracked block; `ixBoard.turnIn` |
| 0.72.4 | Tracked is **also a device app** (`deviceApp('tracked')`, order 1, glyph ◎), the HUD button kept (the user ~04:00) | after the panel code |
| 0.72.4 (check) | leave_check's reputation-chip part reads the turn-in card (with `turnInShow`) | leave_check.py |
| 0.72.5 (not yet merged) | Playtest 2 batch A: item 3 the call-home arrow can replace the first night's bunk arrow (`introArrowTick`'s `ours`); 6-7 `INTRO_CLOCK_AUTO` 08:50; 17 `careerTip` once a save; 9 `t:device-work`, 19 `t:laundry-d2` (TEACH text may be a function) | section 21 (introArrowTick/introArrowWant), section 24 careerTip, section 15 TEACH |
| 0.72.6 (not yet merged) | Batch B: tea + supply delivery in `devDay` (kinds 'tea', 'delivery', goals in `devItemGoal`, tea heads-ups under the everyday switch), `teaBegin` gain 4, `DECK_NAMES[2]` "Officers' quarters and science" | section 19 devDay/devItemGoal/devHeadsTick, section 15 teaBegin, the lift panel |

Nothing I added is saved except what reuses existing saved fields (`SHIP.device.tipsSeen` for careerTip ids `career.<key>`).

## Loose ends (playtest 2, plans/brief-playtest2.md on claude/lead-pillar1)
- **Item 12 (appointment notifications):** appointments already got the 15-min and start heads-ups (tested). Done in 0.72.6 (the lead's call, part b): an invitation still awaiting Accept reminds you too. **Part (a), not built (for U2/the lead):** the timed onboarding beats that aren't booked through apptAdd and so get no heads-up: section 21's `INTRO_WEEK` entries the player should attend (e.g. `d1-briefing`, Torres's training beats `d2-*`, the Day 2 rounds start, `d2-booths` 18:00, Calder's first solo job `d2-solo`), Day 1's 09:00 first shift (only if `R.everyday` is off; it's a Schedule item otherwise). The simplest route: in `devDay`, while `introOn()`, add the beats with a `where` the player is meant to go to (kind 'beat', goal from their `where.deck/room`), so the heads-ups, the Schedule and the Tracked list pick them up together; take care not to list beats that come to you (Zeke walking up).
- **Batch C, not started** (the lead was told to give it to a fresh seat): item 4 (toilet lowers hygiene with the "−N Hygiene" pop-up, section 15's toilet act and needFloat); item 5 (energy drains faster: a 16 h day ends near 20-25%; an alarm clock when you go to bed: pick a wake time, show the energy you'll wake with, a warning if after your shift starts; W2's keys alarm.title, alarm.wake {time}, alarm.energy {n}, alarm.more, alarm.set, alarm.late {start}, alarm.toast {time}, alarm.ring; the sleep card is `#sleepAsk`); items 15/20's place-in-line message (W2: queue.booth / queue.shower {nth}, queue.next, queue.go; X owns the queues); item 1's arrow/tips with E1 (session_01AHeKjieg3qWjnEVuHecsHd; W2: tip.round.take|go|look|mark|next|done {machine}).
- Checks to finish for 0.72.5/0.72.6 before sending: interactions_check --quick, leave_check (careerTip changed), player_check (tea gain), device_check (devDay changed), intro_check --evening (arrows), cadet_test vs the 0.63.3 final (batch A: ALL IDENTICAL).

## Gotchas
- **Two checks on the same build file name clash** (the harness writes `/tmp/cadet-work/test/_run_<name>`): give each run its own copy (`a1.html`, `a2.html`...).
- **Three browsers at once often fail to start** ("game failed to start"): run checks in pairs.
- `pkill -f <pattern>` kills your own shell if the pattern is in its command line: kill by pid.
- cadet_test's Game hides `#needStrip`, so on a phone-size run the Tracked button falls back to the Device row; tests that tap it add `#needStrip{display:flex!important}` and hide `#devTip` (a tip card over it takes the tap).
- The device rows' text is `.rt`; the Tracked app's job row is found by `myJob().title`.
- My quick runners for one part of interactions_check: split the file at the part's comment and exec it (see the "== tracked" and "== playtest 2" parts).

## How to test my parts
`interactions_check.py BUILD --quick` ("== tracked": the app, the button's panel, the film hobby, the turn-in chips; "== playtest 2": items 3, 6-7, 9, 17, 19, 10-11, 18), `tiles_check.py BUILD 300` (the paused line), `leave_check.py`, `device_check.py`, `player_check.py`, `intro_check.py BUILD --evening`, `cadet_test.py OLD NEW` (the HUD button's box is the only expected difference when it changes).

## Open questions for the user (via the lead)
- Item 12: which notification was missing?
- Item 17: every tip already showed once a save except the career warnings; if a different tip repeated, which one?
