# Re-check: the Chief after three missed shifts in a row (claude/leave 90272ef, 0.61.4)

Reviewer 1d, 2026-10-17. This is the user's rule change, on top of 8f1f88a (PASS).

## Verdict: PASS

**The code** (`careerLadder` and the miss loop in `careerTick`):
- A missed workday adds one to `ms`.
- A worked shift sets `ms` and `ca` back to 0.
- Days off, leave and sick days are skipped, so they neither count nor break the run.
- The Chief's step comes at 3 in a row, once per run (`ca`).
- The Captain's step needs `st === 1`, work under 12 and the Chief's latest talk held, so the order still holds.
- Being let go still needs the Captain's talk held and three workdays under 5. That's unchanged.
- `careerLadder` returns while any step is waiting (`c.q`), so 0.61.3's overwrite fix still holds in the new shape.
- `careerClean` defaults `ms` and `ca` to 0, so a save from 0.61.0-0.61.3 loads fine.

**leave_check on 90272ef: LEAVE CHECK OK.**
- Two missed, one worked, two missed: no talk.
- Three missed in a row: the Chief on day 10.
- Late every day with no jobs: no talk (finding 4 is now moot).
- Skipping everything: the Chief on day 10, the Captain day 12, the last day 20.
- Each step re-arms.
- Save 183 bytes.

**My probe** (leave-492364d-probe.py) on 90272ef:
- An older save loaded mid-shift: work stays 50.
- No summons on a leave day.
- New game from the card: works.
- A forced fall: the Chief on day 18, then the Captain day 19, in order.

## A note for the lead (design, not a bug)
A player who misses two shifts, works one, and repeats forever never misses three in a row. So they never get the Chief's talk, and therefore never the Captain's and are never let go:
- That's missing two shifts in every three.
- leave_check's `twoTwo` case drops work to about 21 with no talk.

This follows the user's rule as written. If the user wants that player warned eventually, one option is a second route to the Chief's talk, for example work under 15. Otherwise it stays as it is.

The engineer's design-doc text for the new rule belongs on claude/lead-pillar1 (the lead's copy).
