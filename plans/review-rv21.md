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
| claude/ending-words-a (SW6) | fixes | PASS | aed8af49, b8c89e7a |
| claude/vessel-sky (VB2) | V-5 + V-3 spots, v.1-v.3 | PASS (3 shoulds) | c070862c |
| claude/vessel-sky (VB2) | v.4-v.5 (shoulds done + SW4 words) | PASS | cfc2dbe3 |
| claude/vessel (VB1) | V-1 | PASS | 581fc84f |
| claude/ending (EN1) | E-2/E-3 turns 2-4 | FIXES NEEDED (1 must) | 93eb5380 |
| claude/ending (EN1) | fixes | PASS | cd4196d5 |
| claude/ending-crossing (EN2) | E-1 + E-4, whole ending | own parts PASS (2 shoulds); waits for cd4196d5 merge | da1f8e14 |
| claude/ending (EN1) | new keys' words | PASS | 319b7739 |
| claude/vessel-sky (VB2) | v.6 bench places | PASS | 3fb8eac7 |
| claude/vessel (VB1) | V-2a + V-2b | FIXES NEEDED (1 must) | 73942e8a |
| claude/vessel (VB1) | V-3 + V-4 + lights fix | PASS (V-2 shoulds open) | 6d4b5192 |
| claude/ending-crossing (EN2) | the whole ending (EN1 395fe62e + E-1/E-4 + words) | PASS | d1a61402 (b77733eb) |
| claude/p5s5-puzzles (B4) | Step 5 S5-6 t5-t7 (for RV20) | PASS | 6b07b624 |
| claude/p5s5-m20 (B3) | Step 5 S5-5 sensor array (for RV20) | PASS (4 shoulds) | 7c5d9f79 |
| claude/ending (EN1) | E-2 turn 1 skeleton | PASS (1 should: docs) | 1c72a28d |

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
- ~20:42 UTC: **EN1 claude/ending 1c72a28d (skeleton): PASS.** EV_ENDING_ON off; empty section 29 (29a-29c slots) after 27,
  before the main loop; cadet ALL IDENTICAL; check_fast OK 406 s. Should: 29b header, DEV_NOTES, owners, map still describe
  the kept copy (user said no way back).
- VB2 v.1 e21ade10 received; waiting for v.2 as VB2 asked.
- ~20:50 UTC: SW6 aed8af49 + b8c89e7a: must fixed (no daughter), Keep this ending added (lead corrected the relay: two
  buttons), slow path (crossingBackAddress.plain, endingAsk.slow, unsure.slow, slow Mails/rows), friends neutral, nits done.
  PASS. Nit left: .plain thanks you for leading the oath even if you missed it.
- ~21:00 UTC: **VB2 claude/vessel-sky c070862c: PASS, 3 shoulds.** cadet vs acbb52e0 ALL IDENTICAL; check_fast OK 504 s (its
  deck_check part: 40 chain spots, gap .65). Phone play with a stand-in event (probe in plans/rv21-shots/): ship 14:00 Sat to
  09:10 Tue, engine and three flashes 17:40 Mon, props in their windows, draw calls 154-307, no errors; on screen from the
  lounge's bow tiles (shot plans/rv21-shots/vessel-sky-c070862c-bow-1741.png). Shoulds: impeller 7 blades vs "twelve"
  everywhere (and words say a cracked hub); tap keys differ from SW4's (SW4 inactive: VB2 reads SW4's keys); deck_check only
  asserts VSKY.m exists (off screen from the lounge middle at 900x760).
- VB1 V-1 claude/vessel 581fc84f received ~20:50; code read: off guarded (VESSEL undefined, vesselGuestAt null), times per spec,
  C1-C3 as switches, late rule from Day 28; section 14 guestTrim one-line hook (sim owner to review). Checks running.
- ~21:05 UTC: VB2 cfc2dbe3 (v.4 12 blades + hub crack, SW4's keys, on-screen assertion; v.5 SW4 words + lead's shelf word
  fix): PASS.
- In progress (~21:45 UTC):
  - VB1 V-1 581fc84f: cadet vs d6bb0aba ALL IDENTICAL; events_check: only FAIL = known-old FX24-2 (Farouk, reading corner
    Day 7), vessel part OK; day_check 27, 28 OK on a switched-on copy; 29, 30, bigevents running.
  - VB1 V-2 73942e8a (V-2a f7a32c4a + V-2b; merges SW4 7dd2eb5d, VB2 c070862c, FX29 8a91f1dc): code read. Notes: Taavek's
    goodbye window 14:45-15:00 only (missable: start earlier / the Tern waits like C3); the round one has no fallback if
    missed (12:45); Saturday's sheet: arrow to Calder, Calder doesn't come to you (spec: she comes to find you);
    vesselFind uses setTimeout (real time) not simTimeout. Queue: phone probe (plans/rv21-shots/v2_probe.py), cadet vs
    acbb52e0, events_check.
  - EN1 7029e8ad: cadet vs d9c7e5f0 ALL IDENTICAL, ending_check OK, check_fast OK 540 s, saves_check OK. Head now 93eb5380
    (SW6 words wired, EN2 API, Zeke Sunday, search fix): cadet, ending_check, phone probe, check_fast running. Shoulds so far:
    stale "questions are open" comment (section 29 core); last breakfast arrow level 2 and no fetch (missable); the Monday
    crowd re-staged every minute with no end if you never board (crew stuck all day: needs a fetch/disperse rule);
    end page "What you kept" shows raw trace ids; the handover's plans/ending-shots/ is not in the commit.
- ~21:50 UTC: **EN1 93eb5380: FIXES NEEDED.** Must: on the goodbye Monday (Go) the shift counts as missed (tip "You missed
  a shift without leave"; seen in the phone probe at 09:19 in the bay). Shoulds: crowd re-staged forever; breakfast level 2
  and no fetch; raw trace ids on the end page; stale comment; no screenshots committed. 7029e8ad/93eb5380: cadet identical,
  ending_check OK, check_fast OK, saves OK; probe: offer arrow level 1 at 15:50, ready room scene 16:01, bay 53 at 178 calls.
- ~21:55 UTC: **EN2 da1f8e14 (whole ending): EN2's parts PASS**, 2 shoulds (the oath you lead is missable: fetch from 14:35
  and hold the start; Vance's notice hard-coded). cadet vs aad4d266 ALL IDENTICAL; lines_check PASS (104 warnings);
  content_gen up to date; ending_check OK; probe: oath arrow level 1 14:05, crossingBackOath (19 lines) at 14:45.
- ~22:05 UTC: **EN1 cd4196d5: PASS** (careerOff hook endOffDay for Day 36 Go, section 20 owner to review the line; crowd limits
  + Zeke 10:15 fetch; breakfast level 1 + Pell fetch; keepsakes named). ending_check 10 parts OK (limits: off36, no miss);
  cadet ALL IDENTICAL.
- ~22:05 UTC: **VB1 V-1 581fc84f: PASS.** day_check 27-30 on-copy OK; bigevents late-save FAILs = stale expectations fixed by
  FX29 8a91f1dc (re-running on V-2). V-2 73942e8a: probe, cadet, events, bigevents running.
- ~22:10 UTC: lead 40 (session_01NXybH7NNqM8M4ngiyidq6m) took over from lead 39 (TEAM.md ~22:00). Owners for the missing
  pieces: VB1 vessel arrows_check part + controller presets; EN2 endstay/endgo + presets; RV20 reviewed EN1's careerOff hook (OK).
- ~22:15 UTC: EN1 319b7739 (words for its new keys) PASS. VB2 3fb8eac7 (v.6, six bench places) PASS.
- ~22:35 UTC: **VB1 V-2 73942e8a: FIXES NEEDED.** Must: bigevents on-copy "vesselLights: 47 mean to go for 44 places".
  (V-1's late-save FAILs gone with 8a91f1dc.) cadet vs acbb52e0 ALL IDENTICAL; events_check only FX24-2 and every V-2 live part
  OK; phone probe: level-1 arrows at each beat, the ramp scene at 09:33 with replies. Shoulds: no ramp crowd (rampCrowd
  unused); goodbye window 15 min; round one no fallback; sheet: Calder should come to you; doubled pilot toast;
  setTimeout; merge VB2 3fb8eac7.
- ~23:00 UTC: **VB1 6d4b5192 (V-3 chain + V-4 making + lights fix): PASS.** bigevents on-copy OK; cadet vs 8a91f1dc ALL
  IDENTICAL; events only FX24-2; V-3/V-4 live OK; phone probe (v34_probe.py): Join the chain level 1 from 12:50, tap Zeke
  joins, ring Pass the crate, Deck 5 30 crew ~210 calls; Mon 09:22 Pick two helpers level 1. V-2 shoulds still open (ramp
  crowd, goodbye window, round-one fallback, sheet fetch, doubled toast, setTimeout x7, VB2 3fb8eac7 not merged).
- EN2 b77733eb (the combined ending: EN1 395fe62e + oath fetch + notice key) received; lead 40 says EN2 hands over; fixes to
  EN2, else VB2. Checks running.
- ~23:40 UTC: **EN2 claude/ending-crossing d1a61402: PASS (the whole ending).** lines PASS, words up to date, cadet vs 19400976
  ALL IDENTICAL, ending_check OK. Oath fetch (Vance from 14:35) and the notice key done. Still owed before switch-on (lead 40
  assigned EN2 / successor): endstay/endgo arrows_check parts, controller presets, day_check 31/50 on-copy.
- ~23:45 UTC (lead 40 asked me to take two of RV20's): **B4 p5s5-puzzles 6b07b624 PASS** (cadet vs 5957d244 identical,
  puzzle_check OK, controller s5cases OK, rv20-mys-live.py by real taps: board by the Chief's glass, three cards, the call).
  **B3 p5s5-m20 7c5d9f79 PASS, 4 shoulds** (cadet vs c32aab5d identical; mech_check/controller m20 parts SKIP without the
  preview switch; live play m20_live.py: Day 19, both Mori and Calder in the array room at 10:00, scene plays; teacher name
  mixed Mori/Calder; Tracked row doubled; Calder's 06:20 Mail before the in-person word; recheck after deefa61a).
- ~23:50 UTC: memory ~61%: handover (plans/handover-rv21.md updated). Idle.
