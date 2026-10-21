# Crossing the Line: the event plan (version 1.1, for review: the story added)

Event planner EP2 (session_01GpiqZ9jCYbS9XTNPF8adHr), 2026-10-21. Branch `claude/event-plan-line`, from claude/integration 0.64.6 (675588c). Reports to lead 21. **Planning only: the game is unchanged.**

- **The full page:** `plans/event-line-plan.html` (with the answer form).
- **What it builds on:** the events plan v3.2 (claude/events-plan, section 3), EV1's events base (claude/events-base a2d9f40: F0a, F1a-c, F2 built, switched off), and EW1's lines (claude/events-lines 307addc, `plans/events-ready/crossingLine/`).
- **Order:** the events base, then the ion storm, then this. Crossing the Line comes first in the story (Day 7) but is built second.

## In short
- **Sunday Day 7**, your second day off (Saturday stays free). The Wren crosses into the Veyli reach. One day, no score, nothing breaks.
- **14:30:** the ship's horn on every deck, the hull lights turn gold until the supper ends, and the Captain's short banner address (she's called in on her day off and says so).
- **14:30-15:15, the plaza:** about 50-60 crew. The first-timers stand at the front, you among them. The Captain reads the old oath, you choose one reply, then everyone drinks a mug of Brennan's green Line punch.
- **18:00-19:15, the mess:** the Line supper, in the Sunday table's place, up to about 60 (44 seats and 22 standing spots already built).
- **Monday Day 8:** your Line certificate on your shelf, a brass plaque on the plaza, and the crew retelling who pulled the worst face.
- **A small story runs through it** (the user, 00:55: "a really interesting little story for our first ship-wide events"): recommended, **"Who answers the oath"**, with Tomas, your bunkmate, who also came aboard a week ago. See "The story" below.
- **About 5-6 build turns**, behind a new switch `EV_LINE_ON` (off = today's game), after the storm update.

## The story (version 1.1, the user's ask relayed by lead 21 at 00:58)
Three options, each with a beginning, a middle where your one choice matters, and a payoff on Monday. All use crew already aboard, and none touches an arc's later beats.

### Option A (recommended): "Who answers the oath"
- **Beginning, Saturday night (Day 6).** The old hands have a wind-up for every crossing: "The newest hand answers the oath, in front of everyone. It's always a disaster." (Pell starts it; he's been aboard two years.) Tomas Lind, your bunkmate in Bunk 1, arrived the same week as you and believes every word. After his shift, in the bunk room, he can't settle: "Eighty people. I'll say something stupid. Or nothing." One moment, three replies: practise with him (practical), tell him he'll be fine (cheer), admit you're nervous too (share). If you're not in the bunk room by 22:30, he sends you a short message instead ("Can't sleep. Tomorrow. You?"), so the thread still starts.
- **Middle, Sunday 14:40, the plaza.** It turns out the wind-up is half true. After the oath the Captain asks, "Who answers for the first-timers?" Tomas is in the front row in his Watch uniform: he's on shift, keeping the plaza, and she's pulled him to the front ("Watch can spare you for ten minutes"). Your one choice decides who answers, and with what words:
  - "I'll answer." You say: "We came a long way. We'd like to stay."
  - Nudge Tomas: "Go on. You know what to say." He wobbles, then says: "We're new, and we're nervous, and we came anyway."
  - "We'll answer together." Both of you: "We'll look after each other. That's the whole oath, isn't it?"
  
  Then Brennan's punch, as written.
- **Payoff, Monday (Day 8).** The brass plaque on the plaza carries the words you chose under the date. The crew quote them back ("Nervous and came anyway. I liked that."). Tomas has a line for each ending: proud of you; amazed at himself ("I said it. Out loud. In front of the Captain."); or glad he wasn't alone. Your certificate is on your shelf.
- **If you miss the ceremony,** Tomas answers alone with his line, and on Monday he tells you how it went. It's his words on the plaque, so the story still ends well.
- **No spoilers:** Tomas's nerves here are only about speaking in front of everyone. Nothing about home, his exam or the transfer list (his arc beats 5-7 stay untouched and ungated). Pell's part is a single chatter line.
- **What it needs:**
  - a Saturday moment in Bunk 1 (section 20c's moments, like `moment:quiz`; the social seat);
  - the oath meeting with its choice reworked (EW1);
  - the plaque reading `flag('line.answer')` (the deck architect's dress kit; it reads a saved flag, never the planner);
  - Tomas's three Monday lines (`mem:line.answered`, `mem:line.tomas` and `mem:line.together`);
  - Tomas on the plaza at 14:30 although he's on shift (the meeting names him; Watch keeping the plaza is his post that hour).
  
  About one more turn than the plain ceremony.

### Option B: "The missing recipe"
- **Beginning, Sunday morning.** Brennan's Line punch recipe card is gone: Lukas tidied the galley on Saturday, and a box of old cards went to the swap meet.
- **Middle.** At the swap meet (10:30-12:30) you can find it on a stall, and choose:
  - give it back;
  - suggest a new recipe (the punch comes out a different green);
  - keep the secret and let Brennan improvise.
- **Payoff, Monday.** The card is framed beside the plaque, or Brennan's new recipe becomes "the Wren's own".
- **Weaker:** the story happens before the ceremony, and the oath isn't part of it. It also leans on the volunteer jobs.

### Option C: "The Line roll"
- **Beginning.** Vance keeps the Wren's Line roll: every first-timer since the ship launched has signed it. On Saturday he asks you to bring it up from stores.
- **Middle.** At the ceremony each first-timer signs it, and you choose what you write beside your name (three short lines).
- **Payoff, Monday.** The roll hangs beside the plaque, with your line at the bottom.
- **Weaker:** quiet, and nobody else's story is in it.

**Recommended: A.** It has a person in it (your bunkmate, whom you already know), a choice in front of the whole crew that leaves something permanent, and it still works if you miss it.

## Reactions within minutes of the horn (lead 21: EV1 makes event cues unlock straight away)
The `onset` phase starts at 14:30, so `cue:event.crossingLine.onset` lines can play from 14:31, before the ceremony. Two of EW1's onset lines ("How was the punch?", "A week aboard and a Line crossed") would come too early. **Plan:** the onset file holds lines for 14:30-15:15 (the horn, the gold windows, the walk to the plaza: "Did you feel that? The whole deck went gold."). The after-the-ceremony lines move to a new `event.crossingLine.resolution` file (cue from 15:15), which is also where Tomas's ending and the punch lines go. The warning lines (from Saturday 18:00) gain Pell's wind-up.

## Checked in the game (0.64.6, and the events base a2d9f40)
- **Day 7's traditions:** the swap meet 10:30-12:30 (promenade and plaza); the rec deck's slow stretch 08:00 and Winner Stays On 11:30-16:30; the reading corner 16:00-17:00 and "One week aboard" 17:15-17:55 (both in the bow lounge); the Sunday long table 18:00-19:00 (±10 minutes) in the mess; Lap of the Wren 20:30-21:15. Nothing else (the 4-weekly rec days fall on Days 14, 21 and 28; Day 8 has a birthday).
- **Rotas on Day 7:** the Captain, Calder, Sato and Holt are off; Vance, Brennan, Lukas Dlamini, Zeke and Tomas work. 86 crew aboard; about 53 are off that day.
- **The places are built:** the plaza venue (`DECKS[3].gathers.plaza`: the speaker's spot east of the lift, facing down the promenade, and 71 standing spots, plus the benches) and the mess venue (44 seats and 22 standing spots, spilling onto the plaza). No new crowd places are needed.
- **First-timers** can come from the roster's `since` (how long each person has been aboard): 13 crew arrived in the last two weeks, 4 more in the last six months.
- **The game has no sound** (no audio anywhere), so "the horn" has to be seen, not heard (question 3).
- **The hull-lights evening** (every 28 days) is words only: nothing on screen changes. The gold lights are new (performance seat).
- **The event base:** `EV_CALENDAR` already has `{ id: 'crossingLine', day: 6, kind: 'short' }`; it's passed over until `SHIP_EVENTS.crossingLine` exists. Gathering moments now take their own name, words, places and hash key `k`.

## The day, minute by minute (Day 0 of the event = Saturday Day 6)
| When | What | Where | The base piece |
| --- | --- | --- | --- |
| Fri 5, 16:00 | The Captain's first weekly address mentions Sunday's crossing (the Fridays plan's lines) | rec deck auditorium | FR1 (Fridays) |
| Sat 6, 18:00 | **Warning** begins: Vance's Mail "Tomorrow we cross the Line"; crew start asking "First crossing?" | Mail, every deck | F2 phase note, cue `event.crossingLine.warning` |
| Sat 6, 21:00-22:30 | Story A's beginning: Tomas can't settle in Bunk 1 (a moment, or his message at 22:30) | Deck 4, Bunk 1 | 20c moment |
| Sun 7, 10:30-12:30 | The swap meet, as usual | promenade, plaza | (unchanged) |
| Sun 7, 12:45-14:15 | Two small volunteer jobs (question 8): carry the punch up from the galley; hang gold ribbons on the plaza | galley, plaza | event `jobs` (17) |
| Sun 7, 14:15 | Device notice: "The Crossing the Line ceremony, on the plaza at 14:30", with "show on map" | device | F3a |
| **Sun 7, 14:30** | **Onset.** The horn moment (felt everywhere: a soft gold pulse, crew stop and look up); the hull lights turn gold; the Captain's banner (3 lines, she's called in) | every deck | moment `horn`, `address.onset`, F0b called in |
| 14:30-14:40 | The crowd gathers: first-timers nearest the Captain, everyone else behind and down the promenade | plaza | gathering `lineCeremony` (k 353) |
| 14:40-14:55 | **The oath** (meeting `crossingCeremony`): the Captain reads it, then asks who answers for the first-timers; your one choice (story A: you, Tomas, or both together) and its words go on Monday's plaque | plaza | meeting, cast `tomas`, `first:2` |
| 14:55-15:15 | The "dunking": everyone drinks Brennan's Line punch (mugs out) | plaza | gathering anim `drink` |
| 15:15 | **Resolution** begins: Brennan's Mail "The Line supper tonight at six"; your certificate is on your shelf | Mail, your cabin | `mail.resolution`, trace `lineCertificate` |
| 16:00-17:00 | The reading corner, as usual | bow lounge | (unchanged) |
| 17:15-17:55 | "One week aboard" with Zeke, as built, with two extra lines about your crossing | bow lounge | reactions `event.crossingLine.onset` |
| **18:00-19:15** | **The Line supper**: the Sunday table, re-dressed for the day (question 4), up to about 60 | mess (spills onto the plaza) | Sunday table on Day 7 |
| 19:15 | **Afterglow** begins: the gold fades back over a minute; the plaque goes up overnight | plaza | trace `linePlaque` |
| 20:30-21:15 | Lap of the Wren, as usual | promenade | (unchanged) |
| Mon 8 | Afterglow chatter, status line "First day in the Veyli reach"; the event ends at midnight | every deck | cue `event.crossingLine.afterglow` |

The phases: `warning [0, 1080]`, `onset [1, 870]`, `resolution [1, 915]`, `afterglow [1, 1155]` (clears), `days: 3`. `eventDay` (24k's quiet days) is true on Day 7 only.

## What you can do
- **Turn up** to the ceremony (and be one of the first-timers at the front), choose your reply, drink the punch.
- **Help** (optional, no score): carry the punch to the plaza, hang the ribbons (question 8).
- **Eat** at the Line supper; find a seat or a wall.
- **Miss it** and still be part of it: the gist by Mail, the certificate anyway, and Brennan saves you a mug at supper (question 6).
- **Afterwards:** tap the certificate and the plaque; crew retell it on Monday.
- **No commendation** from this event, even with both jobs done (it isn't scored). The event says so (`commend: false`).

## The build turns (after the storm update; switch `EV_LINE_ON`)
Each turn: small exact edits, a build-table row under "Crossing the Line", the area's checks, `bash check_fast.sh`, cadet_test with the switch off (ALL IDENTICAL), push, report. The build number is the build master's.

| Turn | What | Sections (owners) | Checks besides check_fast |
| --- | --- | --- | --- |
| L1 | The event's data (and story A's reworked oath meeting, its choice setting `line.answer`): `SHIP_EVENTS.crossingLine` only when `EV_LINE_ON` (phases, address, Mail, news, status, `commend: false`, no threads); the first-timers (`lineFirst`, from the roster's `since`, made at load, no `R()`); cast slot `first:2`; the oath meeting; `EV_BEATS` row (the ceremony counts as the Captain's scene that day); move EW1's ready files into `content/` and bake | 18 (traditions: EV1's seat), 22 generated (writers, through content_gen.py) | events_check, bigevents_check (on paper), lines_check, social_check, cadet_test off |
| L2 | The crowds: the ceremony gathering (k 353, plaza venue, front row first), the Line supper as the Sunday table re-dressed on Day 7 (k 440 kept; name, words, 18:00-19:15 with no jitter, pull up to about 60; its Saturday Mail left out), Winner Stays On ends 14:00 that day, the galley's extra batch and a pudding | 18, 14 (sim: the front row's order), 16 (galley), 4e/15r (rec: WSO's hours) | day_check Days 6-8 (on), food_check Day 7, events_check, bigevents_check (crowds: draw calls at both, at 390x844) |
| L3 | The look: gold hull lights (`FEEL_MOODS.crossingLine`), the horn moment (a new `horn` feel: a soft gold pulse, no shake), gold ribbons on the plaza (`DECK_DRESS.lineRibbons`), the plaque (`linePlaque`), the certificate (`lineCertificate`, on your shelf; it moves with you to cabin 4-23 on Day 10 like the Tiles trophy) | 8b (performance), 4d (deck architect), 18 | deck_check Decks 3-4, perf_check (two new scenes), screenshots at 390x844 and 360 wide |
| L4 | Your part: story A's Saturday moment with Tomas (20c, social seat) and his Monday lines, the two volunteer jobs, the Schedule and status lines (F3), the Record line ("Crossed the Line into the Veyli reach, Day 7", never a score), missing the ceremony (Brennan's mug at supper), a reload mid-oath (F4b) | 17 (systems: posting), 19 (device), 18 | player_check, device_check, interactions_check, devmode_check, bigevents_check (live), intro_check `--week` alone |
| L5 | Switch it on (`EV_LINE_ON = EVENTS_ON`) after the user's review, the full round, design-doc and DEV_NOTES | 18 | the full round (intro_check in pieces) |

**About 5-6 turns** (the events plan said 4-5; the story adds up to one), then the adversarial build review, then the user's review.

**Needed first (not this plan's to build):** the storm update (the base is switched on with it); EV1's F0b (called in, and people planned into an event's meetings: the gap EC1 found, being fixed with PB), F3 (device), F4 (reloads), F7 (EC1's `bigevents_check.py`).

**Draw calls:** EP1 measured 236/367 at the storm's party with 64 crew on Deck 3 (budget 450). The crowd is instanced, so 60 people barely move it. The new look adds about 3: the ribbons (1-2) and the plaque (1); the certificate is on Deck 4 (1). The gold is a colour change, no new meshes. bigevents_check's crowd part measures the ceremony and the supper at phone size.

## The lines it uses (EW1, claude/events-lines 307addc, all ready)
- `plans/events-ready/crossingLine/content/banks/event-crossingLine.lines`: Vance's Mail, the three banner lines, status lines (warning, onset, afterglow), the ceremony's tap lines, the Line supper (name, Mail, ask, here, thanks, chatter), the certificate and the plaque.
- `.../meetings/crossingCeremony.meet`: the oath, your three replies, Brennan's punch.
- `.../reactions/event.crossingLine.warning|onset|afterglow.lines`.
- `plans/events-ready/ionStorm/content/reactions/calledIn.lines`: shared (the Captain on Day 7).
- **Story A's lines (EW1, about 30):** the Saturday bunk moment with Tomas (about 8 lines, 3 replies) and his 22:30 message; Pell's wind-up (a warning line or two); the oath meeting's new choice (who answers, three endings); three plaque texts (plus the missed-it one, Tomas's words); Tomas's Monday lines (3 + 1 missed); crew quoting the plaque. The onset lines rewritten for 14:30-15:15 and the after-ceremony ones moved to a new `event.crossingLine.resolution` file.
- **New lines needed (small, EW1):** the horn's one-line notice; two volunteer job titles; Brennan's "saved you a mug" line for someone who missed it (question 6); the Record line; the device notice; the Sunday table's ask/here lines read from the supper's bank on Day 7.
- **Fixes for EW1:** the bank's comment still says "an extra batch and a cake" (the cake was cut: punch and one pudding); lines_check needs its length rule for `event.*.mail.*`, `event.*.keepsake` and `event.*.plaque` (the dialogue engineer's file; EW1's README already asks for it).

## Risks
1. **It all rests on the base's gap:** today nobody is placed into an event's meeting (EC1's finding). Until F0b fixes it, the Captain and Brennan wouldn't be on the plaza.
2. **Off must stay identical:** the event, its gatherings and its places go in only when `EV_LINE_ON`, so `EV_SHIPWIDE` and Deck 3's places come out byte-identical with it off.
3. **Re-dressing the Sunday table** touches the galley's tie (meal, seating, the tasting side dish) and the long-tables decor. food_check Day 7 and the galley owner's review.
4. **The crowd may come in under 50:** Winner Stays On keeps people on the rec deck until 16:30 unless it ends at 14:00 (question 7). The day_check count on Day 7 tells us.
5. **The first week:** Day 7 is still the arrival week (One week aboard, Zeke's invite). intro_check `--week`, run alone.
6. **The certificate must follow you** when you move to the officer's cabin on Day 10, as the Tiles trophy does.
7. **An event with no threads and no jobs-for-commendation** must end cleanly (no band words, no debrief, no commendation). The event's `commend: false` and a check for it.
8. **A gold that reads as "something wrong":** the storm's mood shifts the space outside to violet; the gold must look warm and festive, not alarming. Screenshots at phone size.
9. **The ceremony's 45 minutes** must end before the reading corner (16:00): it ends 15:15; the punch stays at the plaza.
10. **Story A puts Tomas on the plaza while he's on shift:** the meeting names him, so F0b's fix must bring a named person who is on shift (not only people called in on a day off). Watch keeping the plaza is a believable post for that hour.
11. **Reactions unlock at 14:30:** the onset lines must not mention the punch or the oath's result (moved to the resolution file).

## Questions for the user (each with a recommended answer; ids `line-q1` to `line-q9`, plus `line-general`)
- **(line-q9, new in 1.1) Which story?** Recommended: A, "Who answers the oath" (Tomas and you; your choice goes on the plaque). Others: B, "The missing recipe"; C, "The Line roll".
1. **When does the ship start talking about it?** Recommended: with Vance's Mail on Saturday at 18:00 (and the Captain's mention at Friday's address). Others: Saturday morning; Friday's new-hands tea.
2. **What do the gold hull lights look like?** Recommended: a warm gold in every window and slightly warmer light indoors, 14:30-19:15. Others: windows only; also gold light strips along the promenade (a few more draw calls).
3. **The horn (the game has no sound):** Recommended: a felt moment: one soft gold pulse of the lights, crew stop and look up, a one-line notice. Others: also add the game's first sound, one horn note (sound is new work: a mute switch, phones on silent); the banner only.
4. **The Line supper:** Recommended: the Sunday table re-dressed for the day (same dinner, renamed, 18:00-19:15, up to about 60). Other: a separate gathering, with the Sunday table off that day.
5. **Who are the first-timers at the front?** Recommended: you and everyone aboard less than six months (about 17). Others: you and the 13 who arrived in the last two weeks; only you.
6. **If you miss the ceremony:** Recommended: you still crossed (the gist by Mail, the certificate anyway; with story A, Tomas answers alone and tells you on Monday), and Brennan saves you a mug of punch at supper. Others: the gist and the certificate only; the certificate only if you were there.
7. **Winner Stays On that Sunday:** Recommended: it ends at 14:00 that day. Others: runs as usual (a smaller crowd); none that Sunday.
8. **Something to do beforehand:** Recommended: two small volunteer jobs on Sunday 12:45-14:15 (carry the punch, hang the ribbons), never scored. Other: none, just turn up.

## Judgement calls made (tell me if any is wrong)
- No phase pauses any tradition (the storm's way); instead the two that would clash are changed for the day (the Sunday table, Winner Stays On).
- The plaque goes on the plaza's north wall beside the lift doors; the certificate on your shelf.
- The ceremony counts as the Captain's one scene on Day 7 (`EV_BEATS` row, kind 'captain'), so the guard keeps anything else away.
- Hash keys: 353 for the ceremony (354 kept for this event if a second gathering is ever needed); the supper keeps the Sunday table's 440. EV1 confirms they're free.
- No Veyli at the ceremony and nothing about the visit (EW1's rule): the reach is just where the Wren is going.
