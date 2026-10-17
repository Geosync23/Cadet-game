@arc torres
who: torres-zeke
// "Ready" (content/arcs/outlines.md, section 1). The Works writer, arc batch. The man who trains you isn't sure he's
// ready for more himself. Opens after week 1 (he's the confident one that week). needs: listen.
// Places: written so each scene works wherever calm finds him (the overlook is named only as somewhere he goes).

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
tone: serious
where: calm
hint: Sit with me a bit? I won't talk much. I might.
mem: dad
them: My dad taught me coils have moods. Forty years an engine man. He'd put his hand on the casing and just know.
them: I called home last night. He called me by my uncle's name. Third time this month.   [sigh]
them: He's still him. Mostly. He asked if the Wren's coils were behaving. That part he had.
them: Coil three's been quiet all week. I keep thinking she's tired. I know she isn't. It's me.
? choice
* I'm here. Tell me about him.   flavour:listen mem:listened
  them: He used to hum to the engines. Badly. Worse than me, if you can picture it.
  + them: He hums to engines. Badly. Worse than me, which takes doing. I'll tell you about the time he hummed a freighter home.   [laugh]
* Is there anything I can do? Even small.   flavour:practical mem:offered
  them: This is the small thing. You sitting there. It's doing more than you'd think.
* Someone I love got muddled like that. They still knew who loved them.   flavour:share mem:shared
  them: Yes. That's it, isn't it. The names go. Not the rest. I hope not the rest.
them: Thanks for sitting. Here. Last biscuit. I was saving it. For this, apparently.   [nod]

== beat 5
tone: heartfelt
where: calm
hint: I've been to see Calder. Got a minute?
mem: letter
mail: 300 | The last line | I finished the letter to Dad. The last line is: "The coils on the Wren have moods, like you said. I'm learning them." Thanks for helping me find it. Zeke
them: I went to see Calder. About "restless". I asked her straight.
them: She said, "Restless isn't a fault. Unfinished is." Then she went back to her board.   [laugh]
them: So I'm finishing things. The scarf. The application. And a letter to Dad, about the Wren's coils.
them: Can I ask you? If you'd forgotten nearly everything, what would you want to hear in a letter?
? choice
* Something you used to do together. So it feels like his.   flavour:listen mem:together
  them: The engines. Putting our hands on the casing. Yes. He'd know that one.
  + them: The engines. Our hands on the casing, him saying, "Feel that? She's thinking." Yes. He'd know that. Thank you.   [nod]
* That you're all right. That's what my family always wants.   flavour:share mem:allright
  them: That I'm all right. I am, you know. Mostly. More than I was.
* Keep it short. One good thing. He can read it twice.   flavour:practical mem:short
  them: One good thing, read twice. That's very you. I'll try. I talk too much on paper too.   [laugh]
them: Right, onward. I've a letter to write. Properly.

== beat 6
tone: resolution
where: calm
hint: Close your eyes. No. Open them. No, close them.
mem: finished
flag: torres.applied
keepsake: the scarf in Works orange, finished, far too long
learn: Zeke Torres was passed over twice, put his name forward again, and finished your scarf.
them: Close your eyes. Hold out your arms. Further. Further than that.   [laugh]
them: It's finished. Your scarf. It's far too long. You'll have to wind it round twice. Three times.
them: I put my name forward again. Calder signed it. She said "About time," which from her is a parade.
them: And Dad had a good day. He knew me. He asked about the coils. He said, "She's sulking. Give her a minute."   [sigh]
? choice
* It's perfect. I'm never taking it off.   flavour:cheer mem:wearing
  them: You'll take it off in the engine room. Health and safety. But otherwise, yes. Good.   [laugh]
* I'm so glad he had a good day.   flavour:listen mem:goodday
  them: Me too. It won't always be like that. But that one was. I wanted to tell someone.
  + them: Me too. They won't all be like that. That one was, though. And I wanted you to be the one I told.   [nod]
* You were ready all along. I knew it on day one.   flavour:share mem:ready
  them: Day one, you didn't know where the lift was. But thank you, {me}. Properly.
them: Right, onward. Wear it to the board on Monday. Calder will pretend not to see.
