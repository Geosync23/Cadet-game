# Handover: social engineer 0607 (Talking, for 0.60.7)

Written by session_01Q6zXcCnBpTeJQrUP8qPKUP. Read CLAUDE.md, plans/brief-0607.md (on claude/lead-pillar1), plans/plan-0607.html
"Talking" (on claude/plan-0607), DEV_NOTES "Social life" > "Talking" and rows 0.36.82+, and content/keys-0607.md (claude/writer-0607).

## Role, branch and builds
- Branch `claude/social-0607`, from 0.60.6a (c8685cf). Builds 0.36.82+ (social A's series). Lead 10: session_014hkEBULoSV9EKZZSwMWyPd.
- 0.36.82 (80116c5): people stay while you talk, Say hello, Talk a while, the Roster's People I know tab.
- 0.36.83: got-to-go fix (plan times are ship minutes), social_check "Talking" part. 0.36.84: reviewer 0607's fixes (talks on visits, talkDay saved only today).
- 0.36.85-0.36.91: the sim seat's items, moved to me by lead 10 (claude/deck-0607 031c0e4 merged in): trays go with the meal (no tray
  return), morning() takes a gathering before breakfast, seat guards (crewArrive/lineCatchUp `spotTaken`/`arriveNear`, the last step
  in CrewAgent.update, `seatsBeside` counts a served diner's next seat), the named bartender (Ivo Madsen `rota.team 'bar'`, relief
  Tamsin Haddad `rota.relief 'bar'`; galleyRoles/galleyRota, `BARTENDER()`/`BAR_RELIEF()`), crew hobbies (`crewHobby`), the shower queue
  (section 14 `showerQueue`, DA4's 4-shower-queue-* places from deck 55fca8d, else section 10's `washDoorTiles`), `STAFF_ONLY` in
  introPlan. Lead 11 (session_01YKC3CGA9VS4b7wuqLbPT7V) runs the team now. Reviewer 0607: session_01BusfBzBamabWrCsrwQeABh; BM3:
  session_01WrXgDfR5dzwktKJfYwVwsV.

## What I own
- Section 20, the "staying while you talk, Say hello and Talk a while" block just above `chatTick` (constants `CHAT_STAY`, `TALK_*`,
  `socMustGo`, `talkGoCheck`, `talkStart/Next/Answer/End/Step/Meter`, `talkSuits`, `talkText`), the card's buttons in `chatShow`, the
  Say hello branch of `chatDo`, `chatClose`, `chatTick`. Save: rel index 17 `talkDay`.
- Section 19's roster app: `rosterTab` and the People I know view (small edits only).

## Shared formats and seams
- Section 15 (PE6 0.28.61): `leisureAdd(5, 'talk')` after a full talk; `needEffects().friendGain` (1.25 when leisure is high) on talk friendship.
- Bus: `simNote('talk', { id, mins })` after a full talk.
- Lines: the head writer's keys (content/keys-0607.md): hello, talk.start/sit, talk.<topic>.open/more/ask/ans.*, talk.filler/end/stop,
  talk.go.shift/bed/trad; texts talk.<topic>.reply.*, talk.button.*, talk.done.*, roster.*. Fallbacks in code until baked.
- schedU keys 668-670 used (social A range 644-671).

## How to test
- `social_check.py BUILD` (the Talking part), cadet_test against the previous build, device_check (roster), interactions_check.
- Live: open a card with `chatOpen(p)` near a crew agent, `chatDo('talk')`, step frames (50 frames = 1 ship minute at 30 fps).
- With real lines: bake claude/writer-0607's content/ (plus plans/trad_parse.py) into a scratch copy with content_gen.py.

## Gotchas
- `galleyPlan` returns the shared GALLEY_SHIFTS plan array: copy before adding to it.
- cadet_test differences from schedule changes: find the cause by reverting one change at a time in test copies (DEV_NOTES 0.36.90/0.36.91).
- Run at most two browser checks at once here; a third often fails with "game failed to start" (a load timeout).
- `planDay` segment times are absolute ship minutes; `eventPlan` times are minutes from midnight.
- Hearing news in a hello gives its own +REL_PTS.news (not a double count).
- A `//` comment inside a one-line JS string in a check swallows the rest of the line.

## Open
- Nothing blocking. The story arcs use relAdd directly in arc_check, so the smaller hello (+1, was +2) doesn't change it; in play a talk (+5) more than makes up.
