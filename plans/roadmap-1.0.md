# The road to 1.0 (the user, 2026-10-28, 8:1x PM ET)

| Version | What | Notes |
|---|---|---|
| 0.96.0 | Controller, the Diplomatic visit (+ pointers), sound update ON | LIVE 6:42 PM ET Oct 28 |
| 0.97.0 | Dev mode update (J0-J5) | full round running Oct 28 evening |
| 0.98.0 | Optimization pass: game speed on phones, plus fix the two long-standing check failures (career backlog 12, events FX24-2) (the user, 8:3x PM ET; an earlier "Both" was an accidental answer) | OP1 plan page first |
| 0.99.0 | Balance + the 26 backlog fixes (moved from the 1.0 patch) + the title screen (B) | from the balance report (https://claude.ai/artifact/R1NgKLKRoP2Gu5sfgmMumm) once the user answers it |
| 1.0 | One last big playtest patch: the user's own playthrough notes only | the user's own whole-game playthrough on a real phone (incl. the controller test) |

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

Backlog to 1.0 (the user's answers on BT1's page, Oct 28 ~9:40 PM ET; plans/backlog-1.0-final.md on claude/backlog-triage 68c806bf):
- 0.98: FX24-2 + FX12-1 + TQ1-1 (planner walk estimate), SD3-2 (music lookup 4x/s). Clash resolved by the user: earlier answers stand
  (FX24-2 fixed in 0.98; backlog 12 balanced in 0.99).
- 0.99: backlog 12; row 22 cookers (keep the rate, add a small bottom message saying why dinner is late); the two balance-list items.
- 1.0 patch (26): FX17-1, N6-1, PB1-1, TM-1, DV1-1/2/3, 15, CP5-1, 30, 31, JB1-1, FX3-1/2, FX10-1, FX8-1, FX21-1, RV18-C1/C2/D1, EV1-1,
  SD3-1, V-1 seated formal dinner (no Dev jump needed), V-2 vessel nod, RV23-2/3; + the title screen (B).
- Dropped: 28, BAL-1, BAL-2, EV1-2, 1, 5, 6, CP5-2, LD1-1, DM1-4, DM1-5, DM2-1. Everything in groups C/D left alone.

Update (the user, Oct 28 ~9:50 PM ET): "just go to .99; my playthrough notes will be 1.0". The 26 backlog fixes and the title screen
move into 0.99 (with the balance pass). 1.0 = the user's playthrough notes only. The clash re-asked: earlier answers stand
(FX24-2 + FX12-1 + TQ1-1 in 0.98; backlog 12 balanced in 0.99).

Balance answers (the user, on BAL1's report https://claude.ai/artifact/R1NgKLKRoP2Gu5sfgmMumm, Oct 28 ~10 PM ET), all in 0.99:
- f1 Engine Specialist cliff: OTHER: "promotion dynamic, not fixed, but give another chance to test much, much sooner"
  (missing Trusted by the Day 22 test must not mean an 8-10 day wait: a retest as soon as you reach Trusted).
- f1b late story beats: KEEP for now ("I need to play this through first, we may change later").
- f2 promotions follow the calendar: KEEP. -> backlog 12 (career_check "Relied on" before Day 5) becomes a check-expectation
  fix, not a game change (lead's reading; told the user).
- f3 missed shifts: KEEP.  f7 money: KEEP.  f8 ship meters: KEEP.  f9 traditions: KEEP.
- f4 food, f5 fitness, f6 leisure: TRY the report's ranges (measure, pick, show the user the numbers).
- f10: the user asked "is this the way it is now or the way you want it to be": it is how the game is now; no change proposed.
- The two design-doc balance-list items (board jobs' reputation, upkeep pace) close as KEEP with f2 and f8.
- f10 follow-up (the user, ~10:20 PM ET): leave finding 10 as it is EXCEPT social: "a little more pressure on it but not a lot"
  (social easy to keep up; a player who never talks is lonely almost always but the cost is tiny: energy drains 5% faster).
- The user: "You now have everything you need to bring this project to the edge of 1.0." -> drive 0.98 and 0.99 to done; 1.0 = the
  user's playthrough notes.
