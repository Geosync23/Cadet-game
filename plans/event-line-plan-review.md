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
  (5 months) would count too, but they're Veyli. Of those four, **only Teague and Quist are off at 14:30**. Tomas,
  Rossi and Eklund are on shift (Tomas is on watch in Deck 2's watch room, 08:51-17:00). The plan's "13 in two
  weeks, 17 in six months" isn't in the game. Under question 5's recommendation, the front row would be you plus
  two people.
- **Sunday dinner is the crew's vote.** `galleyMenu(7)` is fish and chips (19 votes), with herb flatbread on the side.
  EW1's supper lines promise "a proper roast" and say "the roast ran out".
- **Saruth is at the Sunday table today** (planned 18:16-18:59). They're also at Winner Stays On from 15:01, and in
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
     reaction line can say so, and nothing about the visit). They're at the Line supper as they are at every Sunday
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

## Round 1b: plan 1.1 (85d49ce), the story section (line-q9)

85d49ce was written alongside round 1, so **round 1's fixes 1-12 are all still open**: questions 5 and 7, the crowd
numbers, the dish, Saruth and the rest. This pass is on the story, which I checked against the game the same way
(a new game on 0.64.6).

### Is it a good story? Yes. A is the right recommendation.
- It has a person who wants something: Tomas, your real bunkmate, is in Bunk 1 (`4-B1-1`) with you. He came aboard
  "one week" ago, as you did, and he's the other new face at First Light.
- It has a turn ("the wind-up is half true"), a choice made in front of the crew, and a lasting trace (your words on
  the plaque).
- It still ends well if you miss it.
- It keeps EW1's guard rails: nothing about his exam (beat 5), the list (beat 6) or staying (beat 7), and no Holt.
- Pell (two years aboard) is a believable old hand for the wind-up. With round 1's fix 2(a) ("last in the reach two
  years ago") he's exactly not a first-timer, which is neat.
- B and C are described fairly as weaker. line-q9 says plainly that A replaces the v3.2 "one reply (proud, nervous,
  joking)" wording. No visit spoilers.

### Fixes for the story (S1-S4)
- **S1. Tomas isn't in Bunk 1 on Saturday evening.** On Day 6 in a new game he finishes his shift, then:
  - 19:14-20:36 in the mess;
  - 20:36-21:15 in the garden;
  - 21:15-22:05 in the mess again;
  - 22:08-22:40 climbing on the rec deck;
  - 22:42 in Deck 4's common room, and in bed at 22:46.

  So "21:00-22:30 in the bunk room" never happens, and a 22:30 message would come from the climbing wall. Don't
  move his plans; that's the planner, and it would change Day 6 for everyone near him. Instead:
  - the moment finds him wherever he is from 19:00 until bed (a 20c moment that goes with Tomas, not with a room);
  - or it's at his bedtime in Bunk 1 (from about 22:45);
  - and the fallback Mail comes when he goes to bed (about 22:50), not at 22:30.
- **S2. His post is Deck 2's watch room, not the plaza.** On Day 7 he's at `2-watch-6`, 08:51-17:00, so "keeping the
  plaza is his post that hour" isn't true. Recommended:
  - the Captain sent for him ("I asked the watch to spare you for ten minutes"), and he arrives in his Watch
    uniform;
  - drop the `watch:1` cast slot. The watch hands actually on shift at 14:40 (Nakamura and Ueda in a new game) are
    in the watch room, two decks up, so a line from one "on the plaza" would need F0b to move a second on-shift
    person for one line.

  If a watch line is wanted, it's a Mail or a bubble in the watch room, never a plaza line.
- **S3. "Eighty people."** 76 are aboard, and the crowd will be about 45-60. Use "Everyone. The whole ship." It's
  truer, and just as scary to him.
- **S4. A check that he's there.** bigevents_check's cast part must show Tomas (on shift) planned at the plaza for
  14:40-14:55 and back at his post afterwards. L2 waits on F0b's on-shift case (risk 10), not only its called-in
  case. Without it the story's middle is empty.

Note: under round 1's fix 2(a), Ueda (ten months, on watch) is a first-timer too. That's fine: Ueda stays at the
post, as the watch does.

**Verdict on 85d49ce: PASS WITH FIXES.** That's round 1's fixes 1-12 plus S1-S4. The story itself (A) is good and
should be recommended. I'll review EP2's fix round when it's pushed.

## Round 2: plan v2 (221c492), EP2's fix round and the reworked story

**Round 1's fixes 1-12 are all taken, and taken properly.**
- The facts are true.
- The replacements for q5 and q7 are honest choices, with recommendations I'd stand behind.
- `EV_DAY_DRESS` is named and pure, with what changes and what stays.
- The hash-key table is right (341 is the one-offs' key, as built).
- L2 is gated on F0b.

**The reworked story A, "The one on watch", is the best version yet.**
- It comes from the real rota: Tomas works 08:51-17:00 on Day 7, and he really is the host of that night's Lap of
  the Wren (he's planned on it, 20:27-21:11).
- The choice on the plaque speaks to him ("even the ones on watch").
- The payoff is the same evening, on a walk you may take anyway.
- It works if you miss it, and it keeps EW1's guard rails (nothing about his exam, the list or staying).
- B and C are fairly called weaker. line-q9 says plainly that it changes v3.2's reply wording.

I checked the new parts in a new game. Four fixes:

- **R2-1. Saturday night is still timed for Bunk 1 (round 1b's S1, not taken yet).** On Day 6 Tomas is in the mess
  and the garden 19:14-22:05, climbing on the rec deck 22:08-22:40, and in bed at 22:46. "21:00-22:30, Bunk 1" and
  "not in the bunk room by 22:30" never line up with him. Two fixes, and the planner isn't changed:
  - the moment follows Tomas wherever he is from 19:00 until bed, or it's at his bedtime in Bunk 1 (about 22:45);
  - the fallback Mail comes about 22:50, when he goes to bed.

  The minute-by-minute row and the story text need the same change.
- **R2-2. Tomas's post isn't "the watch room".** On Day 7 his place is `2-watch-6`, a standing watch post in Deck 2's
  lift lobby. The watch office (`2-watch-1..5`) is a different room. My round 1 said "watch room", my mistake. The
  mug's stop should find Tomas at his post from his own plan, not a fixed room: a watch post can change by day.
  Risk 11 then reads "Tomas at his post (2-watch-6 in a new game), reachable from the lift". Lines like "Nobody
  brings things to the watch room" should say "up here" or "to the watch".
- **R2-3. Zeke and Pell aren't on the Lap.** On Day 7 in a new game, 17 walk it: Tomas, the Captain, Raman, Oduya,
  Halloran, Cruz, Lemaire and others. Zeke is in the bow lounge (20:17-21:21) and Pell is on a bench, then in the
  lounge. The Lap's re-dress in `EV_DAY_DRESS` must give `torres-zeke` and `pell` a pull of 1 that night, and
  events_check or bigevents_check should check that both are planned on it.
  - **The judgement call "She isn't on the Lap" is false:** the Captain walks it that night. It's harmless (walking
    isn't a scene), but say so and give her no line in the Lap moment, so the guard's one Captain's scene a day
    still means the ceremony.
- **R2-4. `galley-line` isn't an existing group.** Define it in the plan: galley crew on shift whose plan has them
  cooking 14:30-15:15, with Brennan brought as cast. Also say that "about 50-60" with standing easy is an estimate:
  about 25 are at work and maybe half stand easy. day_check Day 7 gives the real number, and anything from 45 up
  fits the user's "up to about 60".

Note: I've corrected my own round 1 to use they/them for Saruth (facts.md: the Veyli are they/them), as the plan
does.

**Verdict on 221c492: PASS WITH FIXES** (R2-1 to R2-4, all small and exact). Once they're in, it's a PASS; I don't
need another full round, only a look at the diff. The recommendations, A for line-q9 and the rest, are safe for the
lead to take overnight.

### Round 2, update: 5879dbf (54e36dc + EW1's Holt guard rail)
- **R2-1: done.** The Saturday moment follows Tomas until bed, and the Mail comes at about 22:50.
- **The Holt line and the neutral two-years fact ("a quiet charting run"): good.** They keep his arc's border-patrol
  story untouched. The head writer's timeline check before facts.md is the right gate.
- **Still open:**
  - **R2-2:** "watch room" is still in the story's opening line, in "What it needs" (the second stop) and in
    risk 11, which now says both `2-watch-6` and "the watch room's door". His post is in Deck 2's lift lobby.
  - **R2-3:** the Lap's re-dress doesn't yet give Zeke and Pell a pull of 1. "She isn't on the Lap" still stands in
    the judgement calls.
  - **R2-4:** `galley-line` isn't defined yet.

Verdict unchanged: **PASS WITH FIXES** (R2-2 to R2-4). Then it's a PASS.

### Round 2, final: c9d92db
I checked the 5879dbf..c9d92db diff:
- **R2-2:** his post is `2-watch-6` in Deck 2's lift lobby, and the mug stop finds him from his own plan. No
  "watch room" is left.
- **R2-3:** Zeke and Pell get a pull of 1 on the Lap, and bigevents_check confirms it. The Captain walks it with no
  line.
- **R2-4:** `galley-line` is defined, and 50-60 is marked as an estimate (45 or more is fine).

R2-1 was already in 54e36dc.

**Verdict on claude/event-plan-line c9d92db: PASS.** The plan's recommendations, including line-q9 A "The one on
watch", are safe to take. Next for me: the build review of this event, turn by turn, once L1 is pushed.

### a64fb68: option A2 (Tomas comes, added for the user's question)
A fair alternative, with the trade-off stated honestly, and A is still the right recommendation. Two small fixes to
A2's text:
- **A2-1. Three answers, not four.** The meeting takes three replies at most (EW1's format). In A2, "even the ones on
  watch" no longer means anything, because Tomas is standing there. A2's answers should be: proud, "We'll answer
  together", and the punch joke.
- **A2-2. Nobody "comes down".** Tomas's post (`2-watch-6`, the lift lobby) and the watch office are both on Deck 2.
  The covering hand walks across Deck 2 to his post, and Tomas comes down to the plaza.

Verdict stays **PASS**, with A2-1 and A2-2 as wording fixes for EP2. Neither changes the recommendation.

### 9361008: the story decided
The user chose A (01:30, via lead 22). The only changes since a64fb68 mark line-q9 as decided and A2, B and C as
"not chosen". A2-1 and A2-2 no longer matter, because A2 is parked. **PASS stands at 9361008.**

### 84946af: the ceremony moves to the bow lounge (the user, 01:42)
The move is sound. I checked it in a new game on 0.64.6:
- The lounge's 34 seats and its standing spots (60 in the party's venue, 51 of them west of column 49) give room for
  about 50-60, with the promenade and plaza for overflow.
- The new venue `bow-lounge-line` is switched on only with `EV_LINE_ON`, so the party's venue stays identical.
- The Lap's bow turn is 3-lap-6 at (40, 10), on the promenade by the lounge doorway, so moving the old hands' stop
  there needs no route change.
- One week aboard and the reading corner come later in the same room, with no clash.

One fix, and one small point:
- **R3-1. Two of the four lead spots aren't clear.** The venue rule (section 4d's gathers comment) says every
  existing place's tile stays clear. On Deck 3:
  - **(48.5, 10.5), the Captain:** tile 48,10 is where you walk to for lounge seat `3-lounge-27` (seated at 47.84,
    10.2, facing the windows). She'd stand on that seat's spot, half a metre from whoever sits in it.
  - **(47.8, 11.7), a speaker:** tile 47,11 is blocked by furniture.
  - (48.5, 9.3) and (48.6, 12.1) are on tiles 48,9 and 48,12. Those are free, but they're the party venue's crowd
    spots 29 and 36. That's fine in the new venue, as long as its standing list leaves those two tiles out.

  Re-pick the Captain's and the speaker's spots on open tiles that no place uses (deck_check's places check will
  confirm). Or hold `3-lounge-27` for the ceremony and say so.
- **R3-2 (small).** Risk 9 still says "the punch stays at the plaza". In the lounge, the bowl and the ceremony's
  dressing must be gone by 16:00, when the reading corner uses the room. Say so in L3.

Verdict on 84946af: **PASS WITH FIXES** (R3-1, R3-2). Once the spots are on clear tiles, it's a PASS.

### 7040dc8: round 3's fixes
- **R3-1 done.** I checked it in a new game after `goToDeck(3)`:
  - Tiles 50,9, 50,10, 50,11 and 50,12 are open, in the lounge, and hold no daily place or walk tile. Their only
    places are the party venue's crowd spots 51, 48, 52 and 56, which belong to the separate party venue, so that's
    fine.
  - 49,10 and 49,11 are blocked: the furniture in front of the Captain. The deck architect's check that it's low
    furniture, in L2, is the right one.
  - The fallback (hold seat 27) is stated.
- **R3-2 done.** The bowl and ribbons are shown 14:30-15:15 only.

**Verdict on claude/event-plan-line 7040dc8: PASS.**

### d01acd6: reuses the storm's EV_DAY_DRESS
L2 now adds its two Day 7 rows (the Sunday table, the Lap) to the storm's `EV_DAY_DRESS` instead of building its
own. Only text changed. The shape EP2 proposed to EP3 (a Map keyed `<trad>@<day>`, rows of drop, set or add, made at
load, empty when off) is fine. One condition: the add row keeps its k, so the Lap moved to Day 15 keeps 442 and a
plan's hash stays the same. The storm's review checks the final shape. **PASS stands.**

### 61f81be: the user's answers, and "Why the crossing matters" (line-q10)
- **The answers are marked decided** (q1 b; q2-q8 a). The warning starts at Saturday 08:00 as talk only, so the
  free day stays free. Vance's Mail at a fixed minute needs a phase Mail time of its own (`at`) from the base. The
  storm's Monday debrief at a fixed minute needs the same, so ask EV1 for one feature that serves both.
- **Meaning A ("guests in someone else's sky") is the right recommendation.** It explains the oath's words ("we did
  not go alone"), it matters to everyone aboard, and it fits an unarmed survey ship. The lines sit where the player
  already goes. Three wording fixes:
  - **M1. "by the Veyli's leave" brushes the Envoy, as EP2 feared.** "Leave" means permission someone granted, which
    implies an arrangement. Envoy Saruth is the arrangement's obvious face, and their card keeps "why they were
    sent (until close)", which nothing in content/facts.md answers yet. A player will put the two together, and the
    head writer's later answer would have to fit it. Use **"as guests"** only. It says the same thing, and nobody
    granted anything. That means Vance's sentence ("Beyond it, the Wren travels as a guest") and the certificate,
    which already says "as a guest".
  - **M2. "on their charts" contradicts the survey.** Survey "charts Tavessa", "New reach, new charts", and B is
    about charting. If the Wren travels on Veyli charts, what is Survey doing? It also implies a second arrangement
    (charts shared). Drop "on their charts". "Every star already has a Veyli name" carries the meaning.
  - **M3. The new fact "the Concord's charts end at the Line" contradicts the other new fact.** The Wren was last
    in the reach two years ago "on a quiet charting run", so the Concord has some charts past the Line. Write it as
    **"past the Line the Concord's charts are thin: a few runs, never a full survey"**. That fits Zeke's "off the
    map", the two-years fact and the work Survey is about to do. The head writer confirms it in facts.md.
- **Spoilers otherwise: fine.** Nothing on the visit, nothing on Holt's patrol day (his partner Hanne Rook, the six
  hours of silence), and "help is a long way off" is about distance, not danger.

Verdict: **PASS WITH FIXES** (M1-M3, wording only). The rest of the plan's PASS stands.

### 9ea6ec7: M1-M3 in
- "As guests" is used everywhere, and "the Veyli's leave" appears only in the record of the fix.
- "On their charts" is gone.
- The fact now reads "the charts are thin: a few runs, never a full survey".
- The fixed-minute Mail is asked of EV1 for both events and listed under "Needed first".

**PASS at 9ea6ec7.**
