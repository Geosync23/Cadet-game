# Handover: RV24 (reviewer), 2026-10-28 ~11:30 UTC, to RV25

**Role:** reviewer. Lead: lead 43 (session_01GKuymjoDoY2kA9yCK12NG1; send_message, priority "next"). My session:
session_01GKuymnJuoJTWnmYunbN7EP. Notes-only branch `claude/review-rv24`; full log and verdict table: `plans/review-rv24.md`.
Never change the game or push to builders' branches. Verdicts go to the builder, lead 43 and (for merges) BM20
(session_01GKuymiwDEgkwGmjJ2nokvg). RV25 takes over (it wrote from session_01GKuymnwhXNmtzwcz4BjQ6n; lead 43 named
session_01GKuymnnpKvNH4Ki69KEzwG: check TEAM.md).

## Priority (lead 43): 1. EV1 visit-on, 2. Dev mode, 3. sound. Hand over at about 60% memory.

## Exactly what's open
1. **EV1 visit-on (claude/visit-on cf67777): NOT STARTED by me.** First priority: it gates the 0.96.0 round. I hadn't seen it
   arrive; nothing run.
2. **Dev mode J3 (DM1, claude/devmode-j3 2b88ad2, from J1 d9b7b3c): runs mostly done, verdict pending.** cadet vs d9b7b3c ALL
   IDENTICAL (clean); dm_jump.py by taps: "the offer" -> Day 32 15:50 Ready room, Engine Specialist Steady, arrow "The Captain",
   Calder's answer put in; "the goodbye" -> Day 36 09:10 Shuttle bay, Go recorded, but the arrow says "Breakfast in the mess, your
   last one" (pointing out of the bay just before the goodbye: the ending's arrows, probably because the jump skipped breakfast;
   a note for the lead / the ending's owner, not J3's); no page errors. devmode_check (all) and dev_arrow_check were running in
   /tmp/rv24/dm3 (dev.txt, arrow.txt; done.txt lines j3_dev / j3_arrow in /tmp/rv24/pad/done.txt). If I've gone before they end,
   re-run them: `python3 devmode_check.py BUILD`, `python3 dev_arrow_check.py BUILD` in a worktree of 2b88ad2.
3. **Sound 667ad05e (SD3, room B home chime, on top of cacfba97): NOT STARTED.** Section 27 only, no hook; SD3: sound_check OK,
   cadet identical, check_fast OK. Needs: cadet vs e158dcff, sound_check (r3fx), a code read.
4. Not open, but know: SD3's design-doc "Sound" section change on cacfba97 is NOT read (I said so to SD3); read it if the lead wants.

## Verdicts I sent (all in plans/review-rv24.md's table)
- Step 6 (lead 42): W8 promo4 6f13b61a/9063aafe PASS; DA6 p5s6-deck 2df6bfce/5c27b740/4a84e153 PASS; AS1 m24-pick-pointer 5f649b45 PASS.
- Controller update (lead 43): wave A 818ec0b PASS, wave B 177793b6 PASS, wave C 336b00c2/a29a0f48 PASS; A+C+B scratch merge: all
  wave parts + m23 OK. controller_check `idle` is an old intermittent FAIL (device-page DOM-hash pairs -1556429587/978430068 and
  -1256198055/15039922, also with PAD_ON off); CA1 works on a fix.
- Dev mode (DM1): J0 eef5b56 PASS; J1 d9b7b3c PASS (note: Night 2 lands 20:50 with no arrow until 21:00).
- Sound (SD2, then SD3): r3 64077a69, dc3014b6 (farewell A), a09b32b7 (mess hall), f58803b1 (feature sounds), cacfba97 (six
  hooks; my read stood in for the section owners: no owner seats exist) all PASS.

## How I test
- Setup per plans/testing-guide.md section 2: /tmp/cadet-work and /tmp/cadet-work2 (two lanes, at most 2 browsers on 4 cores; a
  third makes screenshots time out and cadet_test show 1-level "renderer noise": re-run alone).
- One worktree per sha under /tmp/rv24/wt-<sha>. Step 6 ON copy: sed the P5_STEP6 line to `P5_STEP5 && true`.
- Probes in plans/rv24-shots/: pad_look.py (pretend pad at 390x844 via controller_check's Run; parts wavec, wavea, waveb),
  dm_look.py and dm_jump.py (Dev mode by taps with #dev; dm_jump takes "Group:label" args), cq_play.py, m23_door.py, d2b_look.py,
  mt_play.py, d22_play.py (stalled at 08:47: debug before use).
- Dev presets in probes: `devmodeRun('Set career: beat', () => devmodeSetCareerTo(day, beat))`; the panel's devmodeSetCareer
  is async (timers), so by taps wait in real time (dm_look does).
- cadet_test's INIT freezes performance.now: timings in a probe read 0.
- Gotchas: never `pkill -f`/`pgrep -f` with a name in your own command line (exit 144 kills your shell); don't sed-edit a lane
  script that's already running (bash keeps the old file open: kill and restart it); a copied check must keep its own file name
  (controller_check/promo_beats find cadet_test.py by it); `timeout 60 git push` (pushes can hang).

## Open questions for the user
None from me.
