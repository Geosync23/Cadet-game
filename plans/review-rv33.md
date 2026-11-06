# Review RV33 (0.99.7 playtest patch)

Reviewer RV33, session_01GKuymoAK9gACR31MRd1CMX, branch claude/review-rv33 (notes and probes only).
Lead: lead 49 (session_01GKuymjjreuZtZeDMBX79xn). Brief: plans/patch-0997.md on claude/lead-49.

Reviews: SC1 (claude/p997-social), CL1 (claude/p997-calendar), EV1 (claude/p997-events),
GM1 (claude/p997-games), TB6 (claude/p997-traditions), AV1 (claude/p997-av).
EV1 and CL1 also checked merged together for first-week clashes.

## Setup
- Base: claude/integration d7ad4c58, game f6ff5ec1...db8a8. cadet_test base vs itself: ALL IDENTICAL.
- Kit: playwright, numpy, pillow; three r128 and acorn 8.12.1 in /tmp/cadet-work; CADET_CHROME=/opt/pw-browsers/chromium.

## Week-1 calendar probe (lead 49's rule: fresh save, intro ON)
- plans/rv33-probes/week1_cal.py BUILD [--json OUT]: fresh save, newGameStart(true), then Days 0-8: traditions (eventsOn),
  events-base beats, call-in meetings, the intro week's timed beats; prints every overlap (the shift and seek-anywhere beats left out).
- Base listing: plans/rv33-probes/cal_base_f6ff5ec1.json. Base overlaps of note (already there before 0.99.7):
  Day 2 call-home booths 18:00-19:00 x Spice shelf supper 18:15-19:15 x rec wall night 18:30-19:45 (TB6's note 51);
  Day 2 knit-and-natter x tiles night 20:00; Day 3 store visit 16:30 x open door 16:40; Day 5 jam x tap night;
  Day 6 Saturday run 07:00 (note 30 cuts it), tiles ladder x cook-along, film x observatory; Day 7 rec WSO 11:30-16:30
  under the Line ceremony and reading corner. Parallel optional evenings are not faults by themselves; what matters is
  anything the intro or an arrow asks the player to be at landing on top of something else asked of them.

## Results

### SC1 social and crew stories (claude/p997-social), switch P997_SOCIAL_ON
**85442de, game e19f1d10...41db (sha256 matched): FIXES NEEDED (one item).** Sections 20, 20c, 22 (generated words).
- Off: cadet_test vs 0.99.6 ALL IDENTICAL. check_fast on the commit: OK (257 s); on a switched-on copy: OK (275 s).
- Note 17 (sc1_card.py: fresh save, manifest signed, introSkip, core crew warmed, Day 9, beside them on their deck, 390x844):
  off: Say hello, Sit with them, Talk a while, Ask about, Help?, Meet up; Sit with them gone after Say hello.
  on: Say hello, Get to know, Talk a while, Help?, Meet up, Do you know...?; Get to know stays after Say hello and opens
  the beat (moment:brennan:1, moment:halloran-emeka:1). Good.
- Note 32 after talking: arrow later that day: off 2 samples (kovac Day 11: 22), on 0. Good.
- **FIX: note 32 shuts the arrow on any flicker.** p997WordOk sets shut when the beat stops being ready, so a person
  walking off a calm spot ends the arrow for the day though you never talked. sc1_arrow2.py (Days 9-22, every 5 ship
  min, never opening a card): off the arrow covers every ready minute; on, kovac Day 9 ready 580 / arrow 35, Day 16
  555/15, Day 18 305/10; torres-zeke Day 10 625/75, Day 13 695/125 (files sc1_arrow2_*_85442de.txt). Note 17 asks the
  story to appear consistently. Suggested: shut only on opening their card.
- Note 38: 575 talks have listen2 (the 4 without are smalltalk fillers); sample of 12 all answer the ask, then ask back;
  commonest opener "Not yet." 10 of 575. content_gen and lines_check changes are small and right.
- Area checks on the switched-on copy of 85442de: TALK CHECK OK, SOCIAL CHECK OK, lines_check PASS (0 errors, 112 warnings, as before).
- Note 39: joined hosted tradition rec-all-hands (marrow): 0 -> 3.2 (her relGain on +4); again same day: no change; not
  joined: no change; off: no change.

**6c39f3b, game f09f730c...f7ef (sha256 matched): the fix.** One line: p997WordOk no longer shuts on a flicker; only
opening their card (p997WordSeen) shuts the day's arrow.
- Off: cadet_test vs 0.99.6 ALL IDENTICAL.
- sc1_arrow2.py on: arrow minutes = ready minutes, every person every day, Days 9-22 (= off; sc1_arrow2_on_6c39f3b.txt).
- sc1_arrow_open.py on: after opening the card, 0 arrow samples the rest of the day (kovac Day 11: off 22, on 0).
- On copy: BUBBLE CHECK OK, DAY CHECK OK, INTERACTIONS CHECK OK. check_fast on the commit: QUICK CHECK OK (239 s).
- stories_check FAILED (14) in my first runs, the same 14 lines on the off copy, on 85442de-on and on unchanged 0.99.6:
  **my mistake: run with the default 30 days; the round runs 36 (backlog BM22-1).** The stalled beats are the ones due
  Days 24-36. Not date- or machine-dependent (cadet_test's INIT fakes Date.now; the check is on paper). Rerun with 36 below.
- stories_check 36 on the switched-on 77e573f: STORIES CHECK OK.


**77e573f, game 6df22594...1705 (sha256 matched): PASS** (sent to SC1 and the lead). The one change: p997HostNote skips an
appointment's event (TB6: apptKeep gives the host its own). Probe: appt-teach-me (sato) 0 -> 0, first-light (raman) 0 -> 4;
off no change. cadet_test off vs 0.99.6 ALL IDENTICAL. (SC1's check_fast on 77e573f: OK, 246 s.)

### AV1 sound and screens (claude/p997-av), switches SND_LIVE, SND_DISC (27), REC_FILM (4)
**15fbf3f, game 4f081164...d5b2 (sha256 matched).** Sections 4 (one line), 4e (+83, the film, rec engineer's), 8c
(one line), 27 (+147). All behind the three switches (const, off).
- Off: cadet_test vs 0.99.6 ALL IDENTICAL.
- Notes 13 and 29 in the real game (av1_levels.py, all three on, phone size, ?sound, a real tap to start the audio, skipTo
  the tradition): late piano Day 2 +18 min: Marrow at 4-music-1 (sit:play), the piece plays, the ship's music ducked to
  0 in the room, about half as loud just outside, nothing on Deck 3 or after it ends. Jam Day 5: Soto plays (sit:play),
  3 parts, the same fall-off. Loudness, hum muted, whole mix: a ship's track on Deck 3 about -50 to -60 dB; the piano
  -44 in the middle of the room, -36 beside it; the jam -33 beside the players. Louder than the ship's own music; the
  engine hum (whole mix about -31) is above all music in the existing balance, not AV1's to change.
- Note 42 (av1_film.py): the film canvas over a minute: lighthouse with sweeping beam, whales, the little ship and the
  ringed planet, sunset with two on a bench, credits; on the auditorium screen it reads the right way round from the
  seats; 133 draw calls; no page errors.
- check_fast on the commit: QUICK CHECK OK (263 s). sound_check (off build; it makes its own switched copies): SOUND CHECK
  OK, live and disc parts included. All three on: EVENTS CHECK OK; PERF CHECK OK (heap flat over a week, deck round trips).
- **PASS** (sent to AV1, lead 49, BM24). Owner note: 4e and 8c are the rec engineer's.

## Gotchas (for a fresh reviewer)
- stories_check needs `36` as its DAYS argument (backlog BM22-1); with the default 30 it fails 14 on any build.
- The chat card is position:fixed: don't filter its buttons by offsetParent. A card opened away from the person (not on
  your deck, out of reach) closes on the next frame: goToDeck to their deck and stand beside them first.
- A fresh save via newGameStart(true) needs the manifest signed (fill form input[maxlength="24"], click the form button).
- Copy BM24 (session_01GKuymnYTNkfxgLvtfFRg7w) on every PASS (lead 49). RV32 is session_01GKuymkDX3gviqiGJcKLWuS.

### GM1 games (claude/p997-games) - moved to SC1 by lead 49 (08:26 UTC)
Before the move: 9175156, game f8936885...e441 matched; cadet_test off vs 0.99.6 ALL IDENTICAL; every edit in 18 and 23
gated by GAMES997_ON; the ACT read in wsoWhere is in whereIs's live layer (tradWhere), not planDay. Handed to SC1.
Merge note: GM1 and TB6 both add their switch line after TRAD995_ON (section 13, line 9757).

### TB6 hosted traditions (claude/p997-traditions), switch TRAD997_ON (section 13)
**53bf2ce (tip 687838e8 adds probes only), game 84d3f8f1...4447 (sha256 matched).** Sections 13 (switch), 15 (2 hooks),
18 (+223, TB6's block), 24c (3 lines), 8b (+11: the loaf prop). With the switch off nothing runs (const).
- Off: cadet_test vs 0.99.6 ALL IDENTICAL.
- TB6's five probes, run here with the switch on (all OK): spice_fresh (fresh save, intro on, Day 2): Brennan at the
  shelf from 19:05, 28 crew there at 19:15, her card, a seat, three tasting plates, eaten by 19:41; clear of the call-home
  meeting (18:00-19:00). Open lab Day 9: card, you at the island, Sato held at 2-open-lab-2, her lines every third bubble.
  Bread day: kneading, loaf in hand, eaten at a mess seat, the loaf (not the tray) on the table; a short knead: no loaf.
  Bunk inspection: Calder stops, "Uniform: clean. Good." / "Bed: not made." / "Locker: tidy.", then "That's a pass" or
  "Not a pass this week. Make the bed before you go, please.", the notice, the Mail when away. Teach x4: each its own
  pose, four coaching lines, the result notice and flag.
- Close-ups (crop of the phone shot): the loaf on its board in your hand, and on the table while you eat: reads well.
- Should (not blocking): Open lab's crowd uses three `here` lines, so in half an hour each comes round about four times
  ("This one's older than the sun. Probably." etc.); Sato's six lines start over after six. More lines, or fewer crowd bubbles.
- Not a fault: the inspection notice logged twice 2 ship minutes apart is the toast queue (guideToast re-calls toast
  when the one on screen clears); the probe's hook sees both calls. Same pattern on other toasts.
- Switched-on checks: DAY CHECK OK Days 2, 4, 7; EVENTS CHECK OK; join, food (1 7), player, check_fast running.

### EV1 new events (claude/p997-events), switches EV997_LIGHT_ON, EV997_SAT_ON, EV997_READ_ON
**8632e57, game 400346af...9451 (sha256 matched).** Sections 18 (+55), 18f range (+105, EV1's slot), 22 (generated words).
- Off: cadet_test vs 0.99.6 ALL IDENTICAL.
- Week-1 listing, all three on (cal_ev1_8632e57_on.json): Day 4 lastLightGlass 14:00-14:30, clear of everything; Day 6
  garden-hour gone; new rec-paddle-club 07:00, window-sketch 09:45, big-jigsaw 10:45, every-song 17:15. To weigh in the
  CL1 merge: big-jigsaw 10:45-12:30 runs into Tomas's sowing invite (11:45, an intro step); paddle-club x Saturday run
  (CL1 cuts the run).
- Saturday Day 6 planned goers (ev1_saturday.py, all on): 12 traditions (9 before): paddle 2, sketch 6, jigsaw 6,
  every-song 8; sowing 13, harvest 4.
- The Last Light from a fresh save, intro on (ev1_light_fresh.py): Vance's Mail "The Last Light tomorrow" Day 3 18:00;
  you clock in, work; at 13:55 to the bow lounge (no arrow leads there from work: only the Mail and the 14:00 address);
  at 14:00 the arrow "Tap Dr. Sato to watch the Last Light with her"; tap: joined, the notice, you at the glass 14:03-14:31;
  14 bubbles (Sato's 8 with the crowd between), setting up the Line ("Sunday at half two. The bow lounge. Don't be
  late.", "That's what the oath is for."); the Captain's address at 14:00 (banner and All hands Mail); no page errors.
  Should: through the gathering the arrow says "Take a job at the board" while the crew stand easy around you.
- Reading corner (EV1's readprobe, Days 7, 21, 35): Esme hands the book round Day 7; Day 21 chapters 1-6 talked through
  in bubbles, your question card, the answer flagged; Day 35 your answer recalled ("{me} said someone's on the island")
  and chapters 7-12. (The probe's "cadet" for {me} is the game's no-name fallback; a real save has your name.)
- **dad2b9b, game 3920ea00...8ace (sha256 matched)**: the jigsaw 10:35-11:40 (my find), its Mail word 10:35; nothing else in the game.
- Switched-on checks (on dad2b9b): BIGEVENTS, EVENTS, JOIN, WEEKEND CHECK OK; DAY CHECK OK Days 4 and 6. check_fast on the
  commit OK (240 s). cadet_test off on dad2b9b: ALL IDENTICAL (renderer noise only, run beside other browsers).
- **PASS** on dad2b9b (sent to EV1, lead 49, BM25). Should left: the shift arrow says "Take a job" while you're at the glass.
- **286ed5e, game 22af83d6...04e1 (matched): PASS carried, should closed.** lightEasyNow() (switch-gated) holds the shift's
  board arrow while the gathering is on and you've joined or are in the lounge. Off: cadet_test ALL IDENTICAL. Fresh-save
  probe: no arrow at the glass 14:03-14:29, "Take a job" back at 14:30.

### CL1 traditions calendar (claude/p997-calendar), switch CAL997_ON (URL_FLAGS cal997, off)
**5c93e8c, game eaf052ee...733b (sha256 matched).** Sections 13, 14, 16, 18 (+136, slot 'Calendar builder'), 18f, 19, 22.
- Off: cadet_test vs 0.99.6 ALL IDENTICAL.
- Alone, on: week-1 listing: Day 2 rec wall night out; Day 3 open door out; Day 4 dawn swim out, birthday 19:00; Day 6
  Saturday run out; Day 8 birthday out. (The spice supper still at 18:15 here: TB6 moves it.)
- 70-day sweep (cl1_sweep.py): birthdays off 13 at all hours -> on 4 (Days 4, 22, 41, 62), all 19:00, none on a
  Friday, 14+ days apart; late piano never two nights running (also true off over 70 days; CL1 also keeps Marrow off the
  jam next to it); Pick-your-own Days 3/10/17/24: off 1-3 people, on 4-9 with Cruz; Saturday run: off Days 6, 34, 62, on none.
- Note 27 (cl1_pace.py): ship minutes per 10 real s during the address: auditorium 6.0 -> 3.6, elsewhere 6.0 both.
- Note 15: Day 3's store visit off the Schedule, its heads-up and arrow only with the switch (devDay line 12070).
- CL1's own checks queued: arrows_check, day 5, check_fast.

### Week 1 merged: CL1 5c93e8c + EV1 dad2b9b + TB6 687838e8 + GM1 9175156 on d7ad4c58 (lead 49's ask)
Local test branch rv33-testmerge 114fddb5 (not pushed), game e9173eb3...91fb8 off. Game conflicts: three one-line
neighbours (section 13 switch lines; tradJoin: GM1's tiles lines then TB6's t997Join; eventsTick: GM1's line then CL1's).
names_check OK, content_gen --check up to date.
- All six switches on, week-1 listing (cal_merge_week1_on.json): Day 2 booths 18:00-19:00 then spice 19:15-20:00; Day 4
  Last Light 14:00, birthday 19:00, no dawn swim; late piano Days 2 and 4; Day 6: no run, no garden hour, jigsaw
  10:35-11:40 before sowing 11:45. Remaining overlaps are parallel optional evenings or the same item twice.
- Arrow trace, fresh save, intro on, clocking in (merge_week1_arrows.py): Pick-your-own 06:05 Day 3; Last Light 13:45 Day 4;
  the address 15:30 Day 5 (to 16:20); Harvest 09:15 Day 6. (The rest of each day is the job my probe took and never did.)
- FIXED by CL1 46259ef (the arrow now reads "The Last Light, 14:00: Bow lounge, Deck 3", room L, in the merge).
- Was a should (CL1 + EV1): CL1's lead arrow for lastLightGlass names and targets the Promenade (cl997Room takes the event's
  first room: Promenade, Lift plaza, Bow lounge) while Sato and the gathering are in the bow lounge; from the Promenade the
  tap arrow takes over at 14:00 and leads to her (merge_lastlight_promenade.py), so it works, but 13:45-14:00 ends at the
  Promenade with no arrow for a few minutes. Prefer the host's room.
- Merged checks (all on; CL1 46259ef in the merge): EVENTS, BIGEVENTS OK; DAY CHECK OK Days 2, 3, 4, 6, 7; **JOIN CHECK
  FAILED: "saturday-run: not on in 400 days"** (CL1's: the cut run is still in TRAD_JOIN, and join_check tries every
  TRAD_JOIN id; events_check was taught the cut, join_check wasn't). FIXES NEEDED sent to CL1 (check-side). fridays, check_fast running.

### Switched-on quick check, merged and alone (11:10-11:40 UTC)
Each builder ran check_fast with switches OFF. On the week-1 merge with ALL on, check_fast FAILED two lines; isolated
with machine_check / device_check on each branch alone, switch on:
| build (on) | machine_check | device_check |
|---|---|---|
| 0.99.6 base f6ff5ec1 | OK (under load 18) | (base, round OK) |
| CL1 46259ef | FAIL food runs; FAIL ship meters: your jobs (fix-sm-freezer@275 without meters) | running |
| EV1 286ed5e | FAIL food runs | OK |
| TB6 7b8a061 | FAIL food runs | - |
| GM1 9175156 | OK | - |
| merge (all on) | FAIL food runs | FAIL Schedule lists Day 6 07:00 Paddle club (1) |
- food runs: identical each time: a 6th meals run, restock-meals@160 open 19:10-19:40 on the check's day 7 (a Sunday,
  Sunday table 18:00-19:45), over the 2 h limit; coldMin 103. A near-miss in the existing game that any change of who
  goes where tips: sent to the lead to find an owner (galley).
- ship meters (CL1 alone): a small-repair kind with no meter mapping; a gap in the existing game exposed. Sent to the lead.
- Paddle club: EV1's Day 6 07:00 showing has 2 planned alone, 1 in the merge: on the Schedule but doesn't happen. Fix asked of EV1.
- CL1 ba61507 (join_check skips the cut run; Day 2 booths window 18:00-18:30): join rerunning on CL1 alone and the merge.
