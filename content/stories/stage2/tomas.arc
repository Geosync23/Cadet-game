@arc tomas
who: tomas
// "The bottom of the ramp" (crew stories, stage 2). SW4, 2026-10-31, for lead 47 and the builder ST1. Tomas Lind,
// Watch rating, your bunkmate. Beats 1-4 stay exactly as in the game (STORY_ARCS.tomas: the star map, his brother's
// birthday call, the dropped call, his brother's star map). Beats 5 onward are new and replace the older words in
// content/arcs/tomas.arc while STORIES_ON is on.
// Built (ST1, 2026-10-31): baked from content/stories/stage2/ like the other stage 2 stories, so it plays only while
// STORIES2_ON is on too (the old beats 5-7 in content/arcs/tomas.arc, parked, play while it's off). SW4's words unchanged.
// The story (the user, 2026-10-31): nobody met Tomas off the Tern when he arrived, and he got lost; now he is the one
// who meets the next newcomer, Basil Bramwell, off the Tern (Off the Tern, the shuttle bay, Day 21, 17:40). Threads
// kept from the old outline: the Watch exam he failed once and never told Holt, the posting near home on the transfer
// list, finding his place, the Wren as home too. needs: listen, so listen replies get the warmer answer.
// New canon (facts.md row): the Tern came in early on his first day and nobody was at the foot of the ramp; he waited
// ten minutes, then went looking for his bunk and found the laundry; that's how the long way round began. Holt walks
// the long way too (his card), and knew about the exam all along.
// Basil's own story (content/stories/bramwell.arc) is untouched: his beat 1 can still follow this scene at the same
// gathering. Not used: star maps (beats 1-4 have them), his brother's call, Basil's plant beyond a glance.

== beat 5
// DAY: 8-20 (after week 1, before the Tern brings Basil)
tone: light
gapDays: 1
where: calm
when: beat:tomas.4 day:8-20
hint: Can I tell you about my first day? It's quick. Quick and a bit sad. Quite funny, though.
mem: nobody
them: The Watch office gets the Tern's list. Who's coming aboard. I'm not meant to read it out. I'm reading it out.   [gesture]
them: One new cadet, for Works. Basil Bramwell. Isn't that a good name? It sounds like someone who owns a boat.
them: When I came aboard, the Tern was early. Everyone was at dinner. I walked down the ramp and nobody was at the bottom.
them: I stood there ten minutes with my kitbag. In case it was a test. Then I went looking for my bunk and found the laundry.   [laugh]
them: That's how the long way round started. I learnt this whole ship by getting it wrong first.
them: I'd like to be at the bottom of that ramp for Basil. Only I'd have to ask Holt. And there's a thing Holt doesn't know.
them: Here it is. I didn't pass the Watch exam. Not the first go. The second go, yes. You're the only one aboard who knows. Oh, no.   [sigh]
? choice
* Ten minutes on your own? That sounds awful.   flavour:listen mem:tenminutes
  them: It was, a bit. The bay's very big when it's only you. I said hello to it. It said hello back. Echoes.
  + them: It was, a bit. Nobody's fault. Dinner's dinner. But I said hello to the bay, and only the bay said it back.
* You'd be the best person for that ramp.   flavour:cheer mem:bestramp
  them: Would I? I'd know what not to do. I know loads of things not to do. That's sort of a skill.   [laugh]
* Ask Holt. I'll wait outside his door.   flavour:practical mem:door
  them: Outside the door. Yes. Close enough to hear me fall over. Not close enough to see it.   [laugh]
them: Don't tell anyone about the exam. Or the laundry. The laundry's worse, actually.

== beat 6
// DAY: 10-20, evening
tone: heartfelt
gapDays: 2
where: calm
when: beat:tomas.5 day:10-20 time:evening|night
hint: Sit with me for a while? I've got something open on my device. I keep not closing it.
mem: posting
them: The transfer list has a posting near the farm moon. Station Watch. You'd see the grey from the window.   [sigh]
them: I haven't applied. I open it, read it, close it. Open it again. My device must think I'm in love with it.   [laugh]
them: My first night here, if the Tern had still been on its pad, I think I'd have got back on. Kitbag and all.
them: Then breakfast happened. Then you came, a week later. Someone newer than me. I had someone to show round.
them: But some days I'm still the one at the bottom of the ramp. Waiting to see if anybody's coming.
them: Is that what the posting is? The ramp feeling again? Or is it home, calling? I can't tell them apart.
? choice
* Which bit of home is loudest tonight?   flavour:listen mem:listened
  them: My brother's feet on the stairs. Bread. A grey sky that never surprises you. That's three. Sorry.
  + them: My brother's feet on the stairs. Bread. The grey. Saying them to you, they feel nearer. And smaller. In a good way.
* Somebody's coming to that ramp this time. You.   flavour:cheer mem:somebody
  them: Me. If Holt says yes. If I ask. If I don't fall over on the way in. Lots of ifs. But me.
* Close it for tonight. Decide another day.   flavour:practical mem:closeit
  them: Another day. Yes. There. Closed. It's still there, but it's closed. That's different. I think that's different.
them: Thanks for sitting. You don't have to say anything clever. The sitting's the clever bit.

== beat 7
// DAY: 13-20 (before the Tern). Holt's yes, told by Tomas; the exam still untold.
tone: light
gapDays: 1
where: calm
when: beat:tomas.6 day:13-20
hint: I did it. I went in. Ask me what happened. No, don't. I'll tell you.
mem: pencil
flag: tomas.meets
them: I went to Holt's office. I knocked. He said "Yes." Not "come in". Just "Yes." I came in anyway.   [gesture]
them: I asked to meet the next Tern. For the new cadet. I said it very fast. It came out as one long word.
them: He looked at me for ages. Then he took a pencil and wrote my name on the rota himself. In the margin.
them: Then he said, "Take him the long way. It's how you learn a ship." Holt! The long way!   [laugh]
them: He walks the long way every morning. I thought I'd been doing it wrong for weeks. I was doing it like Holt.
them: I didn't tell him about the exam. I got as far as "Chief, there's a thing," and then I asked about boot polish.   [sigh]
them: I'm making a sign for the ramp. What should it say? I've got a lot of glitter and not much spelling.
? choice
* WELCOME TO THE WREN, BASIL. Big letters.   flavour:cheer mem:bigletters
  them: Big letters. Big enough to read from the top of the ramp. I'm going to measure the ramp.
* YOU'RE NOT LOST. The thing nobody said to you.   flavour:listen mem:notlost
  them: Oh. Yes. That's it. That's the sign. His name can go underneath. Small.
  + them: Oh. That's it exactly. That's what I needed to read, my first day. How did you know? You knew.
* Practise on me. I'll be Basil.   flavour:practical mem:rehearse
  them: Right. You come down the ramp. Slower. Look lost. Good, very good. Hello! Welcome! Oh, I'm nervous already.   [laugh]
them: My name, in Holt's pencil. I'm not rubbing it out. Nobody's rubbing it out.

== beat 8
// CRESCENDO rides on: Off the Tern (trad off-the-tern), the shuttle bay as the ramp opens, 17:35-17:55; day: 21; cast: bramwell-basil torres-zeke holt; quiet ending: beat 9
// Holt is off duty on Sundays and Tomas asked him; if Holt can't come, his two lines drop and Tomas's "if !here:holt"
// line plays. Basil's beat 1 (bramwell.arc) can follow at the same gathering; nothing here says what his says.
// Lead 47 (2026-10-31): its own scene at 17:35, paired on purpose with Theo's send-off at 14:30 the same afternoon
// (a goodbye, then a hello). Tomas's one nod to Theo says nothing of Basil's berth, so Basil's beat 2 doodle stays a surprise.
tone: resolution
gapDays: 0
where: Shuttle bay
when: beat:tomas.7 trad:off-the-tern day:21
// Built (ST1): a fixed time (at:), 17:45-17:55, once Basil is down the ramp (17:43): Off the Tern is the arrival's own
// event, so the stories' planner hook can't send Tomas to it; section 20c plans him there (come: none: Zeke greets at the
// ramp foot and Basil comes down by their own plans). Holt out of cast: (off on Sundays; his lines are if here:, with
// Tomas's fallback), as SW4 offered.
crescendo: at:17:45-17:55
cast: bramwell-basil torres-zeke
come: none
quiet: 9
title: Tomas meets the Tern
invite: The Tern | Basil's Tern lands tomorrow at {at}. Shuttle bay. I'm on the ramp: Holt wrote it in pencil, so it's official. Stand near me? Tomas
hint: It's nearly time. Stand by me? If I wave too early, pull my arm down.
mem: welcome
keepsake: the welcome sign from the shuttle bay, glitter coming off the B
learn: Nobody met Tomas off the Tern, so he met the next new cadet himself, and told him about the Watch exam, with Holt there.
them: Is the sign straight? It's straight. Is it the right way up? It's the right way up. Is it?   [gesture]
if mem:moment.tomas.notlost | them: YOU'RE NOT LOST, and his name underneath, small. I went over the letters three times.
if mem:moment.tomas.bigletters | them: WELCOME TO THE WREN, BASIL. You can read it from the top of the ramp. I measured.
if mem:moment.tomas.rehearse | them: I've practised. You were a very good Basil. Better at it than I am at being me.   [laugh]
if here:holt | holt: Lind. Feet apart. Shoulders down. You're greeting a cadet, not holding an airlock.
if here:torres-zeke | torres-zeke: Ramp's opening. Coil three always hums before a big push, Tomas. Hum if it helps.
them: Theo went up this ramp this afternoon. Now somebody's coming down it. Busy ramp. I waved at Theo too early, as well.   [sigh]
bramwell-basil: Is that for me? Is that my name? Is that glitter? It's glitter. Hello!   [laugh]
them: Hello! Welcome to the Wren. I'm Tomas. I'm Watch. You're not lost. That was the main bit. The rest is extra.
them > bramwell-basil: When I came down this ramp, nobody was at the bottom. So I wanted somebody to be. Today it's lots of somebodies.
bramwell-basil: Nobody? Not anyone? What did you do? Where did you go? Sorry. Pick one.
them: I found the laundry. Twice. And a secret for your first week: I failed my first Watch exam. And look. Here I am, on the ramp.
if here:holt | holt: Hm. Failed it, then sat the next one an hour early, in a pressed shirt. That's the Watch, Bramwell.
if here:holt | them: You knew? You knew. Of course you knew. Oh. That's good, actually. That's very good.   [laugh]
if !here:holt | them: Don't tell Holt. No. Do tell Holt. I think I've finished not telling Holt.
? choice
* Tell him about the laundry. Both times.   flavour:listen mem:laundry
  them: First time I was looking for my bunk. Second time I was looking for the way out of the laundry. Basil, it's a long way round.   [laugh]
  + them: First time I was looking for my bunk. Second time, for the way back. That's how you learn it, Basil. One wrong door at a time.
* Best welcome this bay's ever seen.   flavour:cheer mem:bestwelcome
  them: Is it? It is. I've seen two. This one's better. Mine didn't have anybody in it.   [laugh]
* Basil, you're in good hands. He's my bunkmate.   flavour:share mem:bunkmate
  bramwell-basil: Your bunkmate? So you were new too? Was he good at it? He's good at it. I can tell.
them: Right, Basil. We're going the long way. It goes past every window on the ship. I've counted them.   [gesture]
them > you: Here. Hold the sign. I need both hands for pointing. Keep it, actually. I know the way now. Oh. I know the way now.

== beat 9
// QUIET ENDING for beat 8: plays only if beat 8 was missed (Basil came off the Tern anyway, and Tomas met him). It
// stands on its own: it reads true even if beats 5-7 ran out of days before the Tern. No time of day: it needn't take
// the comet's evening or your night-shift evenings (Days 22-24).
tone: light
gapDays: 0
where: calm
when: beat:tomas.4 day:21-
hint: You missed the Tern! It's fine. I'll tell it. I'll tell it twice if you want.
mem: missedtern
keepsake: the welcome sign from the shuttle bay, glitter coming off the B
mail: 20 | He's here | Basil's aboard. One plant, a lot of questions. I answered about four. And Holt knew about my exam the whole time. The whole time! I saved you the sign. Tomas
them: You missed the Tern. Don't worry. Basil came down the ramp anyway. Ramps are like that.   [laugh]
them: He had a plant in both hands and a question in every breath. I held my sign up. There was glitter on everybody.
them: My first day, nobody was at the bottom of that ramp. Today somebody was. Me. I didn't even wave too early.
them: Then I told Basil I failed my first Watch exam. Out loud. And Holt was standing right behind me.   [sigh]
them: He said I sat the next one an hour early, shirt pressed. He knew. Every day I've been hiding it, he knew.
? choice
* I'm sorry I wasn't there. How did it feel?   flavour:listen mem:howfelt
  them: Like putting a kitbag down after carrying it all day. I didn't know it was heavy till it wasn't.
  + them: Like putting a kitbag down that I'd carried since the farm. I didn't know how heavy it was. Thanks for asking. Really.
* You did it. You actually did it.   flavour:cheer mem:didit
  them: I did, didn't I? I did a whole welcome. Nobody got lost. Well, I did, after. But only a little.   [laugh]
* Next Tern, I'm holding the sign.   flavour:practical mem:nexttime
  them: Deal. You hold, I point. We'll be a team. A Watch-and-Works team. Holt won't know what to do with us.
them: Here. The sign. Keep it for me. I know the way now. That's a funny thing to say out loud.

== beat 10
// AFTERGLOW: plays after beat 8 or its quiet ending (beat 9), from Day 25 (Day 22 is the comet, Days 22-24 your
// night shifts, lead 47)
tone: light
gapDays: 2
where: calm
follows: 8|9
when: day:25- time:evening|night
hint: Come and look out with me? I want to tell you something. A good something.
mem: twoskies
learn: Tomas closed the posting near home. The Wren is home too now, he says. Basil asks him the way, and he knows it.
them: Basil asked me the way to the garden today. I knew it. First go. No long way, no laundry.   [laugh]
them: Then I took him the long way anyway. He wanted to see the windows. All twenty-two.
them: And I closed the posting. Not opened and shut, like before. Gone. I didn't even read it one last time.
them: I wrote home last week. I said the Wren's home now, as well. My brother wrote back one line: "Told you. Two skies."
them: Somewhere between the laundry and Basil, I stopped waiting at the bottom of the ramp. Inside, I mean.
? choice
* When did it stop, do you think?   flavour:listen mem:stopped
  them: When Holt picked up that pencil, maybe. Or before. Lots of small things. They added up when I wasn't looking.
  + them: Lots of small things. Holt's pencil. The sign. You, standing next to me so I wouldn't wave too early. They added up.
* Your brother's very wise.   flavour:cheer mem:wisebrother
  them: He is. He's also very small. He spelt "skies" with two Ys. Very wise, though.   [laugh]
* My first evening, you came and found me. You were my somebody.   flavour:share mem:mysomebody
  them: Was I? I gave you directions like an old hand. Half of them were wrong. But I was there. I was, wasn't I?
them: Next Tern, you're coming. Somebody has to hold the sign. I'll need both hands. I always do.
