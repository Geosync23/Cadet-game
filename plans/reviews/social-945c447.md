# Re-review: claude/social 45b0595..945c447 (0.36.50-0.36.51)

Reviewer 1, 2026-10-17. **Verdict: PASS.**
- The repair cue reads the machine's own kind first (`machineById(d.machine).kind`), then `d.job`, then `d.kind` unless it's 'repair'. social_check sends a repair through the real `simNote`: `cue True, wrong False, mem True, queued 0`.
- social_check restores the real bonds after its bond test (`B0`).
- **Full merge** (arrival 1353f42 + sim 2f6d8dd + crew 98df62f + social 945c447 + social B 31f8aea, conflicts kept on both sides): SOCIAL CHECK OK, the jump test True, the real bus OK, purity OK. name_check OK.
- Social A's failing jump test on its own merge most likely came from merging `claude/ship-systems` over the sim's newer section 17 (whose `simLater` stamps notes with `SIM_AT`). `claude/ship-systems` must not be merged any more; the sim branch contains it.
