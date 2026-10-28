# Handover: FX14 (rec deck sim bay; then the weekend traditions, 0.92.5 item 16)

**Role:** builder under lead 34 (session_019RdVfeRPRiJpHGjKujZZJA). Reviewer RV13 (session_016ioWtxM6NJRV4Ck3ADwozc), build master BM16 (session_01MB7n4yvCAeGyWN4WZCAGPh), publisher PUB1.

## Done: the sim bay (claude/rec-simbay 328f678a, RV13 PASS, with BM16 for 0.92.5)

Everything behind `SIM_BAY` (section 4e's Rec engineer slot; off = identical, `#simbay` previews). The full story is in DEV_NOTES "The sim bay" and the build table's "rec-simbay S1..S7b" rows; the plan with the user's answers is `plans/rec-simbay-plan.html` (https://claude.ai/artifact/Hmg44se58wGkZaGCMFyRWL); screenshots in `plans/simbay-shots/` (force-added: the repo ignores *.png). Switch-on later: `const SIM_BAY = true;`, then the full round.

## Next: the weekend traditions (branch claude/p925-weekend, from integration ba836359 = 0.92.4)

The user's YES (via lead 34, 2026-10-24) to eight from SW1's pitch (`plans/weekend-traditions-pitch.html` on claude/weekend-pitch 140d9109; artifact https://claude.ai/artifact/C43EjSi7MJXUq9jz6yx5Sn): Saturday run (07:00, every other week, Nandakumar, promenade), Garden picnic (13:00; on the garden's EXISTING benches, no new seats: the user's meal-seats rule), Every song (17:00, music room, Zeke and the five), Night owls' cocoa (22:30, bow lounge, Keane), Bread day (Sun 07:00, Brennan, galley), The big jigsaw (Sun 13:00-15:30, Vance, observation room Deck 1), Gerald clinic (Sun 14:30, every other week, Cruz, garden), The Sunday story (22:15, Holt, junior common room). NO to Mend-it morning (park it: keep it on record as cut, per the user's rule). Rules: birthdays at least an hour from any tradition (FX12 builds that scheduler rule on claude/p925-fx12, session_01DfkfrfvdT2bW2Q1Y7b2AA5: don't edit the same lines), never two in one room, Mail the evening before, decor where fitting, deck head counts, phones first. Words: SW1 (session_01Mjn7ezXqrDgXBrdCtddHHJ) writes them once the keys are named; CS1 reviews voice.

**State at handover (2026-10-24 ~21:30 UTC, FX14 at ~55% memory):** T1 and T2 are built and pushed (claude/p925-weekend 62e81432; build-table row "p925-weekend T1+T2"; not yet sent to RV13: send it). Six traditions as .trad files (saturday-run 458, every-song 459, night-owls-cocoa 463, sunday-story 464, gerald-clinic 465, garden-picnic 466) with stand-in words, their joins in `TRAD_JOIN` (section 18's Traditions engineer slot, `if (WEEKEND_ON)`), the switch in section 13 (`WEEKEND_ON`, `WEEKEND_TRADS`: add each new id there), the loader's one skip line. `EV_MAILBOX` raised to 80 for events_check. SW1 has the T1 key list and was asked for the Sunday story's first chapters and their key shape (not wired yet: the chapter should change week by week, e.g. `story.sunday.<n>` picked by the week number). Numbers: late evening ones are small (Night owls 1-4, Sunday story 1-4: most crew are in bed; raise the odds or accept, ask the lead); Every song is capped at the music room's 6 places (T5 could add standing spots). Not verified: the picnic join's hunger gain (join_check saw the join and its +12 social).
Gotchas found: a `.trad` `where:` extra needs a comma (`garden, ids ^3-garden-`); `3 pool @<event tag>` works for other traditions' tagged places (@lap-of-the-wren, @stretch-garden); `every 2 weeks sunday week 1` includes Day 0 (add `from day 1`); events_check, join_check and deck checks time out loading when three run at once here: run two at most.

The turn plan sent to lead 34 (behind one switch, WEEKEND_ON):
- T1 (medium): the five that need only a trad file and existing places: Every song, Night owls' cocoa, Sunday story, Saturday run (walks like the Lap of the Wren), Gerald clinic. Stand-in words; events_check per tradition.
- T2 (medium): Garden picnic, a meal tradition (a parcel from the servery, eaten on the garden's benches), ending before the 14:00 garden hour; food_check.
- T3 (medium): Bread day: kneading places at the galley counters, flour decor on Sundays only, Monday's "{me}'s loaf" card; food_check, day_check on a Sunday.
- T4 (medium, still picture): the big jigsaw on Deck 1 on Sundays only (Deck 1 pixel-identical on other days); 20 minutes counts as the puzzles hobby.
- T5 (small-medium): decor on the days, head counts, perf numbers.
- T6 (small): the birthday hour with FX12; records, design-doc, full checks.

## How the pieces work (what I learned)

- **Ship traditions** are `.trad` files in `content/traditions/` (rules and words: `@tradition id`, `k:` a unique hash key, `when:` `weekly sunday from day 1` and the like, `at:`, `min:`, `where: <deck> room <Room name>: <place type>`, `who:` with habits and odds, `host:`, `from:`, then `== mail`, `== ask`, `== here`, `== thanks`, `== chatter`), baked into the game by `python3 content_gen.py starship-cadet.html` (check_fast's first step runs it with `--check`). Look at `lap-of-the-wren.trad` for the walking kind. Used k values (2026-10-24): 320-331, 340-341, 351-353, 434-456, 460-462, 475-499 (457 is the sim night's, on claude/rec-simbay). Free: 458, 459, 463-474, 500+.
- **Rec deck traditions** are written in code instead (`REC_TRADS`, section 18, around "the rec deck's traditions"): `{ id, name, k, when, at, min, where: [{ deck, pool }], host, whereFor, who, anim, from, mail, ask, here, thanks }`, pushed into `SHIP_TRADITIONS`. `when` options are in `evDue` (weekday, `every: '2weeks'|'4weeks'` with `week`, rota, after arrival, quarter, year); `skip: d => ...`; `quiet: 'career'` silences the Mail nudge on the career's big days (`recBigDay`). The sim night (`SIM_NIGHT`, Traditions engineer slot) is a small example added behind a switch.
- **Planned days are cached**: after changing something the planner reads, clear `SCHED_DATA = null; SHIP_DAYS.clear(); EV_DAYS.clear()` (the Friday address does this at load).
- **The planner never reads live state**: machine state through the hour record at 22:00 the evening before (`recPlanShut`, `simPlanShut`).
- **Places** a tradition uses are ordinary places with a type; `where` pools are `'<deck>|<type>'`. A switch-guarded build pushes new places in a slot after the deck is defined.

## Testing tips

- Fresh container: `pip install playwright numpy pillow`, three r128 and acorn into /tmp/cadet-work (plans/testing-guide.md 2.0), `CADET_CHROME=/opt/pw-browsers/chromium`.
- Test a switch-on build on a copy: `sed 's/^const SIM_BAY = /const SIM_BAY = true || /'` (do the same for a new switch).
- interactions_check takes 25-40 minutes here. To run one part: exec the file's head (set `__file__` to interactions_check.py first, or it recurses) and the part's text, with `g = Game(pw, path)`.
- Stand-in crew pushed into `DECK_CREW` must leave in the same `evaluate` (the shuffle and update loops read real crew fields).
- perf_check measured while other checks run flags js times on every deck: rerun the flagged scenes alone (`PERF_SCENES=regexp`).
- `until grep ...; do sleep; done` loops: make sure the pattern matches the check's real last line (check_fast ends "QUICK CHECK OK").

## Open questions for the user

None from the sim bay. For the weekend: the Sunday story's chapters (a year of them) are a separate writing job; the jigsaw's picture filling in week by week (and saved) would be the large version; the Gerald as a shelf item you keep would be the medium version. Ask before building those.
