# Review of the "Talk a while" pack (TR1)

**Reviewer:** TR1, for lead 20. **Reviewed:** `claude/talk-pack` at f6005cf: all 26 files in `content/talkpack/` (100 pool
talks, 15 own sets of 4, smalltalk) and `plans/talk-pack-plan.md`, every line read. Checked against `CLAUDE.md`,
`content/README.md`, `content/facts.md`, `content/voice-bible.md`, `design-doc.md` ("Talking"), the voice cards, the arc
outlines and `.arc` files, the theme `.arc` files, `content/banks/talk.lines`, the traditions and the game's ROSTER.

## The plain summary

The pack is good, and close to ready. It sounds like the Wren: kind, light, specific, funny in the right places. Every
talk has the shape the user asked for (their question, your three replies, an answer to each), all 160 talks pass the
length and shape checks, every id is unique, every crew id in a condition is real, and the voices of the story crew
are mostly spot on (Calder's numbers, Tomas's "sort of", Rina's count, Vance's threes, Saruth's no-contractions).

What needs fixing before the engineer bakes it:

1. **Seven blockers.** Four own talks retell a story beat word for word or give it away early: Torres's scarf (his beat 1
   is the surprise), Holt's "nearest suit locker, don't look" (his beat 1), Holt going in for tea with the Envoy (his
   beat 4), and two of the Captain's (her beat 1's "I write the answers down" and her beat 2's Admiral theories, down to
   the cat joke). Two pool talks call the lift club by name, which is Kovac's secret until her beat 2. And two pool
   talks use `{hobby}` so it reads as broken English for everyone ("I've had knitting scarves since I was small").
2. **Facts that clash with the game:** there's no lunch on the Wren (five lines), Brennan is off on Fridays, you have an
   older sibling (Jo), doors open by themselves, Knit and natter is Tuesday in the junior common room, the helm crew
   already work on the bridge, a dozen crew named in talks leave the ship partway through the year.
3. **Overlaps with the struggle themes:** some pool talks are the same story a theme tells later (homesick, "I'm not good
   enough", the transfer list, a secret hobby). A new condition word, `!thread:<theme>`, fixes these in one go.
4. **Repetition:** 45 of the 160 "light" replies are jokes about food (biscuits in 19 talks, Brennan named in 30). Some
   tics are too thick: Holt says "Hm." nine times in four talks, Mensah "Ha!" eight, Kovac "Um" eight.
5. **The plan's data shape is implementable,** with a few gaps to close (below): fired ids must use the file's topic, the
   "talked about lately" and "not twice running" rules need saved state, the old `talk.<topic>` lines need retiring, and
   one design consequence the user should hear plainly: with the pool fired once per save, a keen player runs it dry in
   about a month and then hears only small talk from most of the crew for the rest of the year.

Counts: **7 blockers, 38 should-fix, 30 nits.** Each has the file and line and a proposed fix in the right voice.

---

## Blockers

**B1. `torres-zeke.talk:17-28` (scarf-rows) gives away Torres's beat 1.** Beat 1 "The scarf" is the reveal that he's
knitting you a scarf ("Don't look. It's a surprise."). Every other scarf line in the game waits for it
(`content/lines/torres-zeke.lines:3-4`, gated `mem:moment.torres.scarf`). This talk says it's for you at acquaintance.
Fix: gate it after the beat and let it be the running joke.
```
when: tier>=colleague mem:moment.torres.scarf
them: Two more rows on your scarf. Don't look. Fine, look. It's coming along.   #funny
  (L26) them: Orange! Works orange. Good. Because that's what it is. Too late now.   #funny
  (L28) them: Ha! Practical. I'll knit a gravy row in at the end. For you.   #funny
```

**B2. `holt.talk:6-16` (nearest-locker) is Holt's beat 1 word for word.** Beat 1 "Don't look": "He tests you: 'Nearest
suit locker. Don't look.'" Telling it twice breaks the user's no-repeats rule. Replace the talk (nothing has shipped,
so the slug can change now; never after the engine bakes it):
```
== doors
topic: ship
them: Hm. Cadet. Every door on this ship has a number. I know all of them.
them: Not to show off. Because one night someone will need to know, and I'll be awake.
ask: What do you check before you sleep? Everybody checks something.
listen: Do you really know every door?
  them: Every one. Ask me one. Go on. Thought not.   #funny
share: That my boots are where I can find them.
  them: Boots by the bunk, facing out. Adequate.
cheer: Under the bunk. Just in case.
  them: Fair. The Watch checks the rest. That's what we're for.   #funny
```

**B3. `holt.talk:44-55` (saruth) tells Holt's beat 4 early.** It's gated `beat:holt.2`, but the listen answer has him
going in for tea, kneeling, knees with opinions: that's beat 4 "Tea" (the Envoy invites him through you; "They kneel. My
knees aren't built for it."). Keep the talk at the slow-thaw stage:
```
(L48) them: I don't trust the Veyli. Said so, plainly, to their face. They thanked me. I don't know what to do with that.
(L51)   them: No. Stood at the door a while. Walked on. Another time, maybe.
```
(L48's "Odd people." also goes: the voice bible's rule 7 says never a joke about the Veyli as a people.)

**B4. `marrow.talk:140-151` (admiral) is the Captain's beat 2.** Beat 2 "The Admiral": she collects the crew's theories,
asks for yours, and the cat reply gets "There are no cats aboard. Officially." This talk is the same scene with the
same punchline. Replace it with another canon thing of hers (facts 11: her quiz team came third):
```
== quiz-third
topic: tradition
when: tier>=colleague
them: Our quiz team came third. Third. I have commanded this ship for six years.
them: Commander Vance says third is a podium. He said it very quietly.   #funny
ask: What would you be hopeless at, in a quiz? Be honest. I was.
listen: What was your weak round?
  them: Engines. Calder answered every one before I'd read it. I held the pencil.   #funny
share: Anything with dates. I'm hopeless.
  them: So am I. I remember people, not dates. It's a fair trade, most days.   #warm
cheer: Every round. I'd bring moral support.
  them: Then you'd be our most useful member. I'll save you a chair.   #funny
```

**B5. `marrow.talk:115-125` (one-question) retells her beat 1 and asks the ready-room question again.** Beat 1: "I asked
you one question when we first met... I write them all down." The ready room (`readyRoomFirst`) already asks "what does
this ship need that the senior crew can't see?"; this talk asks "What's one thing on the Wren you'd change?". The opener
is muddled too ("Today's is an easy one. Mind the step on your way in" isn't a question, and you aren't in the ready
room), and the cheer has a slide from Deck 4 *down* to the mess, which is on Deck 3, above it. Replace:
```
== the-step
topic: ship
them: The step in the ready room. Everyone trips on it. I've had it measured. It's a perfectly ordinary step.
them: Commander Vance has tripped on it twice. He would like that kept quiet.   #funny
ask: Is there a spot aboard that always catches you out?
listen: Why not have it fixed?
  them: It's older than I am. Some things you keep because they keep you humble.
share: The lift doors. Every time.
  them: They're quick. Step in like you mean it. That's most of command, too.   #warm
cheer: My own feet, mostly.
  them: Join the club. It's a large club. I'm in it.   #funny
```

**B6. The lift club is named as a known thing, which is Kovac's secret until her beat 2.** Canon (facts 5): each of the
three thinks they're the only one; Kovac's beat 2 is "We're a club. Oh no. We're a club."
- `pool-hobby.talk:38` → `them: The lift would never recover. Nor would the people in it.   #funny`
- `pool-crew.talk:26` → `them: Good choice. It never interrupts.   #funny`

**B7. `{hobby}` makes broken sentences.** `{hobby}` is the roster's verb phrase ("knitting scarves", "learning the
guitar, badly", "looking after a cactus called Gerald"); `{hobbyNoun}` is the noun ("knitting", "guitar").
- `pool-hobby.talk:78` "I've had {hobby} since I was small. It came with me from {home}." reads "I've had learning the
  guitar, badly since I was small" for everyone, and the idea is wrong for ~25 crew whose hobby started aboard (the guitar
  book, the Geralds from Cruz, the comics wall, tiny portraits of the crew, flowers from the garden, crosswords in the bow
  lounge, letters and messages home, Raman's model of the Wren). Rewrite it about something packed, not the hobby:
  ```
  them: Funny what you pack. I brought half of {home} in one small bag.
  them: Some things you pack without thinking.
  ask: What did you bring aboard that you couldn't leave behind?
  listen: What did you bring?
    them: A cup that matches nothing aboard. It's perfect.   #warm
  ```
  (share and cheer stay.)
- `pool-hobby.talk:90` "teaching {friend} a bit of {hobby}" → `them: I've been teaching {friend} a bit of {hobbyNoun}.`
  and add `!who:kowalczyk|achterberg-lars|moreau-signe|soto-marta|vasquez-uma|kim-yusuf|castellano-jem` ("a bit of
  reading" reads like teaching someone to read).
- `pool-hobby.talk:18` "I'm not very good at {hobby}" gives "not very good at brewing terrible tea" and "telling terrible
  jokes"; and from Rina (undefeated at Tiles) and Calder (her hobby is fixing broken things) it contradicts canon.
  → `them: Can I tell you a secret? I'm not very good at the thing I do for fun.` and `when: !who:rina|calder`.

---

## Should fix

### Clashes with established facts or the game

- **S1. No lunch aboard** (design-doc 815 "Two meals a day, no lunch"; 819 lunch answered no).
  `pool-day.talk:101` "I said sorry at lunch" → "I said sorry at tea."; `pool-day.talk:107` → `cheer: Start it again after tea.`;
  `pool-plans.talk:36-37` → `cheer: Half a day at a time. Tea's a milestone.` / `them: Tea at one is a milestone. Put it on a poster.   #funny`;
  `halloran-emeka.talk:84` "Close enough to lunch" → "Close enough to dinner."
- **S2. `pool-food.talk:90` Brennan "made a dish from {home} last Friday":** Brennan's days off are Friday and Saturday
  (Dlamini cooks). → "Brennan made a dish from {home} last week."
- **S3. `pool-news.talk:38-39` twins:** you have an older sibling, Jo (facts 4d), so "Not that I know of. I'll check." is
  wrong. → `cheer: One. Older. They think they're in charge.` / `them: They always will. It's in the rules.   #funny`
- **S4. `pool-day.talk:92` "Held a door with my foot":** the Wren's doors slide open by themselves (design-doc 673).
  → `them: Took the other end of a crate. Tiny thing.`
- **S5. `kovac-zainab.talk:75` "The knitting circle's at the tea corner tonight":** the game's Knit and natter is Tuesday,
  20:00, in the junior common room (`traditions/knit-and-natter.trad`). → `them: Knit and natter's on Tuesday. Junior common room. Me, Dahl, Torres.`
- **S6. `pool-plans.talk:39-49` (bridge) "One day I'd like to see the bridge":** the helm crew (and command) work there
  every day. Add `!dept:helm|command`.
- **S7. Crew who leave partway through the year are named as if they're aboard for good.** The roster's `aboard` field
  takes Teague off on day 35, Moreau and Alvarez on 77, Lindqvist and Santos on 119, Grieve and Haddad on 203. Add the
  existing `!moved:<id>` condition:
  - `pool-hobby.talk:53` comics-wall: `!moved:teague-theo`
  - `pool-hobby.talk:101` guitar-book ("Four people"): `!moved:lindqvist-isak !moved:haddad-tamsin`
  - `pool-news.talk:42` lost-property ("four boxes"): `!moved:grieve-thea`
  - `pool-plans.talk:52` five-years: `!moved:santos-zofia`
  - `vance.talk:76` leaderboard ("Lindqvist, Santos, Moreau": all three leave, on days 77 and 119): drop the names →
    `them: Three juniors are chasing my name. I am not worried. Noted.   #funny`
- **S8. `pool-work.talk:52-62` (well-done) "{boss} said 'nice work'":** for every Works speaker `{boss}` is Calder, who
  never praises like that ("Good. Clean work." only; her "well done" is her arc's payoff), and the same talk's share says
  so ("Calder said 'Good.' Once."). Add `!dept:works`.
- **S9. `pool-news.talk:74` "Tomas talks to the stars. Out loud."** isn't canon. → `cheer: Tomas counts the windows. Out loud.`
  (canon: 22 windows). Same talk: add `!who:tran-chloe|santos-zofia|dlamini-lukas` (your bunkmates: you'd be in the vote).
- **S10. `pool-ship.talk:104-105` (kind-ship) "Have you served on other ships?" "One or two."** Tomas (and the juniors two
  or three months out of training) haven't. → `listen: Has she always been like this?` / `them: Longer than anyone aboard can say. Ask the portraits.`
- **S11. `pool-home.talk:38-48` (sky) "At {home} I mostly looked at the ground. Puddles."** "At Port Halloran" is odd
  English, and Marra Station, the Tevan belt and Hesper Dock are stations: no sky, no puddles.
  → `them: Out here the sky's all stars. Back home I mostly looked at my feet.   #funny` / `them: My shoes, mainly. Now look at me.`
- **S12. Tomas's `{home}` is "a farm moon with a grey sky"** ("Got a letter from a farm moon with a grey sky.").
  Either the roster gets a short home for him, or add `!who:tomas` to the `{home}` talks: pool-home smell, letter,
  cooking-home, leave-one-day; pool-food home-dish; pool-hobby starting-young.
- **S13. `pool-home.talk:5-14` (smell)** names Brennan in the listen answer: add `!who:brennan`.
- **S14. `pool-day.talk:98-108` (bad-start) "I said sorry"** from Holt breaks his card ("never says 'I'm sorry' plainly").
  Add `!who:holt`.
- **S15. `pool-food.talk:28-38` (tried-to-cook) "Can you cook? I burnt toast."** skips the galley but not the bakers and
  cooks: add `halloran-emeka|tran-chloe|yilmaz-karin|mbeki-bo` (and the newcomer bakers `mwangi-rafe|achebe-lumi|quaye-hiro|kowal-priya`).
- **S16. `halloran-emeka.talk:88` mug-rack `aboard>=5`:** the end hook is yours only if you had the Day 5 tea. Use the
  game's own flag: `when: tier>=colleague flag:mug` (used by halloran's lines already). Then `aboard>=` is only used by
  `pool-work.talk:113`, which could be `rep:known` instead, and the engine needs no new word.
- **S17. `smalltalk.talk` is said by Saruth too, with contractions** ("isn't it", "I'm", "We've"). Saruth never uses them.
  Add a set the engine uses for Saruth (and Veyli guests):
  ```
  == small.saruth
  - It is pleasant, to sit a while.
  - The ship is quiet. I like her quiet.
  - Your people knocked twice again today. Very consistent.
  - The seedlings lean towards the lamps. So do I, some evenings.
  - I have nothing to report. That is a good report.
  - You are here. That is enough news.
  == done.saruth
  - We have said everything, I think. Then we may sit. That is also a conversation.   #warm
  - Nothing is left to tell. I find I do not mind.   #warm
  ```
- **S18. `smalltalk.talk` lines tied to a time of day** play at any hour: L119 "quiet tonight" → "The ship's quiet just
  now. I like her quiet."; L124 "Did you get dinner?" → "Have you eaten? Good. Just checking."; L134 "all evening. Shame
  about bedtime." → "I could sit here for hours. Shame about the clock." (L134 is also nearly `talk.filler`'s line.)
- **S19. `nandakumar.talk:154-165` (garden-hour) vs her thread.** Her roster thread is `burnout` (never stops, can't say
  no). "I don't fix anybody for an hour... I like it" says the opposite before the theme gets there. Keep the hint level:
  ```
  them: I'm meant to sit in the garden for an hour off duty. Oduya's orders.
  them: I manage ten minutes. Then I think of something. I'm working on it.   #funny
  ```

### Story arcs and themes the pool steps on

Most of these are cleanest with one new condition word, **`!thread:<theme>`** (the speaker's roster `thread`, which the
engine already reads). Without it, the `!who:` lists below do the same job.

- **S20. Secret hobbies (`talent`):** the theme's beat 2 is "Nobody aboard's ever seen it. You're the first." The pool
  hobby talks have them chatting about it openly. Add `!thread:talent` (Ibarra, Silva, Quist, Jovanovic, Amadi, Juarez)
  to `pool-hobby` one-hour, bad-at-it, teach-me, rest-day.
- **S21. `pool-home.talk:5-14` (smell)** is the `homesick` theme's beat 1 almost word for word ("Smelt bread in the mess
  and I was back on {home}"). Add `!thread:homesick`. Same for `pool-home.talk:110-120` (homesick), plus `!who:tomas`
  (his first month is now).
- **S22. `pool-work.talk:40-50` (mistake) and `:100-110` (pressure)** are the `notgood` theme's beats 1-2 ("When I was
  new, I made a mistake"; over-checking). Add `!thread:notgood`, and to pressure also `!who:pell` (the practical is his
  arc). Pressure L107 "I'm the newest here" stops being true once newcomers arrive → "I'm one of the newest here."
- **S23. Leaving talk from people with a leaving story.** `pool-ship.talk:111-121` (leave-her, "Not soon. Not planning
  to") and `pool-plans.talk:87-97` (stay-or-go, "I've never wanted to") are wrong for the `leaving` theme (Raman,
  Lindqvist, Strand, Teague, Chen), for Brennan (her arc is an offer to leave) and, in stay-or-go, for Calder (her
  junior transferred to the Halcyon and never wrote, beat 4) and Marrow. Add `!thread:leaving !who:brennan|calder|marrow`
  (leave-her already skips Marrow and Tomas).
- **S24. `pool-news.talk:113-123` (news-from-home) "Someone I love is doing better"** steps on the `family` theme
  (someone at home in hospital), Rina's gran (beats 2-4), Torres's father (who won't get better) and Pell's mum's hands.
  Add `!thread:family !who:rina|torres-zeke|pell`.
- **S25. `pool-news.talk:20` (gull) quotes beat vance.1's poem**, the whole of that beat ("Oh treadmill, thou belt of
  endless toil"). Use another poem: `them: The one about the lift doors. It rhymed "door" with "door". Twice.   #funny`
- **S26. The airlock joke is told three times.** It's Holt's beat 1 punchline ("Mensah's terrible joke from last night
  comes out of him"), then `holt.talk:34-35` and `mensah.talk:80`. Give both talks a new one:
  `holt.talk:34-35` → `them: Mensah told me a joke yesterday. Why don't airlocks keep secrets.` / `them: Too much pressure. I laughed. Don't spread it about. He keeps a count.   #funny`;
  `mensah.talk:80` → `them: One about a kettle. Long story, short punchline. Three whole seconds, he laughed.   #funny`
- **S27. `pool-ship.talk:51-61` (lift) "The lift's the heart of the ship... 'Four, please.' I say it in my sleep."**
  From the three who are secretly afraid of it, it rings false. Add `!who:kovac-zainab|cruz-tove|keane-davi`.
- **S28. `pool-plans.talk:63-73` (learn) "Some Veyli... Ferreira's teaching people":** from Holt it gets ahead of his
  thaw, and Rossi is already learning. Add `holt|rossi-femi` to its `!who:`.

### Replies and answers that don't land

- **S29. Listen replies that just repeat the question back:**
  `pool-crew.talk:57` "Has someone looked out for you?" → `listen: Who looked out for you, when you were new?`;
  `mensah.talk:105` "Who looks out for you?" → `listen: And who watches the watcher?`;
  `pool-home.talk:91` "What would you do first?" → `listen: What do you miss most?` (answer "Walk. Just walk, somewhere without a corridor." still fits).
- **S30. `saruth.talk:54-55`** "The coffee. It has opinions." answers "what do you find hardest about my people?" with
  nothing, and "Chief Holt says the same of me" doesn't follow. → `cheer: Knowing when you've made a joke.` /
  `them: Ah. We have the same trouble with you. A sentence late, every time. We are even.   #funny`
- **S31. `mensah.talk:83-84`:** for Mensah "the Chief" is Holt, but his answer assumes Calder. → `cheer: Chief Calder. Once. By accident.`
- **S32. `nandakumar.talk:141-152` (water) is Rina's water talk again** (`rina.talk:125`, also own, same opener). Replace:
  ```
  == silence
  topic: work
  when: tier>=colleague
  them: I ask one question. Then I wait. People fill a silence. That's when they tell me where it hurts.
  them: It works on everyone. Nearly everyone.
  ask: Do you find a silence easy, or do you fill it?
  listen: Who doesn't it work on?
    them: Chief Holt. He outlasts me. We sit there like two clocks.   #funny
  share: I fill it. Every time.
    them: Most people do. Count to five first. It's a kind thing to give someone.   #warm
  cheer: I fill it with biscuits.
    them: Crumbs are a kind of answer. Not a good one. Drink some water.   #funny
  ```
- **S33. `pool-day.talk:113` (best-bit), the no-romance read:** "This. Honestly. Sitting here with you." at friend tier
  is the kind of line the standing rule asks to make plainly about friendship. → `them: This. A proper chat with a friend. Honestly.   #warm`
- **S34. `pool-food.talk:112-122` (supper)** invents a late-night supper the game doesn't have and invites you to it
  ("You should come"). → L114-115 `them: Sometimes the best meal is a late one. A grab-shelf plate, whoever's still up.` /
  `them: Two of us at one table, eating cold stew. Lovely.   #warm`; L118 `them: Whoever's about. Not many. That's the nice bit.   #warm`
- **S35. `brennan.talk:43-54` (bread) and `mensah.talk:95`** invite you to things the game doesn't run (Sunday bread at
  seven; a night round). The writing follows the game: no invitations to what you can't turn up to.
  `brennan.talk:52` → `them: Oh, love. Well. Then stay as long as you like.   #warm`; `:54` → `them: Sunday mornings. Floury ones. The best kind.   #funny`;
  `mensah.talk:95` → `them: It is. The ship talks more at night. Softly. You'd hear it.   #warm`
- **S36. `pool-work.talk:84` "That's the Works way. You'll fit right in."** said by a cook or a doctor. → "That's the Wren's way."

### Voice

- **S37. Pet words laid on too thick** (the voice bible: "a pet word in every line is a parody"). Trim to two or three each:
  Holt "Hm." ×9 in 4 talks (`holt.talk:8,14,16,27,29,42,51,53,55`: keep 8, 27, 42); Mensah "Ha" ×8 (`mensah.talk:63,69,71,82,84,97,106,110`: keep 63, 84, 97);
  Kovac "Um" ×8 and "Sorry" ×5 (drop "Um." from L68, 83, 96, 109 and "Sorry." from L70, 107);
  Halloran "Ha" ×7 and "Lovely" ×6 (drop "Ha." from L103, 106 and "Lovely." from L82, 95); Brennan "love" ×6 (drop it from L13, 39).
- **S38. Food in the light replies:** 45 of 160 cheer replies are about food, so the player reads as permanently
  hungry, and several repeat outright: "Second helpings" (`pool-day:35`, `tomas:40`, `vance:69`, `pool-work:121`),
  "My appetite" (`pool-hobby:85`, `kovac:108`), "Brennan. With biscuits / With a spoon" (`pool-day:95`, `pool-crew:97`).
  Brennan is named in 30 talks, biscuits in 19. Suggested swaps (keep Vance's, it's his regulation joke):
  - `pool-day.talk:35` → `cheer: Nobody asking me where anything is.` / `them: Give it a month. Then you'll be the one they ask.   #funny`
  - `tomas.talk:40` → `cheer: Taking the long way round Deck 2.` / `them: That's mine! You can share it. We'll be late together.   #funny`
  - `pool-work.talk:121` → `cheer: Proud enough to tell my gran.` / `them: Tell her. Grans keep these things. Properly.   #warm`
  - `pool-hobby.talk:85` → `cheer: My bad jokes. Still got them.` / `them: Halloran will want to trade. Brace yourself.   #funny`
  - `kovac-zainab.talk:108` → `cheer: My laundry pile. It's thriving.` / `them: Oh. That's. Very good. Water it with soap.   #funny`
  - `pool-crew.talk:97` → `cheer: Whoever has the best blanket.` / `them: Good choice. A blanket fixes most things.   #funny`
  - `pool-tradition.talk:122` → `cheer: A long shower. Before ten.` / `them: The classic cure. After ten it's character-building.   #funny`
  - `pool-day.talk:95` → `cheer: Whoever saved me a seat at dinner.` / `them: The best kindness aboard. Small and warm.   #warm`

---

## Nits

- **N1.** `pool-day.talk:10` "Kept me going all afternoon" can play in the morning → "Kept me going for hours."
- **N2.** `pool-day.talk:46` "Sleep's the whole trick. Ask Rina." → "Ask the infirmary." (Rina's an aide; Nandakumar runs it.)
- **N3.** `pool-tradition.talk:20` "Fell asleep at one." (one o'clock?) → "Fell asleep at the third one."
- **N4.** `pool-tradition.talk:67` you went to quiz night on Day 4 (facts 9) → "Been back to quiz night yet?"
- **N5.** `pool-tradition.talk:97` there's already a new hand's tea (`traditions/new-hands-tea.trad`) → "There's a new hand's tea already. Make it bigger. Tell someone."
- **N6.** `pool-tradition.talk:123` "Doctors hate it. Well, Rina does." Rina isn't a doctor yet → "The infirmary hates it. Well, Rina does."
- **N7.** `pool-crew.talk:20` "Apart from me." at any tier, to a stranger → `when: tier>=acquaintance`.
- **N8.** `pool-crew.talk:31` "Walked into the mess, sat down, and fell asleep in the porridge queue" (sat, then queued) → "Queued for porridge and fell asleep standing up."
- **N9.** `pool-crew.talk:100-110` (new-faces) asks what it's like being new, also in month nine → `!aboard>=30` if the engine adds `aboard`, else `week1:` isn't enough; leave a note.
- **N10.** `pool-crew.talk:90` "{friend} helped me through a bad patch last year": `{friend}` may be Tomas or a newcomer. Low risk; "a while back" is safer.
- **N11.** `pool-home.talk:83` "It's got a canteen" → "It's got a mess. That's most of home."
- **N12.** `pool-ship.talk:81` "The first one. Varga." Canon says Varga started the gallery, not that Varga was first → "Varga. Started the gallery. Looks like they're about to laugh."
- **N13.** `pool-plans.talk:66` "Or the guitar, but the queue's long" from the four guitar learners → add `lindqvist-isak|park-noor|larsen-hamid|haddad-tamsin` to `!who:`.
- **N14.** `pool-news.talk:27` "Every Friday, I'm there." gives the newsletter a day nobody has set → "Every week, I'm there."
- **N15.** `pool-news.talk:85` and delivery: from Esposito or Ishikawa, "Ask the storekeepers" → add `!who:esposito-yara|ishikawa-orla`.
- **N16.** `pool-work.talk:65` `!who:halloran-emeka` is redundant (`rank:junior` already skips him). Harmless.
- **N17.** `pool-work.talk:97` "Fixing things before they break. Show-off." reads as if the player calls themself a show-off → "Fixing things before they break. Smugly."
- **N18.** `pool-hobby.talk:73` "Check it was flattering, first." is gently about looks (voice bible rule 2); fine as self-teasing, but "Check it got my good side." is softer still.
- **N19.** `pool-day.talk:50-72` (morning-person, evening) from night-shift crew ("Shift done, nothing due" at 20:00 when their shift's about to start). No shift condition exists; leave it, or the engine could treat night crew as `!who:` for these two.
- **N20.** `calder.talk:96` "Fair. Being honest about wanting the first is the right start." is clunky for Calder → "Fair. Honest. Most people only say the second."
- **N21.** `calder.talk:105` "He'll be unbearable about it." is Holt's beat 5 punchline ("Don't tell Mensah. He'll be unbearable.") → "He'll make a rota for it."
- **N22.** `vance.talk:64` and `:103` hard-code "Cadet": his card's nick goes Cadet → Cadet {me} → {me} by tier → use `{nick}` (asks are card lines; tokens work).
- **N23.** `vance.talk:96` "I will not say which. Regulation nine: rest." doesn't follow → "I will not say which. You'll know it when it rattles the windows."
- **N24.** `tomas.talk:46` "Can I show you something? My star map." You share his bunk room and his beat 1 is the star map → "You know my star map? See the pencil circle? Top left."
- **N25.** `rina.talk:149` "Fight me." (nobody aboard talks about fighting) → "Prove me wrong."
- **N26.** `sato.talk:35` and `:38` say "Mori runs the labs" twice in one talk → L35 "I've re-labelled it. And the twelve beside it. My store, my handwriting."
- **N27.** `halloran-emeka.talk:64` his card says he laughs *before* the punchline → "What do you call a spanner that tells jokes? Ha! Sorry. A wrench-ed comedian." and `:77` Brennan's "Hm." is Holt's word → "She took one bite and said 'Well.' Just 'Well.'" (then L79-80 "Is 'Well.' good, from Brennan?" / "From Brennan, 'Well.' is a medal.").
- **N28.** `nandakumar.talk:126` "Follow the person saying 'drink some water'." → "That's me. Or Rina. Both correct."; `:132` repeats `pool-food.talk:78-79` → "Brennan calls them a hazard. She's asked for more twice."
- **N29.** Lines repeated whole across talks: "My bunkmates. Every night." (`holt:39`, `pool-crew:35`), "Are they very hot?" (`nandakumar:24`, `pool-food:81`), "What had you done?" (`pool-day:91`, `pool-work:57`), "Which one's your favourite?" (`pool-ship:80`, `pool-tradition:10`, `tomas:10`). Change one of each.
- **N30.** Friend-tier openers lean on one shape: 7 of the 27 start "Can I tell you / Can I be honest / Can I say / May I tell you / Can I show you". Vary three of them (for example `pool-home:112` → "I was very homesick my first month. Did you know?").

New canon to log in `facts.md` 11 when the pack goes in (the facts page says "ask first"): Saruth's knock count; Mensah's
good-night to the decks ("Night, Three. Night, Garden"); Calder's slogan mug in the machine shop; Halloran's cup on
Calder's desk at one; Sato's comets "two count"; Kovac's 42 beans and 9½ minutes; Vance's "seven salutes this month";
the lighthouse song's disputed line. (Also, outside the pack: `traditions/new-hands-tea.trad`'s comment says Calder
hangs your mug, while facts 11 and the Halloran talk say Halloran gives it. A backlog row for the head writer.)

---

## The data shape (`plans/talk-pack-plan.md`): implementable, with these gaps

1. **Fired ids use the topic, so the topic must be frozen.** `pool.<topic>.<slug>` plus "a talk may override it": if a
   talk ever overrides its topic or moves file, its id changes and old saves lose it. Say: *the id always uses the
   file's `topic:` header; a talk never moves file.* (Slugs aren't unique across the pool: `portraits` is in both
   pool-hobby and pool-ship, so the topic must stay in the id.)
2. **Saved state is more than a set.** "Prefer a topic you haven't talked about with this person lately" and "a done
   line never twice running with the same person" both need memory. Save fired talks as `{ id: [day, crewId] }` rather
   than a bare set: "lately" and "with whom" then come for free, and it helps debugging. Small talk keeps one
   `lastDone[crewId]`.
3. **Seeded picking:** name the seed (for example day + speaker id), so a reload picks the same talk, and nothing at load
   calls `R()` (DEV_NOTES' determinism rule).
4. **Tags on `ask:` lines:** `pool-crew.talk:20` has `#funny` on an ask. The grammar sketch only shows tags on `them:`
   lines; the reader should allow them on asks (or the writer drops it).
5. **Condition words.** `aboard>=` is used twice (S16 shows how to drop both). `tpl:` is unused: drop it from the plan.
   Recommend adding **`thread:` / `!thread:`** (the speaker's roster `thread`; S20-S24). `!moved:`, `!dept:`, `flag:mug`
   already exist. lines_check should learn the two words the pack keeps.
6. **Placeholders.** Say which form each placeholder takes in a talk: `{hobby}` is a verb phrase ("knitting scarves") and
   only fits "I've been {hobby}" / "gave up {hobby}"; `{hobbyNoun}` is the noun. `{trad}` "the next tradition on the
   calendar" must skip rec-deck traditions while `REC_DECK` is off and ones the speaker can't attend, and a line-start
   `{trad}` needs a capital ("Observatory night's coming up").
7. **Retire the old topic lines.** The plan keeps `talk.start/sit/filler/end/stop`, but doesn't say what happens to
   `talk.<topic>.open/more/ask/reply/ans` in `content/banks/talk.lines`. The pack reuses many of them word for word
   (one-hour, cold-tea, tea-queue, something-on, story-each, hum, smells...). When the pack is on, those keys should be
   parked (the cut rule: marked cut, kept on record), or players hear the same lines from both.
8. **Guests.** "Guests don't draw the pool" needs a check on `rank:guest`; Veyli guests need the no-contraction small
   talk (S17).
9. **For the user, plainly (a design question, not a bug):** the pool fires once per *save*. With 100 pool talks and
   Talk a while once a day per person, a player who talks with four or five people a day empties the pool in three to
   four weeks; after that, everyone except the 15 with their own talks only makes small talk, for the rest of a 364-day
   year. The plan says so, but the user should choose: keep it (and plan more pool talks), or fire general talks once
   per *person* and keep "once per save" only for the shared anecdotes (the twins, the Geralds, the comics wall), with
   a `once: save` line on those.
10. **Matching reply:** voice cards with `needs: practical` get their +2 on **listen** (the game's `talkNeed`,
    `starship-cadet.html:38205`). Worth one line in the plan so the next writer knows the listen answer is the warm one
    for Calder, Holt, Vance, Nandakumar and Halloran.

## What I checked by script (scratch, not committed)

- Shape: 160 talks, each with 1-3 `them:`, one `ask:`, all three replies, an answer each. Clean.
- Lengths: card lines 90 (placeholders as 9), replies 44, no tokens or placeholders in replies. Clean.
- Ids unique (pool by topic + slug, own by crew + slug). Clean. Counts match the plan: 100 pool (29 any, 39
  acquaintance, 20 colleague, 12 friend), 60 own.
- Every crew id in `who:` and `@talks` is a real roster id. Clean.
- One "!" a line at most; no US spellings; Saruth's own talks have no contractions. Clean.
- Repetition counts: cheer replies about food 45/160; Brennan named in 30 talks, biscuits in 19, Pell 10, Calder 10;
  "Don't tell" in 9 talks; "Ha!" 28 lines; "Hm." 16 lines; "lunch" 5 lines.
