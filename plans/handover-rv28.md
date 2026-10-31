# Handover: RV28 (reviewer, crew stories stage 2 for 0.99.4)

Session session_014zyJYQKwGvytfCGdrWMoiZ. Lead 47 (session_014zyJYM4mt9ZDCD5H9JZDtN). Builder ST1
(session_014zyJYMy3rmgW9Tv5brJfkM, claude/stories2-st1). Build master BM22 (session_014zyJYNgBPdEPHLxTGrM889).
Branch claude/review-rv28: notes only (plans/review-rv28.md, probes in plans/rv28-probes/, this file).

## State (2026-10-31 ~05:45 UTC; see the next section for later)
- **PASS claude/stories2-st1 df5057d** (game 6f8e1429...633c), from claude/integration 57eceec4 (0.99.3), sent to BM22, ST1,
  lead. ST1 added a docs-only build-table commit after it (same game sha). Lead: stay available for BM22 confirming the commit
  or a round FAIL in the stories.
- Fixed in review: B1 storyCastGoes return inside a comment (stage 1 hook dead even switched off); F2 storyDayHeld only for
  a scene that can happen; F4/W5/W6 words; B5 a booking expiring mid-scene (storyOpen); B6 laid beats in a tradition's held
  room tagged ev-<id>; B7 storyHolds (crewHold) while a crescendo scene is open.
- Open, not blocking: backlog ST1-1 (stage 1's same mid-scene expiry, left so the switch-off game is unchanged).

## After the stage 2 PASS (2026-10-31 06:00-10:05 UTC)
- 0.99.4 round FAILs looked at, both host timing, not the build: BM22's stories_check (the 30-day default; stage 2 needs
  `stories_check.py BUILD 36`; 7c875a26 makes 36 the default, left for the next 0.99.x as backlog BM22-1); R3's devmode_check
  "real" (passed 4/4 alone here, 3/3 for R3); R1's player_check Saving (OK alone here and for R1).
- 0.99.5: **JB2 p995-jobs c6dc9ac + SW4 words 7e30feb: FIXES NEEDED** (W1 bake, F1 scanner job washer at Tier 1, J1 old
  round lines on the tour). The re-check goes to RV29 (session_014zyJYM3D7UBkZN49CsZVuA) or RV30 (OB2, SD5, TB3: lead 47's split).
  Probes: jb_scan.py (fixScanMachine by day), jb_words.py (tour words baked or stand-in). RV29's tour_play.py plays the tour.

## Probes (plans/rv28-probes)
- st_scene.py WORKTREE BUILD tomas|kowalczyk|calder [OUT]: Dev jump before the scene, story set due, plays it, saves and
  reloads on card 4. Env: ST_PACE=3 (a reader at ~3 s a card), ST_PLAY_OTHER=1 (play other scenes first, e.g. Calder's
  end.story), ST_AFTER=N (watch what follows). Calder needs the work rep raised (the probe does it).
- plans_same.py OLD NEW (env DAYS, default 30): every crew member's planDay per day, hashed; the strongest switch-off proof
  (cadet_test plays Days 0-1 only). Catches B1.
- castgoes.py: storyCastGoes and Kovac's Day 19/26 plan, both builds.

## Gotchas
- Setup as handover-rv26: pip playwright numpy pillow; three r128 + acorn 8.12.1 in /tmp/cw-w1..3; CADET_CHROME.
- Switch-on copy: sed 's/var STORIES2_ON = false;/var STORIES2_ON = true;/'. Run each build's own checks from its worktree.
- The ship clock runs during dialogue (~0.6 ship min per real second): paper checks play scenes instantly, so time-window
  bugs show only in a paced real-game probe.
- Background wait loops can outlive their use and get killed at the time limit: harmless.

## Open questions for the user
None from me.
