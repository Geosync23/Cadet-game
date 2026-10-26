# Review log: RV21 (vessel + ending reviewer)

**Role:** reviewer for "A Veyli vessel needs help" (EV_VESSEL_ON) and the ending (EV_ENDING_ON). Hired by lead 39
(session_019V68fz33UFv4cK5Z4iCDvi). My session: session_01AmTyMHLr5UuCY9zo3nQcwS. Notes-only branch
`claude/review-rv21`; I never change the game or push to builders' branches. Verdicts PASS / FIXES NEEDED (must/should)
with the exact sha to the builder, lead 39 and BM18 (session_01A3S2VBMYmTt2wCZa8ej7XR).

**Specs:** plans/veyli-vessel-spec.html and plans/ending-spec.html on claude/p5-specs (f2f9a705).
User answers: vessel C1 commendation yes; C2 ship visible yes; C3 Taavek and Calder WAIT at the ramp up to an hour
(Calder finds you 09:45; Zeke only after 10:30).

**Builders:** vessel VB1 session_01UsjGN26E88zwrNPWwef4iT (claude/vessel, V-1..V-4), VB2 session_01KRBGtugjBpv5iGcV5WDvCP
(claude/vessel-sky, V-5), writer SW4 session_01DgMynb62u2rTUA9RocZi65 (claude/vessel-words); ending EN1
session_01Py28Kh6QV9kk64ri5AzQ5B (claude/ending, E-2, E-3), EN2 session_013er8NqC8eftyZqXBzcSibF (E-4, then E-1),
writers SW5 session_01FFW8ZfuaUqiPPqqhruwZhX (endgame pool), SW6 session_01Gy3XCqRBiA4ky2vp6e8rzR (week + endings).

## What every sha gets
1. Spec followed (beats table, user answers).
2. Switch off = identical (cadet_test vs the branch's base).
3. The piece's checks (as the spec lists) + check_fast.
4. Play at phone size 390x844 with the preview flag (#evvessel / #ending).
5. User rules: works with a game controller; tons of arrows and super obvious progression (ring, level-1 arrow,
   notice, Tracked/Schedule, in person before Mail); key moments are staged scenes with lots of dialogue.
6. Canon: the Admiral is the Captain's fish (never "the Admiral's offer"); every Veyli is they/them; never
   "permission"/"leave" about the reach; comet's Veyli name unspoken; no emojis.

## Verdicts
| Branch | Piece | Verdict | Sha |
|---|---|---|---|

## Log
- 2026-10-26 ~20:05 UTC: started; told all seven builders and lead 39 my session id. Read specs, RV18 handover, TEAM.md.
  Test setup per testing-guide 2.0 in /tmp/cadet-work. Waiting for shas.
