# Reviews: R8 (the rec deck's 0.64.1 determinism fix), newest first

R8 = reviewer started by lead 20 (session_019UJSCUCdtC1kTpYiABWKhs). Branch `claude/reviews-r8` (from R7's notes).
Team (lead 20): lead session_019UJSCUCdtC1kTpYiABWKhs; rec engineer RE20 session_019auXkZkQG3gnNjmArAauLx (all game-file
changes); build master BM10 session_01KpcQGJvrAz57dmKp6AFg4w (check round on claude/rec-cand-s1); R8 session_01GdhqdLeZuGFQSTX7RL92U5.
Scope (lead 20, from the user): item B (career half-xp) dropped. Item C added: the climb queue (R7's note: one belay
tagged out + the holds roping off the other route -> recShut().belays is 1 so recStart doesn't refuse, but recBelaysFree()
is empty with nobody on the wall -> queued forever). Review C for: a refusal instead of queueing when no belay can free
up; a player already queued released with the refusal if the second fault lands mid-wait; wording ("the rec deck");
REC_DECK=false identical; the new check case.
Item D added (the user's ask): on phones the Tracked button (#trkBtn, placed by section 15b's trkPlace) moves under the
needs strip's left end, lined up with its left edge, word kept. CORRECTED (lead 20, the user): the phone stack is
Needs, then Tracked (fixed, never moves), then the activity bar at the very bottom, under Tracked. Review D for: no
overlap with the activity bar, heads-up/tip cards or the round buttons at 390 and 320 px; Tracked doesn't move at all as the bar
shows/hides; the bar sits below Tracked; non-phone layout unchanged (cadet_test shots at 900 px should be 0 px different).

## claude/ways-of-working 4bcbaa9 (docs only, DEV_NOTES' top paragraphs): PASS

The facts check out: archive/starship-cadet-0.64.2-whole.html is there, claude/whole-file-0.64.2 is at c575a8e, the
sha256 matches. Note only: `plans/roadmap-after-recdeck.md` is on claude/lead-pillar1, not on this branch (say so, or
bring it across when merging); `claude/integration` doesn't exist yet (fine, the build master makes it). The arc_check
fix from 928d49a is still open.

## claude/ways-of-working 928d49a (step 2, WW1 session_0192KVdPtywdv7sp3mXUXGHU) vs c575a8e: PASS WITH FIXES

1. **Slots (ff32ddd)**: 17 inserts, 51 lines, all `// ---- slot:` / `// ---- end of slot:` comment pairs plus a blank;
   removing them gives c575a8e's game byte for byte. Each sits between two top-level statements, just before a section
   heading (add_slots.py checks that with acorn too), so none is inside a string, template or regex. cadet_test c575a8e
   vs 928d49a (re-run here): ALL IDENTICAL. The archive copy's sha256 = c575a8e's game (e4897023...).
2. **Exit codes**: cadet_test, day, deck, disc, food, machine, path, perf, social: one `sys.exit` after the unchanged
   OK/FAILED line, on the same `ok`/`bad` that picks the line (inside `with sync_playwright()` after g.close(): fine).
   arc_check's default mode likewise (`arc_ok`). **FIX: arc_check's two other modes still exit 0 on failure**: `booth`
   (line 163 `sys.exit(0)` after "BOOTH CHECK: ...") and `calls` (line 176, after "CALLS CHECK: ..."). Make them
   `sys.exit(1 if bad else 0)` and `sys.exit(0 if (not bad and not g.errors and not any(r['unheard'].values())) else 1)`.
   Not in check_fast, so no false green there today. perf_check now exits 1 on the old memory note (backlog 14): known.
3. **names_check.js / check_fast.sh**: names_check OK on 928d49a; a planted file (a second `function machinesNow`, a
   key added twice with Object.assign, a "Deck 7" string) gives three FAILs and exit 1; a const twice fails as "does not
   parse". check_fast: a step passes only on exit 0 AND its OK line; the lanes are waited by PID (`wait $A`, `wait $B`),
   not a bare wait; the planted file stops it at "parse, names, text" with exit 1. Clean run here: QUICK CHECK OK in
   210 s (rc 0). Limits (documented in the file): names inside if/blocks aren't checked; only "Deck 7" for naming.
4. **1b75316**: CLAUDE.md has the user's two rules (room to comment on every published page; cut things parked, never
   deleted), the build number as the build master's, early merging into claude/integration, owners, slots, backlog,
   check_fast before every push. Build table: all 1036 rows taken out of DEV_NOTES are in plans/build-table.md in the
   same order (plus the new step 2 row); the old "Current build 0.60.7" notes went there too; the old section list is
   replaced by plans/map.md / tools/section.py. Start messages (plans/start-prompts-step2.md) read fine.
5. **quick-check.yml**: valid YAML, `on: workflow_dispatch` only (manual); it installs playwright, three r128 and acorn
   8.12.1 under $RUNNER_TEMP/cw and runs `bash check_fast.sh` with CADET_CHROME '' (Playwright's own Chromium), which is
   what it says. content_gen.py, leave_check.py and device_check.py exist and exit 1 on failure.

## bf71e7a (claude/rc-wip, 0.64.2, vs claude/rec-cand-s1 cf55b35): PASS

Note: the candidate ships with `REC_DECK = true` (0.84.11), so "on" is the build as is; "off" = a copy flipped to false.
- **0.64.1 determinism (recPlanShut)**: as reviewed at 1030f4d, plus my machUseDay fix exactly as asked (`occ.use`;
  a replan makes a new occ, machinesReset drops those SHIP_DAYS entries and their MACH_USE).
- **Maeve's rides (item A)**: the commute segs her recRound adds get tag 'round' (commute segs had no tag before, so
  nothing is overwritten; no other code reads a 'round' tag); dayReport counts 'round' as work. Deck-on only.
- **capOk from a0 - C** in recVisit: the ride down counts on the rec deck. Deck-on only. Fine.
- **Item C (climbing wall)**: recBelaysUsable() (free or busy, not tagged out nor roped off); recStart refuses after the
  "both tagged out" line ('rec.shut.wall', fallback text fine: "One auto-belay's tagged out and the other one's route is
  taped off. No climbing till Works are done."); recFrame ends a climb wait with actEnd(true) + the right toast (both
  tagged out -> 'rec.shut.belays'). All guarded by REC_DECK. interactions_check's new case: OK switched on (tap refused,
  mid-wait released, both with the reason); off: skipped, INTERACTIONS CHECK OK.
- **Item D (Tracked on phones)**: measured at 390x844 and 320x568 (needs strip shown; cadet_test hides it), an activity
  bar forced on and off: needs 14,124-302,160; Tracked 14,168-107,198 in all three states (never moves); the bar
  14,204-302,238 under Tracked; no overlap with Device/Pause (y 86-116) or the round buttons. On cf55b35 Tracked sat at
  209-302 x 168-198 and the bar at 166-200: they overlapped, so this also fixes that. Heads-up cards are placed under
  the lowest of needStrip/actBar/trkBtn (line ~11375), so they clear both. Non-phone: actBar's y and trkPlace's other
  branch unchanged.
- **Regression**: cadet_test cf55b35 vs bf71e7a, on: ALL IDENTICAL; both flipped off: ALL IDENTICAL.
- One owner, no duplicate names (recBelaysUsable once), naming fine in new text.

Note, no fix asked: REC_HABIT_TEXT (unused, pre-existing) still says "rec dec" four times (lines ~9784-9786); harmless
while unused, worth fixing if it's ever shown.

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
