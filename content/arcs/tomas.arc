@arc tomas
who: tomas
// Writer-commons, arc batch. From content/arcs/outlines.md, "3. Tomas Lind". Beats 1-4 are already in the game
// (STORY_ARCS.tomas: the star map, his brother's birthday call, the dropped call, his brother's star map).
// Tomas's card: needs listen, so the warmer answers sit on the listen replies.

== beat 5
tone: light
tier: friend
where: visit
when: weekday:wed time:evening|night
hint: Can I tell you something? Not a big thing. A medium thing.
mem: exam
them: Holt's inspecting tomorrow. I've folded my blanket four times. It looks worse every time.   [sigh]
them: How does a blanket get worse? I'm making it worse. I think it knows.
them: Can I tell you something? You can't tell anyone. Especially Holt. Especially especially Holt.
them: I failed the Watch exam. The first time. I passed the second time. Nobody here knows.
them: If Holt finds out, he'll think I'm the sort of person who fails things. I sort of am, a bit.
? choice
* Your secret's safe with me. Promise.   flavour:listen mem:promised
  them: Thank you. Really. Okay. Okay. Blanket, attempt five.
  + them: Thank you. I knew I could tell you. I don't know how I knew. I just did. Right. Blanket, attempt five.
* You passed. That's the one that counts.   flavour:cheer mem:passed
  them: That's what my brother says. He's very wise. He's also quite small.   [laugh]
* Want a hand with the blanket?   flavour:practical mem:blanket
  them: Would you? Corners are my weakness. Corners and exams.   [laugh]
them: Don't tell Holt. Did I already say that? I'm saying it again.

== beat 6
tone: heartfelt
when: beat:tomas.5 time:evening|night
hint: Got a minute? I've been reading something I probably shouldn't.
mem: list
them: There's a posting on the transfer list. A station near home. Two days from the farm.   [sigh]
them: I've read it about forty times. I nearly know it by heart.
them: Maybe I'm not built for out here. Everyone knows where everything is. I still take the long way round Deck 2.
them: What would you do? No, don't answer that. I want you to answer that. Sort of.
? choice
* I'm listening. What's pulling you home?   flavour:listen mem:listened
  them: My brother, mostly. And the grey sky. Isn't that silly? I left because of the grey sky. Now I miss it.
  + them: My brother. The sky. Knowing every path. You're good at listening, you know. I feel less muddled just saying it.
* You showed me round when you'd only been here a week.   flavour:cheer mem:showed
  them: I did, didn't I? I got the washroom wrong. But I did.   [laugh]
* Come to observatory night with me. Look at it from up there first.   flavour:practical mem:observatory flag:tomas.observatory
  them: Yes. Yes, all right. I'll bring the star map.
them: I haven't decided anything. I just needed to say it out loud to someone. Thanks for being the someone.

== beat 7
tone: resolution
where: calm
when: beat:tomas.6 trad:observatory-night
hint: It's clear tonight. Can I show you something? It won't take long.
mem: home
flag: tomas.meets
keepsake: a corner of his star map, with home marked in pencil
learn: Tomas failed the Watch exam once and told Holt in the end. He's staying, and he'll meet the next new cadet.
them: Look out there, past the edge of the window. That's home. Well, the star near home. Close enough.
them: I told Holt. About the exam. I walked into his office and said it, all at once, before I could stop.
them: He said, "I know. I read your file. You passed. That's the one I care about." And back to his paperwork he went.
them: I've taken the transfer list off my locker. I don't need it there. This is home too. Both of them are.
them: And I've asked to meet the next new cadet off the shuttle. Nobody should get lost on their own. I did. It was awful.   [laugh]
? choice
* You'll be brilliant at it.   flavour:cheer
  them: I'll get the washroom wrong. But I'll get them there.   [laugh]
* I'm really glad you're staying.   flavour:listen mem:staying
  them: Me too. You're a big part of why. You know that, right?
  + them: Me too. You're a big part of why. You were the first person here I didn't have to pretend with.
* Show me where home is again?   flavour:share mem:shown
  them: There. Just left of the bright one. No, my left.
them: Here. The corner of my star map. Home's marked in pencil. I want you to have it. I know where it is now.
