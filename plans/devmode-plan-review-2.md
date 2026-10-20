# Dev mode plan: second review (DR2)

Reviewer DR2, 2026-10-20, for lead 20. Reviewed: `claude/devmode-plan` 2f7b9e4 (`plans/devmode-plan.html` / `.md`, version 1). Base: `claude/integration` 5dd740c (0.64.2 + step 2). These findings were formed before reading DR1's review. My angle: does the plan serve what the user really does, which is playtesting their own game on a phone, quickly, without breaking anything?

## In plain words (the summary)

- **The plan is sound and safe in its bones.** It has its own save, a DEV chip that's always visible, nothing at all without `#dev`, and a regression proof every turn. Replay is the right long-term way to jump to a day.
- **The order is wrong for what the user needs next.** The user's next job is checking the playtest patch: the Day 2 "first solo job" meeting, Calder walking up on Day 0, Zeke's line, the ladder, and undoing a clock-in. All of those happen on Days 0-2 or on any day. Under this plan the user can't jump to Day 2 until turn D7 (Stop 2). The day jump also depends on every career seat adding its line to a shared steady player first (D6).
- **The plan is missing the three cheapest tools a tester uses most:**
  1. **"Take me to…"**: put me at a room or at my next appointment. Walking from your bunk to the Chief's office on a phone takes minutes, every try.
  2. **"Mark this moment / back to mark"**: retry the same 08:40 again and again.
  3. **"Top up my needs"**: after any skip today you arrive starving and filthy. I measured hunger 0, hygiene 0 and bathroom 0 after skipping to Day 2.
- **The day jump's measurements leave out the arrival week.** They were taken with the tests' `nosave` switch on. That switch turns off the arrival, the first week's beats and the clothes. So the "exact" Day 2 the user needs (for the Day 2 bug) hasn't been tried yet.
- **One real safety hole: storage space.** Kept days (~0.8 MB, growing with the game) share the browser's space with the real save. When that space fills, the real game stops saving without a word: `saveGame` swallows the error ("the game carries on unsaved").
- **Simpler and sooner:** a **first version in 3 turns**, with:
  - the switch and Dev save
  - Clock (with needs topped up and shifts excused)
  - Take me to…
  - Mark / back to mark
  - Start a tradition

  That covers about 90% of the patch testing at a first stop. The replay day jump, the career tools and events follow as planned.

Ratings: **2 blockers, 7 should-fix, 6 nits.** None means starting over. They're reorderings and small additions.

## How I checked

- **Played 0.64.2 headless at 390 × 844 with touch** (`#debug`, a scratch copy, not the save of any real link). Signed aboard, used the debug Night/Day button, and read the state after each tap.
- **Timed `skipTo` on the same build:**
  - 1 day takes 0.2 s.
  - 10 days take 1.1 s.
  - The career doesn't move: after 10 days you're still a Junior, with 0 xp and an empty career record.
- **Read in the code:**
  - the plan's claims about storage names, `NOSAVE`, `introWanted` and `CLOTHES_ON`
  - section 21's Day 2 beat (`d2-solo`: 08:45-09:00, Calder, the Works Chief's office)
  - Calder's paper schedule at that hour
- **Took the user's next tasks** from the roadmap on `claude/start-here-review-3qoht9` ("The user's playtest patch and next steps") and the events plan (F6).

## Five real tasks, step by step, with this plan

### Task 1: Reproduce the Day 2 "first solo job" meeting bug (patch item 1)

What the user needs is to stand outside the Works Chief's office on Deck 5 at about 08:40 on Day 2, as a player who did Day 0 and Day 1 properly, and watch whether Calder is there and the meeting starts. Then fix, and try again.

With the plan as written:
1. Tap the Dev link, then the DEV chip, then the Jump tab. **The shortcuts are 0 1 5 9 10 16 23 26 30, with no 2.** So it's "Day…" and typing 2.
2. Wait for the replay, then the page reloads. You wake at 06:00 in your bunk on Deck 4.
3. Clock tab, "to a time…", 08:30. With Skip, before the shift, that's fine. With "Play it steady" it's unclear whether the steady player would take the 08:45 meeting itself.
4. Walk from Deck 4 to the lift, down to Deck 5, through the Works bay to the office. On a phone that's 1-2 real minutes, and the meeting's window is only 15 ship minutes (25 real seconds).
5. Watch. Then, to try again, jump to Day 2 again (a kept day, plus a page reload), then repeat steps 3-4.

**Where it fails:**
- **It's only possible from Stop 2 (D7).** The user's top patch item waits behind the shared steady player (D5-D6), which needs a line from every career seat.
- **The Day 2 it arrives at is untested.** The plan's replay was measured on `?nosave&debug`. `introWanted()` returns false under `NOSAVE` (line ~39382), and so does `CLOTHES_ON` (line ~40083). So the measured replay had **no arrival evening, no first-week beats and no clothes**. The steady player's lines in 4.3 don't mention the first week's checkpoints (section 21's `introAdvance(t, here)` needs the player *at* each beat). My own skip to Day 2 marked every Day 1 beat as passed by at its time, with "(notes)" Mail. That's a player who missed the Day 1 briefing, not a real one. A Day 2 bug that depends on what happened on Day 1 might not reproduce.
- **No way to retry quickly.** Each retry is a jump plus a page reload plus a walk across two decks. Half a dozen tries is 15+ minutes of walking.

**Fix:**
- Add **"Take me to…"**: a short list of places (rooms by deck, "my next Schedule item", the ladder), using the same move the lift uses.
- Add **"Mark here" / "Back to mark"**: one snapshot slot in the Dev save.
- Add **Day 2** to the shortcuts. Better still, make the shortcuts the **arrival week's beats** ("Day 1 briefing", "Day 2 solo job", "Day 3 store", ...), which also land you at the right time and place.
- Make the steady player **do the arrival week** (intro_check's "happy" runner already does it on paper) and measure that.

### Task 2: The ladder works and has a panel (patch item 5)

Any day will do. Open the Dev link, jump to Day 1 (or start a new game and skip to Monday), then walk to the spine ladder.

**Where it fails:**
- Nothing blocks it, but it's the walk again. "Take me to… the spine ladder (Deck 4)" makes it a 3-tap test.
- If rank still gates maintenance access before the patch, the user wants to try it as a Junior and as an Officer. "Set rank (approximate)" (dm-q8) covers that, but it only arrives at D3 (Stop 1). That's fine.

### Task 3: Undo a clock-in or clock-out (patch item 6)

The user needs to be at the Works bay time clock at about 08:55 on a workday, and again at about 16:55, clocked in.

**Where it fails:**
- **Moving the clock while clocked in isn't defined.** With "Skip" from 09:05 to 16:55, are you still clocked in, and is it a missed shift? Skipping counts as missed "as if you slept through it", but you clocked in. With "Play it steady" to 16:55, the steady player has done the shift, and it may clock out at 17:00 before you can test.
- **The plan's "to 17:00" button would step past the moment you want to test.** You'd need "to 16:55". "To a time…" covers it, but on a phone a time picker is several taps.

**Fix:**
- Spell out: **Skip while clocked in keeps you clocked in and counts as worked** (excused). The tester is testing clocking, not the missed-shift ladder.
- Let the time buttons stop **5 minutes before** each shift edge: "to 08:55" and "to 16:55".

### Task 4: Check a ship tradition (for example, Lap of the Wren, or a quiz on a Monday)

Traditions tab, search "quiz", then "In 20 min". The crew go and the goal pointer leads you. **This one works well, and it's ready at Stop 1.**

Small notes:
- The tab label "Trad." is jargon on a phone. Use "Events" for traditions and "Big events" for the ship-wide ones, or icons with words.
- Starting a tradition on Day 0-1, during the arrival, isn't covered. Does the escort's step win, or the tradition? Refusing during the arrival evening, with the reason, is simplest.

### Task 5: See the Officer promotion (Day 10) and the ion storm (Days 10-15)

Promotion: Career tab, "Start promotion now", then "Next step ›".

**Where it fails:**
- **What does "Start promotion now" do on Day 3, with no trainings done?** The Tier 2 test needs the Tier 1 rows (m6 "Making it safe" among them). The plan doesn't say whether it trains the missing rows first, refuses, or runs a test you can't pass. The user will press it on whatever day they're on.
- **The believable route is "Jump to 9 / 10", and that rests on D6.** The plan's own finding is that today's steady player never reaches Officer. Every career seat has to add its line before the jump works. That's the plan's largest schedule risk, and it isn't named as one.
- The career tab shows **row ids** ("Trained m1 m4 m5 m7 · next: m6"). The user doesn't know m6 is "Making it safe". Show names.

Storm: the Events tab is D8, last, and the phase jump waits for F4. That's fine, because the storm comes after the patch and the "Talk a while" pack in the user's order.

## Findings

### Blockers (fix in the plan before building)

**B1. The order doesn't match the user's next job.**
- **Scenario:** the playtest patch is built right after Dev mode. The user opens Stop 1 (Clock, Career, Traditions) and still can't reach Day 2 08:40 as a real player, so the patch's top item can't be checked until Stop 2.
- **Fix:** a first version at Stop 1 (after about 3 turns) with:
  - D1 (switch, Dev save, chip)
  - Clock (needs topped up, shifts excused, stops at 08:55 / 16:55)
  - Take me to…
  - Mark / Back to mark
  - Traditions

  For Days 0-2, "Jump" can at first be "new game, then the steady arrival-week player". That's a small piece: intro_check's happy runner already plays it on paper. Move Career to Stop 2 with the replay.

**B2. Kept days can silently stop the real game from saving.**
- **Scenario:** kept days (0.8 MB now, more as the game grows; the save grew to 118 KB by Day 26) sit in the same browser storage as the real save. Phone browsers allow about 5 MB per site.
  - Once full, `saveGame()` hits its `catch` ("no storage, or full: the game carries on unsaved").
  - The user's real game stops saving with no message, and the progress is lost on the next visit.
- **Fix:**
  - Put kept days in IndexedDB (a separate, larger space), or cap all Dev storage, for example at 1.5 MB, dropping the oldest kept day first.
  - Add a "Clear Dev save" button.
  - devmode_check fills kept days to the cap, then proves the real save still writes.

### Should fix

**S1. The measured replay isn't the real game.**
- **Scenario:** the timings, the "same twice" and the Day 26 save size were measured with `?nosave&debug`, which turns off the arrival, the first week's beats and the clothes (the plan says so itself in section 2).
- **Fix:**
  - Re-measure with the arrival on (DEV's own save, no `nosave`), Day 0 to Days 2, 10 and 26.
  - Add the arrival week's beats (be at the checkpoint, keep the meetings) to DEV_PLAYER's first lines (D5), not later.

**S2. Needs aren't looked after on clock moves.**
- **Scenario:** Clock, "Next morning" twice (Skip), lands you on Day 2 with hunger, hygiene and bathroom at 0 (measured). Low-need markers, arrows and tips then take over the screen and the walk speed, and the test is about something else.
- **Fix:** a "Top up needs" button, and Skip in Dev keeps needs as a normal morning. The plan already promises this for a Jump; do the same for Clock.

**S3. Skip should be excused by default in Dev (dm-q5).**
- **Scenario:** the user skips a day to reach a tradition. Two skips later, summons Mail and the missed-shift ladder are in their test, and enough skips get them let go on Day 20.
- **Fix:** recommend **"Skip, excused" as the default** and keep "Skip, counts as missed" for testing the career ladder itself. Keep "Play it steady" for when they want the day lived. dm-q5 already lists "excused" as an option; it should be the recommendation.

**S4. Opening on a phone needs a ready link, tested in the Claude app (dm-q1).**
- **Scenario:** the user is told to "add #dev to the link". In the Claude app's artifact viewer there's no address bar to type into. In a phone browser, editing the end of a long link is fiddly. Also, a hash change doesn't reload the page: adding or removing `#dev` in an open tab does nothing until a reload, which is confusing.
- **Fix:** the recommendation should be **"the lead gives you a ready Dev link (the playable link with `#dev`) to tap or bookmark"**. Check at Stop 1 that the hash survives in the Claude app, the mobile browser and "Open in browser". If it doesn't, fall back to a separate Dev copy (dm-q1's option 3), which also gets its own storage.

**S5. Add "copy my real game into Dev" (dm-q2's option 3, as a button, not the default).**
- **Scenario:** the user finds a bug in their real game (as with the Day 2 meeting). The fastest way to reproduce it is from that exact moment, without risking the real save.
- **Fix:** keep "its own save" as recommended, plus a button "Copy my real game into Dev". It's one read of the real save; it never writes it.

**S6. Thumb-sized buttons.**
- **Scenario:** the sketches use 26-point buttons in rows of seven. The game's own device uses 44 px+ (DEV_NOTES, the `choose` card). At 390 px wide, "+1 h +3 h To 17:00 To 21:40 Next morning +1 day +7 days" wraps to three rows of mis-taps.
- **Fix:** 44 px buttons, fewer per row, and the most-used ones first ("Next morning", "+1 h", "To a time…").

**S7. Say what "Start promotion now" does when you're not ready, and name D6 as the schedule risk.**
- **Scenario:** pressed on Day 3, it either refuses (say why, in words), or trains the missing rows (marked approximate), or runs a test you can't pass. Pick one.
- **D6 needs a line from every career seat** (24a-24s). If one seat is busy, Stop 2 slips. Name it in the risk table, with a fallback: jump to Day 10 arrives "approximate Officer" (set rank) until the steady player reaches it.

### Nits

- **N1.** Jump shortcuts: add 2, 3 and 7 (the arrival week), or name them by beat.
- **N2.** Show career rows by name, not id (m6, then "Making it safe"); keep the id small for bug reports.
- **N3.** The "Trad." tab label; a tab bar of five at 9.5 px is hard to read on a phone.
- **N4.** The DEV chip "under the clock" shares space with the Device and Pause buttons and the Tracked button (the backlog notes the Tracked panel already fills small phones). Check its place in the 390 × 844 shot.
- **N5.** Starting a tradition or an event during the arrival evening (Day 0): refuse, with the reason.
- **N6.** Today's `#debug` Night/Day buttons write the real save (debug doesn't set `NOSAVE`). Once DEV exists, `#dev.debug` is safe, but a plain `#debug` still isn't. That's worth a row in `plans/backlog.md` (not a fix in this plan).

## On the questions for the user (dm-q1 to dm-q10)

| Q | Plan's recommendation | My view |
|---|---|---|
| dm-q1 opening | `#dev` in the link | Agree, but phrase it as **a ready Dev link we give you**, checked in the Claude app at Stop 1; fall back to a separate Dev copy (S4). |
| dm-q2 saving | its own save | Agree, plus a **"Copy my real game into Dev"** button and **"Clear Dev save"** (S5, B2). |
| dm-q3 day jump | (a) replay + kept days | Agree as the design. Kept days must not share space unchecked with the real save (B2), and it should be re-measured with the arrival on (S1). |
| dm-q4 player kinds | steady now | Agree. |
| dm-q5 shift on clock moves | two buttons: steady / skip (missed) | Change the recommendation to **"Skip, excused" as the default**, with "missed" and "steady" as choices (S3). |
| dm-q6 arrival in a jump | yes | Agree. It's essential for the Day 2 bug, but it isn't in the measured replay yet (S1). |
| dm-q7 tradition today | today, refresh under the lift's fade | Agree. |
| dm-q8 set rank | yes, marked approximate | Agree. It's also the fallback while D6 is incomplete (S7). |
| dm-q9 review rhythm | three stops | Agree on three, but **Stop 1 should be the playtest kit** (Clock + Take me to + Mark + Traditions), not Clock + Career + Traditions (B1). |
| dm-q10 keep in published game | yes, behind `#dev` | Agree. The game is private and the switch does nothing without it. |

**Missing questions the user should be asked** (or the lead decides and tells them):
- Do you want "Take me to…" and "Mark / back to mark"? (Recommended: yes, in the first version.)
- Which do you want to test first: the playtest patch (recommended, so the first version comes first) or the career and events?

## A simpler first version (what I'd build first)

| Turn | Built | What the user can then do |
|---|---|---|
| V1 | `#dev`, the Dev save (with a storage cap and "Clear"), the chip, the sheet; "Copy my real game into Dev" | Test without fear; reproduce a bug from their real game. |
| V2 | Clock (Skip excused by default; to 08:55, to 16:55, next morning, +1 day, to a time), Top up needs, Take me to…, Mark / Back to mark | Days 0-2 tests in a few taps: Day 2 meeting, clock-in undo, ladder, Zeke's line, Calder walking up. |
| V3 | Traditions (start in 20 min / at its time / tomorrow + Mail) | Check any tradition. |
| **Stop 1** | Published Dev link + phone screenshots | The playtest patch can be checked as it's built. |

The plan's D3 (Career), D5-D7 (steady player, replay, kept days) and D8 (events) then follow unchanged, with S1, S7 and B2 folded in. It's the same total work, but the user gets the tools for the next job about four turns sooner.
