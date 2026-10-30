# RV27 reviews (0.99.2)

## SD3 claude/title-music-0992 017d961d (game d923bb23...51cf8): superseded by f65e768f / bc6c6029 below
- Diff: one line, titleC form Hum 2->1, Log 6->4. Bars are section-relative (c.bar = bar.b), so pad/stars still start each section.
- title_check 55 OK; sound_check OK (titleC 47.27 s loop).
- Probe plans/rv27-probes/tm_level.py (real wake tap, analyser on SND.bus.master, ?title&nosave&sound):
  new: rises 4 s, louder from ~19 s (Entry), ~2 s of digital silence at 36.5-38.5 s, back at 39.5 s.
  0.99.1: louder from ~29 s, the same ~2 s silence at 41-42 s, back at 43 s. So the gap is old, not from this change.
- Notes: design-doc line 872 "about a minute" (now 47 s); section 27 comment "the same 16 bars round again" (C is 13).

## SD3 claude/title-music-0992 f65e768f + bc6c6029 (game 09a51bd0...b2d): verdict below
- Diff: one game line, titleC form Hum 1, Entry 4 (+sSing), Log 4 (+sSeq, sSing), Rest 4. Bars section-relative, so each section's
  pad/chords restart. Timing by tempo: Entry 3.64 s, Log 18.18, Rest 32.73, loop 47.27 (matches SD3). bc6c6029 = comment + design-doc only (checked).
- f65e768f: sound_check OK (titleC 47.27 s), title_check 55 OK.
- tm_level on bc6c6029, 56 s after the real wake tap: -50 dB at 3 s, -42 at 4.1, -33 at 5.1 (melody in), -29..-47 after; lowest -59 at 14.2 s (a dip);
  no silent second, loop seam ~47 s fine. The 017d961d / 0.99.1 gap is gone in this form. No page errors.
- cadet_test vs bc4579aa: see below.

## TB1 claude/title-0992 ced89283 (game c2d4eefe...bbbf4)
- Diff: titleClose has two ways. Continue as before. New game / Start over / newgame: body.tiDev, the ship runs (TITLE.on false) under
  the terminal; a rAF wait (>= 3 frames) until INTRO_UI.manifest, or not booting / choosing / on the manifest step; 4 s cap (none while DEV.choose); then off.
  Menu taps ignored once TITLE.on is false (titleAct guard), pad's title panel off with it, titleKey removed. tiDev removed in off().
- title_check (TB1's) 61 OK on ced89283: 0 old-deck frames on New game, Start over, Arrive by shuttle; the device's question on top (z 71); Monday 06:00.
- The same title_check on bc4579aa FAILS the new rows (1 and 2 old-deck frames), so it catches the real flash.
- Merge with SD3 bc6c6029: the game file merges clean; DEV_NOTES and build-table clash (keep both: TB1's hand-over line + SD3's Music line; both rows).
- cadet_test vs bc4579aa, run alone: SD3 bc6c6029 ALL IDENTICAL; TB1 ced89283 ALL IDENTICAL; no page errors.
- Merged game (bc6c6029 + ced89283, game file auto-merged, sha 60786c45...): title_check 61 OK, sound_check title OK.

## Verdicts (2026-10-29 ~22:20 UTC)
- SD3 title-music-0992 bc6c6029: PASS.
- TB1 title-0992 ced89283: PASS.
- To BM21: merge both; only DEV_NOTES (keep TB1's hand-over line + SD3's Music line, drop the old "a hook only" Music text) and the build table (both rows) clash.

## 0.99.3 prep (lead 46: SD3 mess-sound-0993, CH1 chief-0993)
- Probe plans/rv27-probes/ch_dinner.py WORKTREE [--dawdle]: the build's own intro_check part 8 with a per-frame tracker
  (card, Calder's pose, metres from her away seat / your-table seat, step, INTRO_UI.calder).
- 0.99.1 (bc4579aa) baseline, normal and --dawdle: Calder sits through Zeke's cards 0-6, stands on card 7 "Look who's coming
  over" (INTRO_UI.calder true there), walks ~3 game minutes, sits, then introChief. (The check taps cards quickly.)

## SD3 claude/mess-sound-0993 2348a5e6 (game 37fd7559...8756)
- Diff: MESS_BG = false wraps the galley (brown + white noise) and the clatter loop in scene(); every name in the block is local
  to it; the murmur (12 voices) unchanged. M.bg for sound_check; r3mess checks no clinks and 12 loops when parked.
- Probe plans/rv27-probes/mess_level.py (Day 1 in the mess, 6 s, real output by band):
  0.99.1 dinner (44 people): 0-250 Hz -39.6, 250-2k -49.7, 2-6k -55.9, 6k+ -61.7 dB; 35 clinks. Lunch (45): 133 clinks.
  new dinner: -40.3, -51.4, -90.9, -117.6 dB; 0 clinks; 12 voices. Lunch: 0 clinks, -88.2 / -105.5 above 2k. No page errors.
- Docs: design-doc Sound records the change with the user's words; DEV_NOTES notes the parked code.
- sound_check OK (r3mess: 0 clinks at the rush, empty silent, off in the gym and on Deck 4); cadet_test vs bc4579aa (run alone) ALL IDENTICAL.
- **Verdict: PASS** (sent to SD3, BM21, lead 46).

## CH1 claude/chief-0993 9346b1c3 (game cc1fdddf...a651), from bc4579aa
- Diff (section 21): chat = card >= len-2 and not the choice card (the reply card); the clock reason I.done.chief + 10 is gone
  (it fired mid-chat for a player reading ~3 s a card: the clock runs during the chat); new reason = table done, its chat neither
  showing nor queued (reload / no chat). Welcome waits till she's up and sat, 10 min cap from INTRO_UI.calderAt. A reload before her
  welcome queues it again (chief:met and chiefD set in the same step as dialogueShow, so no double queue). introSeat fixed during the steps.
- ch_dinner probe (5 s a card, CH1's part 8): normal and --dawdle: sat on cards 1-6 incl. the choice, up on the reply card (card 7 of 8
  after the choice), walking as "Look who's coming over" shows, then the welcome. My 0.99.1 baseline used fast taps, so it missed the bug.
- ch_reload probe (real save + page reload): card 1: OK. Card 6: part 20's own "seated before the save" row fails because she's
  rightly up on card 6 (expected, the probe's choice); after the reload she got up again 18:40, sat, welcome 18:42-18:47 in full.
- intro_check whole OK (incl. part 8 card by card, part 20 reload); day_check 0 OK; cadet_test vs bc4579aa ALL IDENTICAL.
- **Verdict: PASS** (sent to CH1, BM21, lead 46). Docs: DEV_NOTES explains the cause; design-doc's arrival paragraph updated.

## SD4 claude/title-song-0993 7ac282dc (game 2f6daceb...c3fd), from d180a704 (0.99.2)
- Diff: titleC form = 0.99.1's line exactly (58 s); play(key, { from }); the first copy { fadeIn 2.5, from 5.5 }, later { fadeIn 4 }.
  beforeZero wraps AudioParam / AudioScheduledSourceNode / AudioBufferSourceNode time methods for one synchronous call (time < 0 -> 0;
  argument indexes right: setValueCurveAtTime / setTargetAtTime at 1, start / stop / cancelScheduledValues at 0), restored in finally.
  Clamped envelopes land under the 2.5 s fade. cancelAndHoldAtTime is not wrapped (not used in the file). Note, not blocking:
  AudioScheduledSourceNode needs iOS 14.5+; older Safari would throw there and the title music wouldn't start.
- sound_check OK (C 16 bars, first copy -5.47 s); title_check 61 OK; cadet_test vs d180a704 (alone) ALL IDENTICAL.
- tm_level (real wake tap, a fresh context, so beforeZero runs): sound from 1 s, louder from ~25 s (0.99.1 ~29-30 s), no page errors.
  A smooth 3 s fade to ~2 s of silence at 43-44 s after the tap (song ~48.5-50.5 s, Rest, between its pads), back at 45.4 s:
  the 0.99.1 song's own quiet patch (0.99.1 showed the same shape), not from this change.
- **Verdict: PASS** (sent to SD4, BM21, lead 46).
- ef799975 (game 75b56049...fbb9, on 7ac282dc): beforeZero wraps start/stop on each source node type that exists (typeof); the
  hasOwnProperty check keeps one wrap each. sound_check title OK; tm_level alone: sound from 1 s, louder ~25 s, no silence, no errors.
  **PASS.** (cadet not rerun: the change is sound-only, and SD4's cadet on ef799975 is ALL IDENTICAL.)
- Finding about my own probe: the short silences seen with tm_level (017d961d 36.5 s, 0.99.1 41 s, 7ac282dc 43 s, ef799975 7 s when run
  next to sound_check) come from frame stalls with two browsers busy: titleTick schedules only 1 s ahead (T.tick(now + 1)), from the
  frame. Alone, no silence. Real but old (0.99.0): a phone frame stall over 1 s (loading behind the title) would gap the music. Backlog
  suggestion for the sound seat: schedule 2-3 s ahead or from a timer.
