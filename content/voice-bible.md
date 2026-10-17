# The voice bible

**Kept by the head writer.** How the Wren sounds. Read it with `content/README.md` (the file format), `content/facts.md`
(the canon) and the voice card of whoever you're writing. When this page and the README disagree on format, the README
wins; on tone, this page wins.

---

**Approved by the user (2026-10-17, ~03:37):** the Voices sampler as it stood: all ten story voices (Torres, Calder,
Tomas, Pell, Rina, Brennan, Vance, the Captain, Holt, Kovac), the names, and the arrival scenes. Their cards and lines
are the reference for everyone else's; don't change a story voice without the head writer asking the lead first.

## 1. The one-paragraph version

The Wren is a good place to work, full of competent people who like each other more than they say. Most of what they say
is **light**: small talk, work talk, gentle teasing, a running joke. As you get to know someone, they **show you more of
themselves**, and now and then, when you've earned it, you find out what they're carrying. Those moments are small and
real (homesickness, a parent getting older, an exam, doubting yourself), never melodrama. **Warmth over wit.** Nobody is
cruel, nobody is stupid, nobody flirts with you, nobody dies on screen.

## 2. The rules (the user's, from the plan)

1. **Generally light, cozy and funny.** Roughly: of every ten lines, six are plain and friendly, three are funny, one is
   warm. Serious lines are rare (at most one a ship day reaches you, ship-wide).
2. **Warmth over wit.** A joke that makes someone smaller isn't a Wren joke. Teasing is how friends say they like you;
   it's never about looks, bodies, background, accents or being new.
3. **Serious moments are earned.** Only behind friend tier, an arc beat, a moment or a goodbye (`lines_check` enforces
   it). They're about ordinary things: homesickness, a failed exam, a parent getting older, doubting yourself, a
   friendship cooling, someone they lost. Told plainly, briefly, and the person is still themselves while telling it
   (Rina is dry even when she's frightened).
4. **Gentle grief is allowed; nobody dies on screen.** Someone may have lost a grandparent years ago, or be losing a
   parent slowly to illness or age. We never show a death, never kill a crew member, never make a death a twist.
5. **No romance with the player.** No flirting, no dates, no "you look nice", no blushing, no "more than friends", no
   jealousy about you. Not as a joke either. Crew can love each other in the background (established couples, plainly
   mentioned, never a storyline).
6. **Everyone is good at their job.** Mistakes happen and get fixed; nobody is incompetent for a laugh. Calder's
   exactness, Holt's suspicion, Sato's absent-mindedness are character, not failure.
7. **Holt's distrust of the Veyli is voiced and argued with,** never a slur, never a joke about the Veyli as a people.
   Other crew push back on him; over his arc, he softens.
8. **Never contradict the roster or `facts.md`.** If you need something new, ask.
9. **Nothing the game doesn't have:** no photos, cameras, phones, weapons, real brands, real places, real politics.
   "Blast" is the strongest word aboard.

## 3. How lines read on a phone

- **Short.** A bubble 60 characters at most (aim for 40). A chat card line 90 (aim for 60). A moment or meeting line
  140 (aim for 100). One idea per line.
- **Plain words.** Short words, short sentences. If a twelve-year-old would stumble on it, rewrite it. Ship words are
  fine (scrubber, coil, board, shift, bunk, berth, deck) because the game teaches them.
- **British spelling and idiom:** colour, favourite, mum, biscuit, queue, "all right", "cheers", "fancy a tea?". Not
  "awesome", "gotten", "y'all", "cookie", "mom".
- **People talk, they don't announce.** Not "I am feeling homesick today." Yes: "Funny. Smelt bread in the mess and I was
  ten again." Not "Hello! Welcome to the infirmary, where we treat injuries." Yes: "Sit there. Don't touch anything blue."
- **Contractions, always** (except Holt and Saruth when they're being formal, and Calder when she's being exact).
- **No exclamation marks in a row,** and at most one per line. Earnest and chatty people use them; dry people almost
  never.
- **Specifics beat adjectives.** "Coil three sulked all shift" beats "Work was hard". Name the machine, the dish, the deck,
  the tradition. Use placeholders (`{machine}`, `{dish}`, `{trad}`) so it's always the real one.
- **Names, not pronouns,** for other crew unless `facts.md` gives their pronouns. "Ask Eklund, she'll know" only if
  Eklund's pronouns are listed; otherwise "Ask Eklund. Eklund always knows."
- **The player is never gendered.** Crew call you your name, a nickname from their card, "cadet", "the new hand".

## 4. The tiers: how someone talks to you as you get closer

Every line kind has a ladder. Write for each step. (Tiers: stranger 0, acquaintance 1, colleague 2, friend 3, close 4.)

| Tier | What they're like | What they talk about | Example (one person, Pell) |
| --- | --- | --- | --- |
| **Stranger** | polite, brief, "cadet" | their job, where they work, the ship | "New, are you? Pell. Works. Don't sit on the blue crate, it's Calder's." |
| **Acquaintance** | they say hello first, use your name | a habit, a hobby, where they hang out, small complaints | "Morning, {me}. Panel's sticking again. It's always the panel." |
| **Colleague** | first names, jokes, opinions | what they think of their work, a little of home, an opinion about someone aboard; a running joke starts | "Calder looked at my weld today. Just looked. I'm still recovering." |
| **Friend** | nickname, they seek you out | their struggle, hinted then told; their past | "Mum's sent the three messages again. I haven't opened them. I know what they say." |
| **Close friend** | your person aboard | the secret; how it turns out; what you mean to them | "First month here I nearly left. Glad I didn't. You're part of why I stay glad." |

- **Strangers aren't cold.** The Wren is friendly; a stranger is just someone who hasn't learnt your name yet.
- **The nick** (from their card) appears from the tier the card says. Don't write a nickname into a line: use `{nick}`.
- **Warmth:** `warmth:cold` means you haven't been around; they notice, kindly ("There you are. Thought the lift ate
  you."), never sulk or guilt you.

## 5. Tone tags

| Tag | Use it for | How often | Example |
| --- | --- | --- | --- |
| (none, `#light`) | everyday, friendly, informative | most lines | "Board's busy today. Pick a scrubber, they're quick." |
| `#funny` | a joke, a running joke, a comic complaint | about a third | "The coffee machine and I aren't speaking." |
| `#warm` | affection, thanks, being glad you're there | about one in ten | "Glad it was you on that job." |
| `#serious` | a struggle, worry, grief, a goodbye | rare, earned (friend tier, a beat, a moment, leaving) | "Dad called me by my uncle's name again." |

**The light-to-serious ratio** in a person's own file: for every serious line, at least ten light or funny ones and
two warm ones. Story crew get a few more serious lines because they have arcs; everyone else gets theirs through the theme
library (moments), not their everyday banks.

## 6. What makes a voice

A voice card is not adjectives; it's **habits of speech** a reader could spot with the name covered. Every card should
answer:

- **Sentence shape.** Long and tumbling (Torres excited), clipped (Calder, Holt), questions back (Tomas), lists of three
  (Vance), one word then a pause (Kovac).
- **Pet words and openers.** Torres's "Right, onward." Rina's "Honestly." Holt's "Hm." Brennan's "love". Use sparingly:
  a pet word in every line is a parody.
- **What they notice.** Calder: numbers and sounds. Brennan: whether you've eaten. Tomas: the view. Holt: who's where.
  Pell: what's broken, and food.
- **What they never say.** Calder never says "great job". Holt never says "I'm sorry" plainly (he says "That was badly
  done. By me."). Rina never says how she feels straight out. Torres never talks down. Tomas never brags.
- **How they are with juniors.** The ship's seniors are kind to juniors in their own ways: Calder by being exact and
  fair, Holt by testing you, Brennan by feeding you, Marrow by asking your opinion, Vance by the rules (and a soft spot).
- **Their mood tells.** How do they sound tired, happy, worried? (Calder gets quieter. Torres gets louder. Tomas asks
  more questions. Pell sleeps.)

**The test:** cover the name. Read five of their lines. If you can't tell who it is, the lines are generic. Shared banks
may be generic (that's what voice tokens are for); a person's own lines must not be.

## 7. Voice tokens and shared lines

Shared banks (`banks/`) are said by many people, so they must sound right in any mouth:

- Use `{hi}`, `{bye}`, `{yes}`, `{thanks}`, `{wow}`, `{sigh}`, `{nick}` where a person's own word would go:
  "{hi}, {nick}. Busy day?" becomes "Hm. You. Busy day?" from Holt and "Oi oi, champ. Busy day?" from a playful junior.
- Keep shared lines **neutral in personality** (no strong opinions, no jokes that need a particular sense of humour) and
  specific in **situation** (where, when, what's happening): that's what conditions are for.
- Bank conditions (`dept:`, `rank:`, `trait:`) narrow the speaker: a `trait:dry humour` bank can be dry.
- A voice token at the start of a line must read well with every card's words. "{yes}, I'll be there." works for "Fine",
  "Of course" and "Go on, then". "{wow}! That's great." fails for "Huh".

## 8. The crew's ladder of rank (how they address each other)

- **The Captain** is "Captain" to everyone, always. She calls crew by surname, juniors by first name once she knows them,
  you "cadet" until she knows you.
- **Commander Vance** is "Commander" or "sir" (he prefers "Commander"). Calls everyone by rank and surname. You are
  "Cadet" to him, then "Cadet {me}" (it's in his card's `nick`: in a line, write `{nick}`).
- **Chiefs** are "Chief" (Calder, Holt), "Doctor" or "Dr. Sato" / "Dr. Nandakumar", "Chef" (Brennan; juniors say
  "Chef", officers say "Auda" only when they're friends).
- **Officers** are called by surname by juniors ("Torres") and by first name by each other. Torres insists juniors call
  him Zeke; most don't.
- **Juniors** call each other by first name or surname, whichever's shorter (Pell is Pell; Tomas is Tomas; Kovac is
  Zainab to friends and Kovac on shift).
- **The Envoy** is "Envoy" to everyone except the Captain ("Envoy Saruth") and close friends (just "Saruth", only when
  invited).

## 9. Writing each line kind (quick notes)

- **greet:** varied by time (`time:morning`), place, tier. Never "Hello, how are you today?" Write what they'd *actually*
  say walking past: "Morning. Mind the wet floor."
- **feel:** by `mood:`. Low is never miserable: tired, fed up, a bit flat. High is a good day, specifically why.
- **near:** about where they are and what they're doing: `place:`, `act:`. The garden, the gym, the queue.
- **life / joy:** small specifics from their roster and card. The joy is something they'll talk about happily for ages.
- **callback (`mem:`, `told:`):** they remember what you did. Concrete and pleased ("The lamp's still perfect"). Said once
  (`told:`) for big things; `mem:` for recurring fondness.
- **cue:** reactions to what happened: the storm, a repair, a harvest. A version for "someone did it" and one for "you did
  it" (`.you`).
- **invite / accept / decline:** invitations are small and specific ("Quiz tonight. We need someone who knows engines.").
  Declines are kind ("Can't tonight. Ask me Thursday?").
- **visit / note:** at your bunk. A visit is short and cozy; a note is a few words left on your bunk ("Biscuits in the
  tin. Don't tell Pell. — B").
- **about:** what they say about a crewmate they're bonded with (`bond:best`): affectionate, specific.
- **smalltalk / rumour:** bubbles, 60 characters, said to no one in particular.
- **hint:** a moment is ready. "Got a minute? Properly, I mean." Each story person gets their own.
- **missed:** you missed an appointment with them. Disappointed is fine; guilt-trips are not. "Missed you at the booths.
  Next time?"
- **story.<arc>, moments:** see the arc outlines. Lines up to 140 characters; 4 to 10 lines; one or two choices.
- **goodbye / letter:** warm, specific, memory-heavy. A letter sounds like them writing, not talking (a bit more
  careful, still them).

## 10. Moments: how to write a scene

A moment is 4 to 10 lines in the dialogue panel with one or two reply choices (the social plan, Part 1).

1. **Start in the middle.** No "I've been meaning to tell you something." Start with the thing: "Mum's sent the three
   messages again."
2. **One feeling per moment.** Don't resolve and reveal in the same scene.
3. **The person stays themselves.** Calder's grief is still exact; Pell still makes a joke; Rina's still dry.
4. **Replies are short and kind, in four flavours:** listen ("Go on."), cheer (a joke), practical (offer help), share
   (something of your own). There's never a wrong one; the one that fits their `needs` gets a warmer answer.
5. **Leave something behind:** a memory key (`mem:`), sometimes a flag or a favour, sometimes a Mail later.
6. **End light where you can.** Even a sad moment can end on a small joke or a thank-you. ("Right. Enough of that. Tea?")

## 11. Checklist before you push (the head writer reads every batch against this)

- [ ] `python3 lines_check.py` says PASS.
- [ ] Each person's own lines pass the cover-the-name test.
- [ ] Mostly light; funny ones are kind; serious ones are earned and plain.
- [ ] Nothing contradicts the roster, `facts.md`, the voice card, or a beat already in the game.
- [ ] No pronouns for people whose pronouns aren't in `facts.md`; the player is never gendered.
- [ ] No romance or flirting; no cruelty; no one incompetent for a laugh.
- [ ] **The no-romance read (the lead's standing rule, from reviewer 2):** every moment and arc beat, and every line
      said to you at friend or close tier, is read once just for this. Warmth, closeness and deep friendship are fine;
      anything that could read as romantic toward the player is not (no "I can't stop thinking about you", no lingering
      looks, no jealousy, no "you mean more to me than...", no compliments on how you look). When in doubt, make it
      plainly about friendship or the ship ("You're part of why I stay glad."). lines_check bans some phrasings too.
- [ ] **Voice-card words carry no end punctuation** (`hi: Oh, hi`, not `Oh, hi!`): the line supplies it (`{hi}. Busy?`).
- [ ] Specific: real machines, dishes, places, traditions (placeholders where they vary).
- [ ] Every tier has lines; the stranger lines teach something useful (where things are, who to ask).
- [ ] British spelling; short words; bubbles 60, cards 90, scenes 140.

## 12. Notes from batches (the head writer adds to this as we go)

- Lines are picked by chance, not in order: never number a sequence ("Tip one... tip two").
- A line that only makes sense at one moment needs a condition for it ("the Chief's coming over" needs `act:dinner`).
- Day 0 walking lines are gated by `flag:walk.<step>`, so they're never ordinary chat.
- Rooms with spaces: `place:junior_common_room`, or the aliases (`mess`, `commons`, `lounge`, `booths`, `overlook`,
  `teacorner`, `worksbay`, `chartroom`, `musicroom`).
- The ladder club's secret is the ladder: anyone who avoids the lift "takes the ladder", never "the stairs" (there
  are no stairs between decks).
