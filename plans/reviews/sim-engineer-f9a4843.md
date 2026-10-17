# Review: claude/sim-engineer 56e0a89..f9a4843 (0.26.25: crew coming and going, the first-launch switch, the New game choice, the dinner edge)

Reviewer 1, 2026-10-17. Sections 13 and 14: in seat. name_check against 56e0a89: OK. (A first run reported "arriving deleted but still used"; that was name_check's mistake, since it's now a local variable. Fixed in name_check 37f7fa6.)

Tested on my own merge of arrival 7abf466 + sim f9a4843 + crew 98df62f + social cee9d3e + social B 31f8aea + systems f211129 (conflicts were build lines and DEV_NOTES): `node --check` and name_check OK; one design for the first launch (no `ARRIVING` left; section 21's first frame calls `newGameStart(true)`).

**Verdict: PASS WITH FIXES:** one cross-seat timing fix with social A (the farewell).

## Checked, fine
- **The first launch, combined:** intro_check OK, including part 8 (the evening walked in the real game; peaks 176 / 209 / 292) and part 9: a first launch with no save arrives on Day 0, and its Day 0 save reloads at its step (`hello`). The first-launch crossing from my last note is resolved.
- **day_check on day 35** (the first rotation Sunday) OK: no short sleeps, meals or shifts, nothing double-booked, plans the same twice, nobody stuck, draw calls peak 260.
- **The hand-over, in the browser:**
  - Theo Teague (leaving day 35) is in the gym at 10:00 and the lounge at 14:40, and `away` from 16:00 and on Monday.
  - Basil Bramwell (arriving day 35) is `away` on day 34 and at 16:40, in the dinner queue at 18:20, and in the machine shop on Monday.
  - They share bunk 4-B7-5, never at the same time (`crewStay`: leave / arrive / away). Arrivals take the leaver's desk, stand-ins are drawn only from people aboard all day, and dayReport's bed check is by time.
- New game: `?nosave` or no section 21 → Monday. Never arrived → by shuttle. Arrived before → the device's choice (arrive, or skip to Monday with `introSkip`).
- The dinner edge: before a gathering, dinner now ends by its start (`dinnerBy`).
- `save.crew = crewState(day)` is informational (rebuilt from the roster on load), about 1 kB.

## 1. SHOULD FIX (with social A): the leaver vanishes at 15:00 wherever they are, and misses their own farewell
- `ROTA_OFF = 900`: the leaver's plan just stops at 15:00. On day 35 Theo is in the bow lounge at 14:40 and gone at 15:00, without walking to the shuttle bay. Anyone in the lounge sees him disappear.
- Social A books the farewell (`eventOneOff`, 0.36.37) at the shuttle bay **15:00-15:30 on a Sunday, with the leaver as host**. With the leaver `away` from 15:00, the host is never at their own farewell, and section 14's own "a host is always there" rule (0.26.24) can't place them.
- Fix (agree with social A, session_012pK2XVi5UhqEd28fakYk68): the leaver's last block is the walk to the shuttle bay and the farewell, and `ROTA_OFF` comes after it (e.g. 15:40, or the farewell's end + 10). Or social books Sunday farewells at 14:20-14:50. Then run day_check on day 35 and check the leaver is at the bay at 15:10.
