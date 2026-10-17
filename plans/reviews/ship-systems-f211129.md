# Re-review: claude/ship-systems ae58e43..f211129 (0.33.39: ship notes for social A)

Reviewer 1, 2026-10-17. Section 17 only. name_check against ae58e43: OK. **Verdict: PASS.**
- `repair { who, machine, state, kind, deck, id }`, `jobAbandoned { machine, dept: null, id }` and `jobUnclaimed { machine, dept: null, id }` match what section 20's `repNote` and `memRepair` read (`who === 'you'`, the `failing|broken` state, `machineById`).
- Every section 17 note now waits in `SIM_Q` and goes out after the hour loop, or after your own action (`simFlush`), so a listener never runs in the middle of `jobsHour`. The re-entry this could cause (a listener calling `planDay` → `machinesNow` → `simFlush`) only drains the same queue, and section 13 caps the depth at 8.
- machine_check OK (rerun here): your repair noted with the state it was in; the crew's repairs (25); a dropped job sends `jobAbandoned`; `jobUnclaimed` goes out once per job (4); no badly shaped notes; the reserved-job cases from 0.33.38 still pass.
- Note: after a long skip (sleeping), the notes for all the hours skipped go out together, stamped with the time they're sent. Fine for cues and memories ("in the last day or two").
