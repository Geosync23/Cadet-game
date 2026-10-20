# Review of the nine work pools (TR1)

**Reviewer:** TR1, for TW1 and lead 20. **Reviewed:** `claude/talk-pack` at 7d88673: all nine
`content/talkpack/work-<pool>.talk` files (120 talks, 1,080 lines), every line, against `plans/work-pools-plan.md` as
decided by the user (2026-10-20: work and shared taking turns, once per save, friend tier about what the job means and
ending warm, Works treats you as a workmate), the roster, `ROSTER_ROTATIONS`, facts.md, the voice cards, the arcs and
themes, and the 160 talks already in the pack. Line numbers are the `.talk` files'.

## The plain summary

The pools are well built and they work. Every talk has the question and three replies with answers; lengths pass
lines_check; ids are unique; every talk has at least one person aboard who can say it (I checked each `who:`, `!who:`,
`rank:`, `dept:` and `!thread:` against the roster); arc and theme skips are mostly right; nothing is romantic, nobody
is bad at their job, there's no lunch. Works really does talk to you as a workmate, and there are lovely specific
touches: the Cart that pulls left, "Calder is the clock", the onion count (Varga by three), the store's tall Works
sock-loser, Zielinski's daily haggle, the Captain's "Lovely rock." On a phone at 390 px all 120 talks fit.

Three things to fix before they ship:

1. **The friend tier became a formula.** The plan's friend-tier list (what it means, who you do it for, a proud moment,
   a habit, what you'd teach) was applied in every pool, so the same question comes back from each department: "Has the
   job given you a habit you can't switch off?" is asked six times (Works, Watch, Survey, Comms, Garden, Infirmary),
   "Who do you do the job for, really?" four times, and **your** answer to the habit question is "I notice machines" in
   all six. Ten talks end on "nobody knows it was me, and that's fine". Keep each friend-tier shape in two pools at most,
   and give the rest something only that job has.
2. **Repeats across the whole pack:** eight lines are word for word the same as a line elsewhere (for example "Gerald.
   Obviously." is also Sato's; "Check twice, then switch it on." three times in all), and several talks restate an own
   or shared talk (the Watch office's view of the lift is Tomas's own joke; the Gerald nursery is the shared Gerald talk
   again; people-not-doors is Mensah's own "watching" talk).
3. **Food again:** 57 of the 120 light replies are about food or tea, and biscuits are in 25 of the 120 talks (more
   than the shared pool's 19 of 160, which the first review already asked to bring down).

Plus a handful of fact fixes: two crew who leave mid-year named without `!moved:`, Hart (a late sleeper) watering at
first light, people speaking of themselves in the third person (Varga and Dlamini on the onion count, Calder on her
own ear and her own skipped tea), Friday's quiet bay for crew who are off on Fridays, and the player's gran given a
job she doesn't have.

Counts: **0 blockers, 22 should-fix, 12 nits.**

---

## Should fix

### The friend tier: one shape per pool, not every shape in every pool

**P1. The "habit" talk six times, with the same player answer.** Asks: `work-works:321` "Has the job given you a habit
you can't switch off?", `work-watch:222`, `work-garden:70`, `work-infirmary:101`, `work-comms:95` ("changed how you
hear things"), `work-survey:209` ("changed how you see ordinary things"). Your share reply in each: "I check every lamp
I walk past" (`works:324`, and again `infirmary:104`), "I listen to every machine I pass" (`watch:225`), "I can't stop
listening to machines" (`survey:212`), "I hear every machine's mood now" (`comms:98`), "I tap every panel I pass"
(`garden:73`), "Every machine that's slightly off" (`galley:98`). Keep the habit talk in **Works** (it's yours) and
**Watch** (counting exits is the best one); turn the other four into something only that job has:
- `work-infirmary` listening-habit → keep the opener (breathing is lovely) but change the ask to
  `ask: What do you notice about people that you wish you didn't?` and share `listen: Do you notice it on yourself?` /
  `  them: Never. Doctors are terrible patients. Aides are worse.   #funny`; share `share: When someone's tired before they say it.` /
  `  them: Then you've got it too. Careful. It doesn't switch off.   #warm`.
- `work-comms` comms-habit → make it about the relay delay: `them: The job gave me patience. Everything we send waits twelve hours in the dark.` /
  `them: I used to hate the wait. Now I like it. It's a kind of hope, travelling.   #warm` /
  `ask: What's the longest you've waited for good news?` / share `share: A letter from home. Weeks, once.` /
  `  them: Then you know the hope. Comms just gets to hold it for everyone.   #warm`.
- `work-survey` stars-habit → it's close to Tomas's world (stars, windows); change the share to
  `share: I count the windows on every deck.` / `  them: Tomas does that. Twenty-two. Ask him to show you his.   #warm` (Tomas is Watch, so he never draws it).
- `work-garden` green-hands → share `share: I water anything that looks thirsty.` / `  them: Ha. Then you're one of us. Gerald approves.   #funny`.

**P2. "Who do you do it for?" four times** (`works:297` "Who do you do the job for, really?", `survey:245` "Who are you
doing all this for, really?", `watch:210` "Who do you do your job for, if you had to name them?", `infirmary:89` "Who do
you do the job for, if you had to say?"), and two of the answers are word for word the same ("The people who'll never
know I did it." `watch:213` and `infirmary:92`; "My family. And the crew, now." `works:300` and `survey:248`). Keep it in
Works and Infirmary; change the other two asks:
- `work-watch:210` → `ask: What's the hour you'd least like to give up?` (fits "there's always a face in the Watch
  office"); share `share: The first hour of shift, before it's busy.` / `  them: Same. That's when the ship tells you how she slept.   #warm`.
- `work-survey:245` → `ask: Would you want your name on a chart one day?`; share `share: Maybe. Somewhere small.` /
  `  them: Small's where the good names go. I'll remember you said that.   #warm`.

**P3. "Nobody knows it was me, and that's fine" ten times.** `works:185` nobody-sees, `works:295` asleep-upstairs,
`works:343` what-it-means, `works:355` night-shift-meaning, `watch:208` what-watch-means, `infirmary:87`
infirmary-means, `comms:81` comms-means ("Nobody knows it was you"), `garden:56` garden-means, `galley:81` feed-people
("Nobody thinks. Everybody's glad"), `bridge:72` helm-means ("never think about it"), on top of the shared pool's
`pool-work` invisible and Calder's own `calder.air`. It's a good idea, said once or twice. Keep asleep-upstairs and
feed-people; rewrite the rest to the job's own pride:
- `work-works:183-193` nobody-sees → replace with a talk about the job card: `them: I like the moment you sign a job off. Pen on the card. Done.` /
  `them: Calder reads every one. You can tell which ones she liked. She puts them square on the pile.   #funny` /
  `ask: What's the best bit of finishing something?` (keep the rest's shape; cheer not a food joke).
- `work-works:353-363` night-shift-meaning repeats asleep-upstairs (both: walking past sleepers, "what the job's for").
  Make it about the day crew: `them: On nights, I leave the day lot the bay the way I'd want to find it.` /
  `them: Tools back, bench wiped, a note on the board. That's the whole job, really. Handing over well.   #warm` /
  `ask: What do you hand over well?`.
- `work-bridge:72` helm-means "Seventy-five people asleep while I take them somewhere" is said by day-shift helm too:
  → `them: Know what the helm means to me? Seventy-five people living their day while I take them somewhere.`
- `work-comms:86-87`, `work-garden:59-60` and `work-watch:213-214`: change the answers so they aren't "nobody knows /
  nobody thinks": comms `them: That's the best memory to leave. "It just worked." Sounds dull. It isn't.`; garden
  `them: No. And that's fine. They come in and breathe. We count that as applause.   #funny`.

**P4. The same ask twice inside Works:** `works:211` "Is there a place aboard that feels like it's yours?" and
`works:417` "Is there something aboard that feels like it's partly yours?". Change `works:417` (light-on) →
`ask: Is there something you check on, just because it's yours?`.

### Repeats across the pack

**P5. Word-for-word repeats** (change the work line):
- `work-survey:104` "Gerald. Obviously." / "The cactus lobby..." is Sato's own `sato.talk:28-29`. → `cheer: "Lamp." After my first job.` / `  them: Sentimental. And very Works. I'd allow it.   #funny`
- `work-survey:126` and `work-works:238` "Check twice, then switch it on." (and `pool-work` good-at-it's "Check twice,
  then turn it on."). Keep the shared pool's; Works `:238` → `share: Ask before you open anything live.` / `  them: That's the Works prayer. Calder would sign it.   #funny`;
  Survey `:126` → `share: "Measure it, then measure it again."` / `  them: That's Works's version of ours. Same advice, different tools.`
- `work-comms:26` "My family. Not often enough." is `pool-home:22`. → `share: My sibling. Every week, short.` / `  them: Short and every week beats long and never. They'll keep them all.   #warm` (you have an older sibling, Jo).
- `work-works:180` "Trial and error. Mostly error." is Pell's own `pell.talk:53`. → `cheer: Whoever was nearest. Usually wrong.` / `  them: Wrong teaches too. Slower. Louder.   #funny`
- `work-survey:124` "Who said it?" is `pool-news:94`. Fine as button text; leave it (N2).
- `work-infirmary:104` "I check every lamp I walk past." and `work-works:324`: covered by P1.

**P6. Talks that restate an own or shared talk:**
- `work-watch:22-32` lift-view opens with Tomas's own joke, nearly word for word (`tomas.talk` windows: "The Watch
  office has the best view of the lift. And so of everyone."). → `them: From the Watch office you see the lift doors all day. Tomas says it's the best view aboard.` /
  `them: He's not wrong. You learn who's late, who's early, who holds the lift. Nice people hold the lift.   #warm`
- `work-watch:120-130` people-not-doors is Mensah's own `watching` talk ("You watch people, too. Not just doors. Who's
  eating. Who's quiet.") and Mensah can draw both. Add `!who:mensah`, and rewrite the opener so it isn't the same
  thought: `them: The best Watch tool isn't a scanner. It's a cup of tea, offered at the right door.` /
  `them: Half our rounds end with a chat. Holt calls it "patrolling". We don't argue.   #funny`
- `work-garden:18-28` gerald-nursery is the shared `pool.hobby.gerald` again (same facts, same ask, "something green by
  my bunk" twice). Make it about the work of the nursery: `them: The Gerald tray needs turning every morning, or they all lean the same way.` /
  `them: Seventeen in there right now. Each one's somebody's, soon.   #warm` /
  `ask: Is there a job you do that's really for someone you haven't met yet?` (listen `Who gets the next one?` /
  `  them: Whoever needs one. You can always tell. They stand very still by the tray.   #warm`).
- `work-galley:55-65` learned-by-ear: the listen answer "Like a crowd before the speech. Then it settles." is Brennan's
  own answer ("Quieter. Like a crowd settling.", `brennan.talk:37`). → `  them: Busier. Then a click, a sort of sigh. Then you take it off.`
- `work-works:109-119` cart / `work-works:61-71` tool-wall: fine. `work-works:61` repeats Kovac's own spanners talk
  (seventeen and fourteen) on purpose as a nod; keep, it reads as one.
- `work-works:41` ask "Which machine aboard do you like working on most?" is close to Torres's own coil-three ask; fine
  (different answers), noted.

### Food

**P7. 57 of 120 cheer replies are about food or tea; biscuits in 25 talks.** Change at least fifteen of the cheers. The
plainest repeats first (all `cheer:` lines): `works:58` "Biscuit rankings", `works:192` "Eating the last biscuit so
nobody fights" (Halloran's own "Eating the last biscuit. For the team."), `works:314` "Finding the good biscuits first",
`watch:43` "The last biscuit. Fiercely.", `watch:79` "Only a list of good biscuits.", `watch:203` "Sharing my biscuits.
Twice.", `watch:239` "Second breakfast. Every day." (also `pool-food`'s), `survey:30`, `survey:90`, `survey:140`,
`survey:152`, `survey:202`, `survey:226`, `comms:16`, `comms:76`, `comms:100`, `store:14`, `store:50`, `galley:100`,
`garden:63`, `infirmary:18`, `infirmary:94`, `infirmary:106`. Suggestions in the voice of a Works junior, not food:
"Racing the lift doors. I lose.", "The noise the
washer makes on spin.", "My bunk's reading lamp. It's mine.", "Being first to the board on Monday.", "Holding the door
for nobody. Habit.", "Getting the good stool at the tea corner." (that one's tea: fine once).

### Facts and conditions

- **P8.** `work-survey:45-55` chart-room "Usually Zamora. Usually right.": Zamora leaves on day 161 → add `!moved:zamora-quinn`.
- **P9.** `work-survey:57-67` telescope-four "Four people brought telescopes": Zamora and Ueda leave on 161 → add `!moved:zamora-quinn|ueda-vera` (then "four" stays true).
- **P10.** `work-bridge:10-20` drift "Lindqvist feels it first": Lindqvist leaves on 119 → add `!moved:lindqvist-isak`.
- **P11.** `work-galley:19-29` onions "Varga, by three. Dlamini says it's rigged.": Varga and Dlamini can draw it and talk
  about themselves in the third person → `!who:brennan|madsen-ivo|varga-tariq|dlamini-lukas`.
- **P12.** Calder can draw talks that speak of her as someone else (the file header says she "skips almost all of
  these", but these don't skip her): `work-works:49-59` tea-corner ("Best ten minutes of the shift": she gave up her tea
  break), `:73-83` loud-bay ("Calder has the best one aboard"), `:195-205` proud-skill ("Calder can do it from the
  corridor"), `:365-375` bay-quiet, `:305-315` proud-moment already skips her. Add `calder` to each `!who:`.
- **P13.** Night crew drawing day-only talks: `works:49` tea-corner ("Tea at one": they're asleep), `works:73`
  loud-bay ("The bay's loud in the morning"), `works:133` briefing (Monday ten to nine), `works:365` bay-quiet ("Friday,
  five o'clock"): add `!who:navarro-mateo|reyes-alejandro|keane-davi|jovanovic-petra|kowal-priya`. And night crew in
  Watch: `watch:182-192` all-present ("End of a night round") is said by day ratings too → `who:mensah|achterberg-lars|garcia-greta|park-noor|castellano-jem`,
  and `watch:84-94` why-watch "Seventy-five, every night" → "every shift".
- **P14.** `work-works:365-375` bay-quiet "Friday, five o'clock": Torres and Moreau are off Thursday-Friday, Volkov
  Friday-Saturday (facts 3; the head writer's rule: a day named must match the rota). Add `torres-zeke|moreau-signe|volkov-maeve`
  to its `!who:` (with P13's night crew).
- **P15.** `work-garden:6-16` first-light "Hart waters the garden at first light, before anyone's up": Hart's roster
  habit is `late-sleeper`. → `them: Hart does the first watering, start of the early team. Every day. Without fail.`
- **P16.** `work-watch:141` parent-served cheer "My gran ran the school canteen" gives your gran a job she doesn't have
  (facts 4d: the allotment, the village show, "the box"). → `cheer: My gran grows prize marrows. Very strict.` /
  `  them: Then you come from careful people. Holt would approve.   #funny` (it also drops "security people").
- **P17.** `work-works:159-169` why-works (the clock taken apart at six) and `:317-327` hear-it-everywhere ("My family
  thinks I'm odd") and `:401-411` family-trade ("Nobody in my family fixed things"): Torres's father was an engine man
  for forty years (his arc), so these contradict him; Pell's mum runs a mending shop. Add `torres-zeke|pell` to each
  `!who:` (family-trade and hear-it-everywhere have Pell already).
- **P18.** `work-watch:194-204` proud-watch "A junior got lost on Deck 2 their first week": from Tomas it's about
  himself. Add `tomas` to its `!who:`. And `watch:96-106` holt-lectures ("I learnt the Watch from Holt... for a month")
  is wrong for Tomas (aboard a week before you) and the two who arrive later already trained (Dufresne the cadet,
  Castellano): add `tomas|dufresne-cora|castellano-jem`.
- **P19.** `work-watch:84-94` why-watch is "why they really came aboard", the `startover` theme's beat 2 (Mensah, Dahl,
  Takahashi; the file skips stuck and leaving only) → `!thread:stuck|leaving|startover`. Same for `works:159` why-works
  and `survey:107` why-survey (`!thread:...|startover`; nobody in those two pools has it today, but it keeps them safe).
- **P20.** `work-survey:167-177` night-survey: the tin is Ibarra's (facts 5: Ibarra's secret biscuit tin; Pell found it
  and left a card). From Lemaire, "I won't tell you where the good tin is" claims it. → `who:ibarra-rafael`.
- **P21.** `work-watch:242-252` thursday-checks "Juniors dread it. I love it": the ratings are juniors who are inspected
  themselves. → `when: tier>=friend !rank:junior !who:holt` (Mensah, Dahl, Achterberg, Castellano).
- **P22.** `work-works:207-217` engine-room "First week, I couldn't sleep without it. Now I can't sleep without it.
  Opposite reasons." says the same thing twice. → `them: First week, I couldn't sleep for it. Now I can't sleep without it.   #funny`

## Nits

- **N1.** "Second drawer" for the tape three times in Works (`:79`, `:241`, `:446`): a running joke, but three in one pool
  is one too many; drop `:241`'s.
- **N2.** Replies repeated as button text ("Who said it?" `survey:124`, `pool-news:94`): harmless.
- **N3.** `work-works:13-23` hands: "My bunkmates call me 'the engine room'" fits engine techs, not a bay tech with
  machine oil → `"the oil can"`.
- **N4.** `work-works:25-35` board-first "one red card": the job board in the game has no red cards that I can find;
  "one urgent card" is safe.
- **N5.** `work-works:121-131` tea-rota-mug: listen "When did it feel like yours?" repeats the ask back (the first review's
  S29). → `listen: How long has your mug been up there?` / `  them: Since my first Friday. Same hook. I'd notice if it moved.   #warm`
- **N6.** `work-watch:93-94` "Watch grey": I can't find a Watch uniform colour in facts.md; check it before naming it
  ("The orange was taken" is fine either way).
- **N7.** `work-survey:78-79` "The dinner bell." / "There isn't one.": Pell's own lines have a music box that "plays the
  mess bell", so the ship may have one. → `cheer: The kettle at the tea corner.` (Watch uses it too, `watch:19`: pick another, e.g. `The lift chime.`).
- **N8.** `work-garden:36` "Thank you SO much" in capitals: the house style doesn't shout in capitals → "Thank you *so*
  much" isn't possible on a card; "Thank you so very much." does it.
- **N9.** `work-comms:7-17` static: the listen answer tells what was in someone's call ("Somebody's gran, calling to say
  happy birthday"), against the file's own rule "never what's in anyone's messages". → `  them: Can't say. Comms rules. But it made my whole night.   #warm`
- **N10.** `work-comms:79-89` comms-means "a call home at three in the morning... I put that call through" from day
  Comms crew; and `work-watch:209`, `work-infirmary:88` "Tonight, it's mine" / "Tonight, maybe me" from day crew →
  "Today, it's mine." / "Today, maybe me."
- **N11.** "Then we're the same" (or "same family", "we're the same, you and me") ends 8 of the 120 answers. Vary four.
- **N12.** "Seventy-five / seventy-odd" in 8 work talks (and the shared pool's). Keep three.

## What I checked by script

- Shape, lengths, ids: content_gen bakes 280 talks; lines_check PASS (0 errors); my shape script clean.
- Every work talk's conditions against the roster: each has at least one speaker (17 talks have one or two, all by
  design: night helm, command, bar, store, night Survey, Yoon, Takahashi, the three parents who served).
- Exact repeats across all 280 talks: 8 (listed in P5 and P2). Near-repeat asks: listed in P1, P2, P4.
- Food: 57 of 120 work cheers; biscuits in 25 of 120 work talks.
- In the game (a local merge with TE1's ebd69b6): the take-turns order holds for every pool, and all 2,520 card views fit
  at 390 px. See the addendum in `plans/talk-wire-review.md`.
