# Crossing the Line: adversarial review of the event plan

Reviewer ER2 (session_01S8pboNujAzZgMSWFK84CxD), 2026-10-21. Branch `claude/event-plan-review-2`.
Plan reviewed: `claude/event-plan-line` af02eba, `plans/event-line-plan.md` (EP2, v1). Reports to lead 21 (or lead 22).

## Round 1 (af02eba): PASS WITH FIXES, story section still to come

The shape is right: one Sunday, a ceremony and a supper, nothing scored, everything behind `EV_LINE_ON`, built
after the storm. Most of the day's facts are true. But **two of the numbers the plan is built on are wrong, and
they change two recommendations** (questions 5 and 7). The story section (line-q9) isn't in af02eba, so I can't
judge it yet. Below: what I checked, the 12 fixes, and what the story needs to be worth telling.

### How I checked
Headless Chromium on claude/integration 0.64.6 (the plan's base) and on claude/events-base a2d9f40, a new game,
`schedPeople`, `aboard`, `isWorkDay`, `planDay`, `eventsOn`, `galleyMenu`, `gatherSpots`, `EV_CALENDAR`,
`EV_SHIPWIDE`. Draw calls at 390x844 on Deck 3. Probe scripts are in my scratchpad, not pushed. I also read the lines
EW1 wrote for it (claude/events-lines 307addc) and First Light Cocoa's meeting (claude/patch-e).

### True as written
- **Day 7's traditions and times:** the swap meet 10:30-12:30, the slow stretch 08:00, Winner Stays On 11:30-16:30,
  the reading corner 16:00, One week aboard 17:15-17:55, the Sunday table 18:00-19:00, Lap of the Wren 20:30-21:15.
  Day 8 has a birthday (20:15).
- **Rotas:** the Captain, Calder, Sato and Holt are off on Day 7. Vance, Brennan, Lukas, Zeke and Tomas work.
- **Places:** the plaza has 71 standing spots and one lead spot. The mess has 44 seats, 22 standing spots and one
  lead, and it spills onto the plaza.
- **No sound** anywhere in the game.
- `EV_CALENDAR` has `crossingLine` on day 6. `FEEL_MOODS` holds only the storm. Keys 352-354 are free today.
- **Phases:** with `day: 6`, `onset [1, 870]` is Sunday 14:30, and `eventDay(7)` is true (onset and resolution).
- **Draw calls:** at 390x844 on Deck 3 at 14:45 and 18:35 on Day 7 (73 crew on the deck), 240-256. That's well
  inside 450, so the plan's "about 3 more" is fine.

### Wrong, and what it changes
- **Crew aboard.** There are 76 aboard on Day 7 (74 crew, plus Envoy Saruth and Ulla Jaramillo, the touring
  musician on Days 5-9), not 86. 45 work that day and 31 are off, not "about 53 off".
- **At 14:30, 25 crew are at work.** About 26 are at leisure, 4 are asleep (the night shift) and only 3 are watching
  Winner Stays On. With only off-duty crew coming, the ceremony tops out at **about 35-45, not 50-60**.
- **First-timers.** The roster's `since` gives one person aboard less than two weeks: Tomas ("one week"). Four crew
  have been aboard less than six months: Teague (3 months), Rossi (2), Eklund (2) and Quist (5). The guest Saruth
  (5 months) would count too, but she's Veyli. Of those four, **only Teague and Quist are off at 14:30**. Tomas,
  Rossi and Eklund are on shift (Tomas is on watch in Deck 2's watch room, 08:51-17:00). The plan's "13 in two
  weeks, 17 in six months" isn't in the game. Under question 5's recommendation, the front row would be you plus
  two people.
- **Sunday dinner is the crew's vote.** `galleyMenu(7)` is fish and chips (19 votes), with herb flatbread on the side.
  EW1's supper lines promise "a proper roast" and say "the roast ran out".
- **Saruth is at the Sunday table today** (planned 18:16-18:59). She's also at Winner Stays On from 15:01, and in
  the `everyone` pool for any gathering. The plan's "No Veyli at the ceremony" needs her taken out on purpose, and
  the supper needs a decision either way.
- **Winner Stays On isn't what keeps the crowd small.** It holds 3 crew at 14:30 (Brennan leaves it at 14:28).
  Ending it at 14:00 means editing the rec deck for about 3 people.

### The fixes (round 1)
1. **Correct the facts** in "Checked in the game": 76 aboard (74 crew and 2 guests); 45 on shift and 31 off; 25 at
   work at 14:30; first-timers as above. Change risk 4 to match: it's the day shift, not Winner Stays On, that
   keeps the crowd small.
2. **Question 5, first-timers: redo it with the true numbers.** A cut by `since` gives a front row of 2-3 people.
   Honest options:
   - **(a) recommended:** a written fact, "the Wren was last in the reach two years ago". Everyone aboard under two
     years is then a first-timer: 21 crew, 8 of them off at 14:30 (Rina, Cruz, Bakshi, Silva, Teague, Quist,
     Lemaire, Abara), plus whoever steps out (fix 3). It's made at load from `since`, with no `R()`. The fact goes
     in content/facts.md (the head writer's).
   - **(b)** under six months: 4 crew, 2 of them there.
   - **(c)** only you.

   Whichever is chosen, `lineFirst` must leave out guests (`rank: 'guest'`).
3. **Question 7: replace it.** Winner Stays On stays as it is (drop the rec-deck edit from L2, and the 4e/15r
   owner). The real question is **"Does the day shift step out for the ceremony?"**
   - **Recommended: yes, for 14:30-15:15. Everyone at a post that can wait stands easy, except the bridge, the watch
     and the galley line.** That gives about 50-60, which is what the user's "need more large groups" asks for.
   - Other: only off-duty crew (about 35-45).

   This is a new routine rule for one window (like the storm's `doubleShift` and `stayIn`): section 14, the sim
   seat's review. It goes in L2, with day_check Day 7 counting the crowd (bigevents_check's CROWD cap of 66 still
   holds).
4. **The supper's dish (question 4).** Keep the crew's vote as the dinner (recommended: it's the Sunday table
   re-dressed, so the vote stands), with Brennan adding the pudding. EW1 changes "a proper roast" (Mail), "The
   roast's to get rid of the taste" (here) and "ran out of roast" (chatter) to words that fit any dish, and fixes the
   bank comment ("an extra batch and a cake"; the plan already noted the cake). The other way, a set Line roast
   that overrides the vote, also changes the menu board and the vote note, so it needs the galley owner.
5. **Saruth and Ulla: say what they do.** Recommended:
   - Saruth isn't at the ceremony, by courtesy (a Veyli doesn't watch another people's rite: one afterglow
     reaction line can say so, and nothing about the visit). She's at the Line supper as she is at every Sunday
     table.
   - Ulla is a guest first-timer and goes like anyone off duty.
   - Build it as an explicit `not: ['saruth']` (or `rank: guest`) rule in the ceremony's `who`, checked by
     bigevents_check.
6. **The re-dressed Sunday table needs its mechanism named.** Say exactly where Day 7's override lives: section 18,
   a row read by `eventsOn` that comes only from `EV_CALENDAR` and the event's data, never `eventNow` or
   `SHIP.event` (the planner rule). Also list what it changes: the name, the words, the 18:00-19:15 window with no
   jitter, the extra pull, and leaving out the Saturday 18:00 Mail. And confirm what stays: k 440, `ties.galley`
   (meal, seating, the tasting side) and `decor: longTables`, so food_check Day 7 is the test. As written, L2 says
   "re-dressed" without saying how.
7. **Spots for the cast at the front.** The plaza has one lead spot (the Captain). Brennan (with the punch) and the
   two first-timer speakers need places beside her. Either:
   - add 2-3 lead spots to `DECKS[3].gathers.plaza`, only when `EV_LINE_ON`, so Deck 3's places stay identical
     with it off (the deck architect, 4d); or
   - say the cast takes crowd spots 1-3 in section 14's order.

   "No new crowd places are needed" should say which.
8. **Something to pour the punch from.** L3 has no punch table, bowl or jug. Add one prop (1-2 draw calls, the
   performance seat) at the front of the plaza, from 14:30 to 15:15.
9. **The mugs depend on patch E's mug.** "Mugs out" for the crowd uses the mug in the crowd's hands, the drink pose
   with `MUG_ON` (#30, patch E, PE's handover). Add `MUG_ON` to "Needed first", or say the drink pose shows a glass.
10. **The volunteer jobs: say where you find them.** On Sunday the Works bay board is two decks down from the plaza.
    Post the two jobs on the mess sign-up sheet (`DECK_DRESS.signupMess`, already built for the storm) or have
    Brennan offer them, and say which in L4. The board stays open on days off (section 9), so taking them works
    either way.
11. **A table of hash keys.** Put it on the plan (or in plans/owners.md): 340 the party, 351 the farewell, 352 the
    storm's lantern supper (the storm update should confirm), 353 the Line ceremony, 354 kept for this event, then
    the comet's. Today nothing reserves 352-354, and two events are being planned in parallel.
12. **Small things:**
    - EW1's warning reactions say they run "from the Friday new-hand's tea (Day 5)", but the warning phase starts
      Saturday 18:00. Fix the comment, or start the warning earlier (see the story notes below).
    - Friday Day 5's mention of the Line is in the Fridays plan's `friday-d5.address`, so it needs `SHORT_FRIDAY`
      on. Say so under "Needed first".
    - L5's design-doc edit should add "a short event may say `commend: false`", because the design doc says every
      event commends after two jobs.

### Questions 1-8: are the recommendations honest?
- **q1** (Saturday 18:00) is fine, but it gives the warning one evening. See the story notes: chatter from
  Saturday morning gives anticipation without taking the free day (talk isn't a task).
- **q2, q3, q6, q8** are honest and buildable. On q3: the game already tells sounds in words ("Pell has the
  chalkboard. And the bell."), so the Mail's "the horn will sound" fits a pulse of light plus a one-line notice.
- **q4** is right to re-dress the table, with fix 4 (the dish) and fix 6 (how).
- **q5** has to be redone (fix 2).
- **q7** has to be replaced (fix 3).

### Clashes checked: none found
- **Fridays:** nothing on Day 7, so the Friday 15:30-17:00 hold isn't touched. The Day 5 address mention is fine.
- **The playtest patch:** First Light Cocoa (Day 1) names where the Wren is heading: Tavessa, "the Veyli named it"
  (EW1's replacement for the placeholder). That fits crossing into the Veyli reach on Day 7, and it's a setup the
  story can use. #31 (Ask Zeke) being parked doesn't touch Day 7.
- **Pillar 5:** nothing on Days 6-8. The test is on Day 9.
- **The base's gap (F0b):** the plan names it (risk 1), and it's real. L2 should be gated on it: bigevents_check's
  cast part must show the Captain and Brennan planned on the plaza at 14:40 before L2 counts as done. It does today
  only as "waiting".

### What the story needs (for line-q9, which I'll review in the fix round)
As written, the day is a ceremony, not a story: an oath, a reply, green punch, supper. Nothing is uncertain, and
nobody wants anything. The game's own data already holds a small story. I'd look for these:

- **Tomas, the other newest hand, is on watch through the crossing** (08:51-17:00, in Deck 2's watch room). That's
  true in the rota. It's a want ("I'll miss my own Line") and a turn.
  - You can carry a mug of punch up to him: the punch job's second stop, never scored.
  - Or Brennan saves him one.
  - The payoff: Lap of the Wren at 20:30 is Tomas's to lead that night, so the crew make it his crossing. Someone
    says the oath's last line to him on the walk.

  It also fits fix 3 (the watch doesn't stand down: someone has to watch the ship as she crosses). It reuses the
  "missed it, saved you a mug" piece, and it ties back to First Light, where Tomas and you were the two new faces.
- **A small mystery: what's in the punch?** It's already in EW1's lines ("We don't ask what's in it"). Carrying the
  punch, Brennan tells you one ingredient and swears you to secrecy. At the supper someone guesses, and you can keep
  her secret (a reply, Brennan +1). It's funny and in character (her "nobody goes hungry on my ship" pride), and
  it costs a few lines.
- **Zeke's face.** At One week aboard (17:15), Zeke, twelve years aboard, admits he pulled the worst face at his
  first Line. That sets up Monday's "who pulled the worst face" chatter, which otherwise has no source.
- **Holt, one line.** Holt is off and distrusts the Veyli. One warning reaction ("Veyli reach. Hm. Keep your
  wits.") is in character. It must not step on his arc beats (holt:4 is about the Envoy's tea), so it's a reaction
  line, never a scene.
- **Spoilers: none in what's written.** The oath, the banner, the certificate and the plaque say only "the Veyli
  reach". Keep it so: nothing about a delegation, guests or the Envoy's purpose. Saruth's
  `avoid: "why they were sent (until close)"` is the line not to cross.

**Verdict: PASS WITH FIXES** (fixes 1-12). The story section is still to come: I'll review it, and EP2's fix
round, next.
