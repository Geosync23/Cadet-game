# The road to 1.0 (the user, 2026-10-28, 8:1x PM ET)

| Version | What | Notes |
|---|---|---|
| 0.96.0 | Controller, the Diplomatic visit (+ pointers), sound update ON | LIVE 6:42 PM ET Oct 28 |
| 0.97.0 | Dev mode update (J0-J5) | full round running Oct 28 evening |
| 0.98.0 | Optimization pass: game speed on phones, plus fix the two long-standing check failures (career backlog 12, events FX24-2) (the user, 8:3x PM ET; an earlier "Both" was an accidental answer) | OP1 plan page first |
| 0.99.0 | Balance | from the balance report (https://claude.ai/artifact/R1NgKLKRoP2Gu5sfgmMumm) once the user answers it |
| 1.0 | One last big playtest patch + a title screen (the user, 8:4x PM ET) | the user's own whole-game playthrough on a real phone (incl. the controller test) |

After 1.0 there can still be patches, but this is the map to 1.0.
Each version: plan page first where it's new work, then build, review, full round, the user's OK, publish.
Small backlog items from Oct 28 (seated formal dinner, Veyli vessel nod, DM2-1 End and keep, SD3-1/2 sound tidy-ups,
EV1-1/2, DM1-5) are slotted into 0.98 (tidy/perf) or 1.0 (playtest patch) as they fit.

Decisions (the user, Oct 28 ~8:40 PM ET): no old-save compatibility work (nobody has played yet); switched-off pieces
(TRAY_TRAVELS, INTRO_ASK_ON, ZEKE_CABIN_MAIL, END_WAY_BACK) stay off; backlog sorted by BT1 into a list for the user
before any action; the user does the whole-game real-phone playthrough themself; a title screen for 1.0 (TS1 mockups).

Decisions (the user, Oct 28 ~9:20 PM ET):
- Design-doc open questions: close them all (lead's suggestions: Calder, night shift, fault diagnosis, engine watch closed as built;
  passed over = only delayed; character shaping = no; device colour = as built; the diplomacy game = not part of this game;
  the board jobs' reputation and the upkeep pace move to the 0.99 balance list).
- Title screen: option B, the crew terminal (DOM/CSS, the device's phosphor screen, menu as a list + loading bar). No Credits screen. A music track on the title (the user, ~9:25 PM ET).
- 0.98: any visual change from turns 3-4 shown to the user as a before/after picture first; only incredibly minor changes accepted.
  No 60 fps cap. No battery saver. Backlog 12 (career "Relied on" before Day 5) NOT fixed in 0.98: the user will balance it in 0.99
  (it stays known-old until then). FX24-2: yes, book walking time only for long walks to a tradition.

Title screen B build plan: plans/title-screen-plan.md on claude/title-screen-plan (TS1): new section 30 behind TITLE_ON
(+ mirrored TITLE_EARLY), never shown under webdriver/nosave/dev, ~2 working days + a sound seat for 2-3 music candidates.
Questions for the user before building (ask at the 1.0 patch): keep Saves on the menu? a "tap to log in" gate so music starts
before choosing (TS1: no)? "Back to title" in Settings later?
