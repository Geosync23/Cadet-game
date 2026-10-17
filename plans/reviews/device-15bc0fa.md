# Review: device 0.35.37-0.35.38 (c4b2479, 15bc0fa): New game clears appointments; an occasion's missed is final

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS.** One note for the lead (a decision), one LOW (device_check).

## Tests
- device_check (15bc0fa's) on 15bc0fa: **OK**. cadet_test 0.35.36 vs 0.35.38: **ALL IDENTICAL**.
- **Trial merge** device 15bc0fa + sim 236810f (0.26.34) + social 0154e8d (0.36.74): the html conflicts are only in
  the build labels (and player_check.py), and `node --check` is OK.
- **The lead's case, played on the merge:** the Captain's ready-room summons (`occasionAdd('readyRoom', day 3 11:00)`,
  len 25). I stood by the lift until 11:16 (section 14's apptTick: `apptMissed` at 11:15, the device says missed), then
  stood in the ready room by the appointment's seat from 11:17:
  - the device appointment **stays 'missed'** (11:17, 11:29, 12:01): missed is final;
  - social: `socKept` and `socMem` stay false (0.36.74 skips `a.occ`), no relationship points for Marrow, no
    reputation change: **no points either way**;
  - section 18's occasion record goes to **met, then 'kept'** at 11:29, and the ready-room meeting plays
    (the dialogue opens at 11:17).
  Control: arriving at 11:08 (in time) turns the appointment 'kept' by 11:14 (via `r.met`), as before.
- New game: device_check's new assertion (a New game leaves no appointments) passes.

## Note for the lead (a decision, not a bug in this build)
After a missed summons you can still walk in within the door's window. The meeting plays, and section 18 records the
occasion as **kept**, while the device's Record says **missed**. For the ready room nothing else follows (no trace).
For an occasion with a trace (the Captain's table leaves `framedMenu`) the trace would be given for an appointment
the device lists as missed. If "missed is final" should hold everywhere, section 18's door or meeting would need to
check the device appointment, which is section 18's call. If "late but you came" is fine, leave it as is.

## LOW (device_check, combined builds)
On the merge, device_check **fails** "heads-up: as it starts, once": `again` is false because `HU_Q.length === 1`
doesn't hold. A tradition (Late piano, 21:45) is in the 15-minute window of the test appointment (21:30 two days on),
so the queue holds `appt|4170|901` and `tradition|4185|Late piano`. The strip itself is right: the same start card,
shown once. Count only the test's own keys (`HU_Q.filter(h => h.key.startsWith('appt|'))`) so the check survives
combining with traditions.
