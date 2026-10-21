@arc holt
who: holt
// Writer (command), from outlines.md section 9, "One bad day". His card's needs: practical (beat 3: listen and practical
// both fit, so both get a warmer answer). His distrust is his, about one day; never a word against the Veyli as a people.
// Hanne Rook (she/her, from the outline) only from beat 3. Envoy Saruth (she/her) speaks in beat 4.

== beat 1
tone: light
when: time:morning
where: meal
hint: Cadet. You're up. Walk with me. The long way.
mem: walk
learn: Chief Holt walks every deck before breakfast, the long way round, and sometimes takes you with him.
them: Nearest suit locker. Don't look.   [gesture]
? choice
* Behind the second door. On the left.   flavour:practical mem:locker
  them: Hm. Right. First time.
  + them: Hm. Right first time. Without looking. Adequate. More than adequate. Don't tell anyone I said that.   [nod]
* I've no idea, Chief.   flavour:share mem:noidea
  them: Honest. Better than a guess. Behind the second door. Learn it.
* Is this a test?   flavour:cheer mem:test
  them: Everything's a test. That's the Watch.   [laugh]
them: Come on. The long way. Every deck, every door.
them: Mensah told me a joke last night. Why did the airlock break up with the hatch? Too many seals.   [laugh]
them: Terrible. I laughed for a full minute. Don't tell him.

== beat 2
tone: light
when: deck:2
hint: Hm. You saw that. Come here, then.
mem: cord
learn: You caught Chief Holt re-tying the Envoy's door cord. He tied it properly, which means he learnt how.
them: The Envoy's cord came loose. I'm tying it back. Keeping an eye out. That's all.   [gesture]
them: There. Like that. Under, over, through, and back.
? choice
* You've tied that properly. You learnt how.   flavour:listen mem:learnt
  them: Hm. I watched. It's a door. I keep doors. That's the job.
* Shall I fetch the Envoy?   flavour:practical mem:fetch
  them: No. Hm. No need to make a thing of it.
  + them: No. Leave it. A thing done quiet is a thing done right. Good instinct, though.   [nod]
* Your secret's safe, Chief.   flavour:cheer mem:secret
  them: There's no secret. It's a cord. On a door. Move along.   [laugh]
them: Right. As you were. Both of us.

== beat 3
tone: serious
when: time:evening|night
hint: Cadet. Sit down. I've something to say, and I'll only say it once.
mem: badday
learn: Holt's patrol partner, Hanne Rook, was hurt when a Veyli ship went silent for six hours: a mourning rite. He knows it isn't fair.
them: Border patrol. Years back. My partner was Hanne Rook. Good officer. Better than me.   [sigh]
them: A rescue went wrong. Rook was hurt. Badly. There was a Veyli ship close by. We called them. They didn't answer.
them: Six hours of silence. Rook pulled through. Slowly. Left the service. We still write.
them: Years later I learnt the silence was a rite. Mourning. They couldn't answer. It wasn't a choice.
them: So I know. It isn't fair to hold it against the Envoy. Some days I hold it anyway. That's mine to fix.
? choice
* Thank you for telling me. I'm listening.   flavour:listen mem:listened
  them: Hm. You are. That's rare.
  + them: You are. Most people try to fix it. You just listened. That's rare. Thank you.   [listen]
* What would help? Is there anything I can do?   flavour:practical mem:help
  them: Not yet. Maybe. I'll know when I know.
  + them: Not yet. But you'd do it. I can see that. Hm. That helps more than you'd think.   [nod]
* Knowing it was a rite. Does that help?   flavour:share mem:knowing
  them: Knowing doesn't help as much as you'd think. Some. Not enough.
them: That's all. That's the bad day. Off you go. And cadet. Thank you.

== beat 4
tone: heartfelt
when: beat:holt.3 deck:2
where: any
hint: The Envoy's door. Hm. Stand with me a minute.
mem: tea
learn: Envoy Saruth invited Chief Holt to tea, through you. He went in, after standing at the door for some time.
mail: 90 | Tea | They kneel. My knees aren't built for it. They gave me a cushion. The tea was adequate. Holt
saruth: Ah. Cadet. Chief. Will you carry a message for me? To the Chief. Who is here.   [gesture]
saruth: The Chief is invited to tea. At my hour. Today.
them: Hm.
? choice
* I'll carry it. Chief, the Envoy invites you to tea.   flavour:practical mem:carried favour:holt.invite
  them: Hm. I heard. You heard. Everyone heard.
  + them: I heard. Carried properly, though. That counts. Right. Tea. Hm.   [nod]
* Go on, Chief. It's only tea.   flavour:cheer mem:onlytea
  them: Nothing is only tea. Not with the Veyli. That's what I'm worried about.   [laugh]
* Take your time. I'll stand here with you.   flavour:listen mem:stood
  them: Hm. Thank you.
saruth: The cord is tied loose, Chief. That means you are expected.
them: Right. Knees. Tea. I'm going in.   [sigh]

== beat 5
tone: resolution
when: beat:holt.4
hint: Cadet. Walk the long way with me. I've news. Don't make a fuss.
mem: abouttime
flag: holt.tea
keepsake: his old border-patrol whistle, which he says you'll never need
learn: Chief Holt wrote to Hanne Rook about the Envoy. She wrote back: "About time." He and the Envoy have tea every tenth day now.
them: I wrote to Rook. About the Envoy. About the tea.   [gesture]
them: She wrote back. Two words. "About time."   [laugh]
them: The Envoy and I have tea every tenth day now. I can tie three Veyli knots. I like the Envoy. There. Said it.
? choice
* I'm glad, Chief. Really glad.   flavour:share mem:glad
  them: Hm. So am I.
* Three knots? Show me one.   flavour:practical mem:knot
  them: Under, over, through, and back. That's the first. The other two are the Envoy's to teach.
  + them: Under, over, through, and back. Your hands are good. Take this. My whistle. You'll never need it. Keep it anyway.   [nod]
* Mensah's going to be unbearable.   flavour:cheer mem:mensah
  them: That's why you're not telling him.   [laugh]
them: Don't tell Mensah. He'll be unbearable.
