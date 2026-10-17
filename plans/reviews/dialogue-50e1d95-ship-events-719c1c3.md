# Re-review: claude/dialogue 50e1d95 with claude/ship-events 719c1c3, reviewer 2

**Verdict: PASS WITH FIXES for combining.** The traditions handover now works. Correction to d40f5d5: the 0.34.21
trad_parse.py did still have `parse_trad`; only `bake_traditions` was missing. 50e1d95 no longer uses it.

Trial merge (integration, then ship-events 719c1c3, then dialogue 50e1d95). Conflicts: only the build labels.
- `node --check` on the merged script: OK. There is one `const TRADITIONS`, in section 22.
- `content_gen.py --check` on the merged tree says **OUT OF DATE**: the block baked on the dialogue branch is
  empty. After `content_gen.py`: Sowing is baked, and a second run says "no change" (byte-identical). The baked
  entry equals TRAD_STANDIN's field for field. lines_check: PASS.
- events_check on the merged, re-baked build: sowing loaded, from Chef Auda Brennan, Mail filled; due on days 6, 97,
  188 and 279; 8 of 13 went on day 6; seasons right. The only FAIL is hull-lights, which falls after my short 7-day run.

## Fixes still due
1. **The build master must re-run content_gen.py after merging dialogue** (generated blocks last). Without it, the
   empty `TRADITIONS = []` wins over TRAD_STANDIN and Sowing silently disappears. Make it a hard step: run
   `content_gen.py --check` in the combine checks. Also add an events_check failure when a .trad file isn't loaded.
2. **HIGH, ship-events, still open:** `friends-of-host` -> live `affinity()` inside eventPlan (line ~13300 in the merge).
   Use `affinityPlan(host, p.id, d)`.
3. **MEDIUM, ship-events, still open:** sowing.trad still has "Don't tell Brennan, she'll want it" in `ask` (Brennan
   can say it, e.g. day 97).
4. **MEDIUM, ship-events, still open:** trad_parse still accepts `quarter week 14 saturday` (never due), and
   `hold: abc` still crashes with a ValueError.
