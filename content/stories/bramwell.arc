@arc bramwell
who: bramwell-basil
// "Your turn" (content/arcs/outlines.md, Crew stories, F). SW2. Basil Bramwell, Works cadet, comes off the Tern on Day
// 21 into Theo's old berth. Quick and bright; three questions in one breath; tries to sound like an old hand (his voice
// card, content/voices/bramwell-basil.voice). needs: share, so share replies get the warmer answer. The story is about
// you, four weeks on, not being the newest any more. Window Days 21-30: the lowest gates of all (met counts from Day 21).
// Not used: his parents' repair shop, letters read aloud, the ticket home he's saved for.

== beat 1
// DAY: 21 (Off the Tern, 17:40, as the ramp opens)
tone: light
tier: stranger
metDays: 0
where: any
when: trad:off-the-tern day:21
hint: Hi, hi. Sorry. Are you the one from the beam?
mem: ramp
learn: Basil Bramwell came aboard on Day 21 with a plant from home, and a great many questions.
them: Hello. Hi. Sorry. This is Deck 5. Zeke said. Hello.   [gesture]
them: Are you the one from the beam? Zeke said there'd be someone nearly as new as me.
them: Which way's the Works bay? Do you get lost? Is the lift always that loud? Don't answer all of them.
them: This is my plant. It's from home. It didn't like the Tern much. Neither did I.   [laugh]
? choice
* The Works bay's just through there.   flavour:practical mem:way
  them: Through there. Brilliant. I'll pretend I knew that.
* I got lost twice on my first day.   flavour:share mem:losttwice
  them: Twice? Oh, thank goodness. I'll aim for three, then.
  + them: Twice? Oh, that's brilliant. Not for you. For me. So I can get lost loads and still be fine.
* The lift's always that loud. You stop hearing it.   flavour:cheer mem:loudlift
  them: Good. I thought it was cross with me.
them: Right. Kitbag, plant, Basil. All here. Hello, Wren.

== beat 2
// DAY: 22 (after Name on the beam, 17:05)
// FAVOUR basilPlant (new): take Basil's plant to Tove Cruz in the garden; back in two days; done sets flag:bramwell.plant.done
tone: light
tier: acquaintance
metDays: 1
where: calm
when: beat:bramwell.1 day:22
hint: My name's on the beam! Have you seen? Can I show you my shelf? It's a very small shelf.
mem: shelf
them: My name's on the beam. Basil Bramwell. Up there with everyone's. I keep going back to look at it.
if beat:torres.5 | them: And you handed me the pen. Zeke said you'd want to. I nearly dropped it. Did I? I didn't.
them: Then I put my plant on my new shelf. It looked at me. It's worse. How is it worse?   [sigh]
if beat:teague.5 | them: And under the shelf, someone's drawn a tiny person waving. "Hi, new one." Who did that? I love it.
them: Yellow at the edges. Is that too much water? Not enough? Is it the air? It's the air.
? choice
* Tove Cruz knows every plant aboard. I'll take it to the garden.   flavour:practical favour:basilPlant flag:bramwell.plant mem:garden
  them: Would you? If I went I'd ask Cruz forty questions, and the plant would wilt while it waited.
* It's had a long trip. Give it a day.   flavour:listen mem:aday
  them: A day. Yes. We've both had a long trip. We'll both have a day.
* I brought a bit of home too. It's on my shelf.   flavour:share mem:bitofhome
  them: Did you? What is it? No, don't tell me. Show me. When I'm less new.
  + them: Did you? Oh, brilliant. So it's normal. Everybody's shelf has a bit of home on it. I feel much better.
them: Right. Thanks, thanks. I'll stop talking now. I won't. But I'll try.   [laugh]

== beat 3
// DAY: 23-24
tone: light
tier: acquaintance
metDays: 2
where: calm
when: beat:bramwell.2 day:23-24
hint: Can I ask you some things? Lots of things. Quick ones. Mostly quick.
mem: visitor
them: Does Calder ever blink? I watched her at the board. I counted. I got to none.
them: Is the tea rota first come, first served? No. There's a rota on the wall. Halloran showed me. Twice.   [laugh]
them: Who does the Friday playlist now? Is it still one song too long? Pell says that's tradition.
them: Sorry. One more. A real one.   [sigh]
them: Does it stop? Feeling like a visitor? Like you're only borrowing the bunk?
? choice
* It stopped for me in week two. One day it just had.   flavour:listen mem:weektwo
  them: One day it just had. All right. I'll watch out for that day.
* Ask me again when you've got a mug on the rack.   flavour:cheer mem:mugrack
  them: The mug rack! That's how you know? Oh, I want a mug. When do I get a mug?
* My first nights, the ship's hum kept me awake. Then one night it was just the hum.   flavour:share mem:hum
  them: Just the hum. Yes. I've been listening to it too.
  + them: You lay awake too? I thought it was only me. It's quite a friendly hum, once you stop listening for it.
them: That's helped. Thanks, thanks. I'll still ask you a hundred things tomorrow. Sorry in advance.

== beat 4
// CRESCENDO rides on: dinner in the mess on Thursday Day 25, the Works crew's welcome for him (the crew welcome tea is retired, the user 2026-10-26; lead 37 and FX22b); cast: none (everyone only if there); quiet ending: beat 5
// DAY: 25; plays only if the plant came back (flag:bramwell.plant.done)
tone: resolution
tier: acquaintance
gapDays: 0
where: meal
when: beat:bramwell.3 flag:bramwell.plant.done day:25
crescendo: meal:dinner
quiet: 5
title: Basil's welcome dinner
invite: My dinner! | The Works lot are having dinner with me tomorrow, {at} in the mess. A welcome, Halloran says. Do I bring biscuits? Zeke says no. Pell says yes. Cruz says bring the plant. Basil
hint: My welcome dinner! You're coming? Bring nothing. That's the rule, isn't it?
mem: everybody
keepsake: a little clay pot he painted, with the Wren on it
them: Is that my mug? With my name on? Spelt right and everything. Brilliant.   [gesture]
if here:cruz-tove | cruz-tove: Mm. Here. Less love, more light. That's all it wanted. It's a Wren plant now.
if !here:cruz-tove | them: Tove Cruz left it by my mug this morning. With a note: less love, more light.
them: My plant. Look at it. It was yellow on Sunday. It's green!   [laugh]
if here:pell | pell: Somebody give the plant a mug. It's earned one.   [laugh]
if here:torres-zeke | torres-zeke: Two new names on the beam this month, and now a plant. Coil three's jealous.
if here:halloran-emeka | halloran-emeka: Here. I've cleared a space on the mug-rack shelf, back in Works. It goes there after. Lovely.   [gesture]
if here:halloran-emeka | halloran-emeka: Everybody's now. That's how we do it here.
if !here:halloran-emeka | them: Halloran's cleared a space for it on the mug-rack shelf in Works. Everybody's, he says. That's how it's done here.
them: Everybody's. Oh. It's the first thing of mine that lives here. The rest is still in my kitbag.
them > you: This is for you. I painted two pots on the Tern. One for the plant, one for whoever helped. It's the Wren. Badly.
? choice
* Next year you'll be clearing that shelf for someone.   flavour:listen mem:nextyear
  them: Me? Clearing the shelf? For someone newer than me? Oh. I'd like that.
* That plant's more at home than either of us.   flavour:cheer mem:athome
  them: It's got a mug rack and everything. I'm a bit jealous of my own plant.
* Somebody made room for me, my first week. That's what the shelf is.   flavour:share mem:roomforme
  them: So it goes round. Somebody made room for you, and you made room for me.
  + them: So it goes round. Someone made room for you, you made room for me, and one day I'll make room. That's the best thing I've heard here.
them: Everybody's. I'm going to remember that one. Brilliant.

== beat 5
// QUIET ENDING for beat 4: plays only if beat 4 was missed, or the plant favour wasn't done (Cruz brought it back)
tone: light
tier: acquaintance
gapDays: 0
where: calm
when: beat=bramwell.3
hint: Have you seen the shelf? My plant's on it! Well. It's a plant. But still.
mem: shelfplant
keepsake: a little clay pot he painted, with the Wren on it
mail: 600 | My dinner | You missed a good one! Pell wanted the plant to have a mug. Zeke said coil three was jealous. Halloran put it on the shelf and said it belongs to everyone now. See you at breakfast? I've got questions. Obviously. B.
them: My plant's on the mug-rack shelf in Works. Tove Cruz brought it back this morning. Green as anything.
them: Cruz said it wanted less love and more light, then walked off. I think that's a lot of talking, for Cruz.   [laugh]
them: My welcome dinner was brilliant. Halloran made room on the shelf for it. It's everyone's shelf, he said.
them > you: Here. I painted it on the Tern. It's the Wren. It was for whoever helped. You answered all my questions.
