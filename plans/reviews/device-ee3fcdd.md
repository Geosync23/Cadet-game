# Review: claude/device a946f7c..ee3fcdd (0.35.32), occasions as appointments

Reviewer 1, 2026-10-17. **Verdict: PASS WITH FIXES (partial review).** I stopped early because the lead took this review out of my queue (it had already passed another review). day_check day 20 and social_check on the merge did not run.

Scratch merge: ee3fcdd + origin/claude/sim-engineer, social, ship-events, arrival. I resolved only the build-line conflicts, plus a test-only conflict in player_check.py (kept ours). name_check passed on the branches and on the merge. Probes ran in the browser (`?nosave&debug`; the save test used `?debug`). They gave the same results on ee3fcdd and on the merge. Section 20's social code is already in ee3fcdd.

## Findings, most severe first

### 1. An occasion can be both missed and kept: the player loses reputation and gains points for the same dinner (medium; device + sim)
**Path:** book the Captain's table (19:30, len 90). The player is not at the seat by 19:45.
- At 19:45, section 14's `apptTick` marks it `missed` (APPT_WAIT is 15) and sends `apptMissed`. Marrow leaves the room. Section 18's door stays open and the dinner can still play until 21:00.
- Section 20's `socialAppts` runs every minute. It charges the miss right away: command reputation 10 to 9, kindness 50 to 49, a `missed.<id>` memory, and a missed remark is queued.
- The player then arrives at 19:50, and the meeting plays (`r.met`). `deviceTick` turns the appointment from `missed` to `kept`. `socialAppts` then also pays the kept reward (`socKept`, Marrow's points 0 to 2.4). Marrow walks back to the seat (her stay now runs to 21:00).

**Evidence (probe pA, ee3fcdd and merge give the same result):** `s16: missed`. At T+20 Marrow is commuting to Deck 1 while `occasionDoorOpen` is true. Then `socMem: true`, `remark: true`, `repA command 9, kindness 49`, then `s20: kept`, `socKept: true`, `relKept pts 2.4`. At T+25 Marrow is back at 2-captable-1.

**Fix:** an occasion appointment should wait for the whole occasion. Two ways:
- (a) `apptAdd` sets a field such as `wait: len` on occasion appointments, and section 14's `apptTick` and `apptWhere` use `a.wait || APPT_WAIT` (a one-line guarded change, sim seat).
- (b) `apptTick` skips `a.occ` appointments, and `deviceTick` sets `missed` only once section 18's record is `missed`.

With either fix, the host stays as long as the door is open, and there is no penalty followed by a reward. Owner: device (apptAdd), with a one-line hook in section 14 (sim engineer).

### 2. New game keeps last game's occasion appointments (and the occasions themselves) (medium; device + traditions engineer 2)
**Path:** book the Captain's table for day 4, then call `newGameStart(false)`.

**Evidence (probe pA):** after the New game it is day 1 and `SHIP.device.appts` still holds `captainsTable@4`. The new game's Schedule for day 4 lists "The Captain's table". `SHIP.occasions` still holds `captainsTable@4` as `asked`, so section 14 routes Marrow there and section 18 plays the dinner in the new game. Old once-only occasions (`readyRoom`) can never come again.

Neither section resets on `newGame`. `SHIP.device.appts`, `SHIP.occasions` and `SHIP.commendations` were never reset, so this gap is older than this commit. 0.35.32 makes it visible: Marrow now walks to the stale dinner, and missing it costs reputation.

**Also:** if section 18 is fixed alone, `apptAdd`'s de-dup (`D.appts.find(a => a.occ === occ)`) returns the stale record from the old game. The new occasion would then get no live appointment.

**Fix:** device: `onSim('newGame', ...)` clears `SHIP.device.appts` (or at least drops `occ` ones and anything after the new start). Section 18: reset `SHIP.occasions` and `SHIP.commendations` on `newGame`.

### 3. Penalties for invitations the player never accepted (design question for the lead; social A / device)
Occasion appointments are booked with `status: 'yes'` and offer no Cancel, so the player cannot decline them. A missed one now counts in section 20 like a broken promise: kindness -2 (reduced near the floor), -1 to the host's department reputation when the host is an officer or chief (the Captain: command), a `missed.` memory and a remark ("Waited for you at the captain's quarters earlier..."). Before 0.35.32, missing an occasion only sent its Mail gist. The lead should confirm this is wanted. If not, `socialAppts` could skip `a.occ` when it charges a miss (one line, social A).

### 4. Rewards counted twice when an occasion is kept (low; design note)
When an occasion is kept, `socialAppts` gives `REL_PTS.appt` plus an `appt.invite` memory. The meeting script's choices also give their own `rel` points (`relAdd 'meeting:<key>'`). That may be intended, since an ordinary appointment plus a chat also earns both. It should be written in the hook register.

## Checked and fine
- **Plans stay pure.** `apptWhere` is only read through `whereIs`, which is used in play. `planDay`, `planWhere` and `eventPlan` don't read appointments. `apptFree` now also sees occasion appointments, which is correct: the host can't be double-booked.
- **A skip over the whole occasion:** the appointment and the occasion both end up `missed` (probe pA, last block).
- **Rooms:** `apptOccSpot` finds a spot for all three rooms (1-ready-1, 2-captable-1, 5-office-1). The chance occasion (bridge invite, ship-events) is skipped by ship-events' `!o.chance` guard.
- **Save round trip** (`?debug`, real `saveGame` and reload): ids 7 and 8 are integers and unique; `occ` and `title` survive; the appointments save is 294 bytes; the list is capped at 60 in both `apptAdd` and `deviceLoad`.
- **Missing sections:** `typeof` guards hold both ways (occasionAdd checks for `apptAdd`; `deviceTick` checks `SHIP.occasions` is an array). No temporal-dead-zone risk: `APPT_SEATS`, `DEV` and `apptPlace` are all declared above section 18.

## Tests
- name_check `--branches a946f7c ee3fcdd`: NAMES OK. name_check on the merge: NAMES OK.
- device_check on ee3fcdd: OK.
- device_check on the merge: FAILED on "heads-up: as it starts, once" (`again: False`; a crew appointment, not an occasion). Not attributed: it looks like an interaction with another branch.
- day_check day 1 on the merge: FAILED, "places booked twice 3-mess-9 volkov-maeve/calder@1105" (arrival on). Arrival or sim, not this diff.
- Not run (stopped): day_check day 20 and social_check on the merge.
