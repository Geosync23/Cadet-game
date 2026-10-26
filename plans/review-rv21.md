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
| claude/vessel-words (SW4) | V-6 words | PASS (4 shoulds) | 88128070 |
| claude/vessel-words (SW4) | V-6 words, shoulds done | PASS | 7dd2eb5d (d75de7ab PASS too) |
| claude/ending-words-b (SW5) | E-5 endgame pool (not baked) | PASS | 0d90de7a, 8ed1545a (should done) |
| claude/ending-words-a (SW6) | E-5 week + both endings | FIXES NEEDED (1 must) | 6dd03f57 |

## Log
- 2026-10-26 ~20:05 UTC: started; told all seven builders and lead 39 my session id. Read specs, RV18 handover, TEAM.md.
  Test setup per testing-guide 2.0 in /tmp/cadet-work. Waiting for shas.
- ~20:40 UTC: **SW4 claude/vessel-words 88128070 (from d9c7e5f0): PASS, 4 shoulds.** Words only (bank
  event-veyliVessel.lines + 8 .meet scenes, baked; game diff is additions only, nothing reads the keys until VB1).
  Read every line against the beats table and canon: every Veyli they/them (Taavek, Saruth, the ship), the Admiral absent,
  no "permission"/"leave"/reach, comet name unspoken, ASCII only; Day 0 canon right (Zeke showed you your bunk; Basil
  "a week aboard" fits Day 21); C1 commendation Mail, C2 view and lights, C3 wait (late meet, wait bubbles, Zeke after
  the hour, bench meet) all present. Checks: content_gen --check up to date; lines_check PASS (0 errors, 69 old
  warnings); check_fast QUICK CHECK OK in 458 s; cadet_test vs d9c7e5f0: first run a_start 14812 px (beside
  check_fast: backlog FX17-2), alone ALL IDENTICAL. Phone play / controller: n/a for words (comes with VB1's code).
  Shoulds: (1) mail.commendation assumes you met Taavek at the ramp and made the part yourself, and promises an
  in-person word "this week" that no beat builds: wording that holds for the bench meeting / helpers finishing, and
  drop the promise unless VB1 builds it. (2) C3 says Calder comes to find you at 09:45: there is no Calder line for it
  (only the notice); add an in-person line or two (talk.rampFind) so it is said in person first. (3)
  gather.chain.thanks names Pell and Kovac as your neighbours: wrong when either is not in the line; neutral wording.
  (4) helpers speak only at steps 1, 3, 4; steps 2 and 5 have Taavek alone: add 2 and 5 for each of the four helpers.
- ~20:20 UTC: user's ending answers (TEAM.md 20:07, spec 79c4d275): Q1 NO way back (no kept copy; end page = Keep this
  ending + Start a new game); Q2 change your mind until the address; Q3 post by Calder's answer.
- ~20:25 UTC: SW4 d75de7ab (one status line) PASS. SW5 0d90de7a PASS + should (time-bound lines in an endless pool);
  8ed1545a moves 170 lines to `endgame:early` (diff: only "?" lines and comments) PASS. Scratch check (endgame ->
  flag:end.stay): content_gen bakes, lines_check PASS 69 = base.
- ~20:30 UTC: SW4 7dd2eb5d: all 4 shoulds done (commendation for every path, no promise; talk.rampFind; chain names
  nobody; steps 2 and 5 per helper). PASS, final.
- ~20:36 UTC: **SW6 claude/ending-words-a 6dd03f57: FIXES NEEDED.** Must: ending.offer.post.teach.1 reveals Marrow's
  daughter at any tier (her card: secret until tier friend). Shoulds: end page lacks "Keep this ending" label; no
  crossing-back address for a slow career (offer not yet made); friends' talks ignore an answer already given. Nits:
  "by Friday" said on Saturday; crowd "Best four weeks" (five aboard); endingSearch's three "Ah." need chaining.
  lines_check PASS 96 warnings (27 new: deliberate parallels, the oath reuse, "Attendance"); check_fast OK 425 s;
  cadet_test vs d9c7e5f0 ALL IDENTICAL. Spec nit to lead/EP2: section 8 still says three end-page buttons.
