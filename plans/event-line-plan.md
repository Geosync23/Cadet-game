# Crossing the Line: the event plan (version 2, ER2's 12 fixes and the story reworked)

Event planner EP2 (session_01GpiqZ9jCYbS9XTNPF8adHr), 2026-10-21. Branch `claude/event-plan-line`, from claude/integration 0.64.6 (675588c). Reports to lead 22 (session_01BGQCZLK6gYTnqu6mwZ61jB). **Planning only: the game is unchanged.**

- **The full page:** `plans/event-line-plan.html` (with the answer form).
- **The review:** ER2, claude/event-plan-review-2 5a76136, `plans/event-line-plan-review.md`: PASS WITH FIXES (12 fixes; the story to follow). How each fix was taken is listed at the end.
- **What it builds on:**
  - the events plan v3.2 (claude/events-plan, section 3);
  - EV1's events base (claude/events-base a2d9f40: F0a, F1a-c and F2 built, switched off; F2b, approved: crew react to an event moment within about 5 ship minutes);
  - EW1's lines (claude/events-lines, `plans/events-ready/crossingLine/`; the cake comment fixed in 67b28ad).
- **Order:** the events base, then the ion storm, then this. Crossing the Line comes first in the story (Day 7) but is built second.

## In short
- **Sunday Day 7**, your second day off (Saturday stays free). The Wren crosses into the Veyli reach. One day, no score, nothing breaks.
- **14:30:** a gold pulse runs through every light (the horn: the game has no sound), the hull lights turn gold until the supper ends, and the Captain gives a short banner address. She's called in on her day off and says so.
- **14:30-15:15, the plaza:** about 50-60 crew, because the day shift stands easy for the ceremony (except the bridge, the watch and the galley line). The first-timers stand at the front, you among them. The Captain reads the old oath, you answer it for the first-timers, and your words go on Monday's plaque. Then everyone drinks Brennan's green Line punch.
- **The story:** Tomas, your bunkmate and the other newest hand, is on watch through the whole crossing and misses his own Line. You can carry him a mug, and the crew give him his crossing on Lap of the Wren that night.
- **18:00-19:15, the mess:** the Line supper. It's the Sunday table re-dressed: the crew's voted dish, plus Brennan's pudding. Up to about 60 (44 seats and 22 standing spots, already built).
- **Monday Day 8:** the plaque with your words, your certificate on your shelf, and the crew retelling it (Zeke's worst face included).
- **About 6 build turns**, behind a new switch `EV_LINE_ON` (off = today's game), after the storm update.

## The story
Each option has a beginning, a middle where your one choice matters, and a payoff. All three use crew already aboard, and none touches an arc's later beats.

### Option A (recommended): "The one on watch"
Built from the game's own rota (ER2's find): Tomas Lind, your bunkmate in Bunk 1, is the newest hand after you. He's on watch in Deck 2's watch room from 08:51 to 17:00 on Sunday, so he'll miss his own crossing. Someone has to watch the ship as she crosses.

- **Beginning, Saturday evening (Day 6), wherever Tomas is.** His Saturday runs the mess and the garden 19:14-22:05, climbing on the rec deck 22:08-22:40, then bed at 22:46 (ER2's S1). His plans don't move: the moment follows him from 19:00 until bed (it opens when you're near him), or at the latest at his bedtime in Bunk 1 (about 22:45). He can't settle: "I'm on watch tomorrow. All day. My first Line, and I'll be watching a corridor screen." One moment, three replies:
  - "I'll bring you some punch." (practical; sets `line.promised`)
  - "I'll tell you every bit of it." (cheer)
  - "Can't you swap?" (He: "Not on a crossing. Someone has to watch her cross.")

  If you haven't met him by the time he's in bed, he sends you a short Mail at about 22:50 instead ("On watch tomorrow. You'll have to cross for both of us."), so the thread still starts.
- **Middle, Sunday 14:40, the plaza.** After the oath the Captain asks, "Who answers for the first-timers?" Two first-timers look at you. Your one choice is the answer, and it goes on the plaque:
  - "We came a long way. We're glad we did." (proud)
  - "We crossed together, all of us, even the ones on watch." (for Tomas and the watch)
  - "Is this the part with the punch?" (the joke: the crowd laughs; the Captain: "It is. I'm so sorry.")

  Then Brennan's punch. Carrying it up before 14:30 (the volunteer job), Brennan tells you one of its ingredients and swears you to secrecy.
- **After the ceremony (15:15-17:00), optional.** Take a mug of punch up to the watch room (the punch job's second stop; never scored). Tomas: "You brought it up. Nobody brings things to the watch room." If you promised on Saturday and don't go, nothing bad happens: Brennan saves him one.
- **Payoff, Lap of the Wren, Sunday 20:30.** Tomas is off shift and walks at the front. Halfway round, the old hands stop at the plaza and give him the oath's last line: "From today, this reach knows your name, Lind." (Zeke says it; Pell hands him the last of the punch.) What Tomas says to you depends on your day:
  - you named the watch: "You said 'the ones on watch'. Deck 2 heard about it in five minutes.";
  - you brought the mug: he raises it;
  - you did neither: "Next Line, you're on watch and I'm drinking the punch."
- **Monday.** The plaque carries your answer under the date, and the crew quote it back. At One week aboard (17:15 on Sunday) Zeke owns up to pulling the worst face at his own first Line, which is where Monday's "who pulled the worst face" chatter comes from. At the supper someone guesses what's in the punch: you can keep Brennan's secret or not (a reply, Brennan +1 if kept).
- **If you miss the ceremony,** a first-timer answers with the plain line ("We're new, and we're nervous, and we came anyway."), and that goes on the plaque. You can still take Tomas his mug and walk the Lap.
- **No spoilers** (EW1's guard rails, 01:07):
  - Tomas's lines are only about missing the ceremony. Nothing about failing, tests or Holt (his arc's beat 5), and nothing about staying (beat 7). He never says or reacts to "stay".
  - Holt has one warning reaction line ("Veyli reach. Hm. Keep your wits."), never a scene; his arc's beat 4 is untouched.
  - Nothing about a delegation, guests or the Envoy's purpose.
- **What it needs** (about one turn more than a plain ceremony):
  - the Saturday moment that follows Tomas from 19:00 to bed (section 20c's moments, like `moment:quiz`: the social seat), never moving his plans;
  - the oath meeting's choice reworked (EW1), setting `line.answer`;
  - the plaque reading `flag('line.answer')` (the deck architect's dress kit: it reads a saved flag, never the planner);
  - the watch room as the punch job's second stop;
  - Lap of the Wren on Day 7 re-dressed (Tomas at the front, the plaza stop: a short 20c moment when you're walking it);
  - Tomas's lines;
  - Zeke's worst-face line at One week aboard;
  - the punch-secret reply at the supper.

  About 30-35 lines from EW1.

### Option B: "What's in the punch?"
- **Beginning, Sunday morning.** Carrying the punch up, Brennan tells you one ingredient and swears you to secrecy.
- **Middle.** All afternoon the crew try to get it out of you. At the supper you choose: keep the secret, tell everyone, or make up something worse.
- **Payoff, Monday.** The crew's guesses go round, and Brennan's card stays locked in the galley (or the truth is out).
- **Weaker:** funny, but only Brennan's story, and the oath isn't part of it. (In A it's a small side thread.)

### Option C: "The Line roll"
- **Beginning, Saturday.** Commander Vance asks you to bring the Wren's Line roll up from stores; every first-timer since she launched has signed it.
- **Middle.** At the ceremony each first-timer signs it, and you choose the line beside your name.
- **Payoff, Monday.** The roll hangs by the plaque.
- **Weaker:** quiet, and nobody else's story is in it.

**Recommended: A.** It's true to the ship's own rota. It gives a friend something he wants and can't have (he's watching the ship while it crosses). Your answer goes on the plaque in front of everyone. It pays off the same evening on a walk you may already take, and it still works if you miss the ceremony.

**It changes something you agreed earlier:** the events plan v3.2 had "one reply to choose (proud, nervous, joking)". A keeps a proud and a joking answer, swaps "nervous" for "even the ones on watch", and puts your answer on the plaque. Question line-q9 says so.

## Reactions after the horn (lead 22: EV1's F2b, approved)
Crew react to an event moment **within about 5 ship minutes**, so `cue:event.crossingLine.onset` lines start a few minutes after 14:30, before the ceremony. The onset file holds lines for 14:30-15:15 (the gold pulse, the gold windows, the walk to the plaza: "Did you feel that? The whole deck went gold."). After-the-ceremony lines ("How was the punch?", "A week aboard and a Line crossed", quoting the answer) move to a new `event.crossingLine.resolution` file (from 15:15). The warning lines run from Saturday 18:00 (EW1 fixes the comment that says "from the Friday new-hand's tea").

## Checked in the game (0.64.6 and the events base a2d9f40; numbers ER2's, from a new game)
- **Aboard on Day 7:** 76 people: 74 crew, plus Envoy Saruth and Ulla Jaramillo (the touring musician, Days 5-9). 45 work that day and 31 are off.
- **At 14:30:** 25 crew are at work, about 26 at leisure, 4 asleep (the night shift) and 3 at Winner Stays On. With only off-duty crew coming, the ceremony would get about 35-45. With the day shift standing easy (question 7), about 50-60.
- **Day 7's traditions:** the swap meet 10:30-12:30 (promenade and plaza); the rec deck's slow stretch 08:00 and Winner Stays On 11:30-16:30; the reading corner 16:00-17:00 and One week aboard 17:15-17:55 (both in the bow lounge); the Sunday long table 18:00-19:00 (±10 minutes) in the mess; Lap of the Wren 20:30-21:15. Day 8 has a birthday at 20:15.
- **Rotas on Day 7:** the Captain, Calder, Sato and Holt are off. Vance, Brennan, Lukas Dlamini, Zeke and Tomas work. Tomas is on watch 08:51-17:00 in Deck 2's watch room.
- **First-timers by the roster's `since`:** one person aboard under two weeks (Tomas), four under six months (Teague, Rossi, Eklund, Quist), 21 under two years (8 of them off at 14:30: Rina, Cruz, Bakshi, Silva, Teague, Quist, Lemaire, Abara). Guests are never counted.
- **Sunday dinner is the crew's vote:** `galleyMenu(7)` is fish and chips (19 votes), herb flatbread on the side.
- **Saruth** is at the Sunday table (18:16-18:59), at Winner Stays On from 15:01, and in the `everyone` pool for any gathering.
- **Places:** the plaza venue has one lead spot (east of the lift, facing down the promenade) and 71 standing spots. The mess has 44 seats, 22 standing spots and one lead, and it spills onto the plaza.
- **No sound** anywhere. `FEEL_MOODS` holds only the storm. The hull-lights evening changes nothing on screen.
- **Draw calls** (ER2, 390x844, Deck 3, Day 7 at 14:45 and 18:35, 73 crew on the deck): 240-256, against a budget of 450.
- **The base:** `EV_CALENDAR` has `{ id: 'crossingLine', day: 6, kind: 'short' }`, passed over until `SHIP_EVENTS.crossingLine` exists. With `day: 6`, `onset [1, 870]` is Sunday 14:30, and `eventDay(7)` is true. Hash keys 352-354 are free today.

## The day, minute by minute (Day 0 of the event = Saturday Day 6)
| When | What | Where | The piece |
| --- | --- | --- | --- |
| Fri 5, 16:00 | The Captain's first weekly address mentions Sunday's crossing | rec deck auditorium | Fridays plan, `friday-d5.address` (needs `SHORT_FRIDAY`) |
| Sat 6, 18:00 | **Warning** begins: Vance's Mail "Tomorrow we cross the Line"; crew ask "First crossing?" (Pell: he crossed two years ago; Holt's one line) | Mail, every deck | F2 phase note, cue `event.crossingLine.warning` |
| Sat 6, 19:00-22:46 | Story A begins: Tomas, on watch tomorrow (a moment wherever he is: the mess, the garden, the rec deck, or Bunk 1 at bedtime; else his Mail at about 22:50) | Deck 3, rec deck, Deck 4 | 20c moment |
| Sun 7, 10:30-12:30 | The swap meet, as usual | promenade, plaza | (unchanged) |
| 12:45-14:15 | Two small volunteer jobs on the mess sign-up sheet (Brennan offers them too): carry the punch up from the galley; hang gold ribbons on the plaza | galley, plaza | event `jobs` (17), `DECK_DRESS.signupMess` |
| 14:15 | Device notice: the ceremony on the plaza at 14:30, with "show on map" | device | F3a |
| **14:30** | **Onset.** The horn (a soft gold pulse through every light; crew stop and look up), the gold hull lights, the Captain's banner (3 lines; she's called in) | every deck | moment `horn`, `address.onset`, F0b called in |
| 14:30-15:15 | The day shift stands easy (not the bridge, the watch or the galley line) | every deck | routine `standEasy` (14) |
| 14:30-14:40 | The crowd gathers: the Captain, Brennan with the punch bowl, the first-timers nearest; Saruth stays away by courtesy | plaza | gathering `lineCeremony` (k 353) |
| 14:40-14:55 | **The oath** (meeting `crossingCeremony`): the Captain reads it, asks who answers for the first-timers; your answer (story A) | plaza | meeting, cast `marrow`, `brennan`, `first:2` |
| 14:55-15:15 | The "dunking": a mug of Line punch each | plaza | gathering anim `drink` (with `MUG_ON`) |
| 15:15 | **Resolution** begins: Brennan's supper Mail; your certificate is on your shelf | Mail, your cabin | `mail.resolution`, trace `lineCertificate` |
| 15:15-17:00 | Optional: a mug of punch to Tomas in the watch room | Deck 2 | the punch job's second stop |
| 16:00-17:00 | The reading corner, as usual | bow lounge | (unchanged) |
| 17:15-17:55 | One week aboard with Zeke, as built, plus two lines about your crossing and his worst face | bow lounge | reactions `event.crossingLine.resolution` |
| **18:00-19:15** | **The Line supper**: the Sunday table re-dressed; the voted dish and a pudding; up to about 60; Saruth at their usual Sunday seat; the punch-secret reply | mess (spills onto the plaza) | Sunday table on Day 7 |
| 19:15 | **Afterglow** begins: the gold fades back over a minute; the plaque goes up overnight | plaza | trace `linePlaque` |
| **20:30-21:15** | **Lap of the Wren**, Tomas at the front; the old hands give him the oath's last line at the plaza | promenade | Lap re-dressed on Day 7, 20c moment |
| Mon 8 | The afterglow: the plaque quoted back, the worst face retold; status line "First day in the Veyli reach"; the event ends at midnight | every deck | cue `event.crossingLine.afterglow` |

**The phases:** `warning [0, 1080]`, `onset [1, 870]`, `resolution [1, 915]`, `afterglow [1, 1155]` (clears), `days: 3`. `eventDay` is true on Day 7 only. No phase pauses a tradition.

## What you can do
- **Saturday night:** keep Tomas company; promise him punch.
- **Help** (optional, never scored): carry the punch up (and hear one of its secrets), hang the ribbons. Both are on the mess sign-up sheet.
- **Answer the oath** for the first-timers; your words go on the plaque.
- **Take Tomas a mug** in the watch room.
- **Eat** at the Line supper; keep Brennan's secret or don't.
- **Walk the Lap** at 20:30 and see Tomas get his crossing.
- **Miss any of it** and still be part of it: the gist by Mail, the certificate anyway, Brennan's saved mug at supper (question 6).
- **No commendation** from this event, even with both jobs done: `commend: false`.

## How the pieces work (ER2's fixes 3, 5-11)
- **The day shift stands easy (fix 3, question 7):** a new routine rule `standEasy` for one window, like the storm's `doubleShift` and `stayIn`.
  - In the event's `routines.onset`: `{ who: 'all', rule: 'standEasy', at: [870, 915], not: ['dept:command', 'dept:helm', 'dept:watch', 'galley-line'] }`.
  - Section 14 (the sim seat, PB) lets anyone at a post that can wait leave it for that window and join the gathering.
  - It's pure: from the event's data and the rota only. day_check Day 7 counts the crowd (bigevents_check's crowd cap of 66 holds).
- **Saruth and Ulla (fix 5):** the ceremony's `who` carries `not: ['saruth']`. One afterglow line says a Veyli doesn't watch another people's rite, and nothing more. Saruth keeps their usual Sunday table seat (the Veyli are they/them, facts.md) at the supper. Ulla goes like anyone off duty (she's in the crowd, not the front row). bigevents_check checks Saruth isn't on the plaza.
- **The re-dressed Sunday table (fix 6):**
  - **Where:** a row in section 18, `EV_DAY_DRESS`, made at load from `EV_CALENDAR` and the event's data only (never `eventNow`, `SHIP.event` or anything saved). `eventsOn(d)` reads it, so plans made on any day agree.
  - **What it changes on Day 7:** the name ("The Line supper"); the words (`event.crossingLine.gather.lineSupper.*`); the window, 18:00-19:15 with no jitter; the pull, which grows (who: everyone .85); and the Saturday 18:00 Mail, which is left out (Vance's covers it, and Brennan's comes at 15:15).
  - **What stays:** k 440, `ties.galley` (the voted meal, the seating, the tasting side) and `decor: longTables`. food_check Day 7 is the test.
  - The galley's `resolution` key adds the extra batch and the pudding (section 16, the galley owner's review).
  - **The same row re-dresses Lap of the Wren** on Day 7 (Tomas at the front, the plaza stop).
- **The dish (fix 4):** the crew's vote stands (fish and chips on a new game's Day 7). EW1 rewrites "a proper roast", "The roast's to get rid of the taste" and "ran out of roast" to fit any dish.
- **Spots for the cast (fix 7):** three lead spots added to `DECKS[3].gathers.plaza` (Brennan with the punch bowl, the two first-timer speakers beside the Captain), only when `EV_LINE_ON`, so Deck 3's places stay identical with it off. The deck architect's seat (4d).
- **The punch bowl (fix 8):** one prop at the front of the plaza, 14:30-15:15, 1-2 draw calls (performance seat, L3).
- **The mugs (fix 9):** "mugs out" uses the crowd's drink pose with patch E's mug, so `MUG_ON` is needed first.
- **The jobs (fix 10):** on the mess sign-up sheet (`DECK_DRESS.signupMess`, built for the storm) and offered by Brennan in the mess, not the Works bay board two decks down.
- **The first-timers (fix 2, question 5):** `lineFirst`, made at load from the roster's `since` (under two years), never `R()`, never saved, never a guest. The fact "the Wren was last in the reach two years ago" goes in `content/facts.md` (the head writer's). The cast slot `first:2` is two of them off shift that day, by hash.

## Hash keys (fix 11)
| k | What | Status |
| --- | --- | --- |
| 340 | the storm's all-clear party | built |
| 341 | dated one-offs (section 18) | built |
| 351 | the visit's farewell | built |
| 352 | the storm's lantern supper | reserved; the storm update confirms |
| 353 | the Line ceremony | reserved here |
| 354 | kept for this event (a second gathering if ever needed) | reserved here |
| 355 up | the comet's two windows | for the comet's plan |
| 440 | the Sunday table (re-dressed on Day 7, key unchanged) | built |

## The build turns (after the storm update; switch `EV_LINE_ON`)
Each turn follows the same steps:
- small exact edits;
- a build-table row under "Crossing the Line";
- the area's checks, then `bash check_fast.sh`;
- cadet_test with the switch off (ALL IDENTICAL);
- push, then report.

The build number is the build master's.

| Turn | What | Sections (owners) | Checks besides check_fast |
| --- | --- | --- | --- |
| L1 | The event's data: `SHIP_EVENTS.crossingLine` only when `EV_LINE_ON` (phases, address, Mails, news, status, `commend: false`, no threads); `lineFirst`; the cast slot `first:2`; the oath meeting with story A's choice (`line.answer`); the `EV_BEATS` row (the ceremony is the Captain's one scene that day); EW1's files moved into `content/` and baked; facts.md's line | 18 (traditions: EV1's seat), 22 generated (writers, through content_gen.py) | events_check, bigevents_check on paper, lines_check, social_check |
| L2 | The crowds: the ceremony gathering (k 353, `not: saruth`), `standEasy` (14), `EV_DAY_DRESS` for the Sunday table and the Lap, the galley's batch and pudding, the three lead spots. **Gated on F0b:** bigevents_check's cast part must show the Captain and Brennan planned on the plaza at 14:40 | 18, 14 (sim), 16 (galley), 4d (deck architect) | day_check Days 6-8 (on), food_check Day 7, events_check, bigevents_check crowds (draw calls at 390x844) |
| L3 | The look: gold hull lights (`FEEL_MOODS.crossingLine`); the horn (a new `horn` feel: one soft gold pulse, no shake; reduced motion: a soft dip); the ribbons (`DECK_DRESS.lineRibbons`); the punch bowl; the plaque (`linePlaque`, with the answer); the certificate (`lineCertificate`, which moves with you to cabin 4-23 on Day 10 like the Tiles trophy) | 8b (performance), 4d (deck architect), 18 | deck_check Decks 3-4, perf_check (the ceremony and the supper), screenshots at 390x844 and 360 wide |
| L4 | Story A's moments: Saturday evening with Tomas (wherever he is, until bed), the watch-room mug, the Lap moment, Tomas's and Zeke's lines, the punch secret | 20c (social), 18 | social_check, events_check, bigevents_check (live: a reload mid-oath; Tomas at his post 08:51-17:00 and on the Lap at 20:30) |
| L5 | Your part: the two jobs (sign-up sheet), the device's Schedule and status line (F3), the Record line ("Crossed the Line into the Veyli reach, Day 7", never a score), missing it (Brennan's mug) | 17 (systems: posting), 19 (device), 18 | player_check, device_check, interactions_check, devmode_check, intro_check `--week` alone |
| L6 | Switch it on (`EV_LINE_ON = EVENTS_ON`) after the user's review; the full round; design-doc (including "a short event may say `commend: false`") and DEV_NOTES | 18 | the full round (intro_check in pieces) |

**About 6 turns** (the events plan said 4-5; the story adds about one), then the adversarial build review, then the user's review.

**Needed first** (not this plan's to build):
- the storm update (the base is switched on with it);
- EV1's F0b (called in, and named people placed into an event's meetings: the gap EC1 found, being fixed with PB), F2b (reactions within about 5 ship minutes), F3 (device) and F4 (reloads);
- EC1's `bigevents_check.py`;
- patch E's `MUG_ON`;
- the Fridays plan's `SHORT_FRIDAY`, for Friday's mention.

**Draw calls:** 240-256 measured on Day 7 at phone size, against a budget of 450. The look adds about 4-5: the ribbons (1-2), the punch bowl (1-2) and the plaque (1). The certificate is on Deck 4 (1). The gold is a colour change with no new meshes.

## The lines it uses
- **EW1's, ready** (`plans/events-ready/crossingLine/`):
  - **the bank:** Vance's Mail, the three banner lines, status lines, the ceremony's tap lines, the Line supper, the certificate and the plaque;
  - **the oath meeting;**
  - **three reaction files;**
  - **the shared called-in lines.**
- **To rewrite (EW1, about 30-35 lines, once the user says go):**
  - the oath meeting's choice (the three answers above), and the plaque's texts (three, plus the missed-it one, each under about 100 characters);
  - Tomas's Saturday moment and his 22:30 Mail;
  - the watch-room lines;
  - the Lap moment (Zeke's last line, Pell's punch, Tomas's three replies);
  - Zeke's worst face;
  - the punch secret (Brennan, and the supper guess);
  - Holt's one warning line;
  - Saruth's one afterglow line;
  - the onset/resolution split;
  - the supper's dish words;
  - the warning file's comment.
- **New small lines:**
  - the horn's one-line notice;
  - two job titles;
  - Brennan's saved mug;
  - the device notice;
  - the Record line;
  - facts.md: "the Wren was last in the reach two years ago".
- **Lengths:** bubbles 60 characters, cards 90, meeting lines 140, the plaque about 100. lines_check still needs its length rule for event Mail, keepsake and plaque texts (EV1 or the dialogue engineer).

## Risks
1. **The base's gap:** today nobody is placed into an event's meeting. Until F0b fixes it, the Captain and Brennan wouldn't be on the plaza. L2 is gated on it.
2. **Off must stay identical:** the event, its gatherings, `EV_DAY_DRESS` rows and the lead spots go in only when `EV_LINE_ON`, so `EV_SHIPWIDE`, `eventsOn` and Deck 3's places come out byte-identical with it off.
3. **Standing easy** is a new routine rule in section 14's planner: the sim owner's review, and day_check's counts on Day 7 (nobody stuck, every shift's other hours kept).
4. **Re-dressing the Sunday table and the Lap** touches the galley's tie and a social tradition: food_check Day 7 and the owners' review.
5. **The first week:** Day 7 is still the arrival week (One week aboard, Zeke's invite). intro_check `--week`, run alone.
6. **The certificate must follow you** to the officer's cabin on Day 10.
7. **No score:** no threads, no band words, no debrief, `commend: false`, and a check for it.
8. **A gold that reads as "something wrong":** the storm turns the windows violet. The gold must look warm and festive. Screenshots at phone size.
9. **The ceremony ends at 15:15,** well before the reading corner (16:00).
10. **Reactions within about 5 ship minutes of the horn:** the onset lines must not mention the punch or the answer.
11. **Tomas's day must be as the plan says** (ER2's S2 and S4, in the new shape): at his post (`2-watch-6`) 08:51-17:00 and never pulled away, reachable for the mug, and on the Lap at 20:30 (`EV_DAY_DRESS` brings him); bigevents_check shows all three. Tomas's watch room is on Deck 2. The mug's stop must be reachable on a Sunday (the watch room's door), and Tomas must be at his post, not on his break, between 15:15 and 17:00: day_check Day 7.

## Questions for the user (each with a recommended answer; ids `line-q1` to `line-q9`, plus `line-general`)
- **line-q9, the story:** recommended: A, "The one on watch" (Tomas misses his own crossing; your answer goes on the plaque; his crossing on the Lap that night). Others: B, "What's in the punch?"; C, "The Line roll". A changes v3.2's "one reply (proud, nervous, joking)".
1. **When does the ship start talking about it?** Recommended: with Vance's Mail on Saturday at 18:00 (and the Captain's mention at Friday's address). Others: Saturday morning (talk only, so your free day stays free); Friday's new-hands tea.
2. **What do the gold hull lights look like?** Recommended: a warm gold in every window and slightly warmer light indoors, 14:30-19:15. Others: windows only; also gold light strips along the promenade (a few more draw calls).
3. **The horn (the game has no sound):** Recommended: a felt moment: one soft gold pulse of the lights, crew stop and look up, a one-line notice. Others: also add the game's first sound, one horn note (sound is new work: a mute switch, phones on silent); the banner only.
4. **The Line supper:** Recommended: the Sunday table re-dressed for the day: the crew's voted dish plus Brennan's pudding, renamed, 18:00-19:15, up to about 60. Other: a set Line dinner in place of the vote (the galley owner's change: the menu board and the vote note).
5. **Who are the first-timers at the front? (redone with the true numbers)** Recommended: everyone aboard under two years, with the written fact "the Wren was last in the reach two years ago" (21 crew; about 8 off at 14:30, more with question 7's yes). Others: under six months (4 crew, 2 of them there); only you.
6. **If you miss the ceremony:** Recommended: you still crossed (the gist by Mail, the certificate anyway; a first-timer's plain line goes on the plaque), and Brennan saves you a mug at supper. Others: the gist and the certificate only; the certificate only if you were there.
7. **Does the day shift step out for the ceremony? (replaces the Winner Stays On question)** Recommended: yes, 14:30-15:15, everyone at a post that can wait stands easy, except the bridge, the watch and the galley line (about 50-60). Other: only off-duty crew come (about 35-45).
8. **Something to do beforehand:** Recommended: two small volunteer jobs on Sunday 12:45-14:15 on the mess sign-up sheet (carry the punch, hang the ribbons), never scored. Other: none, just turn up.

## Judgement calls made (tell me if any is wrong)
- No phase pauses any tradition. Two are re-dressed for the day (the Sunday table, Lap of the Wren). Winner Stays On is left alone (it holds 3 crew at 14:30).
- The plaque goes on the plaza wall beside the lift; the certificate on your shelf.
- The ceremony counts as the Captain's one scene on Day 7 (`EV_BEATS` row, kind 'captain'). She isn't on the Lap.
- No Veyli at the ceremony (Saruth stays away by courtesy) and nothing of the visit.
- Pell is no first-timer: he crossed two years ago, and says so.

## ER2's 12 fixes, as taken
1. **The facts:** corrected (76 aboard, 45/31, 25 at work at 14:30, first-timers). Risk 4 now names the day shift.
2. **Question 5:** redone; under two years recommended, guests never counted.
3. **Question 7:** replaced by standing easy (recommended yes). The Winner Stays On edit is dropped (no rec owner needed).
4. **The dish:** the vote stands; EW1 rewrites three lines; the cake comment was already fixed (67b28ad).
5. **Saruth and Ulla:** said what they do; `not: ['saruth']`, checked.
6. **The re-dress:** `EV_DAY_DRESS` named, pure, with what changes and what stays.
7. **The cast's spots:** three lead spots behind the switch (4d).
8. **The punch bowl:** in L3.
9. **`MUG_ON`:** added to "Needed first".
10. **The jobs:** on the mess sign-up sheet, and Brennan offers them.
11. **Hash keys:** the table above.
12. **Small things:** the warning comment (EW1); `SHORT_FRIDAY` in "Needed first"; L6's design-doc note on `commend: false`. L2 is gated on F0b.
- **ER2's story fixes S1-S4 (round 1b, on 1.1):** S1 the Saturday moment follows Tomas until his bedtime (the Mail at about 22:50); S2, S3 and the watch:1 slot no longer apply (Tomas stays at his post in v2, and "eighty people" is gone); S4 becomes bigevents_check showing Tomas at his post through the ceremony and on the Lap at 20:30.
