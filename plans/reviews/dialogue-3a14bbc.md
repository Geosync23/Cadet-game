# Review: claude/dialogue 3a14bbc (0.43.12: overheard conversations played, the saved ring), reviewer 2

**Verdict: PASS WITH FIXES** (low-medium).
Fine:
- The voice budget holds: one conversation at a time; none while a bubble shows, within the chatter gap, or while a
  chat card, meeting or sleep is on; it stops and clears its bubbles when one opens or the pair parts; at most one
  #serious a day.
- Hash keys 752 and 753 are in range; save.lines is read defensively; section 20 gets one typeof-guarded hook line
  (please put it in the hook register).

1. **LOW-MEDIUM, New game:** SHIP.lines is never reset on New game (there's no `onSim('newGame')` here; Tiles and
   section 13 use that hook). The old game's ring entries for days <= today, and `serious` (if it's the same day
   number), carry into the new game. They're saved again with it, and they suppress conversations the new player has
   never heard. Add `onSim('newGame', () => { SHIP.lines = { ring: [], serious: 0 }; OVH = null; })`, typeof-guarded.
2. **LOW, cost on phones as the content grows:** once a ship minute (30% of minutes), every ordered pair of nearby crew
   (up to about 90 pairs with 10 people in range) calls overheardFor, and each call runs linesOk over all of CONVOS.
   With a few hundred conversations baked, a minute with no match is about 90 × 300 condition checks in one frame.
   Cap the pairs tried per minute (say 6, in the seeded order), or skip a pair whose departments or `pair:` sides can't
   match.
3. LOW: the conversation is marked heard before its first line plays, so one cut short by a chat card counts as heard
   for 7 days. That's acceptable; just noting it.

## Addendum: 4cbf62c (0.43.13, one-speaker lines for the call booths): PASS WITH ONE FIX
- **MEDIUM (it never fires as documented):** the game's activity in the booths is `callhome` (whereIs, PLACE_ANIM,
  the planner), but lines_check's act vocabulary has `call`, and LINE_ACTS has no `call` group. So a writer's
  `? act:call` passes lines_check and then never matches in game (`ctx.act` is 'callhome'), and `? act:callhome`
  fails lines_check. Add `call: ['callhome']` to LINE_ACTS (or rename the value), and test one end to end.
  (`place:booths` works: the alias maps to the Call-home booths room.)
- LOW: a one-speaker conversation with no condition plays for anyone standing alone near you, anywhere, as a
  monologue. lines_check should require a place:/act: condition on A-only conversations.
- Fine: callers aren't paired with the next booth; a solo conversation stops when its speaker leaves; the seeding
  with no b is stable.
