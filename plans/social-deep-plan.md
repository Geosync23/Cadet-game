# Pillar 4: the deep social system (plan)

*Draft 1, 2026-10-16, by the social system designer (session_01SMfS1WKqzQ93X6zyZ7NFpJ, branch `claude/social-design`). Written with the Pillar 4 planner (session_01KLFXcNJztCSVLXunD8Jt7R), who owns the overall Pillar 4 plan (arrival, first week, dialogue at scale, traditions, staffing). Nothing here is built until the user approves it. It builds on what section 20 already does (see "Where we start").*

## The pitch (one page)

Pillar 3 gave the Wren's crew a relationship meter, a chat card, gossip, favours and three little story arcs. Pillar 4 turns that into people you actually **get to know**.

- **You get to know someone in steps.** First their name and job, then their habits and hobbies, then what they think about work and home, and once you're close, the thing that's weighing on them. Each step is something you *learn* (it goes into the Crew app as "What you know about Rina"), not just a bar going up.
- **Moments.** When you're close enough, and the time and place are right (a quiet evening in the lounge, the observatory, a late table in the mess), someone opens up: a short scene in the dialogue panel where you hear their struggle, and you answer how you'd answer a friend. **Mostly light; serious and heartfelt as you get close.** Every one of the 75 crew has at least one such thread; the story crew have whole arcs.
- **They remember.** Crew keep a handful of memories of you, which fade unless they were big: the lamp you fixed, the quiz you came to, the evening you listened. They bring them up ("Thanks again for the lamp, it's been perfect"), and big ones are kept for good.
- **They have lives with each other.** Friendships form and fade, a few pairs fall out and make up, mentors take juniors under their wing, and crew talk about each other. You can bring two people together.
- **Small kindnesses.** Give a small gift (a tin of tea from the store, herbs from the garden, a little thing you made in the machine shop). Friends drop by your bunk in the evening, leave a note if you're out, and invite you to things: dinner together, the observatory, their tradition, their show.
- **Your name gets around.** Each department remembers what you've done for them (the galley knows who fixes their ovens). Strangers there start warmer, ask you for favours, and invite you to their things.
- **Lines that fit.** Everything anyone says is picked from banks of lines by who they are (a voice card for each of the 75), how well they know you, their mood, what they remember and what's happening on the ship. Writers fill the banks as plain data; they never touch the game's code.
- **No romance** with the player, ever (the user's rule). **No fail state:** you can't lose a friend for good, and there's never a wrong answer.
- **Cheap:** all of it runs on paper hour by hour for 75 people in well under a millisecond, saved compactly, and checked by an extended `social_check.py` and a new `words_check.py` for the writers' data.

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
3. **No romance with the player** (the user's rule). No flirting lines, no dates, no "more than friends" moments. Writers' lines are checked for it (`words_check` flags a short list of words). Crew-to-crew: see Open questions.
4. **Never a wrong answer.** Every reply in a moment is kind in its own way; the one that fits the person best gives a little more and a warmer reply. Nothing you say makes anyone dislike you.
5. **Nothing locked away by luck.** Every crew member's steps can be reached by ordinary play (chatting, eating together, favours, work); moments wait for you rather than expire (except time-bound ones, which come back in a new form).
6. **Built from the simulation.** Lines and moments use what's really happening (their real schedule, the machine you really fixed, the tradition that really happened, who really came).
7. **The same ship gives the same social life** (the project's determinism rule): every choice is seeded per person, day and hour (`schedU`), never `Math.random`; running a day hour by hour or in one jump comes out the same.
8. **Writers never touch engine code.** All words are data in their own block of the file, checked by a script.
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

**Your knowledge of them is the visible progress.** The Crew app's page for a person shows "What you know" in sections (Work, Home, Hobby, Past, Their story) with the count of what's left ("You know 5 of 11 things about Rina"). Each detail comes from the roster's `about`, the person's voice card, or a moment. This makes getting to know people something to collect, the way Stardew's hearts are, without turning it into a number race.

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

- `key`: what happened, from a fixed list of memory kinds (with an argument): `fav:lamp`, `fixed:<machineId>`, `came:<traditionId>`, `show:pell-show`, `gift:tea`, `moment:<threadId>:<beat>:<reply>`, `intro:escort`, `intro:dinner`, `missed:<apptId>`, `bday`, `visit`, `introduced:<otherId>`, `helped:storm`, `grubby` (you turned up unwashed), `meeting:<id>:<choice>`.
- `day`: the ship day it happened.
- `w`: its weight, 0 to 100, set by its kind.

Memories happen through `memAdd(id, key, { w })`, called by section 20 itself (favours, gifts, moments, traditions joined, appointments) and by other sections through that one function (systems: you fixed a machine they use; events: a meeting reply; the planner's onboarding: intro scenes).

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

1. **Lines call them back.** The line picker (Part 6) can match a memory: `mem: 'fav:lamp'` gives "The lamp's still perfect, by the way." Each callback is said once per memory (it's marked told), so it never nags.
2. **Warmth.** The sum of a person's memory weights is their **warmth** toward you: how present you are in their life right now. It's separate from tier: a close friend you haven't seen in weeks has low warmth ("There you are! Thought you'd left the ship."). Warmth raises the odds of seeking you out, visits and invitations, and picks between "warm" and "missed you" greetings.
3. **Friends of friends hear.** A big memory becomes small news among their friends ("Rina says you sat with her all evening. That was kind."), which gives those friends a small memory too (`heard:<key>`, small) and a warmer first meeting.

---

## Part 3: Crew-to-crew relationships that change over time

### What's kept

The pair affinity (`SHIP.aff`, Int8 per pair, hourly drift from time together) stays: it's cheap and works. Changes:

1. **More visible life.** Today no pair starts at or below -30 and rivalries take about a month. Raise the clash penalty in `affStart` (-12 to -24, the handover's suggestion) and the clash drift, so a 2-week check shows a handful of rivalries (target: 2 to 6 rival pairs and 15 to 40 friend pairs after 14 days). Most of the ship still gets friendlier.
2. **Labelled bonds** for the pairs that matter, kept in a small map `SHIP.social.bonds[pairKey] = { kind, since }` (about 50 to 150 entries, not 2,701):
   - `friends` (affinity 60+), `best` (85+, the closest pairs; each person has at most one best friend);
   - `rivals` (-40 or below; may become a feud, as built);
   - `mentor` (same department, rank gap of one or more, affinity 40+, the senior one's voice card `mentors: true` or traits patient/kind/steady): mentors pass news and favours to their mentee and talk about them;
   - `drifting` (former friends whose affinity has dropped 20 since they became friends, usually because shifts or bunks moved them apart): a bittersweet line, and a chance for you to bring them back together.
3. **Pair stories.** A bond changing can start a small two-person story you witness: an argument in a corridor (two bubbles, as now), a reconciliation dinner (they sit together; `affinityPlan` gets a day hint), a mentor and mentee at the machine shop. Each is a `CONVOS` script (Part 6) with pair conditions.
4. **You as the connector.** On the chat card's Ask about… list, a new topic **"Do you know …?"** offers up to three people you know well who they don't (affinity under 20, you colleague+ with both). Picking one: if they're compatible (no clash), their affinity +15, both get a memory (`introduced:<other>`), and it's news. If they clash, a gentle "We've met. We're… different." and nothing changes. Mending a feud already works (chat to both).
5. **They talk about each other.** Lines can name another crew member by bond: `{friend}`, `{best}`, `{rival}`, `{mentor}`, `{mentee}` fill-ins ("Pell and I are doing the quiz together again." / "If you see Ade, don't mention the coffee machine.").
6. **Seating and plans already use `affinityPlan`** (pure, from starting affinity). It must stay pure for determinism. The deep system adds a **weekly** plan affinity: `affinityPlan(a, b, d)` returns the affinity as it stood at the start of that ship week (a snapshot saved once a week, 2.7 KB), so seating follows friendships that changed without plans ever reading live numbers mid-week. (Needs the sim engineer's OK: plans already built for this week don't change.)

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

**Visiting them:** crew quarters stay private (the privacy rule). A friend can **invite** you to their bunk room or cabin (an appointment of kind `visit`, using the sim engineer's `doorOpenFor`): an evening of Tiles with Rina, Tomas's star map. Without an invitation, their door stays locked as now.

### Invitations

Three kinds, all delivered the same way:

1. **To a ship tradition** (quiz, running club, film night, a birthday cake...). The traditions table (section 18) gets an optional `invite: { host, odds, line }`. Each morning at 07:00 the social system picks at most two invitations for the day: a colleague-or-better who's going to a tradition that day (their plan says so) asks you, the host first. The invitation is their tap line ("Quiz tonight. We need someone who knows the engines. You in?"), and if you haven't met them by 15:00, a short Mail from them.
2. **Personal**, from friends: dinner together, the observatory after dark, a walk round the promenade, help with their hobby, their bunk room for a game. Picked from their habits and voice card (`invites: ['observatory', 'dinner', 'tiles']`).
3. **Their moment's event**: a show (Pell's format, `eventOneOff`), a call home they want company for, a small ritual (the quiet watch).

**Saying yes** makes an appointment (the device's Appointments, `kind: 'invite'`), which they keep in their plan (section 14, as appointments already are). Keeping it: +3 (as appointments today) and a medium memory (`came:<id>`); a tradition joined with the person who invited you: +2 more. **Saying no** is fine ("Next time, then."), no cost. **Missing it**: the existing remark, and a sour memory.

**From officers:** summons and the Captain's table stay the events engineer's (C10); social only supplies who's warm to you.

---

## Part 6: How lines are picked (the line engine)

### One picker for everything anyone says

Every line (the chat card's tap line, the reply after Chat, Ask about answers, chatter bubbles, visit lines, invitations, callbacks) goes through one function:

`say(p, kind, ctx) -> { text, id, kind } | null`

1. Gather the candidate lines for `kind`: the person's own (`VOICE[id].lines[kind]`), their voice template's (`VOICE_TEMPLATES[tpl].lines[kind]`), then the shared bank (`LINES[kind]`).
2. Keep those whose conditions all hold (below).
3. Score each: +3 for each condition it names (the most specific line wins), +2 for the person's own, +1 for the template's; minus a big penalty if said recently (last 6 lines of this person, last 12 ship-wide, kept in memory, not saved).
4. Among the top scores, pick by `schedU(p.seed, hour, k)`, so a second tap in the same hour says the same and the next hour moves on (as now).
5. Fill the placeholders and apply the voice (below).

**Conditions a line can carry** (all optional; writers use the ones they need):

| Field | Meaning | Example |
| --- | --- | --- |
| `tier` | `[min, max]` relationship tier with you | `[2, 4]` |
| `traits` | any of these traits | `['shy', 'quiet']` |
| `dept`, `rank` | their department, rank | `'galley'` |
| `mood` | `'low'`, `'ok'`, `'high'` (crewMood bands) | `'low'` |
| `act` | what they're doing (whereIs act) | `'meal'` |
| `place` | room name match | `'Observatory'` |
| `time` | `'morning'`, `'day'`, `'evening'`, `'night'` | |
| `weekday`, `offDay` | the day | |
| `mem` | a memory of you they hold (key prefix) | `'fav:'` |
| `warmth` | `'cold'`, `'warm'` (missed you vs saw you yesterday) | |
| `bond` | they have a bond of this kind | `'rival'` |
| `cue` | a recent ship happening (below) | `'fixed:oven'`, `'storm:after'` |
| `event` | a ship-wide event and phase | `'ionStorm:onset'` |
| `trad` | a tradition today / last night | `'quiz:today'` |
| `rep` | your standing with their department | `'known'` |
| `week1` | first-week only | `true` |
| `w` | a weight, default 1 | |

**Placeholders:** `{me}` your first name, `{name}` theirs, `{room}`, `{deck}`, `{other}` (whoever the line is about), `{friend}`, `{best}`, `{rival}`, `{mentor}`, `{mentee}`, `{boss}` (their Chief), `{thing}` (a memory's object: "the lamp"), `{trad}`, `{time}`. A line whose placeholder can't be filled is skipped.

**Voice:** a voice card's `words` replace tokens in any line: `{hi}`, `{bye}`, `{yes}`, `{thanks}`, `{wow}`, `{sigh}`, `{nick}` (what they call you, by tier). So one shared line ("{hi}, {nick}. Busy day?") sounds like Holt ("Cadet. Busy day?") or like Pell ("Oi oi, spanner. Busy day?"). This is how 75 voices come cheaply from shared banks.

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

### Ship cues: reacting to what really happened

Other sections tell social about things worth talking about with one call, `socialCue(key, { who, deck, dept, until })`: `fixed:<machine kind>` (systems: a repair finished; `who: 'you'` when it was you), `late:dinner` (galley), `harvest` (galley/garden), `storm:onset`, `storm:after` (events), `trad:<id>:done` with who came (events), `guest:arrived`, `promoted:you` (progression). A cue lasts a day or two; lines with `cue:` conditions pick it up ("The oven's working again. Someone's a hero." and, if it was you and they know it, "That was you on the oven? Thank you!"). Cues are also gossip seeds (news), which fixes "gossip is thin on quiet days".

### Overheard conversations

`CONVOS`: two- to four-line exchanges between two crew, with pair conditions (`pair: { bond, sameDept, aff: [min, max], traits }`) and the usual line conditions. When two eligible crew are settled near each other within chatter range (same room, both awake, not working with a machine), now and then they play one as alternating bubbles (two at most on screen, the existing voice budget). News can ride on one (the second speaker learns it, on screen as on paper). This is the planner's "overheard two-person conversations as you pass"; the planner's writers fill `CONVOS`, the engine is section 20's.

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

## Part 7: The first week, from the social side (with the planner)

The planner owns the arrival and the first week (scripts, tutorials, the "Settling in" list). What social provides, through four functions:

- `socialIntro(id, role)`: `'escort'` (starts at acquaintance, 12 points, a core memory, and becomes your **mentor**: a mentor bond with you, extra week-1 lines, checks on you each evening of week 1), `'boss'` (Calder at dinner: acquaintance, a core memory), `'bunkmate'` (Tomas; Pell and Rina next door: met, 5 points), `'met'` (anyone else introduced on the tour: met, 2 points).
- `memAdd(id, key, opts)`: the intro's memories, called back later ("Remember your first day? You held the spanner upside down.").
- `socialFlag(key)` / `socialFlagged(key)`: saved flags. Social features stay quiet in week 1 until the planner's script opens them: chat cards always work; favours from day 2; friends waving from day 3; invitations from day 5 (the first-weekend tradition invite is the escort's, sent by the planner's script with `socialInvite({ trad, day, from })`); visits and moments after week 1 (except the escort's scripted visit).
- `say(p, kind, ctx)` with `week1: true` lines, so the intro's in-passing lines come from the same banks.

**The escort.** A Works crew member one notch above you (the user): you're a junior, so a Works officer, or a senior junior like Pell (two years ahead). Suggestion: a named Works officer, written as story crew with a full voice card and arc, who's patient, a bit nervous about mentoring and very funny about machines. Who it is: decided with the planner and the crew designer (Open questions).

---

## Part 8: Reputation by department

Each department keeps a standing with you: `SHIP.rep[dept]`, 0 to 100, starting at 10 (Works at 20: they know you're coming). Nine departments: command, helm, comms, works, watch, survey, infirmary, galley, store.

**What raises it:**

| What | How much |
| --- | --- |
| A machine fixed that the department uses (the machine's room's owner: the galley's ovens, the infirmary's air, the bridge's relays) | +3 (+5 if it was failing) |
| A favour for one of them | +2 |
| Being at their tradition (Works tea, Survey's observatory night) | +1, once a week |
| A meeting reply that helps them | +1 to +3 (the script says) |
| Friends: each close friend in the department lifts its floor by 5 | |

**What lowers it** (gently, never below 0 or below the floor): a job you took on one of their machines and left unfinished past `YOU_KEEP` (the systems engineer's limit) -2. That's how "your work matters" reaches the people: neglect gets talked about.

**What it does** (bands named in words, never a number on screen):

| Band | Name in Record | Effect |
| --- | --- | --- |
| 0-19 | "New face" | nothing special |
| 20-39 | "They know your name" | strangers there start at 4 points; reputation lines (`rep: 'known'`) |
| 40-69 | "Well thought of" | strangers start at 8 (nearly acquaintance); favours from them 50% more often; their tradition invites you |
| 70-100 | "One of theirs" | the department's Chief mentions you to Calder (a Record note toward promotion); their crew defend you in gossip; a department "thank you" (Brennan's biscuits for the galley; a round at the bar for Watch) |

The Record app shows the nine standings as words. Reputation feeds the progression hooks (Pillar 3 Part 4): Calder's judgement of you can read `SHIP.rep.works` and the others.

**What crew say about you** (your "known for"): the system counts what you do (jobs, favours, traditions joined, chats, late nights) and gives you up to three tags with the most behind them (`reliable`, `chatty`, `night owl`, `quiz regular`, `gym rat`, `always at the garden`, `the one who fixes ovens`). Lines with `you: 'reliable'` conditions pick them up ("Ask {me}, they always turn up."). Cheap: a handful of counters, saved.

---

## Part 9: The data writers fill (shapes)

All words live in a new **section 20b. SOCIAL WORDS**, pure data, after section 20 in the file. It's split into blocks with markers so several writers can work in parallel and the lead merges block by block:

```
// ---- BEGIN WORDS: voices (story crew) ----     ... // ---- END WORDS: voices (story crew) ----
// ---- BEGIN WORDS: voices (works) ----  ... (one block per department)
// ---- BEGIN WORDS: lines (greet) ----   ... (one block per line kind)
// ---- BEGIN WORDS: moments (themes) ---- ...
// ---- BEGIN WORDS: moments (story crew) ----
// ---- BEGIN WORDS: convos ----
```

Writers never edit anything outside their block; `words_check.py` checks every block (below).

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
LINES.callback = [ { text: 'The lamp\'s still perfect, by the way.', mem: 'fav:lamp' }, { text: 'Still can\'t believe you came to the quiz. You were robbed on the reactor question.', mem: 'came:quiz' }, … ];
LINES.cue = [ { text: 'Did you hear? Someone fixed the oven. Breakfast on time for once.', cue: 'fixed:oven' },
              { text: 'That was you on the oven? {thanks}!', cue: 'fixed:oven', cueWho: 'you', dept: 'galley' }, … ];
LINES.invite = [ { text: '{trad} tonight. You in?', trad: 'today' }, … ];
LINES.visit = [ … ];  LINES.note = [ … ];  LINES.gift = { loved: [ … ], liked: [ … ], polite: [ … ] };
LINES.about = [ … ];   // what they say about a bonded crewmate: { text, bond: 'best' }
```

Line kinds (the head writer's checklist, with a target count each so the planner can size the writing): `greet` (by tier × warmth × time), `bye`, `chat` (after Chat), `near` (by place and act), `feel`, `life`, `joy`, `callback` (per memory kind), `cue` (per cue), `invite`, `accept`, `decline`, `visit`, `note`, `gift`, `about` (crewmates), `rep` (your standing), `knownFor`, `week1`, `smalltalk` (chatter by act), `rumour` (news openers), `hint` (a moment is ready). The current hard-coded lists (`CHAT_GREET`, `CHAT_NEAR`, `CHAT_LIFE`, `CHAT_DEPT`, `CHATTER_IDLE`) move into these banks unchanged at the first build, so nothing said today is lost.

### Moments, themes, convos

The shapes in Part 6 (`MOMENTS`, `MOMENT_THEMES`, `CONVOS`). A theme beat names the roster fields it needs (`needs: ['home']`) and is skipped for anyone without them.

### Writers' rules (in the head writer's brief)

- Plain text in the JS strings; escape apostrophes (`\'`) or use the template's double quotes (the check catches mistakes).
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
- `rep`: nine numbers; `knownFor`: a handful of counters; `flags`: the week-1 and other flags;
- `bonds`: the labelled pairs (about 3 KB at most);
- `affWeek`: the weekly snapshot for planning (2.7 KB, base64 like `aff`);
- per relationship (the array in `save.social.rel`), new slots: `giftWeek`, `moment` (beats told per thread), `momentDay`, `visitDay`, `inviteDay`.

Target: the social part of the save stays under **30 KB** (today's limit in `social_check` is 20 KB; raise it with the lead's OK).

### Testing

**`social_check.py`, extended** (the social engineer's checker; same harness):

1. Determinism: 14 days hour by hour twice, and as one jump, identical (built) now including memories, bonds, rep, invitations and the weekly snapshot.
2. Save round trip, size under 30 KB (built, extended).
3. Sensible numbers after 14 days: friends 15-40 pairs, rivals 2-6, at least one `drifting` and one `mentor` bond; memories per person (median and max), how many faded; reputation per department for a stand-in player who fixes galley machines (galley "They know your name" or better, others lower).
4. A stand-in player who chats with Tomas daily, eats with him, gives a loved gift and keeps an appointment: friend by day 14, his first heartfelt moment ready by day 14 and not before day 7, never two serious moments in one day.
5. Invitations: about 0.5 to 2 a day once week 1 is done; none during week 1 except the scripted one; each one's appointment fits the person's real plan.
6. Visits: a stand-in friend visits within 10 evenings of you sitting in your bunk room; no visit after 22:00; no visitor stuck (their agent gets back to its plan).
7. Phone budget: the hourly pass and the daily pass timed (hourly under 1 ms, daily under 5 ms on the test machine).

**`words_check.py`, new** (runs in a few seconds; the writers run it before handing in): loads the build, then for the words data checks every key is known, every line's placeholders and voice tokens are real, lengths, duplicates, every crew member has a voice card and a thread, every theme beat has fallbacks, every story arc's beats exist with their tiers, choices have 1 to 3 replies with flavours, no banned words (the romance list), no habit named that the person lacks, and prints counts per kind against the head writer's targets. It also renders 20 random chat cards per tier as text so the head writer can read a sample.

Other checks: `cadet_test` stays pixel-identical on decks until the keepsake shelf (Bunk 1 only); `day_check` must show nobody stuck with visits on; `events_check` with tradition invitations on.

---

## Part 11: Interfaces with the other workstreams

| With | They give social | Social gives them |
| --- | --- | --- |
| **Pillar 4 planner** (onboarding, first week) | the intro script calls `socialIntro`, `memAdd`, `socialFlag`, `socialInvite`; week-1 lines in `LINES.week1` | the four functions, the escort's voice card shape, what each week-1 day opens |
| **Planner's dialogue workstream** (head writer, writers) | the words data: voice cards, line banks, convos, moment scripts | the shapes (Part 9), the targets per kind, `words_check.py` |
| **Events / traditions designers** (section 18) | `invite: { host, odds, line }` on traditions; `socialCue('trad:<id>:done', { who })` after each; meeting choices may carry `mem` | who's warm to you (`relTier`, warmth) for invitations and the Captain's table; `say()` for tradition tap lines if they want voices |
| **Device engineer** (section 19) | the Crew app page draws "What you know" sections and counts; the Record app draws reputation bands and "known for"; Appointments takes `kind: 'invite'` and `'visit'`; the dialogue panel plays moments | `crewContacts()` gains `knowSections`, `knowLeft`, `warmth`; `repBands()`; `momentShow(id)` (wraps `dialogueShow`) |
| **Sim engineer** (sections 10, 14) | `crewComeTo(p, placeId, onArrive)` for visits and friends walking over; appointments of kind `visit` with `doorOpenFor`; `affinityPlan` reading the weekly snapshot | the weekly snapshot, pure |
| **Systems engineer** (section 17) | `socialCue('fixed:<kind>', { who, deck })` when a repair finishes; the machine's department (`machineDept(m)`, or a table social keeps); unfinished-job events for reputation | favours that matter (from moments' practical replies) on the existing favour API |
| **Galley / garden** (section 16) | gift-tagged items (garden produce on harvest days); cues for late meals and harvests | nothing new |
| **Player engineer** (section 15) | carried items with a `gift` tag; the store's gift list; the bunk tap for notes | `Give` on the chat card |
| **Crew designer** (section 9, the generator) | each person's `tpl`, `loves`, `likes`, `joy`, `thread`, `needs`, `openness`, `keepsake`, `home`/`family` fields for themes; more `about` details (45 today: aim for 6 or more per person) | the field list |
| **Deck architect** | one keepsake shelf place by Bunk 1 berth 4; "calm" tags on places (which seats count as somewhere to sit and talk) | the list of calm place types |
| **Performance engineer** (8/8b) | the `sigh`, `laugh`, `listen` talk poses for moments and visits; the keepsake instanced mesh | nothing new |

`schedU` keys: section 20 uses 600 to 643; the deep system takes **644 to 699**.

---

## Part 12: Build steps

Builds continue the social range **0.36.x** from **0.36.20** in section 20 (and the new 20b), unless the planner and the lead give Pillar 4 a new range. Each step is small exact-string edits, a build number bump, a DEV_NOTES row, the full test set, a push and a report, as CLAUDE.md asks. Steps marked *(inert)* change nothing you can see, so the writers can start on the data at once.

| # | Build | What | Sections touched | Depends on |
| --- | --- | --- | --- | --- |
| S1 | 0.36.20 | **The line engine and the words section** *(inert)*: section 20b with the empty blocks; `say(p, kind, ctx)`; the conditions, placeholders and voice tokens; today's hard-coded lists moved into `LINES` unchanged; `chatLine` and chatter call `say` (same lines out); `words_check.py` | 20, new 20b | — |
| S2 | 0.36.21 | **Voice cards** from templates for all 74 (generator fields, or social's own fallback table until the crew designer's run); voice tokens on; story crew cards as stubs for the writers | 20b, 9 (generator fields, crew designer) | S1 |
| S3 | 0.36.22 | **Memories with decay**: `SHIP.mem`, `memAdd`, daily fading, warmth, callbacks in the card order; existing events (favours, appointments, chat while grubby, traditions joined, meeting replies) leave memories; save | 20 | S1 |
| S4 | 0.36.23 | **First week hooks**: `socialIntro`, `socialFlag`/`socialFlagged`, `socialInvite`, the gating of favours, waving, invitations, visits and moments; week-1 lines | 20 | S3; agreed with the planner |
| S5 | 0.36.24 | **Steps and "What you know"**: knowledge sections and counts, `crewContacts` fields for the Crew app; time-known gates; openness | 20 (19 draws) | S2 |
| S6 | 0.36.25 | **Moments**: `MOMENTS`, `MOMENT_THEMES`, readiness, the "Sit with them" button, `momentShow` on the dialogue panel, reply flavours, after-effects; Tomas, Pell and Rina's arcs moved into moments; one serious moment a day | 20, 18 (`dialogueShow` accepts a moment script; one line) | S3, S5 |
| S7 | 0.36.26 | **Ship cues and reactions**: `socialCue`, cue lines, cue gossip; the systems, galley and events calls (one line each in their sections, by their owners) | 20 (+ one-line hooks in 16, 17, 18) | S1 |
| S8 | 0.36.27 | **Crew-to-crew**: clash tuning, bonds, mentors, drifting, `{friend}`-style fill-ins, "Do you know…?" introductions, the weekly snapshot for `affinityPlan` | 20 (14 reads the snapshot, sim engineer) | S1 |
| S9 | 0.36.28 | **Overheard conversations** (`CONVOS` as paired bubbles) | 20 (8b's bubbles) | S1, S8 |
| S10 | 0.36.29 | **Gifts**: gift tags, Give on the card, loves/likes, crew gifts, keepsakes; the shelf | 20, 15 (carried item tag), 16 (garden items), deck 4 shelf (architect), 8b (instanced mesh) | S2, S3 |
| S11 | 0.36.30 | **Invitations**: tradition invites, personal invites, `kind: 'invite'` appointments, Mail fallback | 20, 18 (`invite` fields), 19 (appointment kind) | S3, S4 |
| S12 | 0.36.31 | **Bunk visits and notes**: the prompt, `crewComeTo`, visit lines, notes on the bunk, invitations to their quarters | 20, 10 and 14 (sim engineer), 15 (bunk tap) | S6, S11 |
| S13 | 0.36.32 | **Reputation by department and "known for"**: `SHIP.rep`, sources, bands, warm starts, Record lines | 20, 17 (unfinished-job hook), 19 (Record draws) | S3, S7 |
| S14 | 0.36.33 | **The story crew arcs** as the writers deliver them (Calder, Brennan, Holt, Vance, Sato, Marrow, the escort), and the theme library filled; tuning pass with `social_check` numbers | 20b | S6 |

The writers' work runs alongside from S1 (the shapes are fixed at S1): story crew voice cards first, then line banks by kind, then moment themes, then convos, then the story arcs. Each delivery passes `words_check` before the lead merges it.

**Suggested staffing (for the planner to fold into the Pillar 4 staffing):** one **social engineer** for S1 to S8 (section 20 owner; the standby social engineer if their memory allows, else a fresh one with the handover note), a **second social engineer** from S9 (visits, gifts and invitations touch more sections), the **crew designer** for the generator fields at S2, and this designer on call for questions and the tuning pass.

**Order with the rest of Pillar 4 (to agree with the planner):** S1 to S4 first, in parallel with the planner's arrival build, because the intro needs `socialIntro` and the writers need the shapes. Moments (S6) before the first-week check-in if possible, since the user asked for them explicitly.

---

## Risks

- **Too many words to write.** 75 voices and thousands of lines is a lot. *Answer:* templates and voice tokens make shared lines sound personal; generated crew start complete from the generator; writers improve the people the player meets most first; `words_check` counts against targets so we know what's thin.
- **Repetition.** The same line twice in a minute kills the illusion. *Answer:* the recently-said penalty per person and ship-wide; callbacks said once; more variants for the kinds that fire most (greet, near, smalltalk).
- **Serious tone creeping in.** *Answer:* one serious moment a day at most, serious only from friend tier, two light moments for each serious one in each thread, and the head writer's tone pass.
- **Visits feel intrusive.** *Answer:* only friends, only evenings, only when you're there and awake, at most one a day, easy to ignore, never during quiet hours.
- **The player games gifts or favours.** *Answer:* weekly gift limit, daily favour limit (built), time gates on moments.
- **Determinism breaks** (memories or visits reading live state into plans). *Answer:* plans only read the weekly snapshot; live visits never change the paper plan; checks run twice and compare.
- **File size on phones.** *Answer:* words kept compact (no repeated keys where a short form works), measured each build; if it grows past the lead's budget, move rarely-used banks (convos for decks you're not on) into a compressed string unpacked on first use.

## Open questions for the user

1. **The escort:** a named Works officer written as story crew (our suggestion), or Pell (a junior two years ahead, already your neighbour)? The user said "one notch above you in rank".
2. **Crew-to-crew romance:** none anywhere (simplest and safest), or a few established couples who are simply together in the background (no storylines, never involving you)?
3. **How serious can it get?** Struggles like an ill grandparent and homesickness are in. Is grief (someone they lost) in, handled gently?
4. **Visits to your bunk:** OK as designed (friends only, evenings, easy to ignore)?
5. **Gifts from the machine shop** (making small trinkets) once Works lets you, or only bought and picked gifts?
6. **Reputation dipping** when you leave a department's job unfinished: OK, or only ever up?
7. **"What you know" counts** in the Crew app ("5 of 11 things"): nice to collect, or too gamey?

## Appendix: the new shared formats, in one place

```js
// 20. SOCIAL (deep, Pillar 4)
say(p, kind, ctx) -> { text, id, kind } | null                 // every line anyone says
memAdd(crewId, key, { w }) ; memOf(crewId) -> [[key, day, w, told]] ; warmth(crewId) -> 0..
socialIntro(crewId, 'escort' | 'boss' | 'bunkmate' | 'met')
socialFlag(key) ; socialFlagged(key) -> bool
socialInvite({ trad | kind, day, from, at, where }) -> appointment id | null
socialCue(key, { who, deck, dept, until })
momentReady(p) -> momentId | null ; momentShow(momentId)       // plays on section 18's dialogue panel
repBands() -> { dept: { v, band, name } } ; knownFor() -> [tag]
SHIP.mem, SHIP.rep, SHIP.social.bonds, SHIP.social.flags, SHIP.social.affWeek   // all in save.social

// 20b. SOCIAL WORDS (writers; data only)
VOICE[id] = { tpl, talk, cares, jokes, words, needs, openness, loves, likes, invites, joy, thread, keepsake, avoid, lines }
VOICE_TEMPLATES[tpl] = { words, lines }
LINES[kind] = [{ text, ...conditions, w }]
MOMENTS[id] = { who, thread, beat, tone, tier, metDays, gapDays, where, hint, lines, after }
MOMENT_THEMES[theme] = [beat1, beat2, beat3]
CONVOS = [{ id, pair, ...conditions, lines: [{ who: 'a' | 'b', text }] }]

// asked of others
crewComeTo(p, placeId, onArrive)        // section 10 (sim engineer)
SHIP_TRADITIONS[i].invite = { host, odds, line }   // section 18
machineDept(m) -> dept                  // section 17 (or a table in 20)
item.gift = '<tag>'                     // section 15/16 carried items
```
