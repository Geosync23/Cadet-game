# Light review: claude/fix-ghost-tap 0a3277d + 1eeda5d (perf 0.27.34 the ghost-tap guard; 0.27.35 utility spaces open to the player)

Reviewer 1c, 2026-10-17 (light, both small). **Verdict: PASS** (one low).

## 0.27.34, the ghost tap
- The capture listener swallows a click only when it's trusted (a real click, never a scripted one), its target isn't the deck canvas, and it comes within 350 ms of a deck tap's pointerup (`tapUpAt`, the event's own timestamp, the same clock as the click's).
- **No real tap is swallowed in practice:**
  - the deck's own click (target `cv`) passes;
  - keys and scripted clicks pass;
  - HUD and card taps that don't follow a deck tap pass;
  - only a second, separate click on a card or button within 350 ms of a deck tap would be eaten, faster than anyone taps on purpose.
  - A tap that went through the hold or drag paths never sets `tapUpAt`.

## 0.27.35, utility spaces for the player
- `hatchPassable`: the player now passes every service hatch, whatever its tier.
- **Crew access is unchanged:** for crew the tier check (`hatchTier(who) < e.tier` → no) and then `dept === 'works'` are exactly as before; only the player's case moved above the tier check. Other hatches (the spine ladder's) still aren't service hatches, so they're walls as before.
- **Job tiers are untouched:** the job-list tier still uses `PLAYER_TIER` (section 17's `tier = you ? PLAYER_TIER : hatchTier(forWho)`).
- Six room tap texts lost "Tier N access".

## Low
- Four tap texts still say "Tier N access": the Fan hall (F, "Tier 2 access. You can watch it through the window"), the Sensor array (A, "Tier 3 access"), Engine control (K, "Tier 3 access, once power work opens") and the spine ladder ("Tier 2 access", several decks).
- The spine ladder isn't a service hatch, so its text is still right.
- If F, A or K sit behind service hatches the player can now pass, reword those three as the other six were. If they're glass-only or sealed, they're fine as they are.
