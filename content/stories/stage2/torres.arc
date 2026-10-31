@arc torres
who: torres-zeke
// Stage 2 (ST1, 2026-10-31): baked from here (content/stories/stage2/, read only while STORIES2_ON); the words are
// content/stories/waiting/torres.story's, unchanged; only the builders' notes became fields and if-lines.
// "Ready" (content/arcs/outlines.md, section 1). The Works writer, arc batch. The man who trains you isn't sure he's
// ready for more himself. Opens after week 1 (he's the confident one that week). needs: listen.
// Places: written so each scene works wherever calm finds him (the overlook is named only as somewhere he goes).
// Crew stories (SW1, 2026-10-24, from outlines.md "B. Zeke Torres"): beats 1-3 kept word for word. The user's change:
// his dad is well and retiring after forty years on the engines (no memory loss anywhere). Beat 4 rewritten, beat 5
// in part (Calder's lines kept), beat 6 is the crescendo at Knit and natter, beat 7 its quiet ending.
// A line starting "if <conditions> |" plays only when they hold.

== beat 1
tone: light
when: !week1:true
where: calm
duty: true
hint: Don't look. I mean it. Don't look.
mem: scarf
them: Don't look. No, you looked. Fine. It's a surprise. It's orange.   [laugh]
them: It's a scarf. Kovac taught me. Dahl watched once and had to go and sit down.
them: I started it on your first day. Every new hand should have something that's theirs.
? choice
* It's lovely. Honestly.   flavour:cheer mem:lovely
  them: Liar. A kind liar. Thank you. It's got eleven dropped stitches, I counted.
* You started it on my first day?   flavour:listen mem:firstday
  them: Monday. Before the briefing. I thought, right, this one's staying. So, a scarf.
  + them: Monday, before the briefing. You held the spanner upside down that morning. Then you didn't. So, a scarf.   [nod]
* I could learn too. We could be terrible together.   flavour:share mem:knitclub
  them: Oh, Kovac would love that. Two of us to despair of. Quiet evenings, tea corner. Bring patience.   [laugh]
them: Right, onward. Two more rows. Don't look.

== beat 2
tone: light
metDays: 10
where: calm
duty: true
hint: Board's got a new sheet up. Have you seen?
mem: list
them: Engine Specialist list's up. On the board, by the parts racks.
them: Not on it. Second time. Ha. Well. There it is.   [laugh]
them: Right, onward. Coil three won't fix herself.
? choice
* Their loss. You're the best on the coils.   flavour:cheer mem:theirloss
  them: You haven't met many engine officers. But thanks. Really.
* Are you all right?   flavour:listen mem:askedok
  them: Course. Course I am. It's a list.
  + them: Course. It's a list. It's... Yes. Mostly. Ask me again another day, maybe.   [sigh]
them: Anyway. Tea?

== beat 3
tone: heartfelt
when: beat:torres.2
where: calm
hint: Got a minute? Properly, I mean.
mem: restless
them: Can I ask you something? Was I any good? As your trainer, I mean. Honestly.
them: Calder called me restless once. Years ago. I think about it more than I should.
them: Restless. Does that mean you can't be trusted with a reactor? Maybe it does.
them: And then I think, teaching you. Was that a step back? Or was it the most useful thing I've done all year?
? choice
* You were a brilliant trainer. You never once talked down to me.   flavour:listen mem:goodtrainer
  them: Oh. Well. That's the bit I tried hardest at, actually.
  + them: That's the bit I tried hardest at. Nobody's ever said. Thank you, {me}. I'll keep that.   [nod]
* Ask Calder what she meant. She'll tell you exactly.   flavour:practical flag:torres.askCalder mem:askcalder
  them: She would, wouldn't she. Exactly. To the decimal place. Maybe I will.   [laugh]
* I get restless too. I don't think it's a fault.   flavour:share mem:restlesstoo
  them: No? Huh. Maybe it's just being awake. Some of us are louder about it.
them: Right. Enough of that. The coils will be wondering where I am.

== beat 4
tone: heartfelt
when: beat:torres.3
where: calm
hint: Sit with me a bit? I won't talk much. I might.
mem: retiring
them: My dad taught me coils have moods. Forty years an engine man. He'd put his hand on the casing and just know.
them: He's retiring. Next month. Last shift, then a do at the yard on Hesper Dock. Cake on a cable drum, knowing that lot.   [laugh]
them: I won't be there. Too far. That's fine. That's the job. He'd say so himself.
them: He'll ask, though. He always asks. "Specialist yet?" And I'll say no. Again.   [sigh]
them: I've never told him I'm not sure I'm good enough for a reactor. Forty years, and I don't think he was ever not sure.
them: He hums to engines, you know. Badly. Worse than me, which takes doing.
? choice
* Tell me about him. The engine man.   flavour:listen mem:engineman
  them: He talked a freighter's drive home once. Three systems, hand on the casing, humming the whole way.
  + them: Three systems, a freighter's drive, his hand on the casing, humming. Nobody else could. I'll tell it you properly one day.   [laugh]
* Tell him before he asks. Then it's your news, not his question.   flavour:practical mem:tellfirst
  them: Before he asks. Huh. Then the answer's mine, not his. I hadn't thought of it like that.
* I'm not sure I'm good enough most days. I still turn up.   flavour:share mem:notsure
  them: Most days. Yes. Maybe that's all forty years is. Turning up, and putting your hand on the casing.
them: Thanks for sitting. Here. Last biscuit. I was saving it. For this, apparently.   [nod]

== beat 5
tone: heartfelt
where: calm
hint: I've been to see Calder. Got a minute?
mem: letter
mail: 300 | The last line | Dad's letter is done. The last line: "I put my hand on the casing every morning, and she still tells me things. You taught me to listen." Thank you for the question. Zeke
them: I went to see Calder. About "restless". I asked her straight.
them: She said, "Restless isn't a fault. Unfinished is." Then she went back to her board.   [laugh]
them: So I'm finishing things. The scarf. The application. And a letter for Dad, for his last day at the engines.
them: Can I ask you? What would you want to read, on your last day at a job you loved?
? choice
* That it mattered. That someone noticed.   flavour:listen mem:noticed
  them: That someone noticed. All those coils nobody ever thanked him for. Yes. I can say that.
  + them: Forty years of coils nobody thanked him for. I noticed. I'll tell him I did. That's the letter, isn't it. Thank you.   [nod]
* What you learnt from him. In his words, not yours.   flavour:practical mem:hiswords
  them: His words. "Feel that? She's thinking." I've said it to every new hand. You too. He'd like knowing that.
* That the job's in good hands. I'd want to hear that.   flavour:share mem:goodhands
  them: Good hands. Mine, he'd think. That's the bit I'd have to believe first. I'm working on it.   [laugh]
them: Right, onward. I've a letter to write. Properly.

== beat 6
// CRESCENDO rides on: Knit and natter (Tuesday 20:00, the junior common room); day: 23 (the evening you're made Engine Specialist), else any later Tuesday; cast: torres-zeke, kovac-zainab, dahl-mira, you; quiet ending: beat 7
// Gate: close, or friend if beat 5 was told 5+ days before (the builders' day gate)
// As built (ST1, 2026-10-31): a steady player is made Engine Specialist as night 1 starts (Monday Day 22, 22:40) and gets the
// badge on Tuesday Day 23, the first Knit and natter after; your night 2 starts at 21:00, so the scene starts by 20:40
// (until:). The gate: friend, 5 days after his last heartfelt beat (beat 5).
tone: resolution
tier: friend
gapDays: 5
when: beat:torres.5 trad:knit-and-natter weekday:tue day:23-
crescendo: trad:knit-and-natter
quiet: 7
until: 20:40
cast: kovac-zainab dahl-mira
title: Knit and natter with Zeke
where: Junior common room
hint: Close your eyes. No. Open them. No, close them.
mem: finished
flag: torres.applied
keepsake: the scarf in Works orange, finished, far too long
learn: Zeke Torres put his name forward again and finished your scarf. His dad retired after forty years on the engines.
if day:23 myrank:specialist | torres-zeke: Engine Specialist. You. Today. I could knit you a second one. I won't. I might.   [laugh]
torres-zeke: Close your eyes. Hold out your arms. Further. Further than that.   [laugh]
torres-zeke: It's finished. Your scarf. It's far too long. You'll have to wind it round twice. Three times.
kovac-zainab: Two dropped stitches. I counted. Um. It's perfect anyway. It is. It's perfect.
dahl-mira: Wind it from the left. The lumps sit at the back that way. Nobody will know.   [nod]
torres-zeke: I put my name forward again. Calder signed it. She said "About time," which from her is a parade.
torres-zeke: And Dad's reply came. He wrote it on his last shift, sat by the engines. You can tell. It's short.
torres-zeke: "She's sulking. Give her a minute. You'll know her better than I did."   [sigh]
torres-zeke: Hang on. Again. "You'll know her better than I did."
kovac-zainab: Oh. That's. Um. That's a very good line. Sorry. It is.
dahl-mira: Read it again at breakfast. It'll still be true.
? choice
* Read it once more. Slowly.   flavour:listen mem:once
  them: "You'll know her better than I did." There. That's three. I'll stop. I won't stop.
  + them: "She's sulking. Give her a minute. You'll know her better than I did." Thank you, {me}. I wanted someone to ask.   [nod]
* It's perfect. I'm never taking it off.   flavour:cheer mem:wearing
  them: You'll take it off in the engine room. Health and safety. But otherwise, yes. Good.   [laugh]
* You were ready all along. I knew it on day one.   flavour:share mem:ready
  them: Day one, you didn't know where the lift was. But thank you, {me}. Properly.
torres-zeke: Right, onward. Wear it to the board on Monday. Calder will pretend not to see.

== beat 7
// QUIET ENDING for beat 6: plays only if beat 6 was missed (the scarf is left on your bunk; he tells you at breakfast)
tone: light
tier: friend
when: beat:torres.5
where: calm
hint: Been to your bunk yet? Go on. No, wait. I'll tell you first.
mem: onbunk
flag: torres.applied
keepsake: the scarf in Works orange, finished, far too long
learn: Zeke Torres put his name forward again and finished your scarf. His dad retired after forty years on the engines.
mail: 0 | On your bunk | Far too long. Wind it three times. Not twice. I'll check. Z
them: You missed knit and natter. That's all right. The scarf found you anyway. It's on your bunk.
them: It's far too long. I've left a note saying so, in case you try winding it twice.   [laugh]
them: Calder signed my application. Two words. "About time." I've been walking taller since. Ask Reyes.
them: And Dad's retired. He sent me a line from his last shift. "You'll know her better than I did."   [sigh]
? choice
* That's a lovely thing to be told.   flavour:listen mem:toldline
  them: It is, isn't it. I've read it more times than I'll admit. Eleven. I'll admit eleven.
  + them: It is. I've read it eleven times. I'm glad it was you I told first, {me}. Well. Second. Kovac guessed.   [laugh]
* I'll wear it to the board on Monday.   flavour:cheer mem:wearit
  them: Calder won't say a word. That's how you'll know she's noticed.
* Shall I help you write back to him?   flavour:practical mem:writeback
  them: Write back? Oh. Yes. Short, he likes short. You can cut the rambling. There'll be rambling.
them: Right, onward. Breakfast. I'll be last in again. Coil three wanted a word.
