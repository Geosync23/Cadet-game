# Re-review: claude/arrival e7eb18d..58e8418 (0.42.5-0.42.9: the arrival evening in play, skip, the closing-in wait, the kit bag)

Reviewer 1, 2026-10-17. Section 21 plus one hook line in section 12 (`if (typeof introTick === 'function') introTick();`, typeof-guarded, in the hook register). name_check: OK against every branch (social A has renamed). intro_check: OK, with the three one-slow-step cases from my last review now missing nothing.

**Verdict: PASS.** Three low notes, none blocking.

## Checked in play (a smoke run)
- `?nosave&debug`: started the intro by hand (`introBegin()` on Deck 5 at Day 0 17:40, standing in for the sim's Day 0 start). The manifest form appears and the clock holds at Day 0 17:40. Signing as "Sam" sets the name, completes `manifest`, and the steps move on (`ramp`). The goal arrow points at "Zeke Torres". Standing on the ramp checkpoint completes `ramp` and `hello` and moves to `haulway`. No page errors over 500 frames.
- Skip now means no intro (`ended`), with every gate flag and the evening's points; it agrees with social A's `socIntroOn`.
- The d1-shadow / d1-lead notes come from section 17's turn-in of reserved slots 1 and 2, once each.

## Low notes
1. **The escort's "This way!" calls mostly never show on Day 0.** `INTRO_CALL[(now >> 1) % INTRO_CALL.length]`: every Day 0 minute is negative (17:40 is -380), so the index is negative two times in three, and `bubbleSay` returns early on the undefined text. `callAt` is still updated, so he goes quiet for another 15 seconds. Use `((now >> 1) % n + n) % n`.
2. **`setGoal` is called every frame while he leads**, each time making a new goal object (`{ ...g }`) and a new `cellAt` array. It's small, but it's per-frame allocation on phones. Call it only when the goal's tile changes.
3. **A meeting step reached while another dialogue is open never plays.** `introTick` skips it with `continue` and never comes back to it. Rare (two meetings on the evening, minutes apart), but then neither the scene nor its gist Mail happens. Queue it, or send its gist.

## Still waiting on the sim engineer (not this branch)
- `loadGame` rejects saves with `day < 1`, so the save made when you sign the manifest (Day 0) is thrown away on reload. Your reload case should move to a real `saveGame()` / `loadGame()` round trip once the Day 0 start lands.
