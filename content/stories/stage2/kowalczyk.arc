@arc kowalczyk
who: kowalczyk
// Stage 2 (ST1, 2026-10-31): baked from here (content/stories/stage2/, read only while STORIES2_ON); the words are
// content/stories/waiting/kowalczyk.story's, unchanged; only the builders' notes became fields and if-lines.
// "The beacon" (content/arcs/outlines.md, Crew stories J). SW3, 2026-10-24. Low and unhurried, a night voice; wry;
// few words; she pauses before she answers (written as short lines and full stops, never stage directions). Gives a
// junior a job and leaves them to it. needs: listen. New canon (the outline): her father has kept the beacon at the
// edge of Marra Station for thirty years; it goes dark for good at ten to six one morning, a buoy instead. His pattern:
// three long, one short. Never the command she was passed over for; never loneliness spelled out (the lonely theme).
// No pictures (the game has none): someone on Marra saw the lights and wrote to her father.
// Depends on your night shifts (Pillar 5: Days 19-20, 21:00-06:00, as the game holds them; settled with the event swap, 0.93.2, lead 37): beats 2-3 on the first night
// (Day 19, before midnight), the crescendo at the dawn after the second (Day 21, 05:50; it was Days 22-24, with Zeke's on Day 23). No day numbers in lines.
// Numbering: beat 4 is the crescendo, beat 5 the afterglow (after 4 or 6), beat 6 the quiet ending for beat 4.

== beat 1
tone: light
tier: acquaintance
where: Bow lounge
when: time:morning
hint: Ah. You're up early. Or I'm up late. Sit, if you like.
mem: endings
them: Ah. Don't mind me. Last page first. Always.
them: Risk management. I like to know who's still standing before I get fond of anyone.
them: This one's a ship's cook who solves a theft. Everybody lives. The cook gets a medal and a nap.
them: There. Now you needn't read it. You're welcome.   [nod]
? choice
* Doesn't knowing the end spoil it?   flavour:listen mem:spoil
  them: No. It leaves me free for the middle.
  + them: No. Once I know the end, I can take the middle slowly. That's where the good bits hide. Nobody reads middles properly.   [nod]
* Tell me the end of every book aboard. Saves time.   flavour:cheer mem:everybook
  them: Tempting. Book circle would never speak to me again.   [laugh]
* I read the last page first too.   flavour:share mem:lastpage
  them: Do you. Huh. Nice. We're rare. And not popular.   [laugh]
them: Right. Bed, for me. Breakfast, for you. Go on, then.

== beat 2
// DAY: 19
// your first night shift, 21:30-22:30; acquaintance, met 3+ days (the builders' gate for the night shift)
tone: light
tier: acquaintance
metDays: 3
where: Bridge lobby
duty: true
when: beat:kowalczyk.1 time:night day:22-23
hint: Night shift. Come and see the real ship. Quietly.
mem: night
them: Evening, or near enough. Your first night shift. Welcome to the real ship.
them: The day shift think they run her. They're visitors. Very polite ones. They leave at five.
them: Listen. That's the air on Deck 2. That tick's the hull cooling. That's the night helm's kettle.
them: A few of us on the bridge, a doctor, the Watch, the engines. That's the whole night. You learn the footsteps.
them: My father would like it up here. He keeps a beacon. Marra Station, at the edge. Thirty years.
them: Never mind. Your job: the log, on the hour, every hour. Then leave the quiet alone. It's earned it.
? choice
* A beacon? What's it like?   flavour:listen mem:beacon
  them: Bright. Patient. Like him. Another time.
  + them: Bright. Patient. Turns all night and never complains. Like him. I'll tell you more. Not yet.   [nod]
* I can pick out the kettle already.   flavour:cheer mem:kettle
  them: Good ear. You'll be useful by three.   [laugh]
* At home I could tell who was up by the stairs creaking.   flavour:share mem:stairs
  them: Then you know. Nights are for people who listen.
them: On the hour. I'll be at the chart table, pretending not to read.

== beat 3
// DAY: 19
// the same night, an hour after beat 2, 23:00-23:59 (before midnight: that day's one heavy moment); tier and gap set for the night
tone: heartfelt
tier: acquaintance
gapDays: 0
where: Observation room
duty: true
when: beat:kowalczyk.2 time:night day:22-23
hint: Still awake? Good. Sit a minute. It's late enough to say a thing.
mem: dark
them: The beacon. My father's. They switch it off the morning after next. For good. At ten to six.
them: A buoy instead. Smaller. Never needs anyone. Sensible little thing.
them: He won't say he minds. He wrote, "About time. The lamp's older than me." Then three lines about the weather.   [sigh]
them: I can't be there. Long way to Marra. I'll be on the bridge that morning, keeping a log.
them: It's why I leave film night before the lighthouse bit. Everyone thinks it's the plot. It's the light.
? choice
* Tell me about him.   flavour:listen mem:father
  them: Quiet man. Big hands. Polished that lamp every Sunday, whether it needed it or not.
  + them: Quiet man. Big hands. Polished the lamp every Sunday whether it needed it or not. Thank you. Nobody asks about him.   [nod]
* Could the Wren answer it?   flavour:practical flag:kowalczyk.signal mem:answer
  them: Answer it. Huh. The running lights. Three long, one short. That was his. Every ship out there knew it.
* I missed a goodbye like that once. It sits strangely.   flavour:share mem:missedbye
  them: It does. Like a step that isn't there. Thanks for saying.
them: Right. Long night yet. The log won't keep itself. Go on, then.

== beat 4
// DAY: 21
// CRESCENDO rides on: your second night shift, the bridge (Deck 1), 05:50; day: 21; cast: kowalczyk, takahashi-wen (night comms), mensah (night Watch, on his rounds; the builders confirm who's on watch); quiet ending: beat 6
// As built (ST1, 2026-10-31): your nights are Days 22-24 in the game (P5_NIGHTS), so this is the dawn after the second,
// Day 24 (as first written); a fixed time (at:), Tuesday night being her rest night: she comes up for it (section 20c's
// storyPlanBeats), and so does Mensah off his rounds.
tone: resolution
tier: acquaintance
gapDays: 0
where: Bridge
duty: true
when: beat:kowalczyk.3 day:24
crescendo: at:05:35-06:00
quiet: 6
cast: takahashi-wen mensah
title: Dawn on the bridge
hint: Twenty to six. Come up to the bridge. Just yourself.
mem: signal
flag: kowalczyk.lit
learn: Anja Kowalczyk's father kept a beacon on Marra Station. The morning it went dark, the Wren's running lights sent his pattern.
mail: 5770 | From Marra | A letter from my father. Someone on Marra saw a ship's running lights go three long, one short at ten to six, and wrote to tell him. He says the buoy is very sensible. He says thank you. So do I. A.K.
them: Rest night. Came up anyway. Twenty to six. Helm, hold her steady. No flourishes this morning.
takahashi-wen: Comms are quiet. Nothing but static out there. Clean static.
them: The running lights. This key here. Three long, one short. His pattern.
if flag:kowalczyk.signal | them: You asked if the Wren could answer it. She can. So can you.
them: Your hand, not mine. Mine aren't steady enough this morning. Don't put that in the log.
them: Ten to six. Now.   [nod]
? choice
* (Key it slowly, like a lamp turning.)   flavour:listen mem:slow
  them: That's his. That's exactly it.
  + them: That's his. Slow, like the lamp going round. You had it exactly. I didn't have to say a word.   [nod]
* (Key it, then once more, for luck.)   flavour:cheer mem:luck
  them: Twice. Fine. He'd have said once for the ships and once for the dark.
* (Key it, and say good morning to him for her.)   flavour:share mem:goodmorning
  them: Good morning, Dad. There. Somebody said it.
mensah: Every deck's quiet. Thought I'd stand here a minute. If that's all right.
takahashi-wen: Nobody out there for a long way. Clean signal, though. Huh. Clean.
them: Somebody always sees a lamp. That's what he says.
them: Thank you.   [nod]
them: Right. Log it: a test of the running lights. Satisfactory. Very satisfactory.
them: And somebody find me a novel with a dull ending. I've had enough feeling for one shift.   [laugh]

== beat 5
// DAY: from 21
// afterglow: after the night shift, any early morning as she comes off (06:00-07:00); plays after beat 4 or beat 6
tone: light
tier: acquaintance
where: calm
follows: 4|6
when: beat:kowalczyk.4 time:morning day:24-
hint: Ah. You. Here, before I think better of it. It's only a book.
mem: novel
keepsake: a paper novel with her notes in the margins
learn: Anja Kowalczyk gave you the novel she was reading, with her pencil notes in the margins.
them: Ah. You. Something for you. Don't make a thing of it.
them: The novel from the bow lounge, that first morning. My notes are in the margins. Pencil. Mostly rude.   [laugh]
them: I've read the end. It's a good one. Read it in order, if you're that sort.
? choice
* I'll read every note in the margins.   flavour:listen mem:margins
  them: Do. They're the better story.
  + them: Do. The notes are the real book. Nobody's read them. Now somebody will.   [nod]
* Should I read the last page first?   flavour:cheer mem:lastfirst
  them: Up to you. I'd recommend it. Strongly.   [laugh]
* I'll lend you one of mine.   flavour:share mem:swap
  them: Fine. A swap. Bring me one with a lamp in it.
them: Right. Bed, for me. Quiet watch, whenever yours is.

== beat 6
// DAY: 21
// QUIET ENDING for beat 4: plays only if beat 4 was missed (not on the bridge at 05:50); at 06:00 by the lift as she comes off. If you had no night shift at all, the builders play only beat 5 (with one line about the beacon)
tone: light
tier: acquaintance
gapDays: 0
where: calm
when: beat:kowalczyk.3 time:morning !flag:kowalczyk.lit day:24
hint: Morning. Walk me to the lift? Small news.
mem: quietsignal
mail: 5770 | From Marra | My father wrote. Someone on Marra saw a ship's lights go three long, one short at ten to six, and wrote to tell him. He's keeping the letter by the old lamp. A.K.
them: Six o'clock. Not even my night. I went up regardless. Three long, one short, at ten to six.
them: The helm held her steady. Mensah came up off his rounds and just stood there. Nobody asked him to.
them: Out into nothing. Nobody to see it. Didn't matter.
? choice
* How do you feel?   flavour:listen mem:howfeel
  them: Quiet. The good sort.
  + them: Quiet. The good sort, for once. Thank you for asking. And for sitting up with me the other night.   [nod]
* Did you log it?   flavour:cheer mem:logged
  them: A test of the running lights. Satisfactory. The Commander will never know.   [laugh]
* I wish I'd been up there.   flavour:share mem:wish
  them: You were, in a way. You kept me company for the long part.
them: Right. Bed, for me. Sleep well, if it's that time. It's that time for me.
