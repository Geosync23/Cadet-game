# Skim: claude/social-fixes 7869109..9463960 (0.62.5, the 0.60.5b hotfix): calls home stay open, postbox removed

Reviewer 1e, 2026-10-17. A skim, as the lead asked (it ships ahead of this look). I read the code only and ran no browser checks.

## Verdict: PASS

**The cause is right.** `inMeeting(m)` is false with no `m.where`, so section 18's `meetingsTick` closed every 20c dialogue about one ship minute after it opened.

**The fix:**
- The booth picker and live calls get `HOME_WHERE` (Deck 3, `/^Call-home booths$/`). That matches the room's name in DECKS[3] ('Call-home booths') and the intro's `where` for the same room. Walking out ends the call, as the comment says.
- Recorded messages and moments get `hereWhere()`: any room on the deck you're on.

**The postbox:** the kit function and its `place(...)` are gone. No reference to `postbox` is left apart from the explaining comment. Its `IT(...)` tap text went with the place.

## LOW: a recorded message can still close when you're not in a room
`hereWhere()` uses `room: /./`. `inMeeting` needs `roomAt(player.here())` to name a room, and it reads that once a ship minute (under 2 real seconds).

- Recorded messages are played from Mail on the device, so they can start anywhere.
- So a message played while you stand, or walk, on a tile with no room closes by itself. Places that might have no room: a doorway, the lift lobby if it has no room letter. A message also closes if you take the lift.
- I didn't check which tiles have no room. If any reachable tile has none, a cheap fix is a `where` that `inMeeting` treats as "anywhere on this deck". For example, `{ deck, any: true }`, with `if (w.any) return deckDef.num === w.deck;` at the top of `inMeeting`.
- Moments start from "Sit with them" at a crew member's place, so they are nearly always in a room.
