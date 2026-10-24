# RV14 review log (reviewer under Lead 34; took over from RV13, 2026-10-24 ~22:45 UTC)

Scope: 0.92.5 item 16 (the weekend traditions, behind WEEKEND_ON) and item 19 (Cook-along in the galley, not behind
the switch), both on claude/p925-weekend. Builder FX9 (session_01WeXGZBS3DyyLqHGpRjWZzA); BM16; Lead 34.
Base: claude/integration ba836359 (0.92.4, game 2aa6427f...).

## 357ff7ac (game d2ca64c2...): T1-T4, tjActs, weekend_check
- cadet_test 0.92.4 vs 357ff7ac (off): ALL IDENTICAL.
- weekend_check: FAILED only on night-owls-cocoa and sunday-story ("nobody at it": bedtimes; the known attendance gap).
  Everything else ok (each on its day, off = none, joins/acts, tap-join gains, Bread day spots/decor/loaf, jigsaw).
- Words: the baked jigsaw chatter says "Vance ... in her head"; Vance is "he" everywhere else. SW1's df94ab2c (not yet
  merged) rewrites it. Every song's "Sing-along at five" needs a word if it moves to 17:15.
- Hosts: Vance (offDays Wed/Thu) works Sundays; Zeke works Saturdays; Tove Cruz off Sat/Sun (picnic host refused by take()).

## 344c0dd5 + 56293048 (game bcd972f9...): item 19 Cook-along in the galley
- events_check part 13 alone on 0.92.4: FAIL (all five in the mess, talk). Good line.
- cadet_test 0.92.4 vs tip (off): ALL IDENTICAL. content_gen --check, names_check (off and on): OK.
- Probe (/tmp/rv14/scripts/probe_k.py, switch on): Day 6 15:46 and 16:06 Sato at 3-cookalong-3 (38.35,6.9) and Madsen
  at 3-galley-6 (38.5,6.8, prep) 0.18 m apart. Bread-4 has the same point (Sunday samples clear, but galley-6 is a bake
  station). -> FIXES NEEDED (sent ~23:20 UTC): move off galley stations; add a no-overlap line to part 13.
- Depends on bbcea5cb's evTagId 'cook' (tag ev-cook-along-cook): not pickable alone (told BM16).
