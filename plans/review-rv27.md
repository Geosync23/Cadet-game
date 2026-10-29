# RV27 reviews (0.99.2)

## SD3 claude/title-music-0992 017d961d (game d923bb23...51cf8): ON HOLD (lead 46: user wants the melody at 5 s; SD3 reworking)
- Diff: one line, titleC form Hum 2->1, Log 6->4. Bars are section-relative (c.bar = bar.b), so pad/stars still start each section.
- title_check 55 OK; sound_check OK (titleC 47.27 s loop).
- Probe plans/rv27-probes/tm_level.py (real wake tap, analyser on SND.bus.master, ?title&nosave&sound):
  new: rises 4 s, louder from ~19 s (Entry), ~2 s of digital silence at 36.5-38.5 s, back at 39.5 s.
  0.99.1: louder from ~29 s, the same ~2 s silence at 41-42 s, back at 43 s. So the gap is old, not from this change.
- Notes: design-doc line 872 "about a minute" (now 47 s); section 27 comment "the same 16 bars round again" (C is 13).
