# Handover: the player engineer (needs, activities, device, the player's job loop)

Written 2026-10-16 at combined build 0.40.8 (`claude/ship-integration` 980e6a9), for a fresh session taking over this area. Read it with `DEV_NOTES.md` ("Player needs and the device"), `plans/pillar2-plan.md` and `design-doc.md` ("The player").

## Update: builds 0.28.41 to 0.28.44 (player engineer 5, session_01SyRmwPxQEVKab6re9UgyrD; written 2026-10-17)

Read this first. Lead: session_01KPJMYjXAPkNUcrQ8VRkhLE. Head writer 3: session_01FopKMT2ZKxuWcNDcmF7565 (was inactive at writing). Reviewer 1c reviews. Branch sits on ship-integration 0.60.3 (0477b15). Next build **0.28.50** (PE6, session_01AWgP6kgzpprnpA5pMAAiqq, carries on: lamp repair bug, Repair and Put down buttons, Tiles, shuffle-aside). Lead 8: session_01FutyR6xiAmZv29oS4TWKdS; reviewer 1f: session_015UH1fbKg2nCRNi9Y3D96YA; build master BM3: session_01WrXgDfR5dzwktKJfYwVwsV; head writer 5: session_011KTwL5FVSdmWNAkbkZsrgj. Branch has ship-integration 0.60.5 (1e7b3f5) merged in (0.28.47). Plan page: `plans/tips-plan.md`; screenshots: `plans/tips-shots/`.
- **0.28.41:** bathroom 0 -> `'+go'` pose (8b `HOLDS.go`, no prop, `knees`) and `GO_SPEED` 0.7 in `needEffects`; `player.needGo` set in `playerUpdate`, the Walker adds '+go' when it holds nothing. Need warnings: `NEED_WARN`, `needWarnTick` (under 25 / 10, re-armed at 40), quiet moments from `popupWatch` / `POP` (panels four times a second, the rest every frame; a heads-up counts only as it comes up).
- **0.28.42:** `TEACH` (34 tips, `[id, test(c), text, { sure }]`), `teachTick` (once a second; one every 3 min, 60 s after a card/warning, 6 s after a toast; app tips only over their app). `teachHeld()`: only the arrival (day 0 or an intro step); **the intro runs all week (introEnd on day 8)**. `t:rep` is sure (Monday after your first turn-in or from 17:00). Text by head writer 3; t:rep's draft not yet polished by them.
- **0.28.43:** `bondMult(id)` 1/1.2/1.5/2/3 by relTier; `seatTable` (mess seats within 1.3 m make a table: 4 long of 8, 3 round of 4); `company(A)` = your table only, bond-weighted, cap 6. Chats, sitting, Tiles (`A.o.opp`), 15b's `ixBond`, section 18's tradition +12 all by the bond. design-doc updated.
- **0.28.44:** the News feed (Ship app id 'ship', title News feed) and Relationships (section 20's 'crew' app). Feed engine in section 15 (`newsTick` etc., see DEV_NOTES row); head writer 3's bank (`content/banks/news.lines`, claude/content 5417aeb) is NOT in this build: the build master's content merge bakes it into `LINES`, then the feed fills in. Until then only "Today aboard" posts, system posts and Overheard show. Flags they asked for: `trad.tomorrow.<id>` / `trad.done.<id>` are passed as `ctx.flags` (nothing saved).
- **0.28.45:** no tray, no meal (the user's bug): `actStart` turns an 'eat' without `o.fed` into 'sit'; a table tap without a tray just sits you; only the servery line gives `SHIP.player.tray`. Reviews now go to reviewer 1d (session_01AxGXvu4gwTfNVGRKeYbBPw); head writer 4 is session_01MWyyMaXv6D7yKtDNy9VbCA.
- **0.28.46-0.28.47:** head writer 4's tip text; the slow arrival was 0.61.5's sick days (`SHIP.career.sd` 0 matched day 0): `sickToday` needs `sd > 0`. 0.60.5 declares `NEWS_MAX`: the feed's is `FEED_MAX`. device_check's heads-up checks fail on 0.60.5 itself (not ours). Reviewer is now 1e (session_01BcEWju7cay3mnujaL1apzU).
- **0.28.48:** Pause (`PAUSE`, `pauseSet`, `#pauseBtn`, `#pauseCard`; the main loop skips the sim while paused; hidden tab pauses). `TOAST_AT` (toast() stamps it) replaced reading the toast's DOM class: cadet_test compared with itself was differing because real-time toast/tip timers changed what warnings and tips did; cadet_test's `run()` now turns tips off. Inline `display:flex` beats `[hidden]`: toggle `style.display`.
- **0.28.49:** reviewer 1e's MEDIUM (tradition posts showed ids): the feed passes `{ trad: name, tradId: id }`, section 22's `trad` condition matches `ctx.tradId`. Tradition social capped at +20. t:rep: head writer 5's text, 30 ship minutes after the turn-in. 1e's LOWs (in their review note: content timing lines, the 720-minute catch-up, WARN_SAID not saved) are still open, all optional.
- **Gotchas:** an inline `// comment` inserted mid-line swallows the rest of the line (twice now: a JS string in device_check, the TEACH row): put comments at line ends. section 20 has `newsAdd` (so the feed's is `feedAdd`); check new top-level names for clashes, `node --check` misses duplicate function declarations. cadet_test's time skip drains bathroom to 0, so comparisons across 0.28.41 differ unless '+go'/warnings are switched off in a copy. player_check tests that call `teachTick` with a future `t` leave `TEACH_CK` ahead: reset it. A heads-up up (DEV.hu) used to block warnings forever: now only its arrival counts.
- **Open:** head writer 3 to polish t:rep; check the feed with the real bank after the content merge (kinds `news.<src>`, `{machine}` from ctx, `cue:repair.you`).

## Update: builds 0.28.35 to 0.28.40 and the save budget (player engineer 4; refreshed 2026-10-17 ~12:10 UTC at handover)

Read this first. Lead: session_01KPJMYjXAPkNUcrQ8VRkhLE. Reviewer 1c (session_01YcSJkhhJ2MnCjsJs7QV8ud) reviews this branch; build master 2 (session_01F8ph7FKqViF3heRn94YgBr) combines. Galley engineer 3: session_018cicfPQZQXbxmtn6ygmL84. Sim engineer 4 (sim 3 retired): session_01EJUGywZv9BpcUezjXES9AC. Device engineer 3: session_01SskqNx45iEGyQq2W9Fjg5Y. Next build **0.28.41**. Branch head at handover: see the last commit on `claude/player-needs` (this note; the game is 0.28.40 = 9c18045, after it only player_check, DEV_NOTES and this note). Reviewer 1c passed everything to 9c18045 (0.28.40); build master 2 was sent cb01633 for 0.60.3 (pairs with sim 0.26.36). No player work in flight.
- **0.28.35:** the old open player_check failure was a test stub: the game runs inside one wrapper function and `__sc` evaluates inside it, so `window.galleyTurn = ...` never reached the game's own `galleyTurn`. **Rule:** a `window.x` stand-in only works for a name the build doesn't declare; to override a declared function, assign it bare inside `__sc` (and restore it). Leave calls `galleyLeave`.
- **0.28.36:** you join the real line on reaching its back, not at the tap (from across the room you stood at its front while walking and everyone waited). The stand-in heads for the line's current back while sliding in (`phase 'in'`), camera with it.
- **0.28.37:** **owner's ruling: section 16 owns your place in the line.** Section 15 calls only `galleyJoin('player')` / `galleyLeave('player')` and reads `lineSpot('player')`; never `lineJoin`/`lineLeave`. Tap: galleyJoin, read the back, galleyLeave; arrival (`actBegin`): galleyJoin again. Reviewer 1's fixes: `DINNER_SAT` reset in `playerNew`, saved flag `intro.dinnerSat` (`dinnerSat(v)`), `DINNER_TRY` (once a ship minute), `bunkSleep` checks `bedtime()`.
- **0.28.38:** tray cleared by the SIM_ADVANCE hook and off Deck 3; `dishName`; strip pulse in tenths (`STRIP_G`) without a rebuild. player_check: real-line case for combined builds (when `servLine` and `galleyLeave` exist).
- **0.28.39:** the till re-checks credits; a full locker (`LOCKER_MAX` 40) keeps the new comfort, oldest goes.
- **0.28.40:** `crewMakeWay(tile)` fallback (sim 0.26.36): a refused walk-to tile -> `phase 'wait'`, retry every 0.5 s for 8 s, `A.release()` in `actEnd`. Sim 0.26.36 also steps crew aside automatically on tiles two places share, so it rarely fires. player_check's squeeze test now uses [39,3] (not the shared [39,4]; 9ba424c): it passes with sim f16a110 alone and with e4d6ace (0.26.37, which restores squeezing past a shared tile) on top; build master 2 told to keep it.
- **Scratch merges:** galley a39965f (0.29.34) + player 9c18045 + sim f16a110 (0.26.36): player_check's job loop passes; food_check's "galleyJoin / galleyTurn" FAIL there is galley+sim's (it fails without this branch too). Merge conflicts are always the header build line, `GAME_BUILD` (keep the bus block from ship-integration), cadet_test's style line and the washer test; a resolver script did it (take the base side for the build lines).
- **The whole-save budget (you own it):** 250 KB at any point to day 280. `python3 player_check.py BUILD.html --long [DAYS]` (f77e985; ~2 min; skipped without section 13) plays from the real arrival with `skipTo`, saves daily, prints the biggest parts every 10 days, fails above 250 KB. On combined 0.60.2: largest 149.9 KB on day 257 (social 53.4 KB and growing ~0.13 KB/day, ship.jobs 25-50 KB with the board, mail 21). Details in DEV_NOTES "The whole-save budget". Run it on each combined build that adds saved state.
- **Open:** the breakfast line of 21 when a scene starts at 07:12 is sim 4's (time-jump artifact). Galley's food_check "galleyJoin / galleyTurn" FAIL is fixed by galley a0e5b2f (in 0.60.3). Nothing else open for section 15.
- **Testing gotchas:** set `CADET_CHROME=/opt/pw-browsers/chromium` (pip's newer playwright wants a browser that isn't installed). Test a copy of the html (`cp` to the scratchpad) so editing the file doesn't change a run halfway. One browser check at a time; stop a run with TaskStop and `pkill -f "[c]hromium"`. Real-line probe script idea: step 10 frames, read `servLine()`, `lineSpot('player')`, `ACT.phase`.

## Update: builds 0.28.29 to 0.28.33 (player engineer 3's last; written 2026-10-17)

Read this first. Lead: session_01KPJMYjXAPkNUcrQ8VRkhLE. Next build **0.28.35**. **0.28.34** wired the food line part 2 (sim engineer 3's `lineJoin`/`lineSpot`/`lineLeave`, section 10 on claude/sim-engineer 0.26.30; see its DEV_NOTES row), tested against stand-ins only: **first job for my successor: verify it on a scratch merge with claude/sim-engineer** (join, walk up as the line moves, served at the front, Leave). **Before that: one open player_check failure** (DEV_NOTES 0.28.34 row): the stand-in line check ('moving with the line') passes alone (scratchpad-style quick run of just that block on Deck 3 at 17:40) but fails in the full run: the player is served during it although the test sets `window.galleyTurn = () => false` (find out what serves you: the queue def's `until` calls `galleyTurn('player')`; check whether section 16 serves by another path in that state, e.g. `foodFrom`/`GALLEY_JOINED`). I added cleanup after it so the later checks (servery closed at 12:00, the cart run) aren't hit by a leftover tray; rerun player_check to confirm. Sim engineer 3's real line is on claude/sim-engineer 0cf991a (0.26.30). Device marks are order-agnostic now (build master 2's ask, device 0.35.28 lists penalties first). Check DEV_NOTES' 0.28.30-0.28.33 rows for their test results (one full suite covers them; if a TESTS cell is still empty, run the six checks first).
- **0.28.34:** moving with the real line: lineJoin at the tap, lineSpot each frame in `actUpdate` (the stand-in walks a tile at a time, `player.obj` follows), lineLeave on any unserved end (`actEnd`).
- **0.28.33:** the needs strip folds to one heart icon (chevron ‹; `stripFold(on)`, saved as `save.player.stripFold`); the heart is amber while a need is low. Chain of command: the user -> the lead -> everyone; never contact the user.
- **0.28.29, lie down** (the user's "I can't lay down in bed"): tap your own bunk -> `bunkLie` (activity `lie`, the 'lie' pose at the bed place's height); rest: no energy drain + `LIE_GAIN` 0.05/min; from 20:00 `bunkSleep` calls section 13's `offerSleep` once lying (fade, 06:00) and the SIM_ADVANCE hook keeps a `lie` going, so you wake in the bunk. `bunkTap` no longer needs section 20.
- **0.28.30:** no queue count/countdown (`actProgress` null for 'queue'; toast "You join the queue."); social B2's `homeBooth()` hook at the end of `actBegin` for 'call'; Mail's optional `play` field (device engineer 3 asked; social B2 then said not needed; kept, inert).
- **0.28.31, the food line part 1:** served -> `SHIP.player.tray` (dish, not saved), control back, `player.holding` 'tray'; `actStart` turns 'eat'/'sit' at a mess-seat into eating the tray; while queueing a tap/drag shows `queueAsk` ("Leave the queue?" Leave/Stay; `queueLeave` calls `lineLeave('player')` if present). **Open: part 2, moving with the real line** (sim engineer 3, session_01517opwS4UAxYZKNwJytaEK, builds section 10's line; I proposed `lineJoin('player')` -> {x,z,face}, `lineSpot('player')` each frame -> {x,z,face,front}, `lineLeave('player')`; no reply yet). The 'queue' activity's stand-in should glide to `lineSpot` (walking pose) and end when `front` (or galleyTurn); the lead agreed the shape.
- **0.28.32, the needs strip:** see the DEV_NOTES row. Device engineer 3 (session_01SskqNx45iEGyQq2W9Fjg5Y) matches the Needs page using `NEED_COL`, `NEED_AMBER`, `NEED_ICON`; their 0.35.28 reads `NEED_ICON`, `NEED_COL`, `NEED_AMBER`, `NEED_LOW` and builds short effect lines from `NEED_FX`: tell them before renaming or removing any of these.
- **Also:** 0.28.28's dinner seat clash (Calder heads for 3-mess-10) waits on the sim engineer.
- **Gotchas:** cadet_test exits 0 even with DIFFERENCES: grep its log for ALL IDENTICAL. `node --check` on the extracted main script catches a duplicate `const` in seconds (a page that never loads shows only as a 60 s wait_for_function timeout). Needs screenshots: `needs_shots2.py`-style (load ?nosave, step frames by `window.__step`).

## Update: builds 0.28.26 to 0.28.27 (player engineer 3; written 2026-10-17 at 59df90b)

Read this first. **Lead is now session_01KPJMYjXAPkNUcrQ8VRkhLE** (since ~04:35; before it session_01PJtmxWgAPLebXSZKP6ZRpG, then session_01PxXKwc5mkC7tV5MPi3p7PP). **0.28.28** (3713f20): you sit at the arrival dinner (`dinnerTick`, `playerSitNear`; section 21's `introSeat('you')` = 3-mess-10 when free, else the nearest seat). Open: Calder's plan heads for 3-mess-10 on a merge with arrival 7abf466 (the sim engineer's seats). Next build **0.28.29**. Chain of command: the user -> the lead -> everyone; helpers never contact the user. Next build **0.28.28**.
- **0.28.26, kit bag** (onboarding engineer's spec, they confirmed): `KIT_BAG = 'kitbag'` in `P.carry`. `bagTick()` (each frame, playerUpdate) gives it while `introOn()` && `SHIP.intro.step === 'ramp'`; stows it (toast) when `SHIP.intro.done.bunk` is set and 'bunk' isn't in `SHIP.intro.missed`; quietly when the intro is off. Missed bunk: held until a tap anywhere in Bunk 1, Deck 4 (`bagLockerTap`, first line of `playerFloorTap`; bunk lockers have no description). `bagGive/bagStow(quiet)/bagHeld`; `handsFix(what)` words hands-full toasts; main storage's stow skips the bag. Section 21 has no hook (0.42.9 dropped its bagGive call).
- **0.28.26, device lock:** `deviceLocked()` (introOn() && !introFlag('intro.device')), `deviceLockedTap()`, `deviceLockLook()` in floatsTick (label "No device yet", opacity .6, no need glow), capture click listener on #devBtn. Device engineer's 0.35.21 calls deviceLocked/deviceLockedTap in deviceShow: **keep these names**.
- **0.28.27:** STORE gift names per social A 0.36.39: bar of chocolate, paper novel, + music chip, pocket puzzle, spare tiles set (ten store gifts).
- **Test-only:** washer tap accepts a real 4-washer-N (machineTap's nearest, verified on a scratch merge with decks 77d7c44 + systems ae58e43); a junk saved name loads as null. The manifest name has been saved since 0.28.22: reviewer 1's "lost on reload" was on builds without 0.28.22.
- **Checks:** all six green on 0.28.27 (cadet ALL IDENTICAL vs 0.28.25).
- **Gotchas:** in player_check's Saving section frames only move with `window.__step(n, dt)` (virtual rAF), not by waiting. Never `pkill -f player_check.py` from a shell whose own command line contains that text (it kills itself); match with `pgrep -af "[c]adet-game/..."`. Fresh container: `pip install playwright` + `npm pack three@0.128.0` into /tmp/cadet-work/three (DEV_NOTES Testing).

## Update: builds 0.28.22 to 0.28.25 (Pillar 4 on-call rows; written 2026-10-17 at c44df18)

Read this first. Lead: session_01PxXKwc5mkC7tV5MPi3p7PP (build master session_012K7RZ3oSX2vpBb1rR66MBh). Branch sits on ship-integration 0.41.10 (6d91ee1) + systems 0.33.36 (22fb801). Next build **0.28.26**. Pillar 4 plan: `plans/pillar4-plan.md` ("On call": player engineer = kit bag, device lock, gift tags on carried items).
- **0.28.22:** `simAct(act, o)` -> `simNote('act', ...)` (typeof-guarded; section 13's bus not merged yet): wash (shower), eat (`with`: company; grab 0), call, buy (`item`), laundry (a washer run). `SHIP.player.name` + `playerNameSet(v)` (trim, 24 max, saved as save.player.name; onboarding's introBegin calls it, SHIP.intro has no name).
- **0.28.23:** +N notes and the device button's glow fade by `performance.now()` in `floatsTick()` (no CSS animation / setTimeout), so tests are deterministic. cadet_test also hides `#needFx` and `#devBtn` box-shadow (2806e6d).
- **0.28.24:** reserved jobs' `j.make` ('bracket'): never fetched (`shelfNeeds`), made first in the machine shop (`makeMins(j)`: j.makeMins or 60), `jobStopMark(j, 'fetch'|'make')` -> section 17's `jobStepDone` (only for jobs with j.make). Systems engineer confirmed.
- **0.28.25:** gifts (social A's section 20, inert until merged): STORE lines' 4th element = gift name -> `giftAdd` on paying (hands full: bought as before); machine shop with no job makes `GIFT_MAKES` in turn (activity `craft`); `bunkTap` shows `bunkNote()` first; `gardenGift()` (minute tick) gives herbs/tomato from your garden run's lot after pickup on `gardenHarvestDay`; `giftHeld()` words hands-full toasts. Social A confirmed.
- **Checks:** 0.28.22 green; 0.28.23 deck/day green, cadet self-identical; 0.28.24 cadet identical vs 5f62c05, deck/day OK, player running at writing; 0.28.25 untested at writing (see DEV_NOTES rows' "Checks").
- **Names others rely on:** keep `NEED_PULSE` (the device's device_check sets `NEED_PULSE[k]` directly, 0.35.20), `needPulse`, `actProgress`, `playerNameSet`, `FLOAT_LOG`.
- **Gotchas:** the store test pays for `{ ...storePick(k), gift: null }` (gift lines go to hands). Stand-ins via `window.x` work only while the real function is absent from the build. Comparing against ship-systems alone shows huge diffs (it lacks 0.41.10's decks): compare against your own previous commit.

## Update: builds 0.28.19 to 0.28.21 (the user's bathroom need and "You can see it working"; written 2026-10-16 at 15d0209)

Read this first. The lead is now session_01PxXKwc5mkC7tV5MPi3p7PP. Branch `claude/player-needs` sits on ship-integration d89a3f5 (0.41.7); next build number **0.28.22**. All checks green at 15d0209 (cadet_test identical except the debug Day skip's "+69 Energy" note in f_noshadow, which is expected).
- **0.28.19, bathroom:** sixth need `bathroom` on the end of `NEED_KEYS` (label Bathroom), drains 12/h awake, 3/h asleep; `NEED_FX.bathroom` high tasks x1.05, low x0.9 (keep the key and the NEED_FX row together: the device's Needs app breaks without the row). `PLAYER_ACTS.toilet` (+100 in 3 min, sit); `ACT_TAP` `/^toilet$/`, `FLOOR_ACTS.toilet`; `PRIVATE_TYPES` (shower, toilet) never offers someone else's (privatePlace). New game 60, a save without it 80.
- **0.28.20, notes:** `needsSeen()` (end of playerUpdate) diffs the needs each frame and floats "+N Need" (`needFloat`, `#needFx`) when a rise stops (0.6 s) or every 5 s while it goes on; pulses `#devBtn`; `needPulse(k)` (the device engineer's Needs bars use it, device 0.35.19); `FLOAT_LOG` for tests. Times are `performance.now()` (virtual in tests) but the fade/removal is real time, so tests read `FLOAT_LOG`, not the DOM.
- **0.28.21, progress:** `actBar()` / `actProgress(A)`: one bar over the stand-in for any ACT with a fixed `def.mins` and no `until` (incl. 15b's), the queue's wait to `turnAt`. 15b hides its goal marker while `actProgress()` is non-null (their 0.37.x).
- **Gotchas:** any player_check test that times an activity must pin `bathroom: 50` (its task effect); section 17's `shipEffects` doesn't list bathroom (counts 1). Python output is buffered when redirected: use `python3 -u` for live logs.

## Update: builds 0.28.9 to 0.28.17 (the answers pass and after; written 2026-10-16 at b6e8d7e)

Read this first; the older sections below still hold except where this says otherwise. DEV_NOTES "Player needs and the device" has the full detail and the build rows.

**Branch state.** `claude/player-needs` at b6e8d7e sits on merges of ship-integration 0.41.5 (8027d4b), the device engineer's 0.35.0 and systems 0.33.20. The lead merges from it into `claude/ship-integration` (0.41.x). Next build number: **0.28.18**.

**What these builds added (all in section 15 unless noted):**
- **0.28.9, needs give bonuses:** `needEffects(needs)` -> `{ walk, task, drain, socialGain, notes, marks }`. At 75 or over a bonus, under 25 a penalty, effects multiply; the table is `NEED_FX` (in DEV_NOTES). `task` speeds activities, repairs and making parts (`A.done += dm * task`; `taskMins`). Energy drains 4.4 an hour awake: 16 hours (unfit), 17 (average) or 18 (fit) to the tired line. Your bunk from 20:00 sleeps you straight to 06:00 (section 13's offerSleep calls the Sleep button's handler: one line).
- **0.28.10, mail, chatting, store:** `mailSend({ at, from, subject, body, quiet })` and `SHIP.mail` (saved as `save.mail`), `mailUnread()`; the welcome on a fresh start. `playerChat(p)`: +6 social for the first chat a day per person, times socialGain. Since the social engineer's 0.36.1 it's called from their chat card's Chat button, not the crew tap. Company at the mess table: +0.2 a minute each, up to three. `SHIP.player.credits` (40, +15 a job), `locker`, `chats`; `STORE`, `storePick`.
- **0.28.11:** `machineTap` (a real machine within 1.2 m -> section 17's `machineUse(id, 'player')`); the cart run (`cartTap`, `cartStep`, `cartAuto`, `cartEnd`, `SHIP.player.cart`, places from `jobStops` when present; meals runs call the galley's `galleyCartLand`); crawl tiles (`crawlTiles()`, `CRAWL_SPEED` 0.5, `player.crouch`).
- **0.28.12:** sit anywhere (`sitTap`, `SIT_TYPES`, activity `sit` until you walk away; rest `SIT_REST` 0.6, `SIT_GAIN`); squeeze past settled crew (`squeezePath` from one line in section 10's `Walker.goTo`, `squeezeStep` slows you and says "Excuse me, Chef"); 15b's `PLAYER_TAPS` hook in `playerTap`.
- **0.28.13:** player_check only (the cart test takes a free dock and checks the delivery across the docking).
- **0.28.14:** `stubTap`: stub machines (the washers) matched by room, kind name and number.
- **0.28.15:** the tray: `player.holding = 'tray'` walking from the servery or queue to your seat, `'walk+tray'` on the stand-in; `TRAY_ON` (one mesh made at load) on the table while you eat.
- **0.28.16:** on the device engineer's 0.35.0. **The placeholder device is gone:** the device is section 19's (theirs). `device` is a shim there and `deviceOn` is theirs; never fire it from 15. Their apps read only section 15's data (needs, needEffects, needsLine, playerSpeed, credits, locker, carry, work, cart, SHIP.mail, mailSend, mailUnread, ACT). The welcome mail and the job notice now say jobs are taken at the job board.
- **0.28.17, the user's treadmill report:** things with no description of their own aren't tappable (only the middle treadmill had one), so `playerFloorTap(point)` (one line in section 11's `tap`, before a floor tap walks) follows the tap's line of sight up to 1.2 m and uses a gym place, booth, store shelf or public seat it passes within 0.5 m of. A workout costs 6 energy (`PLAYER_ACTS.gym.cost`; any activity may carry a `cost`). Screenshots are in `plans/shot-0.28.17-*.png`.
- **Other people's lines in section 15 and its hooks, keep them at merges:** the galley's numeric face for `galleyJoin`; the performance engineer's Walker pose line (held things win over `'+device'`); 15b's `ixHold()` at the end of the hold expression; and the interactions engineer's player_check lines (`turnInJob` before reading a finished job; `holding is not True`). All are inert without their sections.

**Gotchas learned:**
- **player_check now takes about 25 minutes.** Give it `timeout 2400` or more: a 1500-second limit killed it once mid cart-run, which looked like a hang.
- **The repo ignores `*.png`.** Use `git add -f` for screenshots.
- **Clicks in tests:** a `page.mouse.click` outside the viewport silently does nothing. Put the player near the target first (the camera follows the player) and check the projected point is on screen.
- **Merges:** expect conflicts only in the header build line, `GAME_BUILD` and the DEV_NOTES table or sections. Keep both sides of DEV_NOTES.
- **Food in player_check depends on sections 16 and 17:** a starved galley (cart runs never claimed) once made every eating test fail. Diagnose supply (`galleyText`, `SHIP.galley.cold`) before blaming taps.

**Loose ends:**
- `cartsOut()` reads the player's cart since systems 0.33.20; check the parked cart hides while you push one.
- C11: verify on a combined build that a crate, cart or tray in hand wins over the raised device.
- The stand-in body during activities never shows the device or chores' toolboxes. Decide with the performance and interactions engineers whether it should.
- `playerChat`'s toast remark goes to a hidden toast now that the chat card is used. Harmless; drop it or add a `quiet` option if the social engineer asks.

## Role

- **Who:** the player engineer, Pillar 2. Workstream A3 (the player's needs and activities, the walking-speed rule, the placeholder device), then the player's side of B2 (the job loop).
- **Branch:** `claude/player-needs`. **Builds:** 0.28.x (0.28.1 to 0.28.8). The lead merges them into `claude/ship-integration` (0.40.x).
- **Section of the game file:** `// 15. PLAYER NEEDS & DEVICE`, which sits after section 14 (like 13 and 14, not at the end of the file). Plus small hooks elsewhere, listed under "Hooks" below.
- **Test script:** `player_check.py` (mine). Run all six checks every turn: cadet_test, deck_check, day_check, food_check, machine_check and player_check.

## What's built

### Needs
- `SHIP.player.needs = { hunger, energy, hygiene, fitness, social }`, 0 to 100, 100 = fully met. The key list is `NEED_KEYS`; section 14 declares `NEEDS` with the same list, so don't redeclare that name. The device labels hunger "Food".
- **Drain** per ship hour, awake / asleep (`NEED_DRAIN`):
  - hunger 4 / 2
  - energy 3.75 / 0
  - hygiene 2.5 / 1
  - fitness 0.6 / 0.3
  - social 1 / 0.25
- **Sleep:** asleep, energy rises 12.5 an hour (`SLEEP_GAIN`).
- **Activity gains** (`PLAYER_ACTS`), spread over the activity's ship minutes:
  - a meal at a mess seat +55 in 20 minutes
  - the grab shelf +25 in 3
  - a shower +80 in 10
  - a workout +30 in 30
  - a call home +40 in 15
- **Starting values:** a new game 60 / 100 / 60 / 70 / 70; a `v: 1` save 80 each.
- **Walking speed (the user's rule):** fitness under 25 → 80%; energy under 25 → 80%; both → 64% (`SLOW_BELOW`, `SLOW_SPEED`, `playerSpeed()`). `playerUpdate` sets `player.maxV = PLAYER_V0 * playerSpeed()` each frame, so at full speed it's exactly the old number. Nothing else is ever punished.
- **Time:** `playerUpdate(dt, t)` (main loop) drains by ship minutes since the last frame. A time skip (`SIM_ADVANCE`) drains the gap at once:
  - asleep if you chose Sleep (`sleeping`, section 13), or for any skip starting at night (the debug Day button);
  - awake otherwise.
- **The machines' effect:** `shipEffects(deck)` (section 17) multiplies drains (`drain[k]`) and gains (`restore[k]`). It's read once a ship minute by `playerFx()`; skips use the pure `shipEffectsAt(deck, from)`, which never runs the machines. **`fx.walk` is deliberately ignored** (the user's rule: only fitness and energy slow you).

### Activities (tap the thing)
- The item tap in section 11 asks `playerTap(item, itemPos, tapPoint)` first.
  - `ACT_TAP` maps the item's title to place types and an activity.
  - It then picks the nearest free place of those types within `ACT_NEAR` (2.4 m) of the item.
  - No match → the tap does what it always did.
- **The activities:**
  - shower: public washrooms only; anything private, by room or by a bed's name, is left alone;
  - servery: the galley's queue (`galleyJoin` / `galleyTurn`), then a mess seat;
  - mess table: sit and eat;
  - grab shelf;
  - treadmill, weights, rower, mats;
  - call-home booths;
  - shop shelves, then the counter: browse, then pay. Shopping restores nothing yet.
- **How it plays:** you walk to the place's walk-to tile; a stand-in `FullPerson(PLAYER_SPEC)` slides onto the spot and takes the pose (`poseOf(place)` from section 8b when it's there); your Walker waits hidden on the walk-to tile. Walking away stops it and keeps what you gained.
- **Places crew hold** (`heldBy`: a crew agent's `goalId`) are left alone ("In use: …"). If someone gets there first, you move once to the next free place of that kind.
- **Food** goes through `foodFrom(where, peek)`:
  - with section 16: `takePortion('player')`, and `galleyText` for the dish and the "Closed" text;
  - without it: the meal windows.

### The device (a PLACEHOLDER)
- **The button:** Device, under the clock. It gets an amber dot when a need is under 25.
- **The panel:** `#device`. Sections come from `device.addSection(id, title, render)`, where `render(el)` fills a fresh `el` on opening and every ship minute while open. Also `device.open()`, `close()`, `refresh()`.
- **My sections:**
  - `now`: time and day; what you're doing or a status line (`needsLine()`); "Carrying: …"; your job's progress; the first two ship notes.
  - `needs`: five bars, plus "Walking at N% speed".
- **Other sections:** section 17 adds `jobs` (take it, drop it).
- The user is designing the real device: replace the panel, and keep the data and `addSection`.

### The player's job loop (B2)
1. **Take a job** on the device (section 17's Jobs section).
2. **Tap the machine** (anything near its panel place): you walk to `panelPlace(machine)`. Parts you carry are fitted. Then:
   - the first visit with parts missing is a 3-minute look over that says what's needed;
   - with every part in, you repair for `JOB_TYPES[kind].work × (1 + 0.25 × (tier − 1))` minutes;
   - when done, `finishJob(id)` puts the machine right.
3. **Fetch** (main storage, Deck 5, room `r`): you walk to the nearest free `5-parts-N` place, look for 4 minutes, then `takePart` each needed part. You carry two at most (`CARRY_MAX`), so a three-part job takes two trips.
4. **Make** (machine shop, room `f`): only when a needed part has `SHIP.stores[part]` at 0 and isn't in `NO_MAKE`. You walk to a free `5-make-N` place; it takes 60 minutes and the part goes into your hands. Stores are never written by me.
5. **Pausing:** walking away pauses repairing and making. Progress lives in `SHIP.player.work = { job, fitted: [...], done, seen, make: { part, done } | null }`, and `SHIP.player.carry = [...]`.
6. **Keeping the job:** `touchJob(id)` on progress keeps the job yours past the 12-hour lapse.
7. **Putting parts back:** with no job, a tap in storage puts carried parts back (`returnPart`).
8. **Notice:** when a job you could take is posted and you're free, a "Your device: New job: …" toast (`jobNotice`). Jobs posted during a skip aren't announced.
9. **The crate prop:** carrying shows a crate in your hands. `player.holding` makes `Walker.update` call `animateActivity(this, 'stand+carry')`.

### Saving
- `SAVE_V = 2`. `player.needs`, `player.carry` and `player.work` go in through `SAVE_EXTRA` (section 13); my hook creates `save.player` if it's missing.
- `loadGame` accepts `v: 1` and `v: 2`. `needsLoad`, `carryLoad` and `workLoad` read defensively (clamped, strings only, junk → defaults).
- New game calls `playerNew()`. `?nosave` neither reads nor writes.

### Hooks outside section 15
- **Section 13:**
  - `SAVE_V = 2` and `SAVE_EXTRA` (the systems engineer's lines, copied exactly);
  - `loadGame` takes `v: 1`;
  - `playerNew()` in New game.
- **Section 11:** one line at the top of the item tap: `if (playerTap(...)) return`.
- **Section 12:** `playerUpdate(dt, t)` after the walkers.
- **Section 10:** `Walker.update` uses `animateActivity` once `player.holding` has been set, otherwise `animateRig` as before.
- **The header and the HTML:** the file map line, and the device's HTML and CSS.

## Functions other sections rely on (or I rely on)
- **Mine, used by others:**
  - `device.addSection(id, title, render)` and `device.refresh()` (section 17's jobs section);
  - `playerHolds()`: the place you're using, or null (meant for the schedules; not wired by them yet);
  - `SHIP.player.needs`, `.carry`, `.work`.
- **Theirs, used by me** (all guarded with `typeof`, so section 15 runs without them):
  - section 16: `takePortion`, `galleyText`, `galleyJoin`, `galleyTurn`;
  - section 17: `shipEffects`, `shipEffectsAt`, `myJob`, `takePart`, `finishJob`, `touchJob`, `returnPart`, `panelPlace`, `machineById`, `jobTier`, `JOB_TYPES`, `jobsBoard`, `jobCard`, `PLAYER_TIER`, `ENGINE_KINDS`, `NO_MAKE`, `MACHINE_KINDS`, `SHIP.stores` (read only);
  - section 8b: `poseOf`, `animateActivity`, `FullPerson`;
  - section 10: `placeSpot`, `PLACE_OF`, `DECK_CREW`, `CREW_SPEED`, `FACE_ANGLE`.

## State at 0.40.8: loose ends and weak spots
- **Crew don't avoid your place.** A crew member can walk onto the treadmill you're on. `playerHolds()` exists for the sim engineer, but isn't used yet.
- **The shower pose is just `stand`.** No shower or washing pose exists.
- **Shopping restores nothing.** Items come later.
- **Grab-shelf taps can serve a hot portion.** `takePortion` gives the servery's portion first if there is one. A `takePortion(who, where)` from section 16 would fix it.
- **Activities run in real ship time** (no time controls, by the user's decision): a workout is about 37 s, a meal 25 s, a repair 25 to 112 s.
- **Activity choice depends on item titles** (`ACT_TAP` regexes such as `/^booth/i`, `/table/i`). Renaming an item in the deck dressing can break a tap. The place-proximity check stops false matches, but not missed ones.
- **Talking to crew doesn't raise social.** "Company can come later" (design).
- **The device is a placeholder.** It'll be redesigned.

## Things I'd fix next
1. Crew stepping around `playerHolds()`: the sim engineer's side; a one-line check in `planDay` / `CrewAgent`.
2. Social from company: eating near friends, or talking (once per person per day).
3. Item kinds instead of titles for `ACT_TAP` (needs `place()` to record the kit kind on items).

## Gotchas
- **Name clashes across sections break the whole merged build.** My `NEEDS` and `ACTS` collided with sections 14 and 8b; they're now `NEED_KEYS` and `PLAYER_ACTS`. Before a push, grep the other branches for any new top-level `const` or `function` name.
- **Stand-ins in tests get shadowed.** Once the real functions are in the build (declared inside the game), `window.x` stand-ins are ignored. `player_check` tests the real ones when present (`typeof` in scope), and uses stand-ins only when they're missing. To set a known `shipEffects` result, write `playerFx`'s cache (`FX_MIN`, `FX_NOW`).
- **Merges:** expect conflicts only in the header build line, `GAME_BUILD`, the DEV_NOTES build table and the file map. Keep both sides of section bodies.
- **A merge-resolution regex once ate a `// =====` section line.** Anchor conflict markers to the start of a line (`(?m)^=======`).
- **`pkill -f player_check.py` kills your own shell.** The command line contains the same text. Kill by PID instead.
- **Run the heavy checks one after another, not in parallel.** Two at once made `deck_check` time out loading the page; that's not a game failure.
- **cadet_test pixels:** the device button sits in screenshots. Against a build without it, hide `#devBtn` in a copy to prove nothing else changed. Against 0.40.x it's ALL IDENTICAL.
- **Save hook:** machine_check builds a partial save; the hook must not assume `save.player` exists.
- **Tuning numbers** live at the top of section 15: `NEED_DRAIN`, `SLEEP_GAIN`, `NEEDS_FRESH`, `NEEDS_OLD`, `SLOW_BELOW`, `SLOW_SPEED`, `PLAYER_ACTS` (minutes and gains), `ACT_NEAR`, `CARRY_MAX`, `INSPECT_MINS`. Fetch is 4 min and make 60 (`PLAYER_ACTS.fetch` / `.make`).

## How to test
- **Setup:** see `DEV_NOTES` "Testing". Use `CADET_CHROME=/opt/pw-browsers/chromium`.
- **player_check:** `python3 player_check.py BUILD.html`, about 6 to 8 minutes. It ends `PLAYER CHECK OK`. It covers:
  - a week on paper: a normal day's lowest values are food 55, energy 40, hygiene 52, fitness 62 and social 39.5, never slowed;
  - the speed rule: 1, 0.8, 0.8, 0.64;
  - sleep and skips;
  - every activity tapped on the real decks, with its pose and gain;
  - held places, the closed servery and walking away;
  - the real galley queue, and the ship's effects through a set reading;
  - the job loop against the real jobs: inspect, fetch, pause, resume, finish (condition 100), making a part, the notice, two-part carrying, putting parts back, the crate flag;
  - saving: `v: 1` → 80, `v: 2` kept, junk clamped, `?nosave`.
- **The other five checks must stay green:** cadet_test ALL IDENTICAL against the build you started from, deck_check, day_check day 1, food_check and machine_check.

## Ideas and open questions for the user

(Answered since: social from chatting and company yes, shopping buys things yes, machine trouble slows only the crew. Still open: what the real device should show first is now the device engineer's.)

- **Should talking to crew, or eating with company, raise social?** Today only calling home does.
- **Should shopping buy things** (snacks that restore a little hunger, small comforts), or stay a nice moment?
- **The device:** what do you want on it first, now that needs, jobs and notices all show there?
- **Should machine trouble slow you down?** The machines' `walk` effect is ignored for the player by your rule. Keep it that way?
