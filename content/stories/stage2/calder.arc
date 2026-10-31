@arc calder
who: calder
// Stage 2 (ST1, 2026-10-31): baked from here (content/stories/stage2/, read only while STORIES2_ON); the words are
// content/stories/waiting/calder.story's, unchanged; only the builders' notes became fields and if-lines.
// "Well done" (content/arcs/outlines.md, section 2). The Works writer, arc batch. Nobody says "well done" before
// beat 5: it's the payoff. Beats 1-2 are light and at work (duty: true); 3-5 are off duty. needs: practical.
// Fenn is named only from beat 3; the junior on the Halcyon only from beat 4.
// Crew stories (SW1, 2026-10-24, from outlines.md "D. Chief Ines Calder"): beats 1-4 kept word for word. Beat 5 is
// the crescendo at the Works Friday tea on Day 26, just before her question; beat 6 its quiet ending (the old beat 5,
// as written); beat 7 the afterglow at your bench, with no "well done" in it. Still nobody says "well done" before
// beat 5 or 6. A line starting "if <conditions> |" plays only when they hold.

== beat 1
tone: light
when: rep:known
where: calm
duty: true
hint: Tea's poured. Sit, if you're sitting.
mem: swarf
them: Friday tea. I'm not on a break. I'm standing near the tea.
them: I started in a shipyard. Two years sweeping swarf. Metal shavings. Off every floor.
them: Best two years. You learn where everything falls. And why.
? choice
* Two years of sweeping? I'd have gone mad.   flavour:cheer mem:mad
  them: I did. Quietly. It passed.   [nod]
* What did it teach you?   flavour:listen mem:taught
  them: Where things go wrong. A lathe throws swarf left when it's out of true. You see it before you hear it.
* Shall I sweep the bay after shift? I'd like to see.   flavour:practical mem:sweep
  them: You would. Fine. Left of the lathe first.
  + them: Fine. Left of the lathe first. Then tell me what you find. I'll want the numbers.   [nod]
them: And before you ask. It's a mug.

== beat 2
tone: light
when: rep:known beat:calder.1
where: calm
duty: true
hint: Hands free? I need two minutes of them.
mem: toolbox
them: Hold this. Both hands. I'm moving the shelf.
them: Heavier than it looks. Most things are.
them: Don't open it. It isn't mine.
? choice
* (Hold it very carefully)   flavour:listen mem:careful
  them: Good. Give it here.   [nod]
* Whose is it?   flavour:share mem:whose
  them: Someone's. Shelf's done. Give it here.
* I'll fix that shelf bracket while it's down.   flavour:practical mem:bracket
  them: It's at four turns. It wants five. Go on.
  + them: Four turns. It wants five. You heard that too. Good. Go on.   [nod]
them: Right. Back to it.

== beat 3
tone: heartfelt
when: rep:well beat:calder.2 time:evening
where: calm
hint: You're still here. So am I. Sit a minute.
mem: fenn
them: A letter. On my device. Eleven days ago. Opened. Not answered.
them: My first chief. Fenn. Rhoda Fenn. She's retiring. Marra Station.
them: She taught me everything I know. Every serial number, every sound. She never once said I'd done well.
them: I don't know what to write back. That's new. I always know what to write.   [sigh]
? choice
* What would you want to say, if it were easy?   flavour:listen mem:easy
  them: Thank you. And: was it on purpose. That's two things. That's the problem.
* Start with one true sentence. The rest follows.   flavour:practical mem:onesentence
  them: One true sentence. Hm. That's a procedure. I can do a procedure.
  + them: One true sentence. That's a procedure. I can follow a procedure. Thank you. I mean that.   [nod]
* I've got a letter I haven't answered too.   flavour:share mem:samething
  them: Then we're both behind. Don't tell anyone.
them: That's enough of that. Go and eat something.

== beat 4
tone: heartfelt
when: rep:well beat:calder.3
where: appt
hint: Your progress talk. Sit. It's not about the numbers today.
mem: toohard
them: Your numbers are fine. Better than fine. That's not why I wanted the time.
them: Am I too hard on you? Honest answer. I'll know if it isn't.
them: The last junior I trained transferred to the Halcyon. Very good hands. Never wrote. Not once.
them: I was hard on them. I told myself it was for them. I'm not sure it was. It might have been for me.   [sigh]
? choice
* Sometimes. But I always know where I stand. That matters.   flavour:practical mem:honest
  them: Sometimes. Noted. Thank you for the honest one.
  + them: Sometimes. Noted, and I'll act on it. You know where you stand. That was the point. I'd forgotten it was the point.   [nod]
* Why do you think they never wrote?   flavour:listen mem:whynot
  them: Busy. Or I didn't leave a door open. Probably the door.
* My best teacher was hard too. I still write to them.   flavour:share mem:stillwrite
  them: Do you. Hm. Then it can go either way. That helps more than you'd think.
them: Right. Next talk in four weeks. Book it.

== beat 5
// CRESCENDO rides on: Calder's question (the Works Friday tea, the Pillar 5 career meeting): plays just before her question; day: 26; cast: calder, halloran-emeka, pell, torres-zeke, you; quiet ending: beat 6
// As built (ST1, 2026-10-31): Four weeks aboard (Day 26, 18:40), only once you're an Engine Specialist (her question is
// for one), before she sits down to ask (19:05). A fixed time (at:), not the tradition: by their plans she and the cast are
// still at dinner as it starts, so section 20c plans them at the tea corner 18:40-19:05.
tone: resolution
when: rep:well beat:calder.4 weekday:fri day:26 myrank:specialist
crescendo: at:18:40-19:05
quiet: 6
cast: halloran-emeka pell torres-zeke
title: Four weeks aboard
where: Tea corner
hint: Stay for the tea. All of it. Near the front.
mem: welldone
flag: calder.welldone
calder: Four weeks. Mugs down a minute. Not you, Pell. You can hold yours.
calder: I don't do this in front of people. You all know that. I'm doing it anyway.   [sigh]
calder: My first chief wrote to me. Fenn. I answered her. Late. Four drafts.
if mem:moment.calder.onesentence | calder: One true sentence first, then the rest. Someone told me that. It works.
calder: She wrote back two words. Took her thirty years. I won't take that long.
calder: {me}. Well done.   [nod]
halloran-emeka: Oh, that's lovely. Sorry, Chief. My hands have started clapping on their own.   [laugh]
calder: Halloran.
calder: Fine. Carry on, then.   [gesture]
pell: Get in. That's ours, that is. Works trained. Pell approved.   [laugh]
torres-zeke: Nobody look at me. I'm fine. It's the tea. It's very hot tea.
? choice
* Thank you, Chief.   flavour:listen mem:thankyou
  calder: Noted. Don't make a habit of earning it. No. Do.
* Four weeks. Fenn took thirty years.   flavour:cheer mem:fourweeks
  calder: I had a head start. I knew what it was like without.   [laugh]
* I'll sign the board and get back to work.   flavour:practical mem:backtowork
  calder: Good. Exactly what I'd have said.
  + calder: Good. Exactly what I'd have said, and the board agrees. Twelve jobs. Take the scrubber first.   [nod]
calder: Right. That's that. Now. My question.

== beat 6
// QUIET ENDING for beat 5: plays only if Calder's question (Day 26) passes without beat 5; then it plays when the story is ready
tone: resolution
when: rep:well beat:calder.4
where: calm
hint: There's something on your bench. You'll want to see it first.
mem: welldone
flag: calder.welldone
keepsake: a spare key to the toolbox, on a loop of Works orange wire
learn: Chief Calder's first chief, Rhoda Fenn, never said well done. Calder answered her letter, and said it to you.
them: You've seen the toolbox on your bench. Borrowed. Return it when you're done. No hurry.
them: I answered Fenn. One true sentence, then the rest. She wrote back. Two words.
them: "Well done." Took her thirty years.   [sigh]
them: I won't take that long. So. Plainly, while I've got the nerve.
them: Well done, {me}.
? choice
* Thank you, Chief. That means a lot.   flavour:listen mem:thanked
  them: It should. I don't hand it out.   [nod]
* I'll look after the toolbox. Every tool back in its place.   flavour:practical mem:lookafter
  them: I know you will. That's why it's on your bench.
  + them: I know. That's why it's on your bench and not anyone else's. Here. The spare key. Keep it.   [gesture]
* Thirty years. You only took one.   flavour:cheer mem:onlyone
  them: Don't get used to it.   [laugh]
them: Right. Back to it. Board's at sixteen.

== beat 7
// AFTERGLOW: plays after beat 5 only (beat 6 already has the bench)
// DAY: the next workday after beat 5 (Day 29 in a new game: she's off at weekends)
tone: light
tier: close
gapDays: 1
follows: 5
duty: true
where: Works bay
when: beat:calder.5 flag:calder.welldone time:morning
hint: Your bench. Before the board.
mem: borrowed
keepsake: a spare key to the toolbox, on a loop of Works orange wire
learn: Chief Calder's first chief, Rhoda Fenn, never said well done. Calder answered her letter, and said it to you in front of Works.
them: Your bench. Before you start.   [gesture]
you: "Borrowed. Return it when you're done. I.C."
them: Fenn's. Then mine. Now it's on your bench. That's all it means. Don't read more into it.
them: The top tray sticks. Lift from the left. Fenn never fixed it. Neither did I. On purpose, probably.
them: Hm.   [nod]
? choice
* (Open it. Every tool in its place.)   flavour:listen mem:opened
  them: Thirty-one tools. All where she left them. Keep them there.
* Every tool back where it was. I'll keep it that way.   flavour:practical mem:lookafter
  them: I know. That's why it's on your bench.
  + them: I know. Oil on the hinges, not the tray. Here. The spare key. That part isn't borrowed.   [gesture]
* My first teacher lent me a tool once. I've still got it.   flavour:share mem:lent
  them: Then you know how this goes. You give it back. Then one day you lend yours.
them: Right. Board's at seventeen. Pick two. Back to it.
