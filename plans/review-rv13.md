# RV13 review notes

Reviewer RV13 (session_016ioWtxM6NJRV4Ck3ADwozc), branch claude/review-rv13 (notes only), under lead 32.
Base for 0.92.3 pieces: claude/integration 364c80cb (0.92.2). Verdicts go to LEAD 32 and BM15.

Queue (patch 0.92.3, plans/patch-0.92.3.md on claude/lead-32):
- DV1: items 13 + 23 (Name on the beam: no signing until people arrive, explaining bubbles; your name with the others)
- FX10: items 21, 24, 29 (more science-area work; many rotating repair jobs; board pointer for hauling/stores)
- FX11: items 16, 17, 25 (first-use lockers tip for pool/river; pool swim camera; light disc players visible) (16 moved from AC3, lead 03:17 UTC)
- FX13: item 15 wiring (Talk a while: own line pools for the Captain + main characters; the Captain's first welcome) (words sha dropped by LEAD 33: CS1 words baked in staging, FX13 verified)

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

## DV1 p923-dv1 6aeae8c1 (items 13 + 23, Name on the beam) + SW2 join.lines 2bd054f3: interim FIXES NEEDED (test only)
Game sha256 b3caed3f... (with SW2's words baked in a scratch copy: ba3c31d0...).
- Diff: BEAM.slots reordered (yours = top-row east slot 4.98, right-aligned by BEAM.gap 36/256), nameYours/nameNew text
  alignment; sec 18 beamGather/beamReady/beamWaitTap/beamLines; beamReady gates beamOn, tradJoinMinute tip/arrow, the
  leader's tell. nameNew's plane unchanged (a0/a1 same values). No R(). Not saved (lines again after a reload).
- Screenshots (plans/p923-dv1): before = your name off-screen west; after = "Sam" right before "Ada"; new hands: Basil
  under Sam, Rafe/Priya west column. Looks right.
- join_check fix OK; 0.92.2 ReferenceError beamReady. Planted d1 (ready always) 4 FAIL, d2 (no lines) FAIL, d4
  (tradJoinMinute gate off) FAIL; **d3 (old slot order) JOIN CHECK OK: item 23 has no check line -> asked DV1.**
- SW2 2bd054f3 join.lines (4 explain lines) bake clean, lines_check PASS.
- With SW2's words: join_check OK, Zeke's 4 lines in order, opens 17:19. cadet_test 0.92.2 vs 6aeae8c1 ALL IDENTICAL
  (j_steer1 6 px 1 level, renderer noise). check_fast OK (200 s).
- **FINDING (game, item 13): late arrival can't sign.** 4 lines x 4.2 s real = ~10 ship min (SHIP_RATE 0.6), started
  only once you're in the bay. plans/review-rv13/late_probe.py (BEAM_OPEN reset each run): arrive 17:06 -> open 17:19;
  17:25 -> 17:35; 17:31/17:34/17:37 -> event ends 17:40 still locked. 0.92.2: sign any time to 17:40. -> DV1.
- 54853c2b (test only): item 23 line confirmed: fix OK (gap 0.164 m, arrow 0.431); old order (d3) FAIL (east false, gap 1.424). Item 23 done; item 13 late-arrival finding open.
- **0e329b12 (game 9fa00df9...2bb0): PASS (~04:55 UTC), with SW2's join.lines 2bd054f3.** Fix: lines trimmed to those
  that end BEAM_SPARE (5) ship min before e.to (last ones kept: the hand-over), guard opens at e.to - 5 if a dialogue held
  them, opens at once in the last 5 min. join_check (with words) OK: late 17:32 -> 1 line, opens 17:34, painted; same
  check on 6aeae8c1+words FAILs (17:40, locked, 4 lines). late_probe (with words): arrive 17:06/25/31/34/37/38 -> opens
  17:19/17:32/17:33/17:34/17:37/17:38, all before 17:40. cadet_test 0.92.2 vs 0e329b12 ALL IDENTICAL. check_fast OK.
  Notes: the dialogue guard isn't exercised by a check (small, reads right); arriving 17:38+ leaves ~2 ship min to paint,
  as on 0.92.2 at 17:38.
  Words: BM15 takes join.lines from SW2 4533c325 (line 1 softened to "Right. This is the beam..." after RV13's note; CS1 passed); bakes clean, lines_check PASS; PASS covers it.

## FX11 pool-disc claude/p923-fx11 789f1ff0 (items 16, 17, 25): PASS (~05:15 UTC)
Game sha256 6e445254...75b1 (b2c73694 = game; 838bf732/42bf2eaa/789f1ff0 = disc_check + backlog only).
- Diff: 15r recChangeTip (tipShow 'rec.change', once per save, respects the tips setting; old ixTip 'recChange' retired)
  in recGo's change-first path and recStart; swim gets follow: true (same camera path as kayak/float); 23b slot
  ldCrewRally/ldCrewAt/ldCrewDisc/LD_CV (frame clock, no R(), nothing saved, 1 disc + halo made on first show);
  8c REC_CREW.disc; places 7-disc-1/2 get move {kind:'disc'} (read only by the crew's spot.mv, not the player's act);
  one main-loop line. Does what it says.
- disc_check (new 0.92.3 block): fix ALL OK; 0.92.2 FAILs 7 (#16 x2, #17 7.00 m, #25 x4). Planted: f1 no follow ->
  #17 FAIL; f3 ldCrewAt null -> 3 #25 FAIL; f5 no solo -> lone line FAIL; f6 both DISC.g guards off -> hidden line
  FAIL; f2 (recStart's tip call removed) ALL OK: expected, recGo's call shows it first; recStart's is a backstop for a
  save already in kit (harmless, the tip is once).
- cadet_test 0.92.2 vs fix ALL IDENTICAL; check_fast OK (198 s). FX11's own: day_check 2, perf (court +2 calls).
- Owner sign-off for 15r and 8c (Rec engineer seat not live, LEAD 33): given.
- FX11-1 backlog row: withdrawn by FX11 (probe error), fine.

## FX10 p923-fx10 bce5e885 (items 21, 24, 29 + machine_check share line + arrows backlog 15): interim FIXES NEEDED (test only), ~07:05 UTC
Game sha256 10240cb2...8fa88. Base 364c80cb.
- Diff: sec 17 slot FIX_ROWS (194, 6 parked) / fixTable (lazy, machSeed+schedU, no R()) / fixOk / fixPost; boardTopUp asks
  fixPost first (2 of 3 top-ups), old kinds never the same target twice a day; CHORES.fix (per 0); jobMeterSys j.sys;
  shareOut skips j.fix; jobStepDone done line. 15b: IX_STOP.fix, ixChoreTap sign + tool, boardLesson + board row first,
  class 'lesson', guideShift lesson pointer. Words content/works/fixes.lines baked (1164 baked lines). Extras lapse at
  leaveEnd (boardTopUp line ~20586), as before.
- machine_check: fix OK (18 small repairs, 10 science, 0 repeats; share Days 2-28 53%); 0.92.2 OK (47%) and planted g1
  FIX_ON=false OK -> **no line fails without the fix** (fixOn-gated). g2 (ship stream only) FAIL; g3 (done-today skip
  off) FAIL; **g4 (shareOut j.fix guard off) OK -> crew-never-take not proven.** Asked FX10 for both lines.
- Nit: machine_check comment "both near 45-46%" vs 47/53 here.
- d22d1132 (machine_check only, game unchanged): new 5z lines on any build (quick player's repeats <= 14%, Deck 2 >= 12%;
  small repairs never released/shared/claimed by crew, forced through shareOut). fix OK (8%, 21%); 0.92.2 FAIL (20%, 4%,
  forced fix released); g1 FIX_ON=false FAIL; g2 ship-stream FAIL; g4 shareOut guard off FAIL. Good.
- career_check on the game: OK (first run timed out under load; rerun OK). interactions_check: g5 (boardLesson null)
  FAILs the lesson line; fix run still going.
- **FINDING (game): arrows_check week guide FAILs on FX10's game, 2 of 2:** "the scanner never counted as used by Day 8,
  the next workday after its lesson"; no m2. Same (b75dcf81) arrows_check on 0.92.2: OK (m2 Day 8, scanner used Day 8,
  m6 Day 9). Reading: small repairs (2 of 3 top-ups) fill the follower's Day 8, no scanner use -> m6 never opens. -> FX10.
- **b75dcf81 (arrows_check only, backlog 15): PASS on its own** — old arrows_check on 0.92.2 FAILs at m6; new one OK.
- d22d1132: cadet_test 0.92.2 vs FX10 game ALL IDENTICAL; check_fast QUICK CHECK OK (408 s). FX10 (08:14) confirms the arrows FAIL is real on the final game, investigating.
- **64cc5653 / 1bd0a34e (game 846f8f35...4bb0... ; 1bd0a34e = build-table only): PASS (~09:42 UTC).** fixScanTick (24p slot,
  WORK_TICKS, FIX_ON-gated): from the first workday after the m7 lesson, while the scanner's unused and no part-cause
  repair is open for you, jobReserve('washer', d, 570, slot 24, pump, until shift end), once a day. arrows week guide on
  the fix: OK (scanner first used Day 8, m6 Day 9; earlier d22d1132 FAILed 2/2). machine_check OK with forced states
  (due once; never before the lesson, after a use, on its day or a day off). Plants: h1 used-gate off FAIL, h2 day-off
  gate off FAIL, h3 today's-slot guard off OK (the open-repair guard already blocks a second the same day; backstop).
  career_check OK, mech_check OK, cadet_test 0.92.2 vs fix ALL IDENTICAL, check_fast OK (291 s). FX10: day_check 8 OK,
  interactions_check full OK on 3e5c4fe2 (my own run cut short, no FAIL; LEAD 33 accepted FX10's).
  Owner sign-offs given: section 17 (Systems engineer), 15b (small edits), 24p (Works career; LEAD 33).
  Notes: m2 (work uniform) now Day 9 not Day 8 for the arrow-follower (FX10 notes it in the build table).

## 0.92.4 queue (LEAD 33, ~14:57 UTC): item D, FX10: warn when you take a repair job whose part would run past a lesson start
Base claude/integration 3866c8f3 (0.92.3). Lead 34 (session_019RdVfeRPRiJpHGjKujZZJA) took over ~15:00 UTC. Verdicts to Lead 34, FX10 + BM16 (session_01MB7n4yvCAeGyWN4WZCAGPh). Waiting for FX10's sha.
- FX10 p924-fx10 d8f128be (game c05d277a...; code dcff694f): lessonClash (15b) + ixBoard.take appends "Heads up: it runs to
  about HH:MM (its part has to be made...), and <lesson> with <name> starts at HH:MM." when now + mins + make + 10 > the
  meeting. interactions_check line: near (30 min) warns, far (10 h) not; fails on 0.92.3 (FX10).
  Device Jobs path: not reachable (verified: sec 19 native deviceApp jobs at ~12100 registers first; the shim skips legacy addSection; the live app says "You take jobs at the job board"). Closed.
  Running: interactions fix + k1 (always warn) plant, cadet_test vs 0.92.3, check_fast.
- **PASS 0.92.4 D (~16:45 UTC)** at the branch head (backlog row FX10-1 only after d8f128be; game c05d277a). interactions_check
  OK (near: heads-up with end 11:03, machine shop, "Making it safe with Ines starts at 09:51"; far: none); planted k1 (no
  end<=start return: always warns) FAIL; 0.92.3 has no heads-up text at all (line fails there). cadet_test 0.92.3 vs fix
  ALL IDENTICAL; check_fast OK. Section 15b small edit: sign-off given.

## FX14 sim bay (claude/rec-simbay), Lead 34's ask ~16:55 UTC
Base 3866c8f3. All behind SIM_BAY (#simbay / ?simbay); tested on copies with `const SIM_BAY = true;`.
- S1-S4 8ee61c90 (game 85e62d4d...): room split (S cols 28-31, booth b 32-33; 7-booth-1 at col 32 stays), doors, hatch,
  booth machines moved (ids kept), simBayDress/simBayKit (pods, screens with a small shader, poster, bench, shelf), recSim
  (15 min, leisure +20, queue on the bench), simpod machines (sys 'rec' like the other 13 rec machines; parts bearing/lamp).
  Off: cadet_test vs 0.92.3 ALL IDENTICAL, check_fast OK. On: deck_check OK (Deck 7 lift view 170 -> 171 calls),
  interactions_check OK with the sim part, day_check 2 OK. Planted (screens never play + queue never needed) running.
- S5 35398d43: sim-pilot habit (Raman always; else only those with no rec habit, key 1035); schedBuild 'sim' kind with
  simPlanShut. No new check line yet -> asked. Nit: REC_HABIT_TEXT "rec dec" (table never read).

## DV1 promo-arrows 81e9065c (0.92.5; game fbabb6ae...): reviewing (~18:10 UTC)
Diff: 24p promoPartsAside (tops the shelf up to what the t2 test still needs, at the offer and each minute), promoGuide
(flag 'promoted' once tier >= 2, also for saves already officers; queue asks promo:test/summons/move/ceremony at levels
3/2/1/1), old setGoal arrows only with the queue off, cabin walk at 17:00 even mid-job; sec 25 dvCareerNext drops row asks
while a promo beat is pending. Notes to weigh: free parts for the crew while the test's open; 'promoted' opens Come over and
the newcomer guide (incl. existing officer saves). Plants q1 (no parts aside), q2 (no flag), q3 (no queue asks) ready.
- promo-arrows: arrows promo on the fix: ARROWS CHECK OK (test Day 9 first try; met/walked/met; promoted; 4 queue entries;
  4 "brace the housing" stuck spots = backlog DV1-2, printed only). 0.92.3: FAILs (test Day 10, move by mail, no flag, no queue
  entries). Plant q1 (no parts aside): FAIL (Day 10, stuck on "Look over the air scrubber"). q2/q3 running. DV1's answers:
  parts top-up bounded (own parts, test day, <= 2) and the flag for existing officer saves is intended ("activate").
- sim bay S5: day_check 2 and 6 with SIM_BAY on: OK. S6/S7 cb4387e8 (game ed2b6fc8...): sim night (every other Thursday
  from Day 8, Raman hosts) in SHIP_TRADITIONS when on; S7 loosens the pod test for crew pilots. "rec dec" is the crew's name
  for the deck (not a typo; my nit withdrawn). Still asked: a check line that crew pilots fly. Running: events_check on
  (+ who=0 plant), cadet_test off vs 0.92.3, check_fast.
- **PASS promo-arrows 81e9065c (~19:45 UTC).** Plants: q1 parts aside off FAIL; q2b both flag setters off FAIL (q2, one
  setter, passes: the skip path sets it too: redundant by design); q3 queue asks off FAIL (all four beats, move late, ceremony
  by mail). social_check OK (the flag's features). cadet_test 0.92.3 vs fix identical (j_steer1 6 px 1 level, noise).
  check_fast OK. DV1's own: career, mech, intro, day 1, devmode, dev_arrow OK. Sign-off: 24p, 25 (small edit).
- **PASS sim bay claude/rec-simbay 328f678a (~20:05 UTC; game ed2b6fc8...8c07, unchanged since cb4387e8).** Off: cadet_test vs
  0.92.3 ALL IDENTICAL, check_fast OK. On: deck OK, day 2/6 OK (S5), events OK (sim night), interactions OK incl. the sim part
  and S7b's pilots (6 pilots incl. Raman, 62 turns; pod 1 tagged out -> never planned, pod 2 51 turns). Plants: screens never
  play + queue never needed -> 3 FAIL; sim night who=0 -> 3 FAIL; REC_HABITS sim-pilot removed -> both pilot lines FAIL.
  Screenshots plans/simbay-shots (bdff907c) look right. Sign-offs: 4e, 15r, 17 slot, 14 (recHabit/schedBuild + sim slot),
  18 traditions slot, where the owner seat isn't live.

## FX14 weekend traditions claude/p925-weekend 9e840769 (0.92.5 item 16; game 8ab993b2...), from 0.92.4 ba836359: reviewing ~22:00 UTC
Six .trad files baked into TRADITIONS; the loader skips them unless WEEKEND_ON (#weekend); joins in TRAD_JOIN (18's slot)
only when on. Ungated: EV_MAILBOX cap 40 -> 80: nothing reads it but events_check (not saved), so no player-visible change.
Picnic: Saturday 13:00-13:50 in the garden, hunger +30 on join (FX14: not yet verified). Running: events/join on, join and
events with every-song's join removed, cadet_test off vs 0.92.4, check_fast.
- **FIXES NEEDED 9e840769** (FX11's find, confirmed): weekend joins' PLAYER_ACTS 'tj:'+id never built (the load-time loop runs
  before the slot) -> empty activity, no gain, never ends. join_check OK anyway (+12 generic social), and OK with every-song's
  join deleted (it only walks TRAD_JOIN). events_check on OK; off: cadet_test vs 0.92.4 ALL IDENTICAL, check_fast OK.
  Day 6 leaders not the hosts (every-song: haddad-tamsin vs torres-zeke; picnic: soto-marta vs cruz-tove "always") -> asked.
  FX14 handed over; FX11 fixes with T3/T4 (tjActs() rerun). Review T1-T4 together.
