# Events lines, ready to move in (EW1, for EV1)

Finished files in the formats EV1 and EW1 agreed (2026-10-20). Each event's folder mirrors where its files go:
`plans/events-ready/<event>/content/...` → `content/...`. They're kept outside `content/` on purpose (the lead's call):
`content_gen.py` reads every folder under `content/`, so moving them in changes the game file's baked blocks. EV1
moves an event's files in and runs `content_gen.py` in the turn that builds that event. Nothing here is in the game yet.

| Event | Meetings | Reactions | Bank (event texts) |
|---|---|---|---|
| ionStorm | calderStorm, calderStorm.officer (rank: officer and up), captainAllClear.smooth / .bumpy / .rough | event.ionStorm.warning / .escalation / .resolution; calledIn (shared: Days 7, 14, 27) | event-ionStorm (addresses, Mail, status, the lantern supper, the party, the all-clear's line to you, the commendation, Lap of the Wren on Day 15) |
| crossingLine | crossingCeremony (the oath) | event.crossingLine.warning / .onset / .afterglow | event-crossingLine (Vance's Mail, the banner, status, the ceremony's tap lines, the Line supper, the certificate and plaque) |
| comet | (none) | event.comet.onset / .afterglow | event-comet (Sato's Mail, news, status, both gatherings) |
| firstLightCocoa | firstLightCocoa (Raman's two lines: the Pale Shoals and Tavessa, the user's picks; facts.md has them) | | |
| diplomatic | veyliGreeting (replaces the game's; Veyli they/them), veyliDinner (new) | event.diplomatic.warning / .escalation / .afterglow | event-diplomatic (the memo, the warning, news, status, the greeting line, the dinner's Mail, the farewell) |

**Tested** (a scratch copy with everything moved in, baked, then lines_check): the bake is fine. The only lines_check errors were the 90-character limit on `event.*` keys, and EV1's rule fixes that (claude/events-base bb285a0): Mail (`event.<id>.mail.*`) 400; a gathering's `.mail` and `.thanks`, `.keepsake` and `.plaque.*` 200; the rest 90. Run lines_check again on the build that has EV1's rule.

**For EV1's code:**
- The all-clear's line to you is inserted after Calder's "Mine too" line, from `event.ionStorm.allclear.you.commended | .jobs | .none`.
- The `.meet` reader has no `thread:` key: the courtesy-thread replies are noted in veyliGreeting and veyliDinner.
- The ceremony's stand-ins are `first1` and `first2` (crew on their first crossing), like `tech1` and `tech2`.
- Placeholders: `{me}` (not `{you}`: lines_check knows `{me}`), `{dark}`, `{band}`.

The older plain drafts in `content/events/*.draft` are superseded by these files and kept for the record.
