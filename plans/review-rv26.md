# RV26 review notes (second reviewer for 0.99, hired by lead 45, session_01GKuymnu4NeXJhwPe21FWk7)

Style as RV25's (plans/review-rv25.md on claude/review-rv25): code read, targeted checks, cadet_test against the base,
verdict PASS or FIXES with exact reasons. Base for all three: claude/staging-pad 610ad7f1 (0.97.0, live game).
Builds and logs in my scratchpad (not committed). Probes kept in plans/rv26-probes/ when worth keeping.

Queue (lead 45, 2026-10-29): 1. TB1 title screen claude/title-099; 2. EV2 seated dinner + vessel words claude/visit-099;
3. SD3 title music claude/title-music-099 (on top of title-099). RV25 keeps 0.98 (OP1, RB1); told RV25 I took TB1/EV2.

## TB1 title screen, claude/title-099 8d2a708 (session_01GKuymo2ikX7y7GA88GPXQP)
- cadet vs 610ad7f1 ALL IDENTICAL. names_check (branch's, with the two-switch rule) OK. title_check OK (switched-on copy
  it makes itself; the switch as built: no title, nothing held, even with ?title).
- Code read: off, the page's first script returns at once (TITLE_EARLY false), titleBoot only hides #title; titleHold() in
  freezeSync/saveGame is false (TITLE is a var, undefined until section 30 runs, then on: false). No listeners, no pad
  panel, no onSim when off. The CSS only adds #title to the phosphor lists and #title rules (hidden). On: the first
  script reads only (no writes); a pick made before load waits in data-pick; Continue waits for the first frame (READY);
  saves refused under the title are made on hand-over; Escape/B keep playing; Start is Continue (unshifted ahead of Pause).
- **VERDICT TB1 8d2a708: PASS** (sent to TB1, lead 45, BM20).

## EV2 seated dinner + vessel words, claude/visit-099 b21a531 (session_01GKuymn7YSDpEbeNYGxup6N)
- cadet vs 610ad7f1 ALL IDENTICAL; day_check 18 OK; names_check OK.
- Code read: VISIT_DINNER_ON = EVENTS_ON && EV_SWAP_ON (on); OCCASIONS.veyliDinner due on vdDay() (evCalPlan + 2 = Day 18);
  occasionAdd copies o.places onto the appointment (only when the occasion has places: other occasions unchanged); two
  event-only seats 2-captable-7/-8; EV_BEATS 'beat' 18:45-20:15 Day 18; the dressing is the visit's only escalation
  dressing (nothing overwritten); vdTick: arrow from 18:45, seated once from 18:55 (q.f.sat, saved with the occasion).
  V-2 words: five lines, the visit "last week".
- Play probe (plans/rv26-probes/vd_play.py, Dev jump to Day 18 18:40, 390x844):
  in room C: everyone walks to their own chair (marrow -5, teshavi -7, saruth -1, vance -2, kesrin -8, moleth -4,
  ithra -3), all seated sit:talk by 19:05; you seated and eating at 18:55 (2-captable-6); the scene from 19:00, the
  choice, all 11 lines; the meal ends ~19:31; kept at 20:15, the diners leave by the lift. Shot: the table with food.
  in the galley: the arrow vd:dinner from 18:45 to 20:15; missed at 20:15 with the gist. (A Dev-jump-only promo:home
  arrow, from a cabin move you never walked into, hid it in the first run; cleared by setting promo.sight.home.)
- Notes (not blocking): the Captain, Kesrin and Ithra are still walking in when the scene opens at 19:00 (the Captain
  says "There you are" on the way to her chair); after the 40-minute meal you stand up at ~19:31 while the dinner runs
  to 20:15; Dev mode's jump label "the formal dinner, from the galley" (and its comment "nobody sits there") is now stale
  (the user said no Dev work: a backlog row); EV_BEATS takes the day from EV_CALENDAR, vdDay from evCalPlan (differ only
  if the visit ran late).
- **VERDICT EV2 b21a531: PASS** (with the notes above).

## SD3 title music, claude/title-music-099 19798c3 (on title-099 8d2a708; session_01GKuymir9eBj7X6kLtwLRmq)
- cadet vs 610ad7f1 ALL IDENTICAL (title off as built; SND_TITLE 'A' only acts while SND.titleOn, which only section 30
  sets with the title on). names_check OK. sound_check (branch's, with the new title part) SOUND CHECK OK: candidates
  64 / 71 / 58 s, 'Event', not on the Music list; on: running, one copy, hum hushed; off: [0, False].
  title_check on the SD3 build: TITLE CHECK OK, no page errors.
- Real flow (plans/rv26-probes/tm_flow.py, title switched on in a copy, ?title&nosave&sound): loaded, ship held
  (06:00); a tap on the title: context running, titleA playing, hum:quarters hushed, clock still 06:00; NEW GAME: title
  gone, ship runs, title track list empty, hum back. No page errors.
- Code read: S.frame keeps the context running only while SND.titleOn; the rooms' once-a-second sounds wait under the
  title; titleTick runs only while on or fading; the hum bus's gain is set back to 1 (its own default; nothing else sets
  it). Music app off: no title track (the hum still hushed: a silent title). SND_TITLE 'A' is the provisional pick
  until the user chooses on plans/sound/title-music.html.
- **VERDICT SD3 19798c3: PASS.**

## EV2 follow-up, claude/visit-099 60287f2 (my four notes)
- Diff: occasionAdd's optional `early` (appointment from at - early, len + early; only veyliDinner sets it, 10);
  your meal lasts to the dinner's end (min 20); comment on the hold's day; backlog EV2-1 (Dev jump). Others unchanged.
- cadet vs 610ad7f1 ALL IDENTICAL; day_check 18 OK.
- Probe (vd_play.py now takes VD_AT): from 18:40 in room C, all seven seated by ~18:55, the scene at 19:00 with the
  table full, you eating (80 min) to ~20:08, kept 20:15, diners leave. Walk-in at 19:05 (VD_AT 1145): seated at once
  (70 min), the scene starts for you from its first line, eating to ~20:10, kept. No page errors.
- Note: the Schedule row shows 18:50 while the Mail says 19:00 (EV2 flagged it); arriving early is harmless.
- **VERDICT EV2 60287f2: PASS.**

## EV2 follow-up 2, claude/visit-099 3dda559 (appointment back at 19:00; a.early read by section 14's apptWhere)
- Diff: occasionAdd books at the occasion's own time and sets a.early (like a.places); apptWhere (section 14, the sim
  engineer's): go = a.at - min(30, a.early if > 0) - walk; the end unchanged; no a.early = as before (Number() guards junk).
- Read: only the set-off time moves (they're shown at their chair from go); apptFree/apptReply and the 'kept' rule still
  use a.at; only section 18's occasions set early, so day plans without one are untouched (cadet identical).
- cadet vs 610ad7f1 ALL IDENTICAL; day_check 18 OK; probe from 18:40: all seven seated by 18:55, scene 19:00, you eating
  to ~20:07, diners leave 20:15. No page errors.
- **VERDICT EV2 3dda559: PASS.** Section 14 line: fine on my read; per owners.md the sim engineer may still want a look.
