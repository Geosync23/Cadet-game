# Re-review: claude/social-stories 3042c7c..c689063 (0.39.11)

Reviewer 1, 2026-10-17. **Verdict: PASS.** The tip daf5dec only changes the handover note after c689063.

0.39.11 fixes my three points from social-stories-3042c7c.md. All its lines are in 20c (and the build line); there are no new hash keys.

## Verified
- **homeOk drops the data keys before section 22:** `for (const k of HOME_META) delete o[k];`. The full merge without claude/dialogue still has the old short `LINE_META`.
  - Calls now offer choices there too. Mum's everyday call on day 4 gives `[["send","Tell me about home."],["send","I'm eating. I promise."]]`.
  - A recorded message gets its reply: Gran's message plays, `mailPlayable` goes from true to false after you answer, and her reply is queued (`["Gran", 7921]`).
  - The merge with claude/dialogue gives exactly the same results.
  - HOME_META also covers `odds`, `w` and `old`. The writers' home data uses none of them (grep: 0), so dropping them doesn't change anything.
- **Recorded messages with nothing to say back:** `onEnd(f)` marks the message done when you hear it to the end and there's no choice. I checked this by reading the code; my data always offered a choice, so this path didn't run in a probe.
- **Story favours:** both are now a plain 15-minute stop tagged `favour` at their work station, with no parts and no chore.
  - liftBrakes: `"Check the lift brakes with Zainab (Deck 5)"`, steps `[["favour","5-bench-1"],["return",""]]`.
  - pellPractice: the same shape.
- **Purity still holds:** I ran the queries and 200 `lineFor(..., { peek: true })` calls on a fresh game, with and without dialogue. `SHIP.social.stories` and `socSave()` were unchanged (`storiesSame: true, saveSame: true`).

## Tests
- `name_check.py --branches 3042c7c c689063`: NAMES OK (0 new names). name_check on the full merge and on the dialogue merge: OK.
- social_check (c689063's copy):
  - Tip: OK. Save 15127 bytes; same twice and jump both True.
  - Full merge (reserve in): save 22201 bytes out of 30000, same twice True, purity True, and the only FAIL is the jump test. As reported in social-stories-3042c7c.md, that comes from the other tips (one `repair.recycler` cue differs) and also fails with social B at 0.39.6.
- Browser probes p7/p8 on both builds (`?nosave&debug`), with content's HOME_* baked in: no page errors.
