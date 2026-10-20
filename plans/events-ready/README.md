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
| diplomatic | veyliGreeting (replaces the game's; Veyli they/them), veyliDinner (new) | event.diplomatic.warning / .escalation / .afterglow | event-diplomatic (the memo, the warning, news, status, the greeting line, the dinner's Mail, the farewell) |

**Tested** (a scratch copy with everything moved in, baked, then lines_check):
- The bake is fine.
- lines_check's only errors are length limits: every `event.*` bank key is held to 90 characters, so the Mail bodies (up to about 320) and the toasts, keepsake and plaque texts (up to about 120) fail. Needed: a lines_check rule (the dialogue engineer's file) giving `event.*.mail.*` 400 characters, as `mail.*`, and `event.*.gather.*.thanks|mail`, `event.*.trad.*.mail|thanks`, `event.*.keepsake` and `event.*.plaque` 200, as a tradition's Mail and toast. Everything else passes.

**For EV1's code:**
- The all-clear's line to you is inserted after Calder's "Mine too" line, from `event.ionStorm.allclear.you.commended | .jobs | .none`.
- The `.meet` reader has no `thread:` key: the courtesy-thread replies are noted in veyliGreeting and veyliDinner.
- The ceremony's stand-ins are `first1` and `first2` (crew on their first crossing), like `tech1` and `tech2`.
- Placeholders: `{me}` (not `{you}`: lines_check knows `{me}`), `{dark}`, `{band}`.

The older plain drafts in `content/events/*.draft` are superseded by these files and kept for the record.
