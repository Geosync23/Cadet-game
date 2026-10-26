# Handover: FX24 (builder, lead 37 then lead 38), 2026-10-26

Three jobs for 0.93.2, each on its own branch from claude/integration b957b92d (0.93.1). Reviewer RV18
(session_01PMfvrCN6StPzwVSPGX7ijH); lead 38 (session_01G2y9crUv6vDiiEB2q6Yo9W); build master BM18
(session_01A3S2VBMYmTt2wCZa8ej7XR). Words: CS1 (session_01QcPAXHjQZ2HfZKMCTbaW9v).

## 1. claude/trad-0932: the traditions variety (switch TRAD_0932_ON, off)
- What: six weekly ones take turns from week 2; every-3/6-week rhythms; 14 new traditions + Brennan's tasting table
  after dinner in the galley; the new hand's tea retired under the switch; tap the host -> their join line -> the
  activity with a pose; bubbles from each tradition's own lines; the host's close line. Details: DEV_NOTES "The
  traditions variety", design-doc "Every week a little different", build-table rows 0.93.2-t.1 / t.2.
- State: RV18's first review (M1-M4, S1-S5) fixed (c536ed00 and on); waiting for RV18's re-review.
- Switch on: join/day(1,3,5,7,12,20,27,70)/food/interactions OK; events_check 84 days fails only on backlog FX24-2
  (Farouk misses reading corner Day 7: no walking time on one deck; the same in 0.93.1; known-old by lead 37).
- FX24-1 (Day 32 galley double booking) fixed behind the switch (section 14's galleyTwin).
- Merge notes: claude/event-swap (FX22b) also adds a line to section 18's TRAD_LIST loop (separate lines, agreed);
  Basil's beat 4 (dinner, not the tea) comes from event-swap's bramwell.arc.
- Gotchas: events_check walks a weekly tradition on the deck only once its rhythm is "new" (every N weeks), which is
  how FX24-2 surfaced; join cards need ...cardWhere(e) or meetingsTick closes them at the next ship minute; the rec
  deck two need flag rec.on.

## 2. claude/tray-seat-0932: Take a seat (no switch)
- Done, all checks OK (5892511c). claude/tray-seat (no suffix) is FX6's old branch: not mine, untouched.

## 3. claude/auto-doors-0932: Auto doors (switch AUTO_DOORS_ON, on; setting default on)
- Done, all checks OK (61893eae); awaiting RV18. Arrows only point (lead 38's call).

## Testing
Setup as plans/testing-guide.md section 2 (pip install playwright numpy pillow; three r128 and acorn in CADET_WORK;
CADET_CHROME=/opt/pw-browsers/chromium). Switch-on runs use a copy with the switch flipped by sed. Run long checks in
separate CADET_WORK folders and separate log files (two runs writing one log file corrupt it).
