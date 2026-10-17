# Quick look: section 18's two hooks (social B 31f8aea, traditions 504112e 0.34.27), reviewer 2

**Verdict: PASS** for the two lines; one LOW-MEDIUM side effect of moments reusing the meeting panel.
- `sc.onPick(k, c)` in dialogueStep runs after the `!c` check and before `c.reply` is queued, so social B's
  warmer-reply swap takes effect. `sc.onEnd(finished)` runs after `DIALOGUE = null`. The lines are identical on both
  branches, so they merge cleanly.
- onEnd deletes `MEETING_SCRIPTS['moment:<id>']` before `meetingGist(D.id)`. meetingGist returns early when the
  script is gone, so walking away from a moment sends no Mail and doesn't crash. Fine.
- LOW: onPick isn't in a try. If it throws, dialogueStep stops halfway and the panel stays on that choice. A
  `try { } catch` costs nothing here.
- **LOW-MEDIUM (scoring leak):** a moment goes through `dialogueShow`, which does `eventMine('meetings', 1)`; each
  reply also does `eventMine('choice:moment:<id>', ...)`. During a ship-wide event (moments are only blocked in the
  onset phase), "Sit with them" therefore counts as attending a meeting. Section 18's commendation is
  `jobs >= 1 && meetings >= 1`, so one job plus a chat with a friend earns the storm commendation. Fix: skip
  eventMine when `scriptId` starts with 'moment:' (section 18's line), or pass a flag from momentShow.
