@arc pell
who: pell
// Writer-commons, arc batch. From content/arcs/outlines.md, "4. Pell Okafor". Beats 1-4 are already in the game
// (STORY_ARCS.pell: the screw-tin music box, the swap-meet one, the show, who came). Pell's card: needs cheer.

== beat 5
tone: light
when: beat:pell.4
hint: Right, so. I need someone with a watch. And no mercy.
mem: practical
them: Oi oi. Guess whose name Calder's put down for the certification practical? Go on. Guess. It's mine.   [laugh]
them: I'm thrilled. I'm also going to be sick. Both at once. Is that normal?
them: You strip a pump in front of her. Clean, in order, against the clock. She just watches. She doesn't blink.
them: Would you time me? Slower. No, faster. No, don't tell me the time. Actually, tell me.
? choice
* I'll time you. Every evening till you're sick of me.   flavour:practical mem:timed favour:pellPractice
  them: You're a legend. Machine shop, after shift. Bring biscuits. They're for my nerves.
* You've fixed half this ship. A pump's nothing.   flavour:cheer mem:cheered
  them: Half? Generous. A third. A good third.   [laugh]
  + them: Half! I'll take that. I'm going to think it really loudly at Calder while she watches.
* What's the worst that could happen?   flavour:listen
  them: I drop a bolt, it rolls under the bench, and Calder says "Hm." I'd never recover.   [laugh]
them: Right. Practise. Food first. Then practise.

== beat 6
tone: heartfelt
when: beat:pell.5
hint: Got a minute? I'm going to do a thing. I'd rather not do it on my own.
mem: messages
them: Mum's messages. The three. I'm going to open them. Now. With you here. Don't let me stop.
them: Eat. Sleep. Call. Ha. Same as ever. She's got it down to one word each.   [laugh]
them: There's a fourth. Her hands are getting stiff. She can't do the fine work on the radios any more.
them: She wants me home. To run the shop. Kettles, radios, coats, anything. Where I found my first engine manual.   [sigh]
them: If I go, I'm leaving this. If I stay, I'm leaving her. Either way I'm letting someone down.
? choice
* You don't have to decide tonight. I'm here.   flavour:listen mem:listened
  them: No. I don't, do I. Tonight I just have to know it. That's enough for one night.
* She raised a mechanic in a scrapyard. She'll understand.   flavour:cheer mem:mechanic
  them: She did, didn't she. With a manual with half the pages missing. Ha.
  + them: She did. A scrapyard and half a manual, and look at me. She made me, {nick}. She'll understand. Probably.
* Could someone at home help her for now?   flavour:practical mem:help
  them: There's a lad two doors down who's good with his hands. Maybe. I could teach him by message.
them: Right. I've opened them. That's the hard bit done. Is it? It feels like the hard bit.

== beat 7
tone: light
tier: friend
gapDays: 2
duty: true
where: Works bay
when: beat:pell.6
hint: Did you hear? Did you? Come here. Come here right now.
mem: passed
flag: pell.certified
them: I passed. I passed! The practical. Clean, in order, against the clock. Didn't drop a single bolt.   [laugh]
them: Calder watched the whole thing. Didn't blink. Then she said, "Good. Clean work." Good! Clean work!
them: I nearly cried at the board. In front of everyone. Halloran pretended not to see. Halloran's a gentleman.
them: Tea corner, now. I'm feeding everyone. I've raided the grab shelf. It's an emergency. A happy one.
? choice
* I knew you would.   flavour:cheer mem:knew
  them: You did, didn't you. You kept saying it. I kept not believing it. You win.
  + them: You did. Every single evening. I'm going to say it about you one day, {nick}. Watch me.
* Tell me everything. Every bolt.   flavour:listen
  them: Right, so. First bolt. Calder's looking at me. I'm looking at the bolt. The bolt's looking at nobody...   [laugh]
them: Certified. Me. Pell. Certified. Somebody pass me a biscuit before I fall over.

== beat 8
tone: resolution
when: beat:pell.7
hint: Walk with me? I've just been on the booths. Big call.
mem: call
keepsake: a tiny music box made from spare screws, that plays four notes
learn: Pell passed Calder's practical and he's staying on the Wren. He's helping his mum mend her shop's press by message.
them: I called Mum. A proper call, not a message. The relay held the whole way. Can you believe it?
them: I told her I'm staying. Here. On the Wren.
them: And I'm walking her through fixing the shop's old press. By message. One step a week. Like a proper apprentice.   [laugh]
them: She said: eat, sleep, call. Then she laughed. Then I laughed. Then we both cried a bit. Don't tell anyone that bit.
them: Can I tell you a secret? First month here, I nearly left. Bag packed. I'm glad every day I didn't.
? choice
* So am I.   flavour:cheer mem:glad
  them: Course you are. Who'd show you the panel that sticks?   [laugh]
  + them: Course you are. Who'd feed you? Who'd show you the panel that sticks? Who'd find you the good spanners?
* What changed your mind, back then?   flavour:listen mem:why
  them: Brennan gave me pudding and said nothing. Calder gave me a pump and said nothing. That's how this ship says stay.
* My first week, I nearly packed too.   flavour:share mem:shared
  them: Yeah? Look at us. Still here. Still unpacked. Well, I'm unpacked. You, I'm not sure.   [laugh]
them: Here. The smallest music box. Four notes. One each for eat, sleep, call. And one for you.
