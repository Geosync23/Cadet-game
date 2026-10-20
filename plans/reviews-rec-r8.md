# Reviews: R8 (the rec deck's 0.64.1 determinism fix), newest first

R8 = reviewer started by lead 20 (session_019UJSCUCdtC1kTpYiABWKhs). Branch `claude/reviews-r8` (from R7's notes).

## 1030f4d (claude/rc-wip, WIP 0.64.1, vs 50d55ef): PASS WITH FIXES (pre-review of work in progress)

What it does: crew rec plans read `recPlanShut(d, occ)` (the 22:00 record the evening before, once settled) instead of
`recShutAt(B + t + C)`; shipDay plans a provisional day again once settled; machUseDay doesn't keep a provisional day's
use; machinesReset drops plans that read the old record.

Checked, fine:
- **Determinism:** the only planner read of MACH_HIST is now recPlanShut (schedBuild has no other recShut/recShutAt/
  MACH_HIST reads). "Settled" is right: MACH_HOUR is the first hour not run and serviceMachine rewrites MACH_HOUR - 1,
  so `h <= MACH_HOUR - 2` is final. While the sim runs any hour of day d, day d's hour is settled (except Day 1 and the
  day of a load), so wear never reads a provisional plan in ordinary play. The planner only uses `sh.court/float/belays/
  pool/river`, not `sh.route` (the one field that reads the holds' current lastService), so RC's route gotcha can't
  reach a plan.
- **REC_DECK = false:** recPlanShut returns REC_OK and marks nothing, so shipDay's new test is `undefined != null`
  (false: returns the cache as before), machUseDay keeps its use, machinesReset deletes nothing. Same as 50d55ef.
  (`recSettled` is a const: only reached once recPlanShut has run with the deck on, after load; loads clean switched on.)
- One owner, no duplicate names (recSettled, recPlanShut new, once each), no new on-screen text.

**Fix asked (performance):** a provisional day's use is worked out again on *every* machUse call, because machUseDay
neither keeps it nor caches it anywhere. Day 1 of a new game is provisional all day (its hour -2 is never recorded), and
so is the whole day of every load (machinesLoad clears MACH_HIST), i.e. the first day of every play session. Measured
switched on, machinesNow hour by hour: Day 1 = 953 recomputes (1 on 50d55ef); three days in one jump 0.60 s vs 0.13 s
on 50d55ef: about +20 ms each ship hour on a desktop, several times that on a phone. Suggested two lines, tried here
(0.20 s; still deterministic, since a replan makes a new occ and drops it):
  - after `const { plans, occ } = shipDay(d), byId = schedData().byId;` add `  if (occ.use) return occ.use;`
  - `if (occ.recAt != null && !occ.recSet) return u;` -> `if (occ.recAt != null && !occ.recSet) return occ.use = u;`

Notes, no fix asked:
- MACH_HIST keeps 8 days (192 h); crewNeeds looks back 7 days, and day D-7's hour ((D-8)*24 - 2) is pruned at 23:00 on
  day D. If an event change clears SHIP_DAYS then, D-7 is planned again all clear (and stays so): a week-old rec visit
  can differ. Rare; a per-day memo of the settled answer (cleared in machinesReset) would close it if wanted.
- PICKUPS (recPickups) caches a day's pick-up games from the plans and isn't dropped on a replan; recCourtNow is never
  called today, so it's latent. Whoever wires it up should key it on the plan (e.g. keep it on occ).
- Still to come in RC's list: day_check days 3-8, Maeve's on-shift rides (476/480), career xp, the DEV_NOTES row,
  rebase onto claude/rec-cand-s1 (its tip is now cf55b35, BM9's handover).
