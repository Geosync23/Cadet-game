# RV13 review notes

Reviewer RV13 (session_016ioWtxM6NJRV4Ck3ADwozc), branch claude/review-rv13 (notes only), under lead 32.
Base for 0.92.3 pieces: claude/integration 364c80cb (0.92.2). Verdicts go to LEAD 32 and BM15.

Queue (patch 0.92.3, plans/patch-0.92.3.md on claude/lead-32):
- DV1: items 13 + 23 (Name on the beam: no signing until people arrive, explaining bubbles; your name with the others)
- FX10: items 21, 24, 29 (more science-area work; many rotating repair jobs; board pointer for hauling/stores)
- FX11: items 16, 17, 25 (first-use lockers tip for pool/river; pool swim camera; light disc players visible) (16 moved from AC3, lead 03:17 UTC)
- FX13: item 15 wiring (Talk a while: own line pools for the Captain + main characters; the Captain's first welcome)

Each: diff does only what it says; new check lines FAIL without the fix, PASS with it (planted fault); area checks,
check_fast, cadet_test (every pixel diff explained); nothing else changes.

## Status
- Set up ~03:30 UTC: playwright, three r128, acorn 8.12.1 in /tmp/cadet-work. Waiting for shas.
- Baseline 364c80cb (game sha256 ca2f908d...e7e4 = 0.92.2): check_fast QUICK CHECK OK in 206 s here.

## FX13 own-talks claude/p923-fx13 95b68182 / 1aabb091 (item 15 engine): interim FIXES NEEDED (test only), ~03:45 UTC
Game sha256 aac49362...c40b (1aabb091 = talk_check only). Base 364c80cb.
- Diff: content_gen (several .talk files a person, sorted, <id>.talk first; `only: own` -> TALKS.only; `first: yes`,
  1-4 them: lines; global id-uniqueness check still at line ~937); sec 22 slot (talkOnlyOwn, talkPackOwnAgain, first
  scene picked first, fired only on answer, lineFor cuts tpl+bank for talk.* when only-own, talkFillerOf); sec 20
  talkStart (no hello before a first scene) and talkNext (no chatLine fallback for only-own). Docs + build row.
- Switched by content: baked TALKS block byte-identical to 0.92.2; content_gen --check up to date; lines_check PASS.
- check_fast on 95b68182: QUICK CHECK OK in 285 s.
- talk_check fix OK; 0.92.2 stops on ReferenceError talkOnlyOwn. cadet_test 0.92.2 vs fix ALL IDENTICAL (0 px).
- Planted (plans: /tmp/rv13/plant.py): p1 bank, p2 fire guard, p3 only branch, p4 sort, p7 first pick: all FAIL.
  p5 (talkStart hook off) and p6 (talkNext hook off): TALK CHECK OK = not caught -> asked FX13 for test lines.
- Notes: only-own with no own talk.filler holds the last pack line ~2-7 ship min; tier-0 stand-in repeats daily
  (gap 1) because only one ungated stand-in talk: writers need many ungated talks.
- 7047bf90 (game 2fb90049...687b): talkPackHold (sec 22) + talkStep ask hook (sec 20, third hook): holds the ask while
  first-scene lines remain, then 1 ship min (TALK_ASK - 3*TALK_LINE); talkNext calls talkPackNext first, so no endless
  hold. talk_check OK (6 lines, last at 10, ask at 11). Planted p8 (hold off): FAIL both new lines; p9 (no 1-min tail):
  FAIL (ask at 10.5). cadet_test 0.92.2 vs 7047bf90: ALL IDENTICAL apart from j_steer1 6 px max 1 level (renderer
  noise; nothing in the change touches drawing). p5/p6 test gaps still open on this sha.
- **bc976e7d (game 4ff22c1c...1aae): PASS (~04:05 UTC).** Game change since 7047bf90: only the TALKS.own guard.
  talk_check OK; planted q5 (talkStart hello hook off) FAIL "something in front of the first-talk scene"; q6 (talkNext
  fallback off) FAIL "lines that are not her own" (her chatLine lines). cadet_test 0.92.2 vs bc976e7d ALL IDENTICAL.
  check_fast QUICK CHECK OK 217 s. Section 20 sign-off (owner seat not live): talkStart hi hook, talkNext only-own
  return, talkStep ask hold: all three correct, guarded with typeof, no change for anyone without first/only content.
  Open for the content sha: own talk.filler for only-own people; many ungated talks (strangers repeat otherwise).
