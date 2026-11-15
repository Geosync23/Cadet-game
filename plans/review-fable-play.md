# Starship Cadet 0.99.91: design and playability review (FR2)

Reviewer: FR2, for lead 52. Build: main cdd9efd, game sha256 b321a4ec...95f3 (the live 0.99.91). Phase 1: review only, no game edits. Branch `claude/fable-review-play`. Screenshots are in `plans/review-fable-shots/`.

## Summary in plain words

The ship is lovely to be on. The writing has a real voice, the rooms are full of people doing things, and the first week has several moments that land (the dinner with Zeke and the Chief, your name on the beam, the mug at Friday tea, the result in the Chief's office with the bay cheering outside).

What hurts a new player on a phone is mostly not the content. It is three things:

1. **The gold arrow is the game, and it has blind spots.** A player who simply follows the arrow never eats (Food sits at 0 for six of the first nine days, with one warning ever), is never led to the week's biggest event (the Line oath on Sunday), and is then told by Mail that they took the oath. This is the same family as the results meeting that silently did not happen.
2. **Work is a treadmill.** The arrow leads from one job to the next from 06:00 to 17:00. In nine days the arrow-follower did 203 jobs, every one paying the same 15 credits, ended with 1,525 credits and almost nothing to spend them on, and had the top reputation by the morning of Day 5. The story meanwhile says "one job today, Torres shadows you" and, on Day 2, "your first solo job".
3. **Taps and cards fight each other on a small screen.** In a crowd, a tap meant for a seat, a machine or the person with the star lands on whoever is standing nearest and opens their card. Tips, cards, arrow labels and see-through panels stack on top of each other.

Sixteen findings follow, ranked by how much they hurt, then a proposed fix list for phase 2 and the questions that are the user's to decide.

## How I played, and what I did not cover

- **By hand, at phone size (390 x 844, touch taps):** sign-on, the whole arrival evening (shuttle, Zeke's walk, bunk, device, dinner, the servery, bed and the alarm), Day 1 morning (waking, breakfast, the briefing, clocking in late, the job board, the shadowed job with Zeke, the lathe, turn-in), the fire drill (Day 3), the Last Light (Day 4), Sunday's Line crossing (Day 7) and the Tier 2 result meeting (Day 9). The last four were reached with Dev mode's clock and career jumps. Walking between rooms was partly real taps and partly jumps, to save time.
- **By an automatic player, Days 0 to 9:** a copy of RV32's fresh-walk tool, at phone size, that does only what the gold arrow says (goes where it points, taps the pin, takes the board's job, reads dialogue on) and sleeps at 22:30. I logged every tip, pop-up, line of dialogue, Mail and arrow change, and the needs and credits every ship hour. It finished with no errors and nothing stuck.
- **Limits, stated plainly.** The automatic player jumps instead of walking, so it does not feel distances; it sits through a rest once it starts one (so two things it "missed", the Day 3 drill and the Day 8 test, are its own fault and are not reported as findings). My test clock runs faster than real time, so I cannot judge how long pop-ups stay on screen, only that they overlap while they are up.
- **Not covered:** Sim night, the social stories, the ion storm, the later promotions, the ending, sound, the controller, saves. Days 9 and 11 were only sampled by Dev jump (the storm briefing, team jobs and Tier 2 work are there). What there is to do after week 2 still needs a proper play.

## What is working well

- **The voice.** Zeke ("Dinner. Always dinner first."), Calder ("Nobody thanks the air. That's how you know it's working."), Mum on the relay, Tomas panicking about inspection. Short lines, each person distinct. Mum reacting to things you actually did ("You went to the name on the beam!") is the best trick in the game.
- **The mess hall at dinner** looks and feels alive (shot 12).
- **Zeke really does shadow your first job** and talks you through storage, the shop and the repair, with good lines ("Listen. Nothing. That's the sound of it working.").
- **Crew notice your work** in passing ("Someone fixed the oven. The whole mess can smell it."). This is the "your work matters" pillar actually reaching the player.
- **Kind handling of mistakes:** "Clocked in at 09:30. A little late. It happens." and "Not done isn't failed. Another on Wednesday."
- **The drill now makes sense:** a toast at 14:50, an arrow, tap the Chief at 15:00, nine lines about fire, stand on the line, all-clear at 15:15. It played exactly as the design says.
- **The result meeting works** (Day 9, 08:15): toast, Mail, arrow from 08:00, heads-up, the talk, then crew outside saying "Officer on deck!".
- **Small rituals:** the name on the beam, the mug with your name on it, the Captain's all-hands card.
- **The alarm clock, the Settling in list, the heads-up strips with GO THERE** are all clear and useful.

## Findings, worst first

Each has: what happened, where and when, why it matters, a suggested fix, and its kind: **bug**, **polish** (both fixable now, behind a switch) or **design decision** (the user's, with my recommendation).

### 1. You can miss the Line oath without knowing it was on, and Mail then says you took it

- **What happened.** On Sunday Day 7, I stayed in my bunk room from 14:08 to 15:18. No gold arrow ever pointed to the bow lounge. At 14:11 a heads-up said "Invitation from Zeke Torres starts in 14 min, Bow lounge" (nothing about the Line) while the gold arrow said "Zeke wants a word" on Deck 5. At 14:30 the horn and the Captain's card ("First-timers, to the bow lounge"). At 14:44 a heads-up "The Line oath is starting". Then Mail from the Captain, "The Line oath (notes)": "You crossed the Line into the Veyli reach. The Captain read the old oath, you answered for the first-timers, and you drank Brennan's Line punch. Your certificate is on your shelf." I was never there. The automatic player had the same day: no arrow from 06:00 to 17:55, and the same Mail. (Shot 13: the only arrow that knows about the oath is Dev mode's magenta one.)
- **Why it matters.** This is the first big ship-wide event, built up for three days by the Captain, Dr. Sato and the crew. A player who follows the arrow, as the game has taught them to, misses it, and the game then tells them a memory they do not have.
- **Suggested fix.** (a) For a first-timer, a top-level gold arrow "The Line oath, 14:40: the bow lounge" from about 14:15 until it ends. (b) The heads-up names the event, not "Invitation from Zeke Torres". (c) If you were not in the lounge, the Mail says so in the Captain's voice (for example: "We read the oath without you. Your certificate is on your shelf all the same. Ask the old hands what you missed.").
- **Kind:** bug (the Mail) and polish (arrow, heads-up label).

### 2. Food drops to 0 and stays there for days, with one warning ever

- **What happened.** The arrow-following player got "Very hungry: Starving, tasks are 15% slower" once on Day 1 at 06:20, ate from the grab shelf (Food 33), and was back at 0 by noon. Food was then 0 for 11 hours of Day 1, all of Day 2, most of Day 3, and every waking hour of Days 4 to 9. No further warning on six of those days, and no Food arrow, even in evenings with no other arrow. The rule in the code: a warning is said once and only said again after the need has climbed back above a re-arm level; the marker is refused while any other arrow is up and is not asked again later.
- **Why it matters.** There are two meals and no lunch, the shift arrow runs straight through breakfast and into dinner, and nothing in the day's flow says "eat now". A new player either never notices food matters (the only cost is 15% slower work) or sees a red bar they cannot explain. It also makes the galley, the servery queue and the food simulation invisible to exactly the player who needs showing.
- **Suggested fix.** Polish: while Food is under 10, say the warning again each morning and each time the servery opens, and put the Food marker up whenever no other arrow is showing. Design decision for the user: should the day's own arrow include the meals (breakfast before the shift arrow, dinner after clock-out) during the first week? I recommend yes for week 1.
- **Kind:** polish, plus a design decision.

### 3. The work loop is a treadmill, and its rewards go flat within days

- **What happened.** From Day 2 the board's arrow starts at 06:00, three hours before the shift, and the jobs pay. Every job has the same shape: take it, sometimes fetch a part, stand through a bar of 10 to 30 ship minutes, travel back to the board on Deck 5 to turn it in, take the next. Nine days: 203 jobs turned in. Every one paid 15 credits, whether it was a 12-minute oven or a relay, a bracket made on the lathe and a 26-minute fit. Credits went from 40 to 1,525; the only prices I found in the store are 10, 12 and 15. Reputation went New, Steady (Day 2), Reliable (Day 3 07:36), Trusted (Day 4 07:03), Relied on (Day 5 09:45), which is the top; the next step in the career (Making it safe) was fixed to Day 8 whatever I did.
- **Why it matters.** The pillars say "work is physical" and "you grow by going deeper". In week 1 the work is mostly waiting on a bar and riding the lift back to the board, money stops meaning anything by Day 3, and reputation is used up by Day 5, so the two things that should make the next job feel worth doing are both gone before the first promotion. The user's own note, that the drills "don't make sense", fits the same pattern: the work around them does not ask much of the player either.
- **Suggested fix.** These are the user's calls. My recommendations: (a) no paid board jobs before clocking in (or a short "early start" allowance); (b) pay by the job's length and parts, not a flat 15; (c) a gentle daily stopping point (after a fair day's jobs the board says "That's a day's work. The rest will keep." and the arrow lets go); (d) slow the first-rank reputation steps so Reliable arrives around Day 6 or 7, just before the training that needs it; (e) give credits somewhere to go, or pay less.
- **Kind:** design decision.

### 4. In a crowd, your tap lands on a person instead of the thing you meant

- **What happened.** Four times in one evening and morning:
  - Mess hall, Day 0 19:25: tray in hand, "Find a seat and tap it to eat". 40 of 44 seats were taken and none of the free four was on screen. Every tap on a bench opened a diner's card (Lars, Asha, Hugo). I never managed to eat. (Shot 1.)
  - Machine shop, Day 1 09:43 to 10:40: the arrow said "Make a bracket at the lathe" with its pin on the floor spot in front of the lathe, where four people were standing. Every tap on the pin opened Maeve's card. The lathe itself was hidden behind them; tapping it directly worked at once. (Shot 7.)
  - Bunk 1, Day 1 06:06: a tap on my wardrobe's pin opened Tomas's card.
  - Bow lounge, Day 4 14:09: "Tap Dr. Sato to watch the Last Light"; my first tap on her did nothing I could see, the second joined. (Shot 8.)
- **Why it matters.** A pointer that says "tap here" and then opens a stranger's card is the clearest "the game is not listening to me" moment I found, and it happens in the busiest, best-looking rooms.
- **Suggested fix.** (a) When a tap lands on a person but the current arrow's pin (thing, place or person) is within a thumb's width, the arrow's target wins. (b) With a tray in hand, always point the arrow at the nearest free seat, not only when Food is very low (today's rule). (c) The pin over a place takes taps, as the pin over an item already does.
- **Kind:** polish.

### 5. The first minute: the arrow points at Zeke, and tapping Zeke does not take you to him

- **What happened.** Day 0 17:16, in the shuttle. The tip says "Tap where you want to go". The arrow points at Zeke. I tapped Zeke, then the arrow at the screen's edge, eleven times: each time his description card ("Engine officer. Zeke keeps glancing at the time...") and no step taken. A tap outside the deck does nothing at all. Only a tap on bare floor moves you. (Shot 2.) Later, a tap on a far-off diner did offer a card with WALK OVER, so the game has the idea; the guide in the first minute does not use it.
- **Why it matters.** It is the very first thing a new player does, and the most natural tap gives the least useful answer.
- **Suggested fix.** While someone is leading you, a tap on them (or on the edge arrow) walks you to them. More generally, a tap on the edge arrow walks you toward the goal.
- **Kind:** polish.

### 6. Cards, tips and labels pile up, and panels are see-through

- **What happened.**
  - Day 0 19:31, mess hall: a tip about bedtime, a person's card and a cut-off arrow label all at once, with the tip's last lines hidden behind the card, while I was holding a dinner tray. (Shot 1.)
  - Day 0 18:56: the "Your device" tip sits across the top of the device the moment you first open it. (Shot 11.)
  - The job board and the alarm card are see-through: the needs strip, a speech bubble and the room show through the text. (Shots 5 and 6.)
  - The stack in the top-left corner (place card, device button, needs, Schedule tracker) covers about the top quarter of the screen, and speech bubbles slide under it unreadable. (Shot 12.)
  - Arrow labels are cut off mid-word: "Fire drill, 15:00: Chief Calder at the Wo...", "Tap the lift: Deck 4 · Head to your bun...". The place is the part that is lost. (Shot 10.)
  - The time clock's panel opened on top of a person's card that was already open; closing one revealed the other.
- **Why it matters.** Each one is small; together they make the phone screen feel crowded at exactly the moments the game is trying to teach.
- **Suggested fix.** Solid backgrounds for the board and the alarm card; a tip waits while a card, panel or the device is open; the arrow's label wraps to two lines instead of cutting; opening a panel closes a person's card; bubbles keep clear of the top-left stack.
- **Kind:** polish.

### 7. The story says "one shadowed job" and "your first solo job"; the board says otherwise

- **What happened.** Day 1 08:50, Calder: "Torres. One job, end to end... Torres shadows you today. Every step." The board marks the shadow job clearly (good), but also offers four others, and after the shadow job the arrow simply leads on. The automatic player did 14 jobs alone on Day 1 and 7 more before 08:45 on Day 2, when Calder said: "Your first solo job... You'll do it alone." It was "the other light relay on Four", the same job as Day 1's.
- **Why it matters.** It is the "doesn't make sense" feeling again: the people are telling one story and the job board another.
- **Suggested fix.** Design decision. I recommend: on Day 1 the board holds only the shadow job until it is turned in, then two or three easy ones "with Torres nearby", and then says the day's done; Day 2's first solo job is a different machine.
- **Kind:** design decision.

### 8. The Last Light is over in one blink, and ends on a number

- **What happened.** Day 4. Dr. Sato says "One blink every eleven seconds", but the game shows a single 1.8-second blink at 14:08; I joined at 14:19 and saw only stars and a pop-up, "A pale light blinks past the windows". The lower half of the phone screen is empty space where the light could be. (Shot 9.) The moment ends with "The company helped. Leisure 97." Then Mail from Dr. Sato: "Good to see you at the Last Light. Same time next one?" for something that happens once a voyage.
- **Why it matters.** The build-up is good and the pay-off is a toast.
- **Suggested fix.** Blink every eleven seconds from about 14:05 to 14:20, as she says; end on a line of hers rather than the need read-out; no "same time next one" for one-off events.
- **Kind:** polish.

### 9. The same thank-you Mail after every event

- **What happened.** "Thanks for coming: Good to see you at X. Same time next one?" arrived after the Name on the beam (from Calder, a once-only event), Pick-your-own breakfast, the Last Light, the birthday (from Matthias, not the birthday person: "Good to see you at Birthday"), Quiz night, the Captain's Friday address (from the Captain herself), Harvest morning and Sowing morning. Eight in the first week, word for word.
- **Why it matters.** Mail is where the crew's voices live; a form letter from the Captain undoes that.
- **Suggested fix.** No thank-you for one-off events and the Captain's address; for the rest, a few lines in each host's voice (the writer's), and not every time.
- **Kind:** polish (words through content/).

### 10. Tips arrive days late or at the wrong moment

- **What happened.** "Slept well? Your bunk takes you from 20:00..." at 15:02 on Day 2. The "Your device" tip again at 06:01 on Day 2. "Your needs sit in the strip at the top" on Day 3 at 09:40. "Rotate turns the view. Walls lowers them... Pinch or scroll to zoom" on Day 4 at 21:03. "Need a break? Pause..." on Day 4 at 17:36. "There's a ship tradition today" at 20:44.
- **Why it matters.** The basics of looking around (rotate, walls, zoom) and of needs are things a phone player wants in the first ten minutes, not on Day 4. The four round buttons at the top right have no labels on screen until then.
- **Suggested fix.** Move the view, pause and needs tips into the arrival evening (there is a quiet stretch between dinner and 20:00); tie "Slept well?" to waking.
- **Kind:** polish.

### 11. The device shows 21 apps on the first evening

- **What happened.** Day 0 18:56, the moment Zeke hands it over: Schedule tracker, Settling, Schedule, Appts, Calendar, Needs, Pockets, Maps, Jobs, Mail, Memos, Hobbies, Music, People, Roster, News feed, Record, Tiles, Wallet, Saves, Settings. Four of them are about time. The home page's status lines push all but three apps off the first screen. (Shot 4.) In Calendar, every event has a button that just says "DON'T" (it means "don't remind me"), and the day's time bar labels each event by its first word only ("Sunday", "Sunday", "Name", "First"). (Shot 3.) People lists "Zeke Torres: stranger" after he has walked you round the ship, and "Tomas Lind: acquaintance" before you have met him.
- **Why it matters.** It is a lot to hand someone who does not yet know where the mess is.
- **Suggested fix.** Design decision: apps appear as they become useful (Jobs and Record on Day 1, Wallet with the first pay, Tiles and Hobbies when first offered), or are grouped. Polish now: "DON'T" becomes "No reminder" / "Remind me"; fuller bar labels; Zeke is at least an acquaintance once he has shown you your bunk.
- **Kind:** design decision, with polish items.

### 12. The first morning opens with "Starving" and "Bursting"

- **What happened.** Miss dinner on the arrival evening (easy: see finding 4, and the "Head to your bunk" arrow appears while you are still holding the tray) and you wake on Day 1 with Food at 8. At 06:20: "Very hungry. Starving: tasks are 15% slower." At 07:12: "Bursting. You really need the toilet, now!" The device's home page was already saying "You could do with a trip to the toilet" on the arrival evening, at 49 out of 100.
- **Why it matters.** Tone. The first words of your first working day are two alarms.
- **Suggested fix.** Start the arrival with fuller needs, or hold the firm warnings until after the first briefing; the "Head to your bunk" arrow waits until the tray is eaten or put down.
- **Kind:** polish.

### 13. The promotion arrives in 9 days; the design says about two weeks

- **What happened.** Making it safe on Day 8, the Tier 2 test the same day at 13:00, the result at 08:15 on Day 9: "You're an Officer from today." The design doc's milestone says "the first promotion (about 2 ship weeks of steady work)".
- **Why it matters.** With reputation already at the top on Day 5 (finding 3), the promotion reads as a date on the calendar, not something earned. Either is a fair design; the doc and the game should agree.
- **Suggested fix.** The user's call. If Day 9 is intended, update the design doc; if two weeks is, the reputation pace in finding 3(d) is the lever.
- **Kind:** design decision.

### 14. Small things that happen with no explanation

- Day 8 10:33, in the middle of the burst pipe lesson: a pop-up "Your job: The job isn't yours any more." No reason given. Suggest: "Calder's call comes first. Your job goes back on the board."
- The board's heading when your job is finished and waiting to be turned in: "You have a job. Finish it or drop it to take another." Suggest: "Your job's done. Turn it in."
- The time clock at 09:30: "Shift starts at 09:00. Tap to clock in." Suggest it says the shift has started.
- Day 9 08:22: Theo says "Pip suits you. Very shiny." eight hours before the pip is pinned (he has just said it is this afternoon).
- Day 1 06:06: Tomas greets you with "How was today, honestly? Got a minute to tell me?" It is an evening line, still on him at dawn.
- Signing on with an empty name does nothing and says nothing.
- **Kind:** polish.

### 15. Words: grammar, repeats and slips

- "The light relays is running sweetly again." / "The grow lights is running sweetly again." (plural machines).
- "Calibrate the oven 2", "Calibrate the oven 1".
- "Job taken: Take medical supplies to the infirmary, Deck 3, Deck 3 · infirmary." (the deck twice); the same for "Take dry goods to the galley", "Restock the ship's store", "Inspection round, Deck 3".
- Small jobs say their name in the title and again in the text: "Replace a lamp: lift lobby / Replace a lamp: lift lobby: about 15 minutes."
- The crates you load are called "Wednesday delivery" on Monday, Tuesday and Thursday too.
- Grab and go: "Rolls, fruit and juice, chilled... You take a hot plate of porridge and eggs."
- Quiz: "What does the lift say for the rec dec?" (deck). In `content/banks/quiz.lines`.
- Mum on the fifth call: "Hello, chick! Second time's easier."
- If the player's name is Sam, the call list offers "Call Sam".
- "Follow the marker" in pop-ups, "the arrow" in tips: one word would be clearer.
- **Kind:** polish (words through content/ where they live there).

### 16. Quiet stretches with no pointer (low)

- Day 1, 06:27 to 08:20, and most evenings and the whole of Saturday afternoon: no arrow. For evenings this is right (the heads-up strips and Calendar do the inviting). On the very first morning, two ship hours with nothing suggested is a long time for a new player; one soft suggestion ("Breakfast is on till nine: the mess, Deck 3") would do.
- **Kind:** polish, low.

## Proposed fix list for phase 2 (bug and polish only)

Each behind its own switch, off = identical to 0.99.91. In the order I would build them:

| # | Fix | From finding |
|---|---|---|
| F1 | The Line oath: a gold arrow for first-timers, the heads-up's name, and an honest Mail if you were not there | 1 |
| F2 | Food: the warning said again while Food is under 10 (each morning, each servery opening), and the Food marker whenever no other arrow is up | 2 |
| F3 | With a tray in hand, the arrow always points at the nearest free seat; "Head to your bunk" waits for the tray | 4, 12 |
| F4 | A tap next to the arrow's pin goes to the arrow's target before a bystander; the pin over a place takes taps | 4 |
| F5 | While someone is leading you, a tap on them or on the edge arrow walks you to them | 5 |
| F6 | Solid backgrounds for the job board and the alarm card; a tip waits while a card, panel or the device is open; a panel closes a person's card | 6 |
| F7 | The arrow's label wraps to two lines instead of being cut off | 6 |
| F8 | The Last Light blinks every eleven seconds through the passing; no need read-out as its last word | 8 |
| F9 | No form thank-you Mail for one-off events and the Captain's address | 9 |
| F10 | Tips: view, pause and needs taught on the arrival evening; "Slept well?" on waking | 10 |
| F11 | The small unexplained messages (the burst pipe's "isn't yours any more", the board's heading, the late clock, Theo's pip line, Tomas's evening line at dawn) | 14 |
| F12 | The words list (plural machines, "the oven 2", the deck twice, titles repeated, "Wednesday delivery", the grab shelf, "rec dec", "DON'T") | 11, 15 |

F1 to F5 are the ones a player would feel most. F6 to F12 are tidy-ups. If time is short I would do F1, F2, F3, F4, F9 and F12.

## Questions for the user (design decisions, with my recommendation)

1. **Day 1's board** (finding 7): only the shadow job until it is done, then a few easy ones? Recommended: yes.
2. **Meals in the day's arrow during week 1** (finding 2): breakfast before the shift arrow, dinner after clock-out? Recommended: yes, week 1 only.
3. **Work before clocking in** (finding 3): should board jobs be takeable and paid from 06:00? Recommended: no, or a small allowance.
4. **Pay** (finding 3): flat 15 a job, or by the job's length and parts? And what are credits for after Day 3? Recommended: pay by the job, and either more to buy or lower pay.
5. **A day's work** (finding 3): should the board ever say "that's enough for today"? Recommended: yes, a soft stop.
6. **Reputation's pace** (findings 3 and 13): top of the ladder on Day 5, or Reliable around Day 6 to 7? Recommended: slower.
7. **The first promotion's day** (finding 13): Day 9 as built, or about two weeks as the design doc says? Either way, make the doc and the game agree.
8. **The device's apps** (finding 11): all 21 from the first evening, or appearing as they become useful? Recommended: appearing as they become useful.
9. **Work that asks more of you** (finding 3): most week 1 jobs are a bar to wait through. The later mechanics (rounds, tuning, the scanner, head-scratchers) are better. Would you like one of them to arrive earlier in week 1, in place of some of the plain bars? Recommended: yes, rounds on Day 1 afternoon.

*Space for the user's answers: write under each question above, or tell the lead, and I will record them here.*
