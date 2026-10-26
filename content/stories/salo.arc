@arc salo
who: salo-saad
// "Twice" (content/arcs/outlines.md, Crew stories H). SW3, 2026-10-24. Cheerful, slow, patient; never rushes anyone;
// in bed by ten; the twin's news as a serial. needs: listen. New canon (the outline): the Pallas, a freighter, years
// ago; a valve signed off unchecked; a deck cold for a night; nobody hurt. His little sister Hala, into the academy.
// Every scene is before ten at night. The twin has no pronoun (the twin is "my twin"; the old lines say "they").
// Numbering: beat 4 is the crescendo, beat 5 the afterglow (after 4 or 6), beat 6 the quiet ending for beat 4.

== beat 1
tone: light
where: calm
when: !event:ionStorm
hint: Got a minute? New episode from the Halcyon. It's a good one.
mem: halcyon
them: Hello, hello. Sit down. Last time on the Halcyon: my twin found a chair. The good one, by the mess window.
them: This week, a visiting inspector sat in it. My twin stood beside the chair for the whole of lunch. Not a word.   [laugh]
them: The inspector moved tables. The Halcyon's calling it a victory. Next week: the inspector's report.
them: One more bit of news. Not from the Halcyon. My little sister, Hala. She's got into the academy.
them: Hala. Who used to hide in the laundry basket at bedtime. She's going to be an officer.   [nod]
? choice
* You must be so proud of her.   flavour:listen mem:proud
  them: I am. More than I can say. So I won't, yet.
  + them: I am. I keep reading her message, slowly, as if it might change. It doesn't. She's in.   [laugh]
* Will your twin make it a two-part episode?   flavour:cheer mem:episode
  them: Three parts. Hala's a whole series of her own.   [laugh]
* My family would have thrown a party.   flavour:share mem:party
  them: Mine will. On the Tevan belt they'll hear it over the rain.
them: Anyway. That's enough of me. How was your board today? Tell me slowly.

== beat 2
tone: light
where: Engine room
duty: true
when: beat:salo.1 !event:ionStorm
hint: Come and look at something. Mind the floor, it's just been done.
mem: card
them: Hello, hello. Don't mind me. I'm looking at this valve. Again.
them: That's three. Once for the job. Once for the rule. Once for me.   [laugh]
them: Here. My card. It lives in this pocket. My list, my rule at the top: slow hands, open eyes. It's gone soft as cloth.
them: Shut it, seat it, look again. Nothing clever on it. It's the doing it that counts.
them: Twice is the rule. Three is me. I'm working on that. Slowly.
? choice
* Why three?   flavour:listen mem:whythree
  them: A long story. Not one for the engine room. Another day.
  + them: A long story, and I tell it slowly, so it's longer still. Ask me again some evening. Before ten.   [nod]
* I check mine once and hope.   flavour:cheer mem:hope
  them: Then I'll go over yours two more times. Between us, that's three. Perfect.   [laugh]
* Could I copy your list?   flavour:practical mem:copy
  them: Sure. Copy it in your own hand, though. It sticks better that way.
them: There. Four. No, I'm joking. Three. On we go, slowly.   [laugh]

== beat 3
// DAY: 8-12
// before the storm, so the storm can carry beat 4; early evening, before ten
tone: heartfelt
gapDays: 0
where: calm
when: beat:salo.2 time:evening !event:ionStorm.onset !event:ionStorm.escalation day:8-12
hint: Sit with me a minute? Before ten. There's a story I've not told.
mem: cold
them: Years ago I was on a freighter, the Pallas. Long shifts, old pipes. I liked her.
them: End of a long one, I signed off a valve I hadn't looked at. I was tired. I wanted my bunk.
them: It stuck. A whole deck went cold for a night. People slept in their coats.   [sigh]
them: Nobody was hurt. Nobody remembers it now. I asked, once. They'd forgotten. I haven't.
them: Hala wrote. She asked what she ought to know before the academy. What I'd tell her.
them: And I thought: she's like me. Good at it. Careful. And one tired night away from a cold deck.
them: So I haven't written back. Three weeks. That's not like me either.
? choice
* That's a long time to carry one night. Go on.   flavour:listen mem:carry
  them: It's not heavy. Just old. I keep it in the same pocket as the card.
  + them: It isn't heavy. Just old, and always in my pocket. Saying it out loud is different. Thank you for not hurrying me.   [nod]
* A deck full of people in coats. Sounds like a sleepover.   flavour:cheer mem:coats
  them: Ha. One of the engineers said that, in the morning. He was the only one laughing. Well. Now there's two.   [laugh]
* I've done things I still think about too.   flavour:share mem:shared
  them: Everyone has. Nobody says. Thank you for saying.
them: Right. Twenty to ten. I'll walk you to the lift, then bed.

== beat 4
// DAY: 13
// CRESCENDO rides on: the ion storm (event ionStorm, its Saturday, daytime); he's off duty, so it starts wherever he's sitting:
// Zeke's call on the comm, then the walk down to the Deck 6 coolant loop (lead 36, 2026-10-25); day: 13; cast: salo-saad, torres-zeke (on shift), calder (over the comm); quiet ending: beat 6
tone: resolution
tier: friend
gapDays: 0
where: calm
crisis: true
when: beat:salo.3 event:ionStorm day:13
crescendo: event:ionStorm
quiet: 6
title: The coolant loop with Saad
invite: Tomorrow | The storm's meant to get worse overnight. It's my rest day, but from {at} I'll be down by the Deck 6 coolant loop all the same. I'd be glad of the company. Saad
hint: Deck 6, the coolant loop. Could you come? Now, if you can.
mem: once
flag: salo.signed
learn: Saad Salo once signed off a valve he hadn't checked. In the ion storm he checked one once, properly, and signed it.
torres-zeke: Saad? Loop three's dropping. Need you on it when you can. No rush. Well. Some rush.
them: That's me. Rest day, and I'm going anyway. Storms don't read the rota. Walk down with me, {me}? Glad it's you.
them: Deck 6. Loop three. Here. The valve's sticking. Half open, showing shut.   [gesture]
them: It's the same. The same feel under my hand. The Pallas one did exactly this.
them: Give me a moment. My hand won't go.   [sigh]
? choice
* I'm here. Take your time. We've got a minute.   flavour:listen mem:steady
  them: A minute. Yes. Breathe, then the valve. In that order.
  + them: A minute. You said that the way I'd say it. Breathe, then the valve. Thanks, friend.   [nod]
* Let's check it together. Once, properly.   flavour:practical mem:together
  them: Together. Once. Shut it, seat it, look again. Your eyes and mine.
* If Hala were here, I'd tell her to watch you do this.   flavour:share mem:hala
  them: Would you? Then I'd better do it well.   [laugh]
them: Shut. Seated. Looking.   [listen]
them: There. I checked it once, properly, and it's right. I'm signing it. Once.   [nod]
calder: Deck 6 loop. Holding at forty. Good.
torres-zeke: Loop's steady. Properly done, Saad. Right, onward.   [gesture]
them: My hands are shaking now. After. That's the right order, isn't it?   [laugh]
them: Somewhere in the Service it's past my bedtime. I'm counting that.

== beat 5
// DAY: from 14
// afterglow: after the all-clear (Day 14 on), calm, before ten; plays after beat 4 or beat 6
tone: resolution
tier: friend
where: calm
when: !event:ionStorm day:14-
follows: 4|6
hint: Before ten, could you sit a minute? I've written to Hala. At last.
mem: tohala
keepsake: a checking card he made for you, with your name at the top
learn: Saad Salo sent his sister Hala his old checking card, with one line of his own on the back.
them: I'm sending Hala my old card. The soft one. She'll need a good pocket for it.
them: I wrote one line on the back. Just one. It took me all week. Want to hear it?
them: "Look once, slowly and properly. Then trust your own hands."   [nod]
them: The second half's the hard bit. I only learnt it lately. With you there.
? choice
* She'll keep that for years.   flavour:listen mem:keep
  them: I hope so. Soft as cloth by the time she's my age.
  + them: I hope so. I kept the first half for years. She gets both at once. That saves her a cold deck.   [nod]
* Tell your twin. That's an episode.   flavour:cheer mem:finale
  them: The season finale. The Halcyon will want a sequel.   [laugh]
* I might write my own card.   flavour:share mem:mycard
  them: No need. I've done you one.
them: Here. Your name at the top, my list underneath. In my best writing, which isn't very good.
them: Now. Nine fifty-two. Off to bed. Night, then.

== beat 6
// DAY: from 16
// QUIET ENDING for beat 4: plays only if beat 4 was missed (not friend by the storm, or not on Deck 6); any Deck 6 job after Day 15
tone: light
tier: friend
where: Engine room
duty: true
when: beat:salo.3 !event:ionStorm !flag:salo.signed day:16-
hint: Have you a minute? This one's sticking. I'd like a second pair of eyes.
mem: quietvalve
mail: 180 | One valve | Thank you for this afternoon. One valve, checked and signed once. It doesn't sound like much. It was a lot. Writing to Hala tonight. Before ten, of course. Saad
them: Hello, {me}. Small job. A valve on loop two, sticking a little.
them: The storm's long gone. Just me and a valve now. Easier, in a way. And not.
them: Shut. Seated. Looking. Once, properly.   [nod]
? choice
* I'm watching. Take your time.   flavour:listen mem:watched
  them: I know. That's why I can.
  + them: I know. It's easier with someone who doesn't hurry. You never do. There. Done.   [nod]
* Once? Not three times?   flavour:cheer mem:onlyonce
  them: Once. I'm practising. Don't tell Calder. She'll want it in writing.   [laugh]
* Shall I sign it with you?   flavour:practical mem:cosign
  them: My name's enough. But stand there while I write it. That helps.
them: Signed. Once. First time in years.
