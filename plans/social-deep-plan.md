# Pillar 4: the deep social system (plan)

*Final draft for building, 2026-10-17: the user's answers of 2026-10-17 are folded in (grief yes, background couples yes, bunk visits and later your own room, machine-shop gifts, a fuller reputation system, no counts in "What you know", crew coming and going, guiding a newcomer, the escort is Zeke Torres). Draft 2 folded in the interfaces agreed with the Pillar 4 planner: the content pipeline, the query API, the ship notes bus, onboarding's flags, `lineFor`, two social engineers), by the social system designer (session_01SMfS1WKqzQ93X6zyZ7NFpJ, branch `claude/social-design`). Written with the Pillar 4 planner (session_01KLFXcNJztCSVLXunD8Jt7R), who owns the overall Pillar 4 plan (arrival, first week, dialogue at scale, traditions, staffing). Nothing here is built until the user approves it. It builds on what section 20 already does (see "Where we start").*

## The pitch (one page)

Pillar 3 gave the Wren's crew a relationship meter, a chat card, gossip, favours and three little story arcs. Pillar 4 turns that into people you actually **get to know**.

- **You get to know someone in steps.** First their name and job, then their habits and hobbies, then what they think about work and home, and once you're close, the thing that's weighing on them. Each step is something you *learn* (it goes into the Crew app as "What you know about Rina"), not just a bar going up.
- **Moments.** When you're close enough, and the time and place are right (a quiet evening in the lounge, the observatory, a late table in the mess), someone opens up: a short scene in the dialogue panel where you hear their struggle, and you answer how you'd answer a friend. **Mostly light; serious and heartfelt as you get close.** Every one of the 75 crew has at least one such thread; the story crew have whole arcs.
- **They remember.** Crew keep a handful of memories of you, which fade unless they were big: the lamp you fixed, the quiz you came to, the evening you listened. They bring them up ("Thanks again for the lamp, it's been perfect"), and big ones are kept for good.
- **They have lives with each other.** Friendships form and fade, a few pairs fall out and make up, mentors take juniors under their wing, and crew talk about each other. You can bring two people together.
- **Small kindnesses.** Give a small gift (a tin of tea from the store, herbs from the garden, a little thing you made in the machine shop). Friends drop by your bunk in the evening, leave a note if you're out, and invite you to things: dinner together, the observatory, their tradition, their show.
- **Your name gets around.** A reputation system (the user's ask): each department remembers what you've done for them (the galley knows who fixes their ovens), and the whole ship forms a view of you as a worker, a shipmate and a part of ship life. It has real consequences, good and (gently) bad: warmer strangers, favours and invitations, officers who notice, Calder's view of you for promotion.
- **People come and go.** Now and then crew are transferred off (they say goodbye a day or two before, talking about your friendship, and again at the shuttle on the day), new crew and new cadets like you arrive, and later you're asked to guide a newcomer the way you were guided.
- **Lines that fit.** Everything anyone says is picked from banks of lines by who they are (a voice card for each of the 75), how well they know you, their mood, what they remember and what's happening on the ship. Writers fill plain files under `content/` that a generator bakes into the game (the planner's pipeline); they never touch the game's code.
- **No romance** with the player, ever (the user's rule); a few established crew couples live in the background. **No fail state:** you can't lose a friend for good, and there's never a wrong answer.
- **Cheap:** all of it runs on paper hour by hour for 75 people in well under a millisecond, saved compactly, and checked by an extended `social_check.py` (the writers' data by the planner's `lines_check.py`).

## Where we start (section 20, built in Pillar 3, 0.36.0 to 0.36.17)

What's already there, and stays (the deep system extends it, never replaces it):

| Part | What it does | Where |
| --- | --- | --- |
| Relationships | `SHIP.rel[id] = { pts, tier, met, lastTalk, known, chatDay, mealDay, workDay, favDay, seekDay, arc, arcDay, showDay }`; tiers 0/10/30/60/100 (stranger, acquaintance, colleague, friend, close friend); points never drop below a reached tier; friends of friends warm faster | `relAdd`, `relTier`, `REL_PTS` |
| Crew affinity | one Int8 per pair (2,701 pairs), starts from `affStart` (dept, bunk room, shift, habits, traits, clash), drifts hourly from time in the same room | `SHIP.aff`, `socialHour`, `affinityPlan` (pure, for seating) |
| News | items born from birthdays, traditions, habits, faults, pairs; spread hour by hour between people together | `NEWS`, `newsAdd`, `newsKnownBy`, `playerHeard` |
| Chat card | tap someone: one line (missed appointment, guests, story beat, feud, birthday, news, feeling, where they are, a life detail, a greeting), buttons Chat, Ask about…, Help?, Meet up | `chatLine`, `chatOpen`, `chatDo`, `CHAT_SKIN` |
| Ask about | the roster's `about: [{ tier, topic, text }]` told up to your tier, into `rel.known` | `chatDo('ask-work'/'ask-home')` |
| Favours | ideas from their life (left something behind, a flickering lamp) on section 17's favour API | `favourOf` |
| Seeking you out | friends in free time wave you over (prompt at the screen edge) | `socialSeek` |
| Chatter | overheard lines as speech bubbles (news, or small talk by activity) | `socialChatter`, `bubbleSay` (8b) |
| Story arcs | Tomas, Pell, Rina: four beats each, one per tier, with Mail and Pell's show | `STORY_ARCS`, `arcBeat`, `arcTold` |
| Dramas | a pair falling out is a three-day feud you can smooth over by chatting to both | `feudOf`, `feudTalk` |
| Appointments | kept: +3; missed: a remark next time | `socialAppts`, `apptMissedBy` |
| Device | the Crew app, `crewContacts`, `newsFeed`, `shipNews` | section 19 draws |

And section 18's **meetings with dialogue** (`MEETING_SCRIPTS`, `dialogueShow`, `dialogueStep`, the device's `deviceDialogue` panel): a script of `{ who, text, pose, to }` lines and `{ choice: [{ text, rel, job, reply }] }` choices. The deep system plays its moments, intro scenes and visits through that same panel and that same line shape.

What's thin today (from the social engineer's handover and a read of the code): lines are a few generic lists with no per-person voice; nobody remembers anything you did beyond points; only 45 `about` details exist across 74 crew (mostly the story crew); rivalries almost never happen; gossip is thin on quiet days; friends who wave don't walk over; there are no gifts, visits, invitations or reputation.

## Ground rules for the social design

1. **Cozy first.** Tiers never drop. Memories fade, but fading only means they stop being mentioned. A neglected friendship cools in *words* ("Haven't seen you in ages!"), never in tier.
2. **Generally light, heartfelt as you get close** (the user). Strangers and acquaintances are friendly and funny; colleagues share opinions and small worries; friends share struggles; close friends share what matters most. At most **one serious moment a ship day** for you, ship-wide, so the tone stays light.
3. **No romance with the player** (the user's rule). No flirting lines, no dates, no "more than friends" moments. Writers' lines are checked for it (`lines_check` flags a short list of words). **Crew-to-crew: a few established couples in the background** (the user, 2026-10-17): together from the start, no romance storylines, never involving you (Part 3).
10. **Serious is allowed, gently** (the user, 2026-10-17: "all of it is OK"), including grief for someone they lost. **Nobody dies on screen.**
4. **Never a wrong answer.** Every reply in a moment is kind in its own way; the one that fits the person best gives a little more and a warmer reply. Nothing you say makes anyone dislike you.
5. **Nothing locked away by luck.** Every crew member's steps can be reached by ordinary play (chatting, eating together, favours, work); moments wait for you rather than expire (except time-bound ones, which come back in a new form).
6. **Built from the simulation.** Lines and moments use what's really happening (their real schedule, the machine you really fixed, the tradition that really happened, who really came).
7. **The same ship gives the same social life** (the project's determinism rule): every choice is seeded per person, day and hour (`schedU`), never `Math.random`; running a day hour by hour or in one jump comes out the same.
8. **Writers never touch engine code.** All words are plain files under `content/`, baked into marked blocks of the game file and checked by a script.
9. **Phones first.** Card lines fit a phone (90 characters or fewer for a card line, 60 for a bubble); no new draw calls except the bunk keepsakes (one instanced mesh).

---

## Part 1: Getting to know someone, in steps

### The five tiers stay, and gain "steps"

The tiers and their points stay as built (stranger 0, acquaintance 10, colleague 30, friend 60, close friend 100; the points table in design-doc "Social life"). What changes is what each tier **means**. Each tier is a step in getting to know them, with things to learn and things that unlock:

| Tier | What you learn (Ask about…, chats, moments) | How they treat you | What unlocks |
| --- | --- | --- | --- |
| **Stranger** | Name, job, where they work | Polite; "cadet" | Chat, Ask about (work) |
| **Acquaintance** | A habit, a hobby, where they hang out | Say hello first; your name | They show on the Roster by name; small favours; small talk in chatter includes you |
| **Colleague** | What they think of their work; home and family (light); an opinion about someone aboard | First name; jokes; a running joke starts | A **light moment** (a small worry or a funny confession); invitations to group things (their tradition, a table at dinner); gifts matter more |
| **Friend** | Their struggle, hinted then told; their past | Nickname (from their voice card); they seek you out | **Heartfelt moments** (their struggle thread); bunk visits; personal invitations (dinner, the observatory); they cover a job, tip you off about parts, a good word to Calder |
| **Close friend** | The secret (the roster's tier-4 `about`); how the struggle turns out | "My favourite person aboard" | The **resolution moment**; a keepsake gift; they toast you at their birthday; they ask you for the favour that matters |

**Your knowledge of them is the visible progress.** The Crew app's page for a person shows "What you know" in sections (Work, Home, Hobby, Past, Their story). Each detail comes from the roster's `about`, the person's voice card, or a moment. **No counts** (the user, 2026-10-17: "too gamey"): the page just grows, and a section you know nothing of yet simply isn't shown.

### Time as well as points

Points alone let a player rush a friendship with favours in a day. So each step also needs **time known**: days since you met (`rel.met`), and for moments, days since the last moment. Starting numbers, to tune in play:

| Unlock | Tier | Also needs |
| --- | --- | --- |
| Light moment | colleague | met 3+ days ago |
| First heartfelt moment | friend | met 7+ days ago, 2+ days since their last moment |
| Next heartfelt moments | friend | 2+ days since their last moment |
| Resolution | close friend | 3+ days since the last heartfelt moment |

Points still arrive as now (favour +8, work +6, meal/appointment/birthday +3, chat +2, news +1), plus the new sources below (moments, gifts, visits, invitations kept, introductions, reputation's warm start). **Openness** comes from the voice card: shy or private people gain points 20% slower but their moments give 50% more; chatty and sociable people the other way round. So the quiet ones feel earned.

### Moments: really getting to know them

A **moment** is a short scene, 4 to 10 lines with one or two reply choices, played in the dialogue panel (section 18's `dialogueShow` with a moment script; the device's CRT strip). It's the user's "moments where you really get to know them, maybe their struggles".

**When a moment is ready**, the person's chat card gets a fifth button, **"Sit with them"** (or "Walk with them" if they're on the move between places), and their tap line hints at it ("Got a minute? Properly, I mean."). A moment only offers itself when:

- the tier and time rules above are met;
- you're both off shift, and they're somewhere calm: a lounge seat, the observatory, a common room, the garden, a bench, the mess after the dinner rush, or your bunk room (a visit), or at an appointment you made with them;
- no other serious moment has played for you today (light ones can share a day);
- the ship isn't mid-crisis for them (during the storm's onset, moments wait unless the moment is *about* the storm).

Nothing is ever forced: you can ignore the button forever. If you have an appointment with someone whose moment is ready, the moment plays there (so "Meet up" becomes the natural way to make room for one).

**Replies.** Each moment's choice offers up to three replies in four flavours: **listen** ("I'm here. Go on."), **cheer** (a joke, lightness), **practical** (offer help: often starts a favour that matters), **share** (something of your own). The person's voice card says which they need most (`needs: 'listen'`). The fitting reply gives +4 extra and a warmer reply line; the others are still kind and still move the story on. Every reply leaves a memory ("listened about Gran"), which later lines can call back.

**Struggle threads for everyone.** The story crew (Calder, Brennan, Holt, Vance, Marrow, Sato, the escort, plus Tomas, Pell, Rina already) get hand-written arcs. The other ~65 crew each get **one thread from a library of struggle themes**, assigned by the roster generator from their traits, life and age (deterministic, saved in the roster), plus one **joy** (a light thing they love and will share early). Themes (each a three-beat thread: hint at colleague, opens up at friend, resolution at close friend), written as templates with fill-ins from their roster data:

| Theme | Hint (colleague) | Opens up (friend) | Resolution (close friend) |
| --- | --- | --- | --- |
| Homesick | quiet at the windows | misses a place, a person, a food | a call home goes well; the galley makes the food |
| Exam nerves | studying at meals | afraid to fail the certification | passes (or retakes; either way, you were there) |
| Family worry | checks Mail a lot | someone at home is ill / struggling | news comes; good, or bittersweet with comfort |
| Feeling stuck | "same job, five years" | wants to try another department | asks their Chief; a trial shift |
| Not good enough | over-checks their work | a mistake they still think about | someone senior tells them it was fine; or you do |
| Lonely in a crowd | eats alone | doesn't know how to join in | you bring them to a tradition; they find a group |
| An old loss | quiet on a certain day | who they lost, and when | the quiet watch (day 300) or a small ritual with you |
| Secret talent | humming, sketching | shows you, shy | a little show (Pell's show format) or a gift they made |
| Burning out | always the last to leave | can't say no | takes a day off; you cover a small job |
| Leaving soon? | looks at transfer lists | unsure whether to stay | decides (they stay, mostly; leaving needs a roster change, so not now) |
| Old rivalry | sharp about someone aboard | why it started | the two make up (a crew-to-crew drama) |
| Starting over | evasive about the past | why they really came aboard | they say it out loud, and are glad they did |

Light moments at colleague come from the joy and from small confessions ("I've named the scrubber on Deck 4. Don't tell Calder."). That keeps the ratio about two light moments for every serious one.

**Pacing in numbers.** With today's points, a player who chats daily and eats with someone reaches friend in about 2 to 3 weeks (Tomas in the social check: a friend after two weeks). A whole three-beat thread therefore unfolds over about a month of play for the people you're closest to, while acquaintances stay at the light level. About 6 to 10 close friends in a long game feels right; nothing caps it.

### Story crew arcs (hand-written)

The existing four-beat arcs (Tomas, Pell, Rina) become the model, now told through moments rather than single card lines (their beats 2 to 4 become moment scripts, beat 1 stays a card line). New arcs, written by the writers from the head writer's outlines (the planner owns the writers' schedule; this plan owns the shape):

- **The escort** (your mentor, see Part 7): week 1 is their arc's opening; later beats are their own struggle (suggested: "not good enough", wondering whether they're ready to be a mentor at all).
- **Chief Calder**: the boss who certifies you. Strict, fair, funny when off duty. Her thread is about the apprentice she lost to a transfer and her fear of investing in juniors who leave. Beats open by tier *and* by your Works record (needs the progression hooks).
- **Chef Brennan**: the galley as her family; a recipe from her mother she can't get right in space (the garden can grow the herb; a favour that matters).
- **Chief Holt**: distrust of the Veyli, from an old incident; softens through the diplomatic visit if you're friends (ties to the event's discourtesy thread).
- **Commander Vance**: by the book; secretly writes terrible poetry for the ship's newsletter under a pen name.
- **Captain Marrow**: distant at first (rank); her arc only opens late (Officer rank or close friend) and is about the weight of command and the piano on Thursdays.
- **Dr. Sato**: her lab, her rules; an old discovery nobody believed.

---

## Part 2: Crew remember what you did (memories with decay)

### What a memory is

Each crew member keeps **up to 8 memories of you**: `SHIP.mem[crewId] = [[key, day, w], ...]`.

- `key`: what happened, from a fixed list of memory kinds (with an argument): `fav.lamp`, `fixed.<machine kind>`, `came.<traditionId>`, `show.pell-show`, `gift.tea`, `moment.<thread>.<beat>.<flavour>`, `intro.arrival`, `intro.dinner`, `missed.<apptId>`, `bday`, `visit`, `introduced.<otherId>`, `helped.storm`, `grubby` (you turned up unwashed), `meeting.<id>.<choice>`, `heard.<key>` (a friend told them).
- `day`: the ship day it happened.
- `w`: its weight, 0 to 100, set by its kind.

Memories happen through `memAdd(id, key, { w })`, called by section 20 itself, mostly from the ship notes bus (Part 6): `repair` (you fixed a machine they use), `favour`, `gift`, `tradition` (you came), `apptKept`/`apptMissed`, `choice` (a meeting reply), `introStep` (the planner's onboarding). Other sections never call it directly; they post a note.

### How they fade

Every ship day at 04:00 (on paper, with the hours), each memory loses weight by its kind's half-life; it's forgotten below 10. When a ninth memory comes, the lightest goes.

| Kind | Starting weight | Half-life |
| --- | --- | --- |
| Small (a chat topic, came to a tradition, a gift they were lukewarm about) | 30 | 7 days |
| Medium (a favour, a fixed machine they use, a liked gift, a kept appointment, a visit) | 60 | 21 days |
| Big (a moment, a loved gift, the show you came to, your help in the storm) | 90 | 60 days |
| Core (the intro, a resolution moment, the keepsake) | 100 | never |
| Sour (a missed appointment, turning up grubby) | 40 | 4 days |

No memory ever takes points away. Sour memories only change words ("You stood me up on Tuesday, you know. I'm over it. Mostly.").

### What memories do

1. **Lines call them back.** The line picker (Part 6) can match a memory: `mem:fav.lamp` gives "The lamp's still perfect, by the way." Each callback is said once per memory (it's marked told), so it never nags.
2. **Warmth.** The sum of a person's memory weights is their **warmth** toward you: how present you are in their life right now. It's separate from tier: a close friend you haven't seen in weeks has low warmth ("There you are! Thought you'd left the ship."). Warmth raises the odds of seeking you out, visits and invitations, and picks between "warm" and "missed you" greetings.
3. **Friends of friends hear.** A big memory becomes small news among their friends ("Rina says you sat with her all evening. That was kind."), which gives those friends a small memory too (`heard.<key>`, small) and a warmer first meeting.

---

## Part 3: Crew-to-crew relationships that change over time

### What's kept

The pair affinity (`SHIP.aff`, Int8 per pair, hourly drift from time together) stays: it's cheap and works. Changes:

1. **More visible life.** Today no pair starts at or below -30 and rivalries take about a month. Raise the clash penalty in `affStart` (-12 to -24, the handover's suggestion) and the clash drift, so a 2-week check shows a handful of rivalries (target: 2 to 6 rival pairs and 15 to 40 friend pairs after 14 days). Most of the ship still gets friendlier.
   *Measured and agreed with Social B (2026-10-17):* clash penalty -24, clash drift .4 an hour together, friendly drift .7 an hour up to 90, but only while both have fewer than their friend cap (4; 5 for chatty, sociable, warm or cheerful people; 3 for shy, private or quiet ones) or are already friends. Measured over 42 days: day 14, 18 pairs at 60+ (9 best, 7 friends, 5 mentors) and 2 rivals; day 42, 89 at 60+ (19 best, 63 friends, 11 mentors) and 12 rivals, levelling off. No drifting without shift changes or transfers, which is intended. Mentors: same department, a rank or more apart, the senior one patient, kind or steady (or `mentors: true` on their voice card), affinity 40+, at most 2 mentees each and one mentor each, formed once a day, dropped under 25; mentees are juniors or officers. The player's mentor bond with the escort is separate.
2. **Labelled bonds** for the pairs that matter, kept in a small map `SHIP.social.bonds[pairKey] = { kind, since }` (about 50 to 150 entries, not 2,701):
   - `friends` (affinity 60+), `best` (each person's mutual closest friend at 65+, at most one each; nobody reaches 85 with today's drift, measured by Social B);
   - `rivals` (-40 or below; may become a feud, as built);
   - `mentor` (same department, rank gap of one or more, affinity 40+, the senior one's voice card `mentors: true` or traits patient/kind/steady): mentors pass news and favours to their mentee and talk about them;
   - `drifting` (former friends whose affinity has dropped 15 below its peak: bonded friends not together for 4 days fade 1 a day, so it shows over weeks, usually because shifts, bunks or transfers moved them apart): a bittersweet line, and a chance for you to bring them back together.
3. **Pair stories.** A bond changing can start a small two-person story you witness: an argument in a corridor (two bubbles, as now), a reconciliation dinner (they sit together; `affinityPlan` gets a day hint), a mentor and mentee at the machine shop. Each is a `CONVOS` script (Part 6) with pair conditions.
4. **You as the connector.** On the chat card's Ask about… list, a new topic **"Do you know …?"** offers up to three people you know well who they don't (affinity under 20, you colleague+ with both). Picking one: if they're compatible (no clash), their affinity +15, both get a memory (`introduced.<other>`), and it's news. If they clash, a gentle "We've met. We're… different." and nothing changes. Mending a feud already works (chat to both).
5. **Couples in the background** (the user, 2026-10-17). A few established couples (about 4 to 6 pairs among the 74, fixed in the roster by the crew designer's generator as a `partner` field; adults of any gender, same rank band or not) are simply together: they start at affinity 90 with a `couple` bond, sit together, spend free time together, share a day off where rotas allow, and turn up in each other's lines ("{partner} says hello.", "{partner} and I are doing the quiz again."). No romance storylines, no break-ups, nothing that involves you; a couple can be part of someone's thread (missing a partner on another shift, a transfer that splits them; see Part 8b).
6. **They talk about each other.** Lines can name another crew member by bond: `{friend}`, `{best}`, `{rival}`, `{mentor}`, `{mentee}`, `{partner}` fill-ins ("Pell and I are doing the quiz together again." / "If you see Ade, don't mention the coffee machine.").
7. **Seating and plans already use `affinityPlan`** (pure, from starting affinity). It must stay pure for determinism. The deep system adds a **weekly** plan affinity: `affinityPlan(a, b, d)` returns the affinity as it stood at the start of that ship week (a snapshot saved once a week, 2.7 KB), so seating follows friendships that changed without plans ever reading live numbers mid-week. (Needs the sim engineer's OK: plans already built for this week don't change.)

---

## Part 4: Small gifts

**What you can give.** Gifts are things you carry in your hands, like parts (you already carry two items): you buy them at the crew store (a tin of tea, biscuits, a postcard, a little plant), pick them in the garden on harvest days (herbs, a tomato, a flower), or make them in the machine shop (a small trinket from scrap, once Works lets you: a keyring, a bookend, a little gear on a chain). The store's and the garden's lists get a `gift` tag; the machine shop gets three cheap "make" recipes.

**How you give.** With a giftable item in your hands, the chat card shows **Give …** (the item's name). One gift per person per ship week (`rel.giftWeek`), so it can't be farmed.

**How it lands.** Each voice card lists `loves` and `likes` (by gift tag: `tea`, `sweet`, `plant`, `garden`, `made`, `book`, `music`, `star`, ...). Loved: +10, a big memory and a delighted line; liked: +6, a medium memory; anything else: +2, a small memory and a polite line ("Oh! That's… thoughtful. Thank you."). Never negative. On their birthday, double, and they mention it at their cake. Gifts teach you about people: a loved gift adds "Loves tea" to "What you know".

**Crew give you things.** Friends now and then leave you something (once a week at most across the ship): a biscuit from Brennan, a sketch, a cutting. At close friend, after their resolution moment, each person gives a **keepsake** (from their voice card: Tomas's spare star map, Rina's Tiles piece, Pell's smallest music box). Keepsakes go on a **shelf by your bunk** (the deck architect adds one shelf place to Bunk 1 berth 4; keepsakes are small props on one instanced mesh, at most 8 slots, so one draw call). On your birthday (day 50), your friends remember it (cake if you've got 3+ friends; the galley already bakes for birthdays).

---

## Part 5: Bunk visits and invitations

### Visits to your bunk

From friend tier, a friend may **drop by your bunk room** in the evening (19:00 to 21:30) when you're there and awake: a prompt at the screen edge ("Rina knocks at the door.") like the wave-over. Tap it and they come in, sit on the bunk or the step, and the chat card opens with a visit line; if a moment is ready, it's offered first (visits are where many heartfelt moments happen). If you ignore it, they say something kind and go.

If you're **out**, sometimes they leave a **note on your bunk** instead: tap the bunk to read it (it also lands in Mail as "A note on your bunk"). Notes carry invitations, thanks for a favour, or a "missed you".

Odds: at most one visit or note a ship day, at most one per friend every 5 days, higher with warmth. During the first week, the escort's visit on night 1 is scripted by onboarding (the planner).

**How it's shown:** a visit is live and only on your deck: the crew member's agent walks to your bunk room door and in (section 10 needs a small hook, `crewComeTo(p, placeId, onArrive)`, which the friends-waving-you-over feature already wants). On paper their plan is unchanged; afterwards they walk back to it. Bunk 1's other residents (Tomas) are fine with it; at 22:00 visitors leave (quiet hours).

**Your own room, later** (the user, 2026-10-17). Once you're promoted and move into an officer's cabin (design-doc: walking the officers' corridor with your own key is the moment of promotion), you can **invite people over**: from the Crew app or a chat card, "Come over" makes an appointment of kind `visit` at your cabin for one friend or a small group (up to four, about an hour, 19:00 to 22:00). They turn up, sit, talk among themselves as well as to you (overheard lines between guests who get on), and it counts as a calm place, so moments can happen there. Hosting gives each guest +3 and a medium memory (`visit.yours`), and a little to your Kindness standing (Part 8). Until promotion, the bunk room's visits above are the version you have. Built after the progression hooks give a cabin; the plan keeps the shape ready.

**Visiting them:** crew quarters stay private (the privacy rule). A friend can **invite** you to their bunk room or cabin (an appointment of kind `visit`, using the sim engineer's `doorOpenFor`): an evening of Tiles with Rina, Tomas's star map. Without an invitation, their door stays locked as now.

### Invitations

Three kinds, all delivered the same way:

1. **To a ship tradition** (quiz, running club, film night, a birthday cake...). The traditions table (section 18) gets an optional `invite: { host, odds, line }`. Each morning at 07:00 the social system picks at most two invitations for the day: a colleague-or-better who's going to a tradition that day (their plan says so) asks you, the host first. The invitation is their tap line ("Quiz tonight. We need someone who knows the engines. You in?"), and if you haven't met them by 15:00, a short Mail from them.
2. **Personal**, from friends: dinner together, the observatory after dark, a walk round the promenade, help with their hobby, their bunk room for a game. Picked from their habits and voice card (`invites: ['observatory', 'dinner', 'tiles']`).
3. **Their moment's event**: a show (Pell's format, `eventOneOff`), a call home they want company for, a small ritual (the quiet watch).

**Saying yes** makes an appointment (the device's Appointments, `kind: 'invite'`), which they keep in their plan (section 14, as appointments already are). Keeping it: +3 (as appointments today) and a medium memory (`came.<id>`); a tradition joined with the person who invited you: +2 more. **Saying no** is fine ("Next time, then."), no cost. **Missing it**: the existing remark, and a sour memory.

**From officers:** summons and the Captain's table stay the events engineer's (C10); social only supplies who's warm to you.

---

## Part 6: How lines are picked (social state + the dialogue engine)

*Agreed with the Pillar 4 planner (draft 2): the planner's **dialogue engine** owns `lineFor(p, kind, ctx)` and the content pipeline; **section 20 decides which kind of line matters most** and owns the pure **query functions** that line conditions read. Writers never see either.*

### Who does what

1. **Section 20 picks the kind** (the order below: a missed appointment, then a moment ready, then a story beat, and so on down to a greeting), exactly as `chatLine` does today.
2. It asks the dialogue engine for the words: `lineFor(p, kind, ctx)` returns `{ text, id, kind }` or null (null: section 20 moves down its list).
3. `lineFor` gathers the person's own lines, their voice template's, then the shared bank for that kind; keeps those whose conditions all hold; scores the most specific highest (person's own above template above shared); takes off points for lines said recently (last 6 by this person, last 12 ship-wide, not saved); picks by `schedU(p.seed, hour, k)` so a second tap in the same hour says the same and the next hour moves on (as now); fills placeholders; applies the voice tokens.

What social needs from `lineFor` (the planner's dialogue engineer builds it): that scoring and seeding, the recently-said penalty, `told:` handling (a memory callback is said once and then marked told through `memTold(id, key)`), voice tokens from the voice card, and the social placeholders filled through the query API.

### The query API (section 20, pure, never changes state)

| Function | Answers | Condition in line files |
| --- | --- | --- |
| `relTier(id)` | 0-4 | `tier>=friend`, `tier<colleague` |
| `mem(id, key)` | the memory, or null; keys are `kind.arg` with prefix match | `mem:fav`, `mem:fav.lamp`, `mem:fixed.oven`, `mem:came.quiz` |
| `warmth(id)` | `'cold'` / `'warm'` (recent memories vs none for a while) | `warmth:cold` |
| `affBand(a, b)` | `'rival'` (-40 or less), `'neutral'`, `'friend'` (60+) | `aff:rival` |
| `bondOf(id, kind)` | a crewmate they have that bond with, or null | `bond:best`, `bond:mentor`, `bond:drifting`, `bond:couple` |
| `moodOf(p)` | `'low'` / `'ok'` / `'high'` (crewMood bands) | `mood:low` |
| `beatOf(arcId)` | beats told so far (`arcBeat(p, t)` already exists for "the next beat due", hence the new name) | `beat:tomas.3` |
| `knowsNews(p, newsId)` | bool | `news:<id>` |
| `repBand(dept)` | `'new'` / `'known'` / `'well'` / `'theirs'` | `rep:known` |
| `repShip(kind)` | `'low'` / `'ok'` / `'high'` for work, kindness, spirit | `ship.work:high` |
| `aboard(id, day)` | is that person on the ship that day | (engine only) |
| `knownFor()` | your tags | `you:reliable` |
| `cue(kind)` | a recent ship note still talked about (the bus, below) | `cue:repair.oven`, `cue:repair.oven.you`, `cue:tradition.quiz` |
| `flag(key)` | the shared flag store (section 13, beside the bus) | `flag:met.calder`, `week1:true` |

Other conditions are the dialogue engine's (`event:ionStorm.onset`, `time:morning`, `place:mess`, traits, dept, act, season, odds). The vocabulary freezes at the end of wave 1.

**Agreed with the dialogue engineer (session_01UmrVVpV7eBqEsa4sBucASP, 2026-10-17)**, on top of the table: tiers as `tier>=friend` (names stranger, acquaintance, colleague, friend, close); `told:<key>` (an untold memory; `lineFor` calls `memTold` after saying it); `beat:<arc>.<n>` = at least n beats told and `beat=<arc>.<n>` = exactly n; `aff:rival|neutral|friend` toward `ctx.other`, plus `aff:<crewId>:<band>` toward a named crewmate; `ship.work:high` style for the ship standings; `week1:true` = `inWeek1()` (an intro is running and `week1.done` isn't set; skip-intro sets it), not `week1.d2`; new social conditions `leaving:soon` / `leaving:you` (`leavingSoon(id)`), `newhere` (`newHere(id)`: arrived within 7 days), `moved:<id>` (`movedOff(id)`), `guide:true` (`flag('guide.active')`); `place:calm` reads section 20's `CALM_TYPES` (also used for moment readiness); `{thing}` from `memThing(key)`. Tone `#serious` is allowed only behind `tier>=friend`, a `beat:`, a `mem:moment` or `leaving:soon`. Extra line kinds: `goodbye`, `letter`, `newcomer`, `host`. Any condition can be negated with `!`.

**Placeholders social fills:** `{me}`, `{nick}` (what they call you, by tier, from the voice card), `{partner}`, `{friend}`, `{best}`, `{rival}`, `{mentor}`, `{mentee}`, `{boss}` (their Chief), `{thing}` (a memory's object: "the lamp"), `{trad}`. A line whose placeholder can't be filled is skipped.

**Voice:** a voice card's `words` replace tokens in any line: `{hi}`, `{bye}`, `{yes}`, `{thanks}`, `{wow}`, `{sigh}`, `{nick}`. So one shared line ("{hi}, {nick}. Busy day?") sounds like Holt ("Cadet. Busy day?") or like Pell ("Oi oi, spanner. Busy day?"). This is how 75 voices come cheaply from shared banks.

### The chat card's order, extended

The order of "what matters most" (today's `chatLine`) becomes, top first:

1. A missed appointment (built), the guests line (built).
2. **Week 1 lines** (onboarding's: the escort's checks, Calder's first-day line).
3. **A moment ready**: the hint line, and the "Sit with them" button.
4. A story beat (built; now mostly moments).
5. A feud (built).
6. Birthday (built), **a gift for their birthday you gave** (callback).
7. **An invitation** for today.
8. **A memory callback** (an untold memory, heaviest first, 60% of the time).
9. News (built).
10. **A reaction to a ship cue** (below), 50%.
11. How they feel (built), where they are (built).
12. A life detail (built), **their joy**, **talk about a bonded crewmate**.
13. A greeting by tier and warmth (built, now through `say`).

### Ship notes: reacting to what really happened

The planner's **ship notes bus** (`simNote(kind, data)` / `onSim(kind, fn)`, placed early in section 13 so load order never bites) is how every section tells the others what happened. Social listens to: `repair { who, machine, kind, deck }`, `favour { who, from }`, `tradition { id, day, came, you }`, `gift { to, item }`, `apptKept` / `apptMissed { id, with }`, `introStep { step, who }`, `eventPhase { id, phase }`, `choice { script, k, who }` (meeting replies), `jobAbandoned { machine, dept }` (reputation), `harvest`, `lateMeal`. From these it makes memories, reputation, gossip (which fixes "gossip is thin on quiet days") and **cues**: each note stays talked about for a day or two, read by `cue:` conditions ("The oven's working again. Someone's a hero." and, if it was you, "That was you on the oven? {thanks}!"). Social emits `tierUp { id, tier }`, `moment { id, who, beat }`, `bond { a, b, kind }`, `invite { from, id }` for others (onboarding's Settling-in list, the device).

### Overheard conversations

Two- to four-line exchanges between two crew as you pass (the planner's dialogue workstream: `content/overheard/*.lines`, played as alternating bubbles under the existing voice budget). Social's part: pair conditions read through `affBand` and `bondOf`, and news riding on a conversation is passed on (the second speaker learns it, on screen as on paper) through `newsAdd`'s spread. The dialogue engine plays them (agreed with the planner), with a small saved ring so none repeats within 7 ship days.

### Moment scripts

Moments use section 18's script shape exactly, plus a few fields:

```js
MOMENTS['rina:gran:2'] = {
  who: 'rina', thread: 'gran', beat: 2, tone: 'heartfelt',     // 'light' | 'heartfelt' | 'serious'
  tier: 3, metDays: 7, gapDays: 2,                            // when it's ready (Part 1's table; defaults by beat)
  where: ['calm'],                                            // 'calm' | 'visit' | 'appt' | a room name
  hint: 'Got a minute? Properly, I mean.',                    // the tap line while it's ready
  lines: [
    { who: 'rina', text: 'No news from the station for two days. I haven\'t slept.' },
    { who: 'rina', text: 'Gran used to say worrying is just praying with your hands tied.', pose: 'sigh' },
    { choice: [
      { text: 'I\'m here. Tell me about her.', flavour: 'listen', mem: 'listened', reply: { who: 'rina', text: 'She cheats at Tiles. Shamelessly. Let me tell you about the time…' } },
      { text: 'Want to lose to me at Tiles? Distraction.', flavour: 'cheer', reply: { who: 'rina', text: 'You? Beat me? Ha. Go on, then.' } },
      { text: 'I can ask Comms to watch for station traffic.', flavour: 'practical', favour: 'askComms', reply: { who: 'rina', text: 'Would you? That would really help.' } },
    ] },
    { who: 'rina', text: 'Thanks, {me}. Really.' },
  ],
  after: { mail: { after: 240, subject: 'Thank you', body: '…' } },   // optional: a Mail, a show (eventOneOff), a gift, a cue
};
```

Generated crew's moments come from **theme templates** (`MOMENT_THEMES.homesick = [beat1, beat2, beat3]`) whose lines use placeholders from their roster (`{home}`, `{family}`, `{hobby}`, `{since}`) and their voice tokens, so one well-written theme serves a dozen people and still sounds like each of them. A person's own `MOMENTS` entry, when a writer has written one, replaces the theme's beat.

---

## Part 7: The first week, from the social side (agreed with the planner)

The planner owns the arrival and the first week: `SHIP.intro = { step, day, done, skipped }`, the scripts, tutorials and the "Settling in" list. The seam with social is small:

- **Relationships:** onboarding calls `relAdd(id, 'intro:<step>', pts)`. After the arrival evening: the escort 10 (acquaintance), Tomas 10, Pell 5 (10 if Pell is the escort), Calder 3, Brennan 3 (the planner's numbers). Social never hard-codes the escort: it reads the escort's id from `SHIP.intro` (or the `escort.<id>` flag). Skip-intro sets the same end state.
- **Flags:** onboarding sets flags in the shared store (`flagSet('met.calder')`, `escort.<id>`, `mug`, `seedling`, `week1.d2` at Tuesday 06:00 ... `week1.done`; the store is section 13's, beside the bus, owned by the sim engineer and saved in the main save); line conditions read them (`flag:met.calder`).
- **Memories:** social listens for `simNote('introStep', { step, who })` and adds core memories (`intro.arrival` with the escort, `intro.dinner` with Calder and the escort, `intro.shadowShift` with the escort), so they can be called back for the rest of the game ("Remember your first day? You held the spanner upside down."). It also makes a **mentor bond** from the escort to you: extra week-1 lines (`week1:true`), a check-in each evening of week 1.
- **Gating:** social features stay quiet until onboarding's flags open them: chat cards always; favours from `week1.d2`; friends waving you over from `week1.d3`; invitations from `week1.d5`; moments and bunk visits after `week1.done`. The first-weekend tradition invitation comes from **Tomas** (your bunkmate, free that Saturday), sent on Friday by the planner's script through `socialInvite({ trad: 'sowing', day: 6, from: 'tomas' })` so it becomes a real appointment (Sowing morning in the garden, then film night). Halloran's part that week is the Friday mug at Works tea. A scripted escort visit on night 1 is the planner's call.

**The escort: Zeke Torres** (the user: "not Halloran, Zeke Torres or Pell, they're future friends"; the planner's pick, 2026-10-17). Works engine officer, Officer rank (one notch above you), cabin 4-14; curious, ambitious, knits scarves. His rota swaps with Halloran's so he's on duty that Sunday evening (Torres off Thursday and Friday, Halloran off Saturday and Sunday; the crew designer). Flag `escort.torres`, a mentor bond from Torres to you, the same starting numbers (Torres 10, Tomas 10, Pell 5, Calder 3, Brennan 3). He becomes story crew with a full voice card and an arc (suggested thread: ambitious and curious, wondering whether he wants Deck 6's engines for life, and whether he's any good at mentoring). Pell stays the junior friend next door; Halloran keeps his Friday mug at Works tea. Calder's days off move to Saturday and Sunday (she stops by Sunday dinner on her day off), Monday she runs the briefing, and your first solo job comes from her on Tuesday; the week-1 gates don't change (`week1.d2` = Tuesday).

## Part 8: Reputation (a fuller system, the user's ask)

The user, 2026-10-17: reputation can dip, and "add a reputation system". So reputation is a system of its own, in two layers, with consequences you feel. It stays cozy: it never locks a friendship, never fails you, and always recovers with good work.

### Layer 1: standing with each department

Each department keeps a standing with you: `SHIP.rep.dept[dept]`, 0 to 100, starting at 10 (Works at 20: they know you're coming). Nine departments: command, helm, comms, works, watch, survey, infirmary, galley, store.

| Raises it | How much |
| --- | --- |
| A machine fixed that the department uses (the machine's room's owner: the galley's ovens, the infirmary's air, the bridge's relays) | +3 (+5 if it was failing) |
| A favour for one of them | +2 |
| Being at their tradition (Works tea, Survey's observatory night) | +1, once a week |
| A meeting reply that helps them | +1 to +3 (the script says) |
| A close friend in the department | lifts its floor by 5 each |

| Lowers it (gently) | How much |
| --- | --- |
| A job on one of their machines you took and left past `YOU_KEEP` (the systems engineer's limit) | -2 |
| One of their machines failing while a job for it sat on the board unclaimed during your shift (and you were free) | -1, at most once a day |
| A missed appointment with one of their officers | -1 |

Standing never goes below its floor (0, or 5 per close friend there), and drifts back up toward the floor by 1 a week when it's below it, so a bad patch fades.

| Band | Name in Record | Consequences |
| --- | --- | --- |
| 0-19 | "New face" | strangers start at 0; their gossip about you is neutral or grumbly when you've let them down ("Is the new tech ever going to look at our chiller?") |
| 20-39 | "They know your name" | strangers there start at 4 points; reputation lines (`rep:known`) |
| 40-69 | "Well thought of" | strangers start at 8 (nearly acquaintance); favours from them 50% more often; their tradition invites you; their crew **ask for you by name** on jobs (a job on their machine is marked "asked for you" on the board) |
| 70-100 | "One of theirs" | their Chief mentions you to Calder (a Record note toward promotion); their crew defend you in gossip; a department "thank you" (Brennan's biscuits for the galley; a round at the bar for Watch); you're on their guest list for their occasions (a Survey briefing, the galley's tasting night) |

### Layer 2: the ship's view of you

Three ship-wide standings, `SHIP.rep.ship = { work, kindness, spirit }`, each 0 to 100, built from what you do (a running score with a slow pull toward the middle, so it tracks recent weeks, not a lifetime):

| Standing | What builds it | What brings it down (gently) |
| --- | --- | --- |
| **Work** (reliable, skilled) | jobs finished and turned in, failing machines fixed, being at work on time (the sim knows where you are at shift start), event jobs taken in meetings | jobs left past `YOU_KEEP`, being well late for shift, skipping a summons |
| **Kindness** (a good shipmate) | favours, gifts, visits hosted, moments where you listened, smoothing over feuds, guiding a newcomer | missed appointments, declining many favours in a row (only the streak counts, not one no) |
| **Spirit** (part of ship life) | traditions joined, events joined, birthdays wished, chatting with people outside your department | none: staying in is never punished; it just doesn't build |

**Consequences:**

- **Promotion and trust.** Calder's view of you (the progression hooks, Pillar 3 Part 4) reads Work and Works' standing; certification steps want "Work: steady" or better. The Captain's table and briefings (the events engineer's C10) read all three.
- **Gossip about you.** Each standing gives you a reputation that crew pass on as news: high ones ("Ask {me}, they always turn up.", "{me} sat with Rina all evening when her gran was ill."), low Work ones ("The new tech's been missing shift starts, Calder's noticed."). Strangers who've heard it greet you accordingly (`rep:` and `you:` conditions).
- **Who comes to you.** High Kindness: more favours and visits, and crew confide sooner (moments' time gates shortened by a day). High Spirit: more invitations, and you're asked to help run a tradition now and then (carry the quiz answer sheets, hand out lanterns). High Work: crew bring you urgent jobs first ("asked for you").
- **Low standings** never take tiers or friends away. They show as words: grumbles in gossip, a cooler first meeting with strangers, Calder's note in your Record ("Two late starts this week. Let's not make it a habit."), fewer invitations from officers. Doing well again lifts them within a week or two.
- **Known for:** the system counts what you do and gives you up to three tags with the most behind them (`reliable`, `kind`, `chatty`, `night owl`, `quiz regular`, `gym rat`, `always at the garden`, `the one who fixes ovens`, `good with newcomers`). Lines with `you:reliable` conditions pick them up.

**On screen:** the Record app (section 19) shows a "Reputation" page in words only, never numbers: the nine departments by band, the three ship standings as short phrases ("Work: dependable", "Kindness: the one people go to", "Spirit: often seen at things"), and what you're known for. A change of band is a quiet badge on the Record app, never a toast.

---

## Part 8b: Crew come and go (the user's ask, 2026-10-17)

"Not often." The Wren's crew changes a little over time: some are transferred off, new crew arrive, including new cadets like you, and at some point you're asked to guide a newcomer the way you were guided.

### How it works without breaking the ship

- **A fixed reserve pool.** The roster gains about **12 reserve crew** (`ROSTER_RESERVE`, generated like everyone else, with full data, voice cards and threads), who start off the ship. Social's arrays (affinity, knowledge, memories) are sized for all 74 + 12 from day one, so a transfer never changes their shape and **saves never reset**. Each person gets `aboard: [fromDay, toDay]` (null for always).
- **Crew rotation day.** A deterministic calendar (the crew designer's generator, read by the sim engineer): about **every 6 ship weeks**, a Sunday shuttle takes **1 to 3** crew off and brings **1 to 3** on, the bunks and cabins they free going to the arrivals. Nobody leaves in the first 4 weeks of a game. The first rotation brings a new cadet; later ones sometimes do.
- **Keys:** relationships, memories and knowledge are keyed by crew id, and affinity by a reserve-sized index (74 + 12), so ids beyond today's 74 work from day one.
- **Who leaves** (chosen when the rotation is planned, 10 days ahead, seeded): never the Captain, the Chiefs, the escort, Tomas, Pell or Rina; never someone mid-heartfelt-thread (a thread's beat in progress); preferably someone whose thread has ended, or whose thread is "Leaving soon?", which can now resolve either way. A couple transfers together, or one stays and it becomes part of the other's thread. The player's close friends **can** leave: the goodbye is the point (the user).
- **What the sim does:** before `fromDay` and after `toDay` a person has no plan on board (`schedPeople` skips them); on rotation day the leavers walk to the shuttle bay for 15:00 and board; the arrivals walk off the ramp, to their quarters, to dinner (onboarding's escort lead mode, with a crew member as their escort).

### Goodbyes (social)

- **News first.** When a transfer is planned (10 days ahead) it's news, spread the usual way ("Did you hear? Okoro's transferring to the Halcyon."), and it changes what the leaver says (`trad:` style condition `leaving:soon`).
- **A day or two before** (the user): anyone who knows you at **acquaintance or better** finds you (a wave-over prompt, or a visit at friend tier) for a **goodbye**: a short scene in the dialogue panel that **talks about your friendship**, built from their heaviest memories of you ("The lamp. The quiz. That night you sat with me when Gran was ill."), their tier, and their thread. Writers write goodbye scripts per tier and per voice template, with memory callbacks as slots; story crew and close friends get their own. A close friend gives you a keepsake (Part 4).
- **On the day:** a small gathering at the shuttle bay (a gathering in the events engineer's format, `gathering({ id, where, at, who })`): their department, their friends and you if you come. A last line each; they walk up the ramp. If you weren't there, a Mail ("Sorry I missed you at the shuttle…").
- **After:** they're not gone from your life. Friends and up send **letters** now and then (Mail from "the Halcyon", every couple of weeks at first, then rarer), using their voice and your memories, and they stay in the Crew app under "Moved on". Crew left behind talk about them (`bond:` lines with a "missed" form). A couple split by a transfer is a thread for the one who stays.

### New arrivals

- New crew arrive on rotation day: news before ("We've got a new navigator coming Sunday"), the dinner with their department, then they're strangers like anyone, with a short "new here" period (week-1 style lines of their own: lost in the lift, asking where things are).
- **New cadets like you** arrive the same way you did, met by someone one notch above them. Tomas's thread ends with him meeting the next arrival (the planner's arc).

### Guiding a newcomer (your assignment)

"At some point you get an assignment to guide a newcomer the way you were guided." When the first new cadet arrives after you've been aboard at least **4 ship weeks** and Works thinks well of you (standing "They know your name" or better), Calder assigns them to you (a meeting, or a Mail if you miss it). Then:

- **You are the escort.** The arrival steps run in reverse: you meet them at the ramp, lead them through the haulway to their bunk and to dinner, and shadow them on their first job (the onboarding engineer's escort modes with the newcomer as the follower; you're always in control, and you can hand them back to Calder at any point with no penalty).
- **They ask you things.** Their lines come from a `newcomer` line bank (where is the mess, who's the scary one, is the food always this good), and your answers are reply choices (helpful, funny, honest), echoing your own first week.
- **Social side:** a mentor bond from you to them, memories both ways, their tier with you starts at acquaintance, Kindness and Works standing go up as they settle in, a `good with newcomers` tag, and the first-week moments of *their* arc involve you. Later they're the one who waves you over at the quiz.

### Data and checks

- Roster fields (crew designer): `ROSTER_RESERVE`, `aboard`, `partner`, `transferTo` (the ship they go to, for letters).
- Social state: `SHIP.social.moved` (who left, when, their last memories for letters), saved; letters ride on `SHIP.social.mail` (built).
- `social_check`: run 14 weeks on paper with rotation on: nobody leaves mid-thread or in the first 4 weeks; arrays never change size; a save made before a rotation loads after it; goodbyes fire 1 to 2 days before for acquaintances and up; letters arrive; the newcomer assignment fires once its conditions hold.

## Part 9: The data writers fill (shapes)

Writers and designers write **plain files under `content/`** (the planner's pipeline): `content/lines/<crewId>.lines`, `content/overheard/*.lines`, `content/reactions/*.lines`, `content/arcs/<id>.arc`, `content/traditions/<id>.trad`, and for social: `content/voices/<crewId>.voice` (voice cards), `content/themes/<theme>.arc` (the struggle-theme library), `content/gifts.list` (gift tags and items). The planner's `content_gen.py` bakes them into marked blocks of the game file (`// ---- BEGIN LINES ... END LINES` and so on), and `lines_check.py` lints them. The file syntax is the planner's; **what each baked block must hold is below** (the shapes section 20 reads, written as the JS the generator produces). Engine tuning (memory kinds, weights, half-lives, time gates, odds) stays in section 20 as one table the engineers tune, not in `content/`.

### Voice card (one per crew member; story crew hand-written, the rest start from a template)

```js
VOICE.rina = {
  tpl: 'dry',                          // the template it builds on (VOICE_TEMPLATES)
  talk: 'Dry, quick, deadpan; teases the people she likes; never says how she feels straight out.',   // for writers, not shown
  cares: ['her gran', 'Tiles', 'the infirmary running right'],
  jokes: ['she has never lost at Tiles (she has, once)', 'calls the doctor "the boss of bones"'],
  words: { hi: ['Oh, it\'s you', 'Hey'], bye: ['Off you go', 'Don\'t break anything'], yes: ['Fine', 'Go on then'], thanks: ['Ta', 'You\'re all right, you'],
           wow: ['Well, look at that'], sigh: ['Honestly'], nick: [null, null, '{me}', 'trouble', 'trouble'] },   // nick by tier
  needs: 'cheer',                      // which reply flavour fits her best in a moment
  openness: 'guarded',                 // 'open' | 'normal' | 'guarded': how fast points come, how much moments give
  loves: ['game', 'sweet'], likes: ['tea', 'garden'],
  invites: ['tiles', 'running'],       // personal invitations she makes
  joy: 'Tiles',                        // the light thing she shares early
  thread: 'gran',                      // her struggle (a story arc, or a theme for generated crew)
  keepsake: 'a Tiles piece, the cheating one',
  avoid: ['talking about her sister'], // topics writers keep her off
  lines: { greet: [ { text: '{hi}. You look like you lost a fight with a scrubber.', tier: [1, 4] } ], … },   // her own lines, any kind
};
```

**Templates for the generated crew.** About 10 `VOICE_TEMPLATES` (`warm`, `dry`, `shy`, `brisk`, `chatty`, `earnest`, `gruff`, `dreamy`, `steady`, `playful`), each with its own `words` and lines, picked from the roster's traits by the generator. The generator also writes each generated person's small personal fields (`loves`, `likes`, `joy`, `thread`, `needs`, `openness`, `keepsake`) from their traits, habits and life, so every one of the 74 has a full card on day one. Writers then improve cards one by one (the head writer's list: department chiefs and officers first, then anyone who shows up a lot).

### Line banks

```js
LINES.greet = [ { text: '{hi}, {nick}.', tier: [1, 4] }, { text: 'Morning! Or is it evening? I lose track.', tier: [0, 1], time: 'night' }, … ];
LINES.callback = [ { text: 'The lamp\'s still perfect, by the way.', mem: 'fav.lamp' }, { text: 'Still can\'t believe you came to the quiz. You were robbed on the reactor question.', mem: 'came.quiz' }, … ];
LINES.cue = [ { text: 'Did you hear? Someone fixed the oven. Breakfast on time for once.', cue: 'repair.oven' },
              { text: 'That was you on the oven? {thanks}!', cue: 'repair.oven.you', dept: 'galley' }, … ];
LINES.invite = [ { text: '{trad} tonight. You in?', trad: 'today' }, … ];
LINES.visit = [ … ];  LINES.note = [ … ];  LINES.gift = { loved: [ … ], liked: [ … ], polite: [ … ] };
LINES.about = [ … ];   // what they say about a bonded crewmate: { text, bond: 'best' }
```

Line kinds (the head writer's checklist, with a target count each so the planner can size the writing): `greet` (by tier × warmth × time), `bye`, `chat` (after Chat), `near` (by place and act), `feel`, `life`, `joy`, `callback` (per memory kind), `cue` (per cue), `invite`, `accept`, `decline`, `visit`, `note`, `gift`, `about` (crewmates), `rep` (your standing), `knownFor`, `week1`, `smalltalk` (chatter by act), `rumour` (news openers), `hint` (a moment is ready). The current hard-coded lists (`CHAT_GREET`, `CHAT_NEAR`, `CHAT_LIFE`, `CHAT_DEPT`, `CHATTER_IDLE`) move into these banks unchanged at the first build, so nothing said today is lost.

### Moments, themes, convos

The shapes in Part 6 (`MOMENTS`, `MOMENT_THEMES`, `CONVOS`). A theme beat names the roster fields it needs (`needs: ['home']`) and is skipped for anyone without them.

### Writers' rules (in the head writer's brief)

- Plain text in the planner's file format (the generator handles quoting).
- British spelling, as the game already uses; short sentences; one idea per line.
- A card line 90 characters or fewer; a bubble 60 or fewer; a moment line 140 or fewer.
- Never contradict the roster (`bio`, `life`, `about`, `habits`, `birthday`): the check flags lines naming a habit the person doesn't have.
- No romance with the player, no flirting; nothing cruel; serious is fine when it's earned (friend tier and up).
- Never mention things the game doesn't have (no photos, no Camera app, no weapons).

---

## Part 10: Simulated cheaply, saved, tested

### Cost on a phone

| Work | When | Cost |
| --- | --- | --- |
| Affinity drift, news spreading (built) | once a ship hour (100 real seconds) | small (the social check runs 14 days hour by hour in seconds); to be timed in S1 |
| Bonds update | in the same hourly pass, only for pairs whose affinity crossed a line | tiny |
| Memory fading, warmth, reputation floors | once a ship day (04:00) | 75 × 8 multiplications |
| Invitations, visits' odds, gifts from crew, cues expiring | once a ship day (07:00) and on a few minutes' ticks | a few hundred checks |
| Moments ready? | only when you tap someone | one person |
| The line picker | only when a line is shown (a tap, a bubble every 12+ s) | filters a bank of a few hundred lines: under 0.2 ms |
| Overheard convos | the chatter tick (once a ship minute, near you only) | as chatter today |

Nothing new is drawn except the keepsake shelf (one instanced mesh) and visitors (agents already on the deck). Crew on other decks are on paper only, as now. The words data adds an estimated 150 to 300 KB to the file by the end of the pass (75 voice cards × about 1 KB, 1,500 to 2,500 lines × about 80 bytes, 40 moment themes × 3 beats, 60 story moments); the planner and the lead should keep an eye on the file size (now about 1 MB) for phone load time.

### Saving

Everything new joins `save.social` (no new `SAVE_V`: missing fields load as empty, so old saves keep working):

- `mem`: `{ crewId: [[keyIndex, day, w, told], …] }` with a key dictionary `memKeys: [...]` so keys are stored once (about 75 × 8 × 12 bytes ≈ 7 KB at the most, usually far less);
- `rep`: `{ dept: nine numbers, ship: { work, kindness, spirit } }`; `knownFor`: a handful of counters; `moved`: crew who left (id, day, their last memories for letters);
- all per-crew arrays (affinity, knowledge, memories) sized for the roster **plus the reserve** (74 + 12 = 86: 3,655 pairs, 3.6 KB), so transfers never change the save's shape; the save's crew-list hash covers the whole list, reserve included;
- `bonds`: the labelled pairs (about 3 KB at most);
- `affWeek`: the weekly snapshot for planning (2.7 KB, base64 like `aff`);
- per relationship (the array in `save.social.rel`), new slots: `giftWeek`, `moment` (beats told per thread), `momentDay`, `visitDay`, `inviteDay`.

Target: the social part of the save stays under **30 KB** (today's limit in `social_check` is 20 KB; raise it with the lead's OK).

### Testing

**`social_check.py`, extended** (the social engineer's checker; same harness):

1. Determinism: 14 days hour by hour twice, and as one jump, identical (built) now including memories, bonds, rep, invitations and the weekly snapshot.
2. Save round trip, size under 30 KB (built, extended).
3. Sensible numbers after 14 days: friends 15-40 pairs, rivals 2-6, at least one `mentor` bond; drifting is checked by a forced test (a bonded friend pair kept apart for 3 weeks becomes `drifting`), and appears naturally in the rotation run once crew come and go (friends who meet daily never drift); memories per person (median and max), how many faded; reputation per department for a stand-in player who fixes galley machines (galley "They know your name" or better, others lower).
4. A stand-in player who chats with Tomas daily, eats with him, gives a loved gift and keeps an appointment: friend by day 14, his first heartfelt moment ready by day 14 and not before day 7, never two serious moments in one day.
5. Invitations: about 0.5 to 2 a day once week 1 is done; none during week 1 except the scripted one; each one's appointment fits the person's real plan.
6. Visits: a stand-in friend visits within 10 evenings of you sitting in your bunk room; no visit after 22:00; no visitor stuck (their agent gets back to its plan).
7. Phone budget: the hourly pass and the daily pass timed (hourly under 1 ms, daily under 5 ms on the test machine).

**The planner's `lines_check.py`** covers the writers' files; social asks it to check, for social data: every key is known, every line's placeholders and voice tokens are real, lengths, duplicates, every crew member has a voice card and a thread, every theme beat has fallbacks, every story arc's beats exist with their tiers, choices have 1 to 3 replies with flavours, no banned words (the romance list), no habit named that the person lacks, and prints counts per kind against the head writer's targets. Social asks for one extra: render 20 random chat cards per tier as text so the head writer can read a sample.

Other checks: `cadet_test` stays pixel-identical on decks until the keepsake shelf (Bunk 1 only); `day_check` must show nobody stuck with visits on; `events_check` with tradition invitations on.

---

## Part 11: Interfaces with the other workstreams

| With | They give social | Social gives them |
| --- | --- | --- |
| **Pillar 4 planner** (onboarding, first week) | `relAdd(id, 'intro:<step>', pts)`, flags (`flagSet`), `simNote('introStep')`, the scripted first-weekend `socialInvite`; the ship notes bus and the flag store (section 13) | memories and the escort's mentor bond from intro notes; the gating of social features by week-1 flags (Part 7) |
| **Planner's dialogue workstream** (dialogue engineer, head writer, writers) | `lineFor(p, kind, ctx)`; `content/` files baked by `content_gen.py`; `lines_check.py`; overheard conversations | the kind order; the query API (Part 6); the voice-card, theme and moment shapes (Part 9); `memTold` for callbacks |
| **Events / traditions designers** (section 18) | `invite: { host, odds, line }` on traditions; `simNote('tradition', { id, day, came, you })` after each; `simNote('choice', ...)` for meeting replies | who's warm to you (`relTier`, `warmth`) for invitations and the Captain's table |
| **Device engineer** (section 19) | the Crew app page draws "What you know" sections (no counts) and a "Moved on" list; the Record app's Reputation page (words only);  Appointments takes `kind: 'invite'` and `'visit'`; the dialogue panel plays moments | `crewContacts()` gains `knowSections`, `warmth`; `repView()` (department bands, the three ship standings as phrases, known-for tags); `momentShow(id)` (wraps `dialogueShow`) |
| **Sim engineer** (sections 10, 14) | `crewComeTo(p, placeId, onArrive)` for visits and friends walking over; plans that skip people outside their `aboard` window and the rotation-day walks; the flag store and the bus in section 13; appointments of kind `visit` with `doorOpenFor`; `affinityPlan` reading the weekly snapshot | the weekly snapshot, pure |
| **Systems engineer** (section 17) | `simNote('repair', { who, machine, kind, deck })` when a repair finishes; `simNote('jobAbandoned', ...)`; the machine's department (`machineDept(m)`, or a table social keeps); unfinished-job events for reputation | favours that matter (from moments' practical replies) on the existing favour API |
| **Galley / garden** (section 16) | gift-tagged items (garden produce on harvest days); `simNote('lateMeal')`, `simNote('harvest')` | nothing new |
| **Player engineer** (section 15) | carried items with a `gift` tag; the store's gift list; the bunk tap for notes | `Give` on the chat card |
| **Crew designer** (section 9, the generator) | `ROSTER_RESERVE` (about 12), `aboard`, `partner` (4 to 6 couples), `transferTo`, the rotation calendar; each person's `tpl`, `loves`, `likes`, `joy`, `thread`, `needs`, `openness`, `keepsake`, `home`/`family` fields for themes; more `about` details (45 today: aim for 6 or more per person) | the field list |
| **Deck architect** | one keepsake shelf place by Bunk 1 berth 4; "calm" tags on places (which seats count as somewhere to sit and talk) | the list of calm place types |
| **Performance engineer** (8/8b) | the `sigh`, `laugh`, `listen` talk poses for moments and visits; the keepsake instanced mesh | nothing new |

`schedU` keys: section 20 uses 600 to 643; the deep system takes **644 to 699** (the planner's map: arrival 700-749, lines 750-799, new traditions 434-499). `lineFor` is the dialogue engineer's (section 22, builds 0.43.x).

---

## Part 12: Build steps

**Two social engineers** (the planner's staffing, agreed): **Social A** owns section 20 on `claude/social` and carries on the social range **0.36.20+**; **Social B** works in a marked sub-block `// 20c. SOCIAL STORIES` (so their merges never clash) on branch `claude/social-stories`, range **0.39.x** (set by the planner). Each step is small exact-string edits, a build number bump, a DEV_NOTES row, the full test set, a push and a report, as CLAUDE.md asks. Steps marked *(inert)* change nothing you can see.

**Wave 1 (foundations, before the writers' vocabulary freezes; alongside the planner's dialogue engine and arrival):**

| # | Who | Build | What | Sections touched | Depends on |
| --- | --- | --- | --- | --- | --- |
| A1 | A | 0.36.20 | **The query API** *(inert)*: `mem`, `warmth`, `affBand`, `bondOf` (stub until B2), `moodOf`, `beatOf`, `knowsNews`, `repBand` (stub until A6), `knownFor` (stub), `cue`; listeners on the ship notes bus | 20 (+ the bus in 13, the planner's) | the bus |
| A2 | A | 0.36.21 | **Memories with decay**: `SHIP.mem`, `memAdd` from bus notes, daily fading, `memTold`, warmth; save | 20 | A1 |
| A3 | A | 0.36.22 | **The kind order calls `lineFor`**: today's hard-coded lists (`CHAT_GREET`, `CHAT_NEAR`, `CHAT_LIFE`, `CHAT_DEPT`, `CHATTER_IDLE`) move to `content/` unchanged (same lines out, `cadet_test` identical); the extended order with callbacks and cues | 20 | A1, the dialogue engine |
| A4 | A | 0.36.23 | **First week gating**: flags read, intro memories, the escort's mentor bond, `socialInvite` | 20 | A2, onboarding's flags |
| B1 | B | 0.39.0 | **Voice cards and steps**: `VOICE` read (generator fields from the crew designer, fallback by traits until then), openness, "What you know" sections for the Crew app (no counts), time-known gates | 20c (19 draws; 9 generator) | A1 |
| B2 | B | 0.39.1 | **Crew-to-crew**: clash tuning, bonds (friends, best, rivals, mentor, drifting), `bondOf`, "Do you know…?" introductions, the weekly affinity snapshot for `affinityPlan` | 20c (14 reads the snapshot) | A1 |

**Wave 2 (the deep features):**

| # | Who | Build | What | Sections touched | Depends on |
| --- | --- | --- | --- | --- | --- |
| B3 | B | 0.39.2 | **Moments**: arcs engine reading `content/arcs` and `content/themes`, readiness, the "Sit with them" button, `momentShow` on the dialogue panel, reply flavours, after-effects, one serious moment a day; Tomas, Pell and Rina's arcs moved into moments | 20c, 18 (`dialogueShow` takes a moment script: one line) | B1, A2 |
| A5 | A | 0.36.24 | **Gifts**: gift tags, Give on the card, loves/likes, crew gifts, keepsakes and the shelf | 20, 15 (carried item tag), 16 (garden items), Deck 4 shelf (architect), 8b (instanced mesh) | A2, B1 |
| A6 | A | 0.36.25 | **The reputation system**: department standings and the three ship standings (Work, Kindness, Spirit), bus sources (repairs, jobs left, late for shift, favours, traditions), floors and recovery, bands and their consequences (warm starts, "asked for you" jobs, reputation gossip, Calder's Record notes), "known for", the Record's Reputation page | 20, 17 (`jobAbandoned` note, the "asked for you" mark), 14 (on time for shift), 19 draws | A2 |
| A7 | A | 0.36.26 | **Invitations**: tradition invites, personal invites, `kind: 'invite'` appointments, Mail fallback | 20, 18 (`invite` fields), 19 (appointment kind) | A2, A4 |

**Wave 3:**

| # | Who | Build | What | Sections touched | Depends on |
| --- | --- | --- | --- | --- | --- |
| A8 | A | 0.36.27 | **Bunk visits and notes**: the prompt, `crewComeTo`, visit lines, notes on the bunk, invitations to their quarters | 20, 10 and 14 (sim engineer), 15 (bunk tap) | A7, B3 |
| B4 | B | 0.39.3+ | **Story crew arcs** as the writers deliver them (the escort, Calder, Brennan, Holt, Vance, Sato, Marrow), the theme library filled, pair stories | 20c, `content/` | B3 |
| A9 | A | 0.36.28 | **Crew come and go, social side**: arrays sized for the roster plus the reserve, `aboard` windows respected, transfer news, the farewell at the shuttle, letters after, "Moved on" in the Crew app, new arrivals' "new here" lines | 20 (9: `ROSTER_RESERVE`, `aboard`, `partner`, `transferTo`, rotation calendar by the crew designer; 14: plans skip people not aboard, rotation-day walks, sim engineer; 18: the shuttle gathering) | A2, B3 |
| B5 | B | 0.39.4 | **Goodbye moments**: the scenes 1 to 2 days before a transfer that talk about your friendship, built from their heaviest memories of you, on the moments engine | 20c | B3, A9 |
| B6 | B | 0.39.5 | **Couples in the background**: the `couple` bond from the roster's `partner`, `{partner}` lines, seating and free time together | 20c (9: `partner`) | B2 |
| A10 | A | 0.36.29 | **Guiding a newcomer**: Calder's assignment, the newcomer's mentor bond and questions (`newcomer` lines with reply choices), standings and the `good with newcomers` tag | 20 (21: the onboarding engineer reuses the escort modes with you leading) | A9, the arrival |
| A11 | A | later | **Your own room**: "Come over" visits to your cabin after promotion | 20, 14, 19 | A8, promotion (progression hooks) |
| A12/B7 | both | — | **Tuning pass** with `social_check` numbers and the user's play | 20, 20c | all |

The writers' work runs alongside from wave 1 (the shapes and vocabulary freeze at its end): story crew voice cards first, then line banks by kind, then moment themes, then the story arcs. Each delivery passes `lines_check` before the lead merges it.

**Also needed:** the **crew designer** for the generator fields (B1) and the reserve pool, `aboard`, `partner`, `transferTo` and the rotation calendar (A9, B6), the **sim engineer** for `crewComeTo`, `affinityPlan`'s snapshot and people who aren't aboard (A9), the **onboarding engineer** for guiding a newcomer (A10), this designer on call for questions and the tuning pass. Moments (B3) before the first-week check-in if possible, since the user asked for them by name.

## Risks

- **Too many words to write.** 75 voices and thousands of lines is a lot. *Answer:* templates and voice tokens make shared lines sound personal; generated crew start complete from the generator; writers improve the people the player meets most first; `lines_check` counts against targets so we know what's thin.
- **Repetition.** The same line twice in a minute kills the illusion. *Answer:* the recently-said penalty per person and ship-wide; callbacks said once; more variants for the kinds that fire most (greet, near, smalltalk).
- **Serious tone creeping in.** *Answer:* one serious moment a day at most, serious only from friend tier, two light moments for each serious one in each thread, and the head writer's tone pass.
- **Visits feel intrusive.** *Answer:* only friends, only evenings, only when you're there and awake, at most one a day, easy to ignore, never during quiet hours.
- **The player games gifts or favours.** *Answer:* weekly gift limit, daily favour limit (built), time gates on moments.
- **Determinism breaks** (memories or visits reading live state into plans). *Answer:* plans only read the weekly snapshot; live visits never change the paper plan; checks run twice and compare.
- **File size on phones.** *Answer:* words kept compact (no repeated keys where a short form works), measured each build; if it grows past the lead's budget, move rarely-used banks (convos for decks you're not on) into a compressed string unpacked on first use.

## The user's answers (2026-10-17), and where they went

1. **The escort:** not Halloran: **Zeke Torres or Pell**, "future friends"; the planner picked **Zeke Torres** and aligned the rotas (Part 7).
2. **Crew-to-crew romance:** **yes, a few established couples in the background**, never involving the player (Part 3, B6).
3. **How serious:** **all of it is OK**, including gentle grief; nobody dies on screen (ground rule 10; the "An old loss" theme stays).
4. **Bunk visits:** **yes**, and **later your own room** to invite people over after promotion (Part 5, A11).
5. **Machine-shop gifts:** **yes** (Part 4).
6. **Reputation dipping:** **yes, and add a reputation system** (Part 8, rewritten as two layers with consequences; A6).
7. **"What you know" counts:** **no, too gamey**; the page just grows (Part 1).
8. **Also asked for:** crew transferred off with goodbyes a day or two before and on the day; new crew and new cadets arriving; an assignment to guide a newcomer (Part 8b; A9, A10). Varied days off for everyone (the sim's; visits, invitations and waving use each person's real days off). Tiles as a playable game later in the pillar (the planner's; social adds Tiles invitations and Rina's thread).

No open questions remain on the social side. Numbers (points, half-lives, odds, gates) are starting values to tune in play.

## Appendix: the new shared formats, in one place

```js
// 20. SOCIAL (deep, Pillar 4): pure queries (line conditions read only these)
relTier(id) ; mem(id, key) ; warmth(id) ; affBand(a, b) ; bondOf(id, kind) ; moodOf(p) ; beatOf(arcId)
knowsNews(p, newsId) ; repBand(dept) ; repShip(kind) ; knownFor() ; cue(kind) ; aboard(id, day)
inWeek1() ; leavingSoon(id) ; newHere(id) ; movedOff(id) ; memThing(key) ; CALM_TYPES
// state changes (section 20 only, mostly from bus notes)
memAdd(crewId, key, { w }) ; memTold(crewId, key)
socialInvite({ trad | kind, day, from, at, where }) -> appointment id | null
momentReady(p) -> momentId | null ; momentShow(momentId)       // plays on section 18's dialogue panel
SHIP.mem, SHIP.rep = { dept, ship }, SHIP.social.bonds, SHIP.social.affWeek, SHIP.social.moved   // all in save.social
// emits on the bus: tierUp, moment, bond, invite

// the planner's, which social uses
simNote(kind, data) ; onSim(kind, fn) ; flag(key) ; flagSet(key)   // section 13
lineFor(p, kind, ctx) -> { text, id, kind } | null                 // the dialogue engine
// baked from content/ by content_gen.py (shapes in Part 9):
VOICE[id] = { tpl, talk, cares, jokes, words, needs, openness, loves, likes, invites, joy, thread, keepsake, avoid, lines }
VOICE_TEMPLATES[tpl] ; LINES[kind] = [{ text, ...conditions, w }]
MOMENTS[id] = { who, thread, beat, tone, tier, metDays, gapDays, where, hint, lines, after } ; MOMENT_THEMES[theme] = [b1, b2, b3]

// asked of others
crewComeTo(p, placeId, onArrive)        // section 10 (sim engineer)
SHIP_TRADITIONS[i].invite = { host, odds, line }   // section 18
machineDept(m) -> dept                  // section 17 (or a table in 20)
ROSTER_RESERVE ; p.aboard = [fromDay, toDay] ; p.partner ; p.transferTo   // section 9 (crew designer)
item.gift = '<tag>'                     // section 15/16 carried items
```
