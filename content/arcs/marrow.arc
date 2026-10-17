@arc marrow
who: marrow
// Writer (command), from outlines.md section 8, "The ready room". Close friend for the heartfelt and resolution beats
// (social B: no Officer rank in Pillar 4). Beat 1 no longer needs mem:readyroom (social B, 0.48.13: met the Captain
// before the ready room meant the arc never began); it's "when we first met", which covers the ready room too. Her card's needs: share, so the share replies get the warmer answer.

== beat 1
tone: light
hint: Walk with me a minute? I've a question. You know I always have one.
mem: answer
learn: The Captain wrote down the answer you gave to her one question when you first met, and still thinks about it.
them: I asked you one question when we first met. You gave me an answer. I wrote it down. I write them all down.   [gesture]
them: I've read yours a few times since. Do you still think so?
? choice
* I do. More than before.   flavour:practical mem:stillthink
  them: Good. Then I'll keep pushing for it. Quietly. That's how it's done up top.   [nod]
* I've changed my mind, a bit.   flavour:share mem:changed
  them: Good. People who never change their minds worry me.
  + them: Good. Tell me what changed it. I mean that. That's the part I never get to hear.   [listen]
* Did you really write it down?   flavour:cheer mem:wroteitdown
  them: In a little book. You're on page forty. Calder is on page one, every page.   [laugh]
them: Thank you. Nobody else answers me straight. It's the rank. Back to it.

== beat 2
tone: light
when: weekday:thu
hint: You'll want to hear this. Or I will. Sit a moment?
mem: admiral
learn: The crew have theories about the Admiral. The Captain collects them, and confirms nothing.
them: Pell thinks the Admiral is a plant. Rina thinks he's a very old officer who never retired.   [laugh]
them: Brennan thinks he's a cake. I don't know why. I collect them, you see. The theories.
them: What's yours?
? choice
* He's a ship's cat. A very quiet one.   flavour:cheer mem:cat
  them: There are no cats aboard. Officially. I'll write it down. He'd be pleased you asked.   [laugh]
* I think he's whatever we need him to be.   flavour:share mem:whatever
  them: That's the best one yet. And I'm still not saying.
  + them: That's the best one yet. You'd make a good captain, saying that. I'm still not saying.   [nod]
* I'd rather not know.   flavour:listen mem:notknow
  them: Wise. Most mysteries are better left in the ready room.   [nod]
them: Thursday. I should go and play. Mind the step on your way out. Habit.

== beat 3
tone: heartfelt
tier: close
when: weekday:thu time:evening|night
hint: I've played my last piece tonight. Stay a bit, if you like.
mem: thursday
learn: The Captain says everyone aboard is kind to her, and nobody is her friend. "That's the job. I chose it."
them: Varga, Moro, Brenner. The portraits. I know every one of their names. Mine's at the end.   [sigh]
them: Every one of them sat where I sit, and had no one to tell. That's the chair.
them: Everyone is kind to me. Nobody is my friend. That's the job. I chose it.
? choice
* I'm here. Go on, if you want to.   flavour:listen mem:listened
  them: There isn't much more. That's what's odd. It's a small thing. It's every day.
* I eat alone some days too. Even with people round me.   flavour:share mem:shared
  them: Then you know. Thank you for saying it.
  + them: Then you know. I didn't think anyone aboard would. Thank you. That's a real thing to give someone.   [listen]
* Then come to the quiz. Nobody's the Captain at quiz night.   flavour:cheer mem:quiz
  them: Calder would make me captain of the team in a minute. But perhaps.   [laugh]
them: There. That's my Thursday, said out loud. Thank you for staying.

== beat 4
tone: heartfelt
tier: close
when: trad:observatory-night
hint: You're young and far from home. May I ask you something about that?
mem: letters
learn: The Captain writes to her daughter at the Concord academy every week. Her daughter writes twice a quarter.
them: My daughter is at the Concord academy. She writes twice a quarter. I write every week.   [sigh]
them: You're young and a long way from home. Tell me. What do you want from a letter from home?
? choice
* Just ordinary news. What's for dinner. Who said what.   flavour:share mem:ordinary
  them: Ordinary. I've been writing her speeches. Oh dear.
  + them: Ordinary. I've been writing her speeches, like a captain. I'll write her about the stew. Thank you.   [laugh]
* To know they're not worried about me.   flavour:listen mem:notworried
  them: Then I'll stop asking if she's eating. Perhaps every other week.   [laugh]
* Not to have to write back straight away.   flavour:practical mem:noreply
  them: Hm. Permission not to answer. That's a kind thing to give. I'll give it.   [nod]
them: Look at that one. Bright. It's further away than she is. That helps, somehow.

== beat 5
tone: resolution
tier: close
where: appt
hint: Come up to the ready room tomorrow. Not a summons. A favour.
mem: ayear
flag: marrow.stays
keepsake: a page of piano music, the piece she plays last on Thursdays
learn: The Captain was offered a post at the Concord academy, near her daughter. She stays, for now. "Ask me again in a year."
mail: 120 | A letter | My daughter wrote today. She says: "Mum says there's a cadet who tells her the truth. Is that true?" I said yes. Thank you. O. Marrow
them: Mind the step. Sit. I've been offered a post at the Concord academy. Near my daughter.   [gesture]
them: I've thought about it every night for a month. You tell me the truth. Should I go?
? choice
* Go. She'd be glad, even if she doesn't say so.   flavour:practical mem:go
  them: Perhaps. I think so too, some nights.
* I'd miss you. But it's your life, not the ship's.   flavour:share mem:miss
  them: That's the first time anyone's said the second part to me.
  + them: That's the first time anyone's said the second part. Or the first part, come to that. Thank you.   [listen]
* What does the ready room say?   flavour:cheer mem:readyroom
  them: The Admiral says nothing, as usual. Very unhelpful.   [laugh]
them: I'm staying. For now. Ask me again in a year.
them: Take this. The last piece I play on Thursdays. Someone should have it who'll know what it means.
