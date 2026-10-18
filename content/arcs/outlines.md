# Arc outlines: the story crew and the struggle themes

**The head writer's**, to be agreed with social engineer B (who owns arc structure, gating and how beats unlock:
`plans/social-deep-plan.md`, Parts 1, 6, 9). Each outline is the **story**; social B's notes on shape go in the
"Agreed" line under each. Writers write the beats from these (into `content/arcs/<id>.arc` once social B's format is
in, wave 2-3); nobody writes a beat that isn't outlined here.

**Status:** AGREED with social B (2026-10-17, 03:15), all ten arcs as stories, with the shape notes below. Writers may
write beats once the dialogue engineer's `.arc` grammar is out.

## How every arc works (the shared shape)

- **Steps, not chapters.** Beats open by tier *and* time known (social's `STEP_GATES`: light at colleague, met 3+ days;
  heartfelt at friend, met 7+, 2+ days since their last moment; resolution at close friend, 3+ days after the last
  heartfelt). At most one serious moment a ship day reaches you.
- **Tone per beat:** `light` (a joy, a confession, a joke), `heartfelt` (the struggle, told), `serious` (a heavier
  heartfelt beat: grief, fear), `resolution` (how it turns out, at close friend). About two light beats for every
  serious one.
- **Where:** `calm` (they're off shift, somewhere you can sit: a lounge seat, the observatory, a common room, the
  garden, the mess after the rush, the engine overlook), `visit` (your bunk), `appt` (an appointment you made with them),
  or a named room.
- **Choices:** one or two per moment, up to three replies each in four flavours (listen, cheer, practical, share).
  Never a wrong answer; their card's `needs` gets the warmest reply. Every reply leaves a memory key; a practical reply
  may start a **favour that matters** (a personal job).
- **Already told:** Tomas, Pell and Rina have four beats in the game (section 20, `STORY_ARCS`, told as card lines).
  Social's plan turns beats 2-4 into moments. **Their stories stay exactly as told**; the outlines below keep them as
  beats 1-4 and add beats 5 onward.
- **Hooks an arc needs** are listed per arc so the engineers can say yes or no before anyone writes.
- **Nobody leaves** in an arc (story crew never transfer); **nobody dies on screen**; grief is for people off the ship,
  told gently.

Tones by beat, at a glance:

| Arc | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| torres | light | light | heartfelt | serious | heartfelt | resolution | | |
| calder | light | light | heartfelt | heartfelt | resolution | | | |
| tomas | (told) | (told) | (told) | (told) | light | heartfelt | resolution | |
| pell | (told) | (told) | (told) | (told) | light | heartfelt | light | resolution |
| rina | (told) | (told) | (told) | (told) | light | heartfelt | resolution | |
| brennan | light | light | heartfelt | heartfelt | resolution | | | |
| vance | light | light | heartfelt | heartfelt | resolution | | | |
| marrow | light | light | heartfelt | heartfelt | resolution | | | |
| holt | light | light | serious | heartfelt | resolution | | | |
| kovac | light | light | heartfelt | resolution | | | | |

---

## Social B's shape notes (agreed 2026-10-17; they apply to every arc)

- **Answers:** theme ids `notgood` and `startover` win (in social B's code since 0.39.1). Cards hold `thread: arc:<id>`
  (the code strips `arc:` and finds `content/arcs/<id>.arc`). Arc ids as above; `beat:torres.4` style conditions.
- **(a) Tomas, Pell, Rina:** beats 1-4 stay as told (1 a card line, 2-4 moments already in the game with placeholder
  replies, which we may rewrite through `content/arcs`); new beats are 5+. **New arcs start with beat 1 as a moment.**
- **(b) Gates default from the tone:** light = colleague, 3 days known; heartfelt or serious = friend, 7 days, 2 days
  since their last moment; resolution = close, 3 days after the last heartfelt. Write `tier` / `metDays` / `gapDays`
  only where a beat differs (Torres beat 2: `metDays 10`). Extra gates go on a `when:` line in the beat header, in the
  frozen condition vocabulary (`rep:known`, `rep:well`, `flag:torres.askCalder`, `beat:x.n`, `flag:`/`event:` for the
  diplomatic visit). One moment a day per person; one serious (heartfelt, serious or resolution) a day for you.
- **(c) Where:** `calm` (the default: off duty at a seat, or visiting you), `visit` (your bunk), `appt` (an appointment
  with them), or a room name, which only works if their own off-duty schedule takes them there (Marrow's music room on
  a Thursday evening: check their habits). **Beats at work places** (Calder's glass office, the Works board, the Works
  bay) need `duty: true` so they can open on shift: fine for light beats; heartfelt ones stay off duty (so Calder beat 3
  is "the Works bay after shift", off duty; Pell beat 7 at the board is light, `duty: true`).
- **Marrow:** close friend only (no Officer rank in Pillar 4); "or Officer" stays a note, not a condition.
- **(d) Favours from practical replies** (Pell, Brennan, Holt, Kovac): a reply's `favour:` naming the job; social B
  wires it to social A's favour API. The jobs themselves (the lift brakes, the garden crop) need the systems and galley
  engineers' yes through the lead.
- **(e)** Mail after a moment: `after: mail` on the beat. Keepsakes: the beat's `keepsake:` text. Both built.
- **(f)** Calling back intro memories (`mem:intro.arrival` and so on) is fine.
- **(g)** Holt beat 4's "carry the invitation" favour and the visit's flags are fine as conditions; the Envoy's lines are
  writer-command's.
- **Memory keys:** give each reply (or the beat) its word with `mem:`; social stores `moment.<arc>.<word>`. Without one,
  it mints `moment.<arc>.<beat>.<flavour>`.
- **Gift tags and invite kinds** are social A's lists (gifts A5, invitations A7); being confirmed with social A.

---

## 1. Zeke Torres (`arc:torres`): "Ready"

**The heart of it:** the man who trains you isn't sure he's ready for more himself. Passed over twice for Engine
Specialist, he wonders if he's too restless to be trusted with the reactor; mentoring you is either a step back or the
thing that makes him ready. Later, gently: his father, an engine man too, is losing his memory back home.

**Before the arc:** week 1 is his mentor role (onboarding's script and the `week1` lines): he's the confident one.
The arc is the other side of him, so it opens only after `week1.done`.

| Beat | Tier, gate | Where | Tone | What happens | Leaves |
| --- | --- | --- | --- | --- | --- |
| 1 "The scarf" | colleague | tea corner, Works bay, common room | light | He's knitting. Badly. Kovac taught him; Dahl despairs of him. It's for you ("Don't look. It's a surprise. It's orange."). He admits he started it on your first day because "every new hand should have something that's theirs". | `mem:moment.torres.scarf`; the scarf joke starts in his lines |
| 2 "The list" | colleague, 10+ days known | the Works board | light (with a sting) | The Engine Specialist list goes up. His name isn't on it, for the second time. He laughs it off a bit too fast ("Right, onward."). Light on the surface; the hint is in the silence after. One choice. | `mem:moment.torres.list` |
| 3 "Restless" | friend | the engine overlook, evening | heartfelt | He asks if he was any good as your trainer. Calder once called him "restless". He wonders if that means he can't be trusted with the reactor; if teaching you was a step back. | memory by reply; practical: "Ask Calder what she meant" sets `flag:torres.askCalder` |
| 4 "Dad" | friend, 2+ days after 3 | the engine overlook, or after his call at the booths | serious | His father taught him that coils have moods. Forty years an engine man. On the last call he called Zeke by his uncle's name. Third time this month. Told plainly; Torres stays himself (he talks about the coils to get through it). | `mem:moment.torres.dad` |
| 5 "Properly" | friend, 2+ days after 4 | the Works bay after shift | heartfelt | He's been to see Calder (whether or not you suggested it). She said: "Restless isn't a fault. Unfinished is." He's going to finish things: the scarf, the application, a letter to his dad about the Wren's coils. Asks you what you'd want to hear in a letter if you'd forgotten nearly everything else. | `mem:moment.torres.letter`; Mail from him later: the letter's last line |
| 6 "Finished" | close | your bunk (a visit) or the overlook | resolution | The scarf, finished, far too long (keepsake). He's put his name forward again, and Calder signed it. His dad had a good day: knew him, asked about the coils, said "she's sulking, give her a minute." Bittersweet, warm. | keepsake; `flag:torres.applied`; `mem:moment.torres.finished` |

**Calls back:** your arrival (`mem:intro.arrival`), the shadow shift (`mem:intro.shadowShift`): "You held the spanner
upside down. Then you didn't."  **Hooks:** `flag:` set from a meeting reply (beat 3), Mail after a moment (beat 5),
keepsake (beat 6). Nothing else new.  **Agreed** (social B, shape notes below).

## 2. Chief Ines Calder (`arc:calder`): "Well done"

**The heart of it:** the toolbox on her shelf belonged to her first chief, **Chief Rhoda Fenn** (new canon), who taught
her everything and never once said "well done". Fenn is retiring to **Marra Station**, a long way off, and has written
to her. Calder hasn't answered: Fenn was hard on her, and Calder has become hard in the same way, and she isn't sure that
was right. Under it: she's afraid of investing in juniors who leave (the last one she trained transferred off and never
wrote).

**Gate:** by tier **and your Works record** (reputation with Works, `rep:`): she only opens up to someone who's shown
her the work. Each beat also needs `rep:known` (beats 1-2) and `rep:well` (beats 3-5).

| Beat | Tier, gate | Where | Tone | What happens | Leaves |
| --- | --- | --- | --- | --- | --- |
| 1 "Swarf" | colleague, `rep:known` | Works Friday tea | light | Off duty, just barely. She started as a junior in a shipyard sweeping up swarf, two years of it. "Best two years. You learn where everything falls." The mug: "It's a mug." | `mem:moment.calder.swarf` |
| 2 "Don't open it" | colleague, `rep:known` | the glass office | light | She asks you to hold the toolbox while she moves the shelf. It's heavier than it looks. "Don't open it. It isn't mine." That's all she says. Dry; the hint is how carefully she puts it back. | `mem:moment.calder.toolbox` |
| 3 "Fenn" | friend, `rep:well` | the Works bay, late evening, nobody else there | heartfelt | A letter on her device, opened, not answered. "My first chief. Fenn. She's retiring. Wrote eleven days ago." Fenn never said well done. Calder learnt everything from her. She doesn't know what to write back. | memory by reply |
| 4 "Too hard" | friend, 2+ days after 3 | a progress talk (her office, an appointment) | heartfelt | The progress talk turns. She asks, unusually: "Am I too hard on you?" She tells you about the last junior she trained, who transferred to the Halcyon and never wrote. She's not sure the hardness was for them or for her. | memory by reply; honest replies count |
| 5 "Borrowed" | close, `rep:well` | your bench in the Works bay, a morning | resolution | The toolbox is on your bench with a note: "Borrowed. Return it when you're done. — I.C." Later: she answered Fenn. Fenn wrote back two words: "Well done." "Took her thirty years. I won't take that long." Then, to you, plainly: "Well done." | keepsake (the spare key on Works orange wire); `flag:calder.welldone` |

**Her first "well done"** is the payoff of the whole arc: **nobody writes "well done" in Calder's lines before beat 5.**
(She says "Good. Clean work." instead.)  **Hooks:** `rep:` conditions on beats (social A's reputation, built);
a beat at an appointment (the progress talk, `calderProgress`); the toolbox as a prop on your bench is optional (a
note in Mail does the same job if the deck architect can't spare it).  **Agreed** (social B, shape notes below).

## 3. Tomas Lind (`arc:tomas`): "Somewhere new"

**Already told (beats 1-4, as in the game):** misses home and the star map; his brother's birthday call; the call drops,
his brother thinks he hung up; his brother writes back and has taped a star map to his own ceiling.

**What's left:** he's still a little lost. Failed the Watch exam once before passing and hasn't told Holt. He's been
looking at the transfer list: a posting near the farm moon. He finds his place, and becomes the one who meets the next
new arrival.

| Beat | Tier, gate | Where | Tone | What happens | Leaves |
| --- | --- | --- | --- | --- | --- |
| 5 "The exam" | friend | Bunk 1, evening (a visit, or both of you there) | light | Thursday's bunk inspection is tomorrow and he's panicking about Holt. Then it comes out: he failed the Watch exam once. Passed the second time. Never told Holt. Comic-anxious; he makes you promise not to tell. | `mem:moment.tomas.exam` |
| 6 "The list" | friend, 2+ days after 5 | the junior common room window seat, late | heartfelt | He's been reading the transfer list. A posting on a station near home. "Maybe I'm not built for out here. Everyone else knows where everything is." He wants you to tell him what to do; you can't, but you can be there. | memory by reply; practical: "Come to observatory night with me" (an invitation) |
| 7 "Home, both of them" | close | the observatory, observatory night | resolution | He told Holt about the exam. Holt said: "I know. I read your file. You passed. That's the one I care about." He's taken the transfer list off his locker. He shows you where home is on the big window, then says this is home too. And he's asked to be the one who meets the next new cadet off the shuttle ("Nobody should have to get lost on their own. I did. It was awful."). | keepsake (the star map's corner); `flag:tomas.meets` (social's newcomer hook: he meets the next arrival) |

**Hooks:** the newcomer escort role on rotation day (social's Part 8b) reads `flag:tomas.meets`; Holt's line in beat 7
is Holt's (writer-command writes Holt's matching `callback`).  **Agreed** (social B, shape notes below).

## 4. Pell Okafor (`arc:pell`): "Eat, sleep, call"

**Already told (beats 1-4):** the music box from the screw tin; the rusted one from the swap meet; his music-box show in
the Deck 4 music room; who came.

**What's left:** the three unread messages from his mum, who wants him home to run the family repair shop (new canon:
a small mending shop for kettles, radios, coats, anything, with the scrapyard behind it where he found his engine
manual). He's scared of disappointing her either way. And Calder's certification practical, which he wants more than
anything and is scared of.

| Beat | Tier, gate | Where | Tone | What happens | Leaves |
| --- | --- | --- | --- | --- | --- |
| 5 "The practical" | colleague or friend | the machine shop, after shift | light | Calder's put his name down for the certification practical. He's thrilled and terrified. Asks you to time him stripping a pump ("Slower. No, faster. No, don't tell me."). | `mem:moment.pell.practical`; practical reply: a favour (help him practise: a personal job in the machine shop) |
| 6 "Three messages" | friend | the junior common room, late, or your bunk room | heartfelt | He opens his mum's messages with you there. Eat, sleep, call, as always, and a fourth: her hands are getting stiff; she wants him home to run the shop. He's scared of letting her down either way: staying or going. | memory by reply |
| 7 "Passed" | friend, 2+ days after 6 | the Works bay | light | The practical. He passes. Calder says "Good. Clean work." and he nearly cries at the board. Celebration at the tea corner; he feeds everyone. (If you helped him practise, he says so to everyone.) | `mem:moment.pell.passed`; `flag:pell.certified` |
| 8 "Call" | close | the call-home booths, then the bow lounge | resolution | He called his mum. Told her he's staying, and that he'll walk her through fixing the shop's old press by message, one step a week, like a proper apprentice. She said: eat, sleep, call. He laughs. Then the secret: he nearly left the Wren in his first month, and he's glad every day he didn't. | keepsake (the four-note music box) |

**Hooks:** a favour from a moment's practical reply (built: the favour API); `flag:pell.certified` read by his and
Calder's lines.  **Agreed** (social B, shape notes below).

## 5. Rina Deshi (`arc:rina`): "Sit the exam"

**Already told (beats 1-4):** gran taught her Tiles and cheated; gran in hospital (her sister, the doctor, told her);
two days without news; gran home and cheating again; gran's love to "the friend who listened".

**What's left:** she wants to be a ship's doctor and quietly thinks she'd be good at it. She hasn't sat the qualifying
exam. She keeps finding reasons (the infirmary's busy; next quarter; her sister keeps sending dates, which makes it
worse). Underneath: if she fails, she'll have proved her sister right, and after the hard year at home that brought her
to the Wren, she can't face being the one who didn't make it.

| Beat | Tier, gate | Where | Tone | What happens | Leaves |
| --- | --- | --- | --- | --- | --- |
| 5 "Quiz me" | colleague or friend | the junior common room (the Tiles table) | light | She's using her journals as a pillow again, and you catch her reading them instead. "Quiz me. And if you say 'easy' I'll beat you at Tiles for a month." You quiz her. She's brilliant. She bets you a game she can't name three bones. She names eleven. | `mem:moment.rina.quiz`; she may invite you to quiz her again (an invitation) |
| 6 "Next quarter" | friend | the infirmary after hours, or the garden | heartfelt | Her sister's sent another exam date. Rina's said "next quarter" four quarters running. It comes out sideways: if she fails, her sister was right, and she's not doing that again. She doesn't say "scared". She says "I'd rather not." | memory by reply; cheer fits her (her card) |
| 7 "Cheat if you have to" | close | the call-home booths, then wherever you are | resolution | She's booked it. Nandakumar will sit with her for it. Gran's message: "Cheat if you have to." Then, plainly, once: the hard year at home, the one where everything went wrong at once and she was the one holding it together, and how the Wren's routine helped more than she expected. Later Mail: she passed the first part. "Don't make a fuss. Fine. A small fuss." | keepsake (gran's cheating Tiles piece); `flag:rina.exam` |

**Hooks:** Mail after a moment (built); Nandakumar's matching line (writer-command).  **Agreed** (social B, shape notes below).

## 6. Chef Auda Brennan (`arc:brennan`): "Seventy-five covers"

**The heart of it:** she ran a restaurant on Port Halloran until a fire (nobody was hurt; she made sure). She came to
the Wren because a galley's order comforts her. Now an old friend, **Nell Arrowby** (new canon), offers her a restaurant
on Hesper Dock. And her mother's soup, which she's never got right in space, because the garden doesn't grow **blue
sage** (new canon).

| Beat | Tier, gate | Where | Tone | What happens | Leaves |
| --- | --- | --- | --- | --- | --- |
| 1 "The book" | colleague | the mess after the dinner rush | light | Her book of everyone's favourite dish. She asks yours. She writes it down and underlines it twice. "Fridays. Don't tell anyone, they'll all want one." | `mem:moment.brennan.book`; (later, now and then, your dish turns up on a Friday) |
| 2 "Blue sage" | colleague | the galley's pass | light | Her mother's soup. She's made it ninety times aboard and it's never right. It needs blue sage, and the garden doesn't grow it. Practical reply: ask Tove Cruz (a favour that matters). | `mem:moment.brennan.sage`; practical: `favour` (ask Cruz; the garden grows it over two weeks) |
| 3 "Port Halloran" | friend | the galley, late, the pans put away | heartfelt | A letter from Nell Arrowby on Hesper Dock: a restaurant, hers if she wants it. She tells you about her old place on Port Halloran, and the fire. "Nobody was hurt. I made sure of that. I counted them out the door. Twice." She came here for the order of it. | memory by reply |
| 4 "Tasting table" | friend, 2+ days after 3 | the tasting table (a tradition, if it's in; else the mess) | heartfelt | She's cooking the menu she'd serve on Hesper Dock, one dish a week. She wants your honest verdict on each. She's not sure if she's saying goodbye to it or hello. | memory by reply; she may invite you to the next tasting |
| 5 "Seventy-five covers" | close | the mess, a Friday | resolution | The blue sage grew. The soup is right. She serves it to the whole mess and doesn't say why. To you, after: she wrote back to Nell. No. "My kitchen's here. It's got seventy-five people in it, and one of them's you." | keepsake (the page from her book, with your dish) |

**Hooks:** a favour that the garden fulfils (galley/garden engineer: a one-off crop, or simply a timed favour);
the tasting-table tradition (trad-weekly designer) if it exists, else the mess.  **Agreed** (social B, shape notes below).

## 7. Commander Teo Vance (`arc:vance`): "Gull"

**The heart of it:** by the book because he once broke every rule in it. Two messages from home wait unopened: from his
father, whom he hasn't spoken to since the academy nearly expelled him. And, lightly: he writes the worst poems in the
ship's newsletter under the name "Gull".

| Beat | Tier, gate | Where | Tone | What happens | Leaves |
| --- | --- | --- | --- | --- | --- |
| 1 "Gull" | colleague | the bow lounge, the newsletter on the table | light | Someone's reading the newsletter aloud: this week's poem by Gull, about the treadmill. It's terrible. Vance listens with great dignity and corrects the scansion under his breath. | `mem:moment.vance.gull` (you suspect) |
| 2 "Thirty seconds" | colleague | the gym | light | He's six seconds off Lindqvist's time on the treadmill board. He asks you to time him. Formally. He beats it by one second and says "Adequate" in exactly Holt's voice. | `mem:moment.vance.board` |
| 3 "Two messages" | friend | the observation room after his watch, or the gym | heartfelt | The two messages from home. From his father. They haven't spoken since the academy: Vance broke the rules, badly, and was nearly thrown out, and his father was ashamed of him. He hasn't opened them. "One is probably 'I'm still ashamed'. I can't guess the other." | memory by reply |
| 4 "Opened" | friend, 2+ days after 3 | wherever you're sitting together | heartfelt | He opens the first with you there. His father followed his whole career. Has every posting written down. Wants to see him at the next port. Vance reads it twice and recites a regulation he doesn't need. | `mem:moment.vance.opened` |
| 5 "The rule" | close | the observation room, late | resolution | The rule he broke: as a cadet he took a training shuttle out without leave to bring back another cadet stranded on a test flight. Nearly expelled; the stranded cadet is a captain now. He's replied to his father. Next week's newsletter has a poem by Gull about a father. It's still terrible, and it's the best thing in it. He admits it's his. "Tell no one. That's an order. Of sorts." | keepsake (the rowing pin he's "lending" you) |

**Hooks:** the newsletter is flavour only (no new system); Mail after a moment.  **Agreed** (social B, shape notes below).

## 8. Captain Odile Marrow (`arc:marrow`): "The ready room"

**The heart of it:** what it is to be responsible for everyone and friends with no one. She asks a junior's view because
nobody else tells her the truth. Her daughter at the Concord academy doesn't write often enough. She thinks about
retiring and can't imagine anyone else in the ready room.

**Gate:** her arc opens late: **close friend, or Officer rank** (social's rule). Beats 1-2 at colleague are light,
and rare (she's the Captain; you see her on Thursdays, at observatory night, on her evening walk).

| Beat | Tier, gate | Where | Tone | What happens | Leaves |
| --- | --- | --- | --- | --- | --- |
| 1 "Your answer" | colleague, `mem:readyroom` | the observation room, her evening walk | light | She remembers the answer you gave her in the ready room (social A's keys `readyroom.lights`, `.filters`, `.month`). Asks if you still think so. Takes notes, apparently. | `mem:moment.marrow.answer` |
| 2 "The Admiral" | colleague | the music room, Thursday, before she plays | light | The crew's theories about the Admiral. She collects them. Yours? She won't confirm or deny anything. "He'd be pleased you asked." | `mem:moment.marrow.admiral` |
| 3 "Thursday" | friend (or Officer) | the music room, late Thursday | heartfelt | You stay while she plays. She tells you about the portrait gallery: every captain before her, and the loneliness that comes with the chair. Everyone is kind to her; nobody is her friend. "That's the job. I chose it." | memory by reply |
| 4 "Letters" | friend, 2+ days after 3 | the observatory, observatory night | heartfelt | Her daughter at the academy writes twice a quarter. Marrow writes every week. She asks you, as someone young and far from home, what you want from a letter from home. | memory by reply; a share reply fits her |
| 5 "Ask me in a year" | close (or Officer) | the ready room (an appointment) | resolution | She's been offered a post at the Concord academy, near her daughter. She's thought about it every night for a month. She asks you the truth: should she go? Whatever you say, she stays, for now: "Ask me again in a year." Her daughter has written: "Mum says there's a cadet who tells her the truth. Is that true?" | keepsake (a page of her Thursday piano music); `flag:marrow.stays` |

**Hooks:** reading the reply you chose in `readyRoomFirst` (a `mem:` from a meeting's choice: social A's `choice`
note); Officer rank as a gate (progression: may not exist in Pillar 4, then close friend only).  **Agreed** (social B, shape notes below).

## 9. Chief Bram Holt (`arc:holt`): "One bad day"

**The heart of it:** he distrusts the Veyli because of one bad day on a border patrol, years ago, and knows it isn't
fair. He asked for the cabin next to the Envoy's to keep an eye out, and has started to like the Envoy. A slow,
grudging thaw, alongside the diplomatic visit. His distrust is voiced and argued with, **never a slur**.

**New canon (the bad day):** his patrol partner, **Hanne Rook**, was badly hurt in a
rescue that went wrong when a Veyli vessel nearby went silent and didn't answer for six hours. Rook recovered, slowly,
and left the service; they still write. Years later Holt learnt the silence was a Veyli mourning rite: the ship
couldn't answer. "Knowing doesn't help as much as you'd think."

| Beat | Tier, gate | Where | Tone | What happens | Leaves |
| --- | --- | --- | --- | --- | --- |
| 1 "Don't look" | colleague | a deck, before breakfast (his long walk) | light | He tests you: "Nearest suit locker. Don't look." You get it right (or not). He walks you the long way, and Mensah's terrible joke from last night comes out of him in a voice he doesn't use often. | `mem:moment.holt.walk` |
| 2 "Keeping an eye out" | colleague | Deck 2, the senior corridor | light | You catch him re-tying the Envoy's door cord, which came loose. "Keeping an eye out." He's tied it correctly, which means he learnt how. | `mem:moment.holt.cord` |
| 3 "One bad day" | friend | the Watch office, the late shift | serious | The border patrol. Rook. Six hours of silence. He tells it plainly, short sentences. He knows now it was a rite. He knows it isn't fair to hold it against the Envoy. He holds it anyway, some days. | memory by reply; listen and practical both fit |
| 4 "Tea" | friend, 2+ days after 3; best after the diplomatic visit | the Envoy's door, Deck 2 | heartfelt | The Envoy has invited Holt to tea, through you (a favour: carry the invitation). He goes, after standing at the door for some time. Afterward: "They kneel. My knees aren't built for it. They gave me a cushion." | `favour` (carry the invitation); `mem:moment.holt.tea` |
| 5 "Don't tell Mensah" | close | the Watch office, or his walk | resolution | He's written to Rook and told her about the Envoy. Rook wrote back: "About time." He and the Envoy have tea every tenth day now. He can tie three Veyli knots. He likes the Envoy. "Don't tell Mensah. He'll be unbearable." | keepsake (the border-patrol whistle); `flag:holt.tea` |

**Hooks:** the diplomatic visit's flags (events engineer: has it happened, did it go smoothly) as an optional
condition (`flag:` or `event:`); a favour that is "carry this to someone" (social A's favour API); the Envoy's lines
for the tea are writer-command's (Saruth).  **Agreed** (social B, shape notes below).

## 10. Zainab Kovac (`arc:kovac`): "Four, please"

**The heart of it:** small, funny and kind, to show anyone aboard can matter. She can strip a scrubber in ten minutes
flat, she knits perfect scarves, and she's secretly afraid of the lift. She rides the lift like everyone, both hands on
the rail ("Lovely lift"), and keeps sharing it with Tove Cruz and Davi Keane, who hold the rail too. (Was: the ladder;
changed in 0.48.51 because the game moves everyone by lift.)

**Before the arc:** she gives you your first favour on Thursday of week 1 (onboarding's), which is a small personal
job on Deck 5 or 4. She's grateful you didn't make a fuss.

| Beat | Tier, gate | Where | Tone | What happens | Leaves |
| --- | --- | --- | --- | --- | --- |
| 1 "Lovely lift" | colleague | calm | light | She's wobbly from the lift, both hands on the rail the whole way. Cruz was in it, eyes shut: "Lovely lift." Then Keane got in at Four: "Lovely lift." Nobody said anything else. | `mem:moment.kovac.ladder` |
| 2 "The lift club" | colleague | the tea corner, knitting | light | She tells you, so quietly you nearly miss it: she's afraid of the lift. Then she guesses about Cruz and Keane, and is delighted, and then horrified that she's delighted. "We're a club. Oh no. We're a club." | `mem:moment.kovac.club` |
| 3 "A whole night" | friend | the garden, or the junior common room | heartfelt | Why: when she was small, a lift on Marra Station stuck between floors with her in it, alone, a whole night. Nobody came till morning; she counted the bolts in the ceiling (there were 112). She's fine. She just doesn't like the counting. Practical reply: "We could service the lift together. You'd see how it works." | memory by reply; practical: sets `flag:kovac.liftjob` (a personal job: the lift's brakes, with Calder's OK) |
| 4 "Four, please" | close | the lift | resolution | You service the lift's brakes together (or, if you didn't, she does it with Calder). She knows every bolt now. She steps in and says "Four, please" (your first words on the Wren, from your arrival). Then she tells Cruz and Keane, and the lift club rides together, and for the first time nobody holds the rail. Very brave, all three. | keepsake (a perfect scarf in Works orange and garden green) |

**Hooks:** a personal job on the lift (systems engineer: a favour job on the lift's brakes; a light one), the
`kovac.liftjob` flag; Cruz and Keane get matching lines (writer-commons for Cruz, writer-works for Keane).
**Agreed** (social B, shape notes below).

---

## The struggle themes (for the ~65 generated crew)

Social's theme library (Part 1): each a three-beat thread (hint at colleague, opens up at friend, resolution at close
friend), written as **templates with fill-ins** from the roster (`{home}`, `{family}`, `{hobby}`, `{since}`) and the
speaker's voice tokens, so one theme serves a dozen people and still sounds like each. The writers write them in wave 2-3
(themes go to writer-commons first, then shared out). Ids are the canonical ones (social plan Part 1).

**Rules for every theme:** each beat must work for any department and either shift; it must not name a habit the
person may not have (use conditions); it must read well through any template's voice tokens; beat 1 is a hint, never a
confession; beat 3 is hopeful (even "an old loss" ends in a small ritual with you, not in sorrow).

| Theme id | Beat 1 (colleague): the hint | Beat 2 (friend): it opens | Beat 3 (close): it turns | Tone notes |
| --- | --- | --- | --- | --- |
| `homesick` | quiet at the windows; mentions a smell, a food, the rain on {home} | misses a place, a person, a food; the call home that's hard to make | a call home goes well, or the galley makes the dish (Brennan's book) | gentle, sensory; never "I want to go home" outright until beat 2 |
| `exams` | studying at meals; a joke about forgetting everything | afraid to fail the certification; what failing would mean to them | passes, or decides to retake; either way, you were there | Rina's and Tomas's arcs are the models; keep it lighter than theirs |
| `family` | checks Mail a lot | someone at home is ill or struggling ({family}) | news comes: good, or bittersweet with comfort; never a death on screen | the heaviest theme: friend tier, short lines, a warm close |
| `stuck` | "same job, {since}" | wants to try another department | asks their Chief; a trial shift in another department | funny-sad; their Chief is kind about it |
| `notgood` | over-checks their work | a mistake they still think about | someone senior tells them it was fine (or you do) | never about an actual failure that hurt anyone |
| `lonely` | eats alone | doesn't know how to join in | you bring them to a tradition; they find a group | the reward is visible: they wave you over later |
| `loss` | quiet on a certain day | who they lost, and when (a grandparent, a friend, years ago) | the quiet watch (day 300), or a small ritual with you | gentle grief; long ago; never recent, never on screen |
| `talent` | humming, sketching, whittling | shows you, shy | a little show (Pell's format), or a gift they made | light all the way through |
| `burnout` | always the last to leave | can't say no | takes a day off; you cover a small job | warm; Oduya (the Counsellor) may appear |
| `leaving` | looks at the transfer list | unsure whether to stay | decides: stays, mostly (a real transfer needs the rotation) | can end in a real goodbye if the rotation picks them (social's Part 8b) |
| `rivalry` | sharp about someone aboard ({rival}) | why it started (something small that grew) | the two make up | never cruel; the rival gets a matching line |
| `startover` | evasive about the past | why they really came aboard | they say it out loud, and are glad they did | quiet, hopeful |

**Note for social B:** the game's code (0.39.0, `VOICE_THEMES`) uses `notEnough` and `starting` where the plan's
canonical ids are `notgood` and `startover`. The story cards here use `thread: arc:<id>`; the code's fallback uses the
crew id. One of us should change; I've written to you.
