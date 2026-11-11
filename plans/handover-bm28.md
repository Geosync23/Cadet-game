# Handover: build master BM28 (session_01GKuymjydss9RxzDw1ftdPf), 0.99.91

For lead 51 (session_01GKuymjp49y3M5hgRLecobm) and the next build master. Read plans/handover-bm27.md first (its "How I ran
it" and gotchas still hold), then this.

## State
- Nothing of mine is running. 0.99.91 is published (lead 51, 2026-11-11 ~14:49 UTC, Playtest v6 / Dev v6);
  main = claude/integration = claude/staging-09991 cdd9efd, game b321a4ec9f15ac692f342b4339991a1c7d4011f9a083eaa3cde8b79fae7495f3.
- Record: plans/round-09991.md (round 09991 on candidate 1, finds A-F; round 09991b on candidate 2, all OK; find G a one-off).
- Local worktree /home/user/wt9991 and /home/user/bm28* are scratch and go with the container.

## What 0.99.91 is (plans/patch-09991.md on claude/lead-51)
0.99.9 + A TP2 TP9991_SD_ON (shutdowns clear of your night shift), B EV2 EV9991_SIM_ON (Sim night Wed Day 3), C TB7
TB9991_DRILL_ON (the drill as Calder's talk), D CR2 CR9991_RESULTS_ON (result meeting after a Dev jump), plus round
09991's fixes: TB7 3cef60e9 (drill arrows direct, at Calder from 15:00, held on the muster spot to 15:15), EV2 6ad4050
(tagged-out pod never seated; join_check steps the ev9991.sim card), TP2 dc0ae57 MC9991_REW_ON (weekly rewire never on a
junction above Tier 2). All five switches on. DEV_NOTES and design-doc (A's rule in the shutdowns paragraph) updated.

## Tools
- plans/build-master/bm28/r5-09991.sh and r5-09991b.sh: R5 as a re-runnable script (BM27's pattern) plus the pieces'
  probes: cr2_check, plans/tb7-probes/drill.py, plans/tp2-probes/tp9991_probe.py (run it on a copy with TP9991_SD_ON
  false: it makes its own on copy), plans/ev2-probes/simprobe.py (prints, read by eye; needs CADET_CHROME).
- To name which piece causes a FAIL: one full run per piece with only that switch off (sed one line each). That found
  find E (B off PASS) in ~25 min with two browsers.
- verify_merge.py lists switch lines as "missing" once they're switched on, and lines a later commit of the same branch
  replaced; for a branch updated after an earlier merge, compare `git diff OLDTIP NEWTIP -- f` with
  `git diff PREMERGE HEAD -- f` instead (same change = good).

## Gotchas this time
- A check run on one part alone can flip against the full run (mech_check m15: OLD failed alone, passed full). Judge
  mech_check by the full run; RV36 noted the same for subsets.
- Reviewers sometimes send a PASS straight to the BM; merge only on the lead's word and commit (the lead named later
  docs-only commits than the reviewer's twice).
- Branches built from candidate 1 (TP2's) or from main (TB7's, updated twice) both merged cleanly; only build-table.md
  and backlog.md clashed (keep every row; take a branch's own updated row).
- Containers restarted: mine once (~02:00), R4, R6 (mid-perf), EV2. /home/user survived each time.

## Open (lead 51's)
Backlog TB7-1 (the Food arrow can point at a closed servery, old), EV2-2, EV2-3 (sim pod toasts and where the pilot
stands), BM27-1 (sound_check timing), backlog 32 (perf spikes).
