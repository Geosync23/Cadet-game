# Traditions: seasons, the year and life moments (design note)

Seat 17, the seasons designer, `claude/trad-seasons`. For the traditions engineer (who merges these files and builds what needs code), and through them the galley engineer, the deck architect, the sim engineer and social. The files are `content/traditions/<id>.trad` (the format: `plans/trad-format.md`). Hash keys: 434 (Sowing, the sample) and 475-499 (this seat's block); used so far 475-484.

Tone throughout: light and cozy; a few warm lines; nothing sad for long (the user: gentle grief is fine, nobody dies on screen). No #serious lines here: lines_check only allows those behind a friendship condition, and tradition tap lines have none.

## What's in, and what changed from the plan's list

| Tradition | id, k | When (first year) | Where, time | Change from the plan, and why |
| --- | --- | --- | --- | --- |
| Sowing morning | `sowing` 434 | first Saturday of each season (6, 97, 188, 279) | garden, 11:45-12:40 | Kept. The Mail no longer says "after the harvest": harvest morning is only on 6 and 188. Tove Cruz (senior gardener) hosts; Tomas invites you (your first weekend). |
| First-fruit supper | `first-fruits` 475 | Greening week 7, Monday (134) | mess, dinner 18:15-19:05 | **Made lighter:** an ordinary dinner with a bowl of the first crop on every table, so the galley cooks its normal dinner plus one dish. Six weeks after Greening's Sowing morning. Monday, so it never meets the weekend's traditions; ends before running club. |
| Harvest supper | `harvest-supper` 476 | Harvest week 7, Sunday (231) | mess, 18:00-19:30 | Kept. The day after a harvest morning (230). Long tables, all from the garden, a pie (cake: yes), and a vote for the best of the harvest (tally). **Replaces the Sunday roast that week** if the weekly designer builds one (same deck and time; the rarer wins). |
| Lantern walk | `lantern-walk` 477 | Lanterns week 7, Monday (316) | promenade, 20:30-21:20 | Kept, once a season, not weekly (the draw-call risk). Holt's Watch dims the promenade lights; crew walk with paper lanterns and hang them on the rail. Monday: after running club, so two that evening, never at once. |
| Midtour | `midtour` 478 | year day 182 (a Sunday) | bow lounge, 20:00-21:00 | Kept. Oduya (the counsellor) hosts and keeps the letters. Takes the weekly letters evening's place that Sunday if it's built (letter-writing either way). |
| Year's end | `years-end` 479 | year day 364 (a Sunday) | bow lounge, 20:00-21:15 | Kept. The Captain reads from the log; the Midtour letters come back. prio 3, like Founding Day. |
| New hand's tea | `new-hands-tea` 480 | your first Friday (5) | Works tea corner, 18:40-19:30 | **Merged with Works Friday tea:** that Friday the weekly tea becomes yours (same deck and time; the rarer wins). Calder hangs your mug on the rack. |
| One week aboard | `one-week-aboard` 481 | your first Sunday (7) | bow lounge, 15:30-16:15 | Calder's Mail, plus a tea with Zeke Torres and Pell. **Afternoon**, so it doesn't count towards an evening's two. |
| Four weeks aboard | `four-weeks-aboard` 482 | your fourth Friday (26) | Works tea corner, 18:40-19:30 | **Merged with Works Friday tea** (it replaces it that Friday): the Works team's cake. On day 26 (the 4th Friday), not day 28, so it can be at Friday tea. |
| Farewell supper | `farewell-supper` 483 | the evening before a rotation day | mess, 18:00-19:20 | **Draft** (`farewell-supper.trad-draft`, not baked): needs a rotation rhythm (below). |
| New hand's tea, for new crew | `crew-welcome-tea` 484 | the first Friday after a rotation day | mess, 18:40-19:30 | **Draft** (`crew-welcome-tea.trad-draft`): the plan's "newcomers get their own new hand's tea". Needs the same rhythm. |

Not added: anything else for the seasons. Each season already has Sowing morning; Greening, Harvest and Lanterns each get one more. Sowing has none, since it has Founding Day (100, just after it ends). Founding Day and the quiet watch stay hand-written in section 18 (the engineer's).

## Asks of the traditions engineer (code or checks)

1. **A rotation rhythm** for the two drafts: `when: rotation -1` (the day before each rotation day) and `when: rotation friday` (the first Friday after one), read from the sim engineer's / crew designer's rotation calendar. The honorees are that rotation's leavers (`-1`) or arrivals (`friday`), so `{names}` and `{first}` fill like a birthday's. New `who` words: `friends-of-honoree` (affinity 40+ with any honoree, like `friends-of-host`), `dept-of-honoree`, `bunk-of-honoree` (the birthday's own department and bunkmate rules). When it's in, I rename the drafts to `.trad` and check them. (Checked now with a stand-in rhythm: both parse.)
2. **`events_check.py`'s walk-sim of works-tea on day 5** now fails ("works-tea not on day 5"): new hand's tea replaces it on day 5 by design. Swap that sim to `new-hands-tea` on day 5 (or `works-tea` on day 12). Same on day 26 (four weeks aboard).
3. **Midtour and Year's end letters:** joining Midtour sets a flag (your letter written, and the day); at Year's end the player gets a Mail "A letter from you" (from Matthias Oduya), whether or not you go. The letter is one of a few seeded templates that name what was true at Midtour (your Works reputation band, a friend's name, the season). The writers can write the templates; you say where they go. If you never went to Midtour, no letter: Oduya's Mail just says "Next year, then."
4. **The tally** for the harvest supper: `harvest-best`, choices tomatoes, beans, squash, herbs, kept for a week. The winner could be planted more next season (a nice-to-have for the galley engineer's garden; the result as news is enough).
5. **Meals:** the meal traditions use `ties: galley meal=dinner ...` (the parser has no `meal:` key yet). Per your agreement with the sim engineer, put `meal: 'dinner'` on the eventPlan entry from `ties.galley.meal`, or add a `meal:` key to the grammar and I'll switch to it.
6. **The voice budget:** please check the year's evenings once the weekly and monthly designers' files are in. Mine are picked to fit: Monday evenings (with running club), Sunday evenings where they take the place of a weekly one, Friday teas they replace, and an afternoon. The farewell supper (Saturday dinner) would be a third Saturday evening tradition next to film night and observatory night. I'd count a meal tradition for friends only, with no Mail to everyone, as outside the budget; your call.
7. **Words for lines_check** (the dialogue engineer's SHIP_WORDS): `Midtour` and `Year` (as in "Year's end") are flagged as unknown names (warnings only).
8. **`trace:`** (on `claude/ship-events`, not yet in 0.60.0): when it's merged, the new hand's tea could take `trace: mugYours` (your mug stays on the rack after day 5), and Sowing keeps `seedlingYours`. I didn't add them, because the 0.60.0 parser rejects `trace:`.

## Asks of the galley engineer

- **First-fruit supper (day 134):** `dish=first-fruits`, a small bowl on each mess table at dinner (the first crop of Greening's beds). `ties: garden harvest` that day.
- **Harvest supper (day 231):** `dish=harvest-supper batch=60`, a dinner all from the garden, plus a pie after (`cake: yes`: a pie, not a cake, if that's easy to tell apart).
- **Four weeks aboard (day 26):** `cake: yes`, but the cake goes to the **Works tea corner (Deck 5)** at 18:40, not the mess. It's the only cake that isn't in the mess.
- **Farewell supper (draft):** `dish=favourite`: the leaver's favourite dish if the roster has one (`loves`), otherwise the Friday treat.
- **Year's end (day 364):** `cake: yes` after the reading.

## Asks of the deck architect (decor: at most 6 draw calls, only on its deck, only during its window)

| Decor id | Deck | What | Budget |
| --- | --- | --- | --- |
| `lanternWalk` | 3, promenade and lift plaza | paper lanterns on the promenade rail and a basket of them at the lift plaza, plus the dimmed hall lights. **The known risk:** one instanced mesh for the lantern bodies (with emissive colour through `col()`) and one for the hanging cords, about 30 lanterns: at most 3 draw calls. No real lights: the glow is the material. Places tagged `event: 'lantern-walk'` along the rail (standing, `talk`) come first. | ≤ 3 |
| `harvestTables` | 3, mess hall | the long-table look: table runners and a few produce baskets, merged into one mesh | ≤ 2 |
| `yearsEnd` | 3, bow lounge | a lectern for the Captain and a string of small lights on the windows, merged | ≤ 2 |
| `mugRack` | 5, Works tea corner | the mug rack's new mug (the plan already has the rack; this is your mug showing from day 5 on, so it's a lasting mark, really `trace:` when that's in) | ≤ 1 |
| `cake` | 5, Works tea corner | the existing `cake` prop, at the tea corner on day 26 | as now |

Nothing for Midtour or One week aboard (people at their seats are enough).

## Asks of the sim engineer

- **Meal traditions:** first-fruit supper (dinner, Monday), harvest supper (dinner, Sunday) and the farewell supper (dinner, Saturday): those going eat their dinner at the tradition's places instead of the servery queue, in the dinner window. The harvest supper's long tables mean nearly everyone off duty (70%) eats there.
- **Hosts:** Tove Cruz hosts Sowing and the two garden suppers; she's a gardener on day shift, off Saturday and Sunday in 0.60.0, so she's free for those. Holt (lantern walk) and Oduya (Midtour) must be free on a Monday or Sunday evening; the Captain on day 364.
- **One week aboard:** Zeke Torres and Pell at 15:30 on day 7. Both are free on Sundays in the plan's days off.
- **Rotation days:** the farewell supper needs the rotation calendar readable on paper (pure), so `evDue` can say "the day before a rotation day".

## Asks of social (A and B)

- **Invitations:** Tomas (Sowing, lantern walk), Imani O'Neill (first fruits), Brennan (harvest supper), Oduya (Midtour), Pell (one week aboard). Calder needs none for new hand's tea: it's yours, and her Mail says so.
- **The farewell supper** sits between social B's goodbye moment (a day or two before) and the shuttle-bay farewell (on the day). Its words assume you know the leaver, but they're fine if you don't.

## The texts

Every tradition has a Mail, 2-4 `ask`, 2-4 `here`, 1-2 `thanks` and 1-3 `chatter`. Placeholders: `{time}` and `{season}` only (plus `{names}`/`{first}` in the drafts). No crew pronouns: the roster doesn't record them, so lines use names or none. Lines that name the host are skipped when the host says them (section 18's rule), so each section has lines without names.

## How it was checked (before every push)

- `python3 plans/trad_parse.py`: 9 traditions OK.
- `python3 content_gen.py --check`: OUT OF DATE in the repo's own game file. That's expected, since this seat never touches the game. Baked into a scratch copy, it's up to date, and `lines_check.py` on that copy gives PASS (0 errors, 10 warnings: the names `Midtour` and `Year`).
- The drafts: parsed with a stand-in rhythm (`weekly saturday` / `weekly friday`) in a scratch folder.
- `events_check.py` on the scratch copy: see the latest report to the traditions engineer.
