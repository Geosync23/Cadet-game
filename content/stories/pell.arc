@arc pell
who: pell
// Writer-commons, arc batch. From content/arcs/outlines.md, "4. Pell Okafor". Beats 1-4 are already in the game
// (STORY_ARCS.pell: the screw-tin music box, the swap-meet one, the show, who came). Pell's card: needs cheer.
// Crew stories (SW1, 2026-10-24, from outlines.md "A. Pell Okafor"): beats 5-6 kept word for word; beat 7 is the
// big scene (the practical, in the Works bay); beat 8 its quiet ending; beat 9 the afterglow (was beat 8). His mum's stiff hands
// are getting older, not illness. A line starting "if <conditions> |" plays only when they hold (for the builders).

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
// The big scene, as a moment in the Works bay on a weekday afternoon, Days 17-24 (FX21's first runs, 2026-10-25: Pell
// can't get a seat at the open-door tea corner, so it no longer rides on it). Parked from the crescendo version:
//   when: beat:pell.6 trad:open-door weekday:wed day:17- / crescendo: trad:open-door / cast: calder halloran-emeka kovac-zainab
//   title: Pell's practical / invite: The practical | Tomorrow. Open door tea, the bench in the Works bay, 16:40.
//   Calder's timing it. Stand where I can see you. Pell
// quiet: 8 stays: if Day 24 passes without it, beat 8 (the quiet ending) comes next.
// Not on the comet's Monday (Day 22, FX25; EP1's events-plan-2 A5): Raman's big moment has that day to itself.
tone: resolution
tier: friend
gapDays: 2
duty: true
where: Works bay
when: beat:pell.6 time:afternoon day:17-24 !event:comet.warning
quiet: 8
hint: It's today. The practical. Stand where I can see you. Not too close.
mem: passed
flag: pell.certified
calder: Pump on the bench. Twelve bolts, one impeller, two seals. Strip, inspect, rebuild. The clock starts when you touch it.
pell: Right, so. Hands clean. Spanners in order. Nobody breathe. No, do breathe. Just quietly.   [laugh]
if here:halloran-emeka | halloran-emeka: I'm not watching. I'm stood here with my tea, facing this way. That's all. Lovely tea.   [laugh]
if here:kovac-zainab | kovac-zainab: Seven. Eight. Um. Sorry. I count. Nine.
calder: Four minutes ten.
pell: Impeller's out. Seals are good. That's a lovely seal, that. Look at it. No, don't. I'm busy.
if here:kovac-zainab | kovac-zainab: Bolt. The edge. Oh. Oh no. Stopped. It stopped.   [sigh]
if !here:kovac-zainab | pell: Bolt's rolling. The edge. Oh no. Oh. It stopped. It stopped.   [sigh]
if here:torres-zeke | torres-zeke: Properly, Pell. Properly.   [nod]
calder: Nine minutes twelve. Hands off.
calder: Good. Clean work.   [nod]
pell: I. Hang on. Give me a second. All my words have gone somewhere.   [sigh]
pell: Right. While you're here. I'm staying. On the Wren. I've told Mum. In writing, so she can't argue till Sunday.
pell: And the lad two doors down from her shop is learning the radios. By message. One step a week. He mended his first on Monday.
if mem:moment.pell.timed | pell: And {me} timed me. Every evening, in the machine shop. Every single run. That's half of this, right there.
if mem:moment.pell.help | pell: The lad was {me}'s idea, by the way. Credit where it's due. It's due over there.
if here:halloran-emeka | halloran-emeka: Oh, that wants biscuits. I'd say that wants a lot of biscuits.
? choice
* Told you. Every bolt, in order.   flavour:cheer mem:knew
  pell: You did. Every night. I kept not believing it. You win, {nick}.
  + pell: You did. Every single evening. Right. One day I'm saying it about you, in front of this lot. Watch me.   [laugh]
* Tell us about the bolt that stopped.   flavour:listen mem:bolt
  pell: It rolled. Right to the edge. I watched my whole career go with it. Then it just sat there. Somebody gasped.   [laugh]
* Sit down before your knees go. I'll pour.   flavour:practical mem:pour
  pell: Knees. Yes. They were fine for nine minutes and now they've gone. Cheers. Two sugars. Three.
calder: Sign the card on my desk tomorrow. Today, tea.
pell: Certified. Me. Somebody fill my mug. Then fill it again. Then point me at the biscuits.   [laugh]

== beat 8
// QUIET ENDING for beat 7: plays only if beat 7 was missed (it still happened: certified, staying)
tone: light
tier: friend
gapDays: 2
when: beat:pell.6
hint: Where were you? No, don't tell me. Sit down. I've got news.
mem: missedit
flag: pell.certified
mail: 20 | PASSED | PASSED. Capitals. Calder said "Good. Clean work." I'd like it on a mug, please. Pell
them: Oi oi. You missed it. Doesn't matter. I'll do it again for you. Not the pump. The telling.   [laugh]
them: Nine minutes twelve. One bolt rolled to the edge of the bench and stopped. Just stopped. Kovac nearly sat on the floor.
them: Then Calder looked at the pump for ages. Ages. And said, "Good. Clean work."
them: I passed, {nick}. Then I told the whole bay I'm staying. And the lad by Mum's is learning the radios.
? choice
* I'm sorry I missed it. Tell me again, slower.   flavour:listen mem:again
  them: Slower. Right. There's a pump. Twelve bolts. Guess how many I dropped. None. That's the whole story.   [laugh]
* I knew you'd pass. I'd have bet my pudding on it.   flavour:cheer mem:knew
  them: Your pudding? That's faith, that is. I'd have taken the bet and lost it happily.
  + them: Your pudding. That's proper faith. Cheers, {nick}. I'm having it anyway. Pudding's owed.   [laugh]
* Let's celebrate. Grab shelf. I'm buying.   flavour:practical mem:treat
  them: It's free. You can't buy it. I like the gesture though. Come on, before anyone counts the plates.   [laugh]
them: Certified. I keep saying it out loud. I'll stop by Friday. Probably.

== beat 9
// AFTERGLOW (was beat 8): plays after beat 7 or its quiet ending, beat 8
tone: resolution
when: flag:pell.certified
follows: 7|8
hint: Walk with me? I've just been on the booths. Big call.
mem: call
keepsake: a tiny music box made from spare screws, that plays four notes
learn: Pell passed Calder's practical in front of Works and he's staying on the Wren. A lad near his mum's shop is learning the radios.
them: I called Mum. A proper call, not a message. The relay held the whole way. Can you believe it?
them: Told her about the practical. Every bolt. She made me say the time twice. Nine minutes twelve.
them: Her hands were stiff today. She mended a kettle while we talked anyway. Course she did.
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
