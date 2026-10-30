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
