@arc halloran
who: halloran-emeka
// "Groaning means breathing" (content/arcs/outlines.md, Crew stories, G). SW2. Emeka Halloran stays aboard. Warm and
// unhurried; laughs before the punchline; "lovely"; always asks if you've eaten; never says no; never an unkind joke.
// needs: practical (his voice card), so practical replies get the warmer answer. The terrible jokes were his late
// dad's, who died some years ago (past grief, told gently, once, in beat 3); his mum on Coriel is well and writes every
// week. New canon: Dad's joke book, 412 jokes, numbered, in his hand; one every breakfast, never skip, never repeat.
// Not used: hospital, illness, letters read aloud, baking as the plot. Every joke here is new to the ship.

== beat 1
tone: light
where: meal
when: time:morning
hint: Morning, morning. I've a joke for you. You'll regret it. Sit.
mem: joke
them: Morning, morning. Sit down, sit down. Have you eaten? Good. Then you're strong enough.
them: Number two hundred and seventy-one. Ready? What's a spanner's favourite day of the week?   [gesture]
them: Torque-sday. Ha! Sorry. I laughed before I got there. I always do.   [laugh]
? choice
* That's dreadful.   flavour:cheer mem:dreadful
  them: Isn't it? Dreadful's the whole point. Dreadful is lovely.
* (Groan)   flavour:listen mem:groaned
  them: There it is. That's the noise. Lovely.
* Why number two hundred and seventy-one?   flavour:practical mem:number
  them: Because yesterday was two hundred and seventy. I keep count. Somebody has to.
  + them: Because yesterday was two hundred and seventy. I keep count, so nobody gets the same one twice. Tidy, isn't it?
them: That one's my dad's. They're all my dad's, really.
them: A hundred and forty-odd left. Then I'll have to write my own. Heaven help you all.   [laugh]

== beat 2
tone: light
where: Tea corner
when: beat:halloran.1
hint: Got a minute by the mug rack? I've something to show you. It isn't a scone.
mem: notebook
them: Here. Careful with it. The spine's held on with tape and hope.   [gesture]
them: My dad's joke book. Four hundred and twelve of them. All numbered, all in his hand.
them: Look how the writing goes. Neat at number one. By four hundred you can't read it. The jokes get worse too.   [laugh]
them: He had rules. One a day. Never skip one. Never tell the same one twice.
them: And when the whole table groans? "Groaning means they're breathing." That was his.
? choice
* He sounds like a lot of fun.   flavour:listen mem:fun
  them: He was. Loud, mostly. You'd hear him a deck away.
* Can I read one?   flavour:cheer mem:readone
  them: Number thirty. "What's brown and sticky? A stick." He laughed at that one for a week.
* Do you keep it somewhere safe?   flavour:practical mem:safe
  them: Biscuit tin, top shelf in my cabin. Then down to breakfast every morning, in my pocket.
  + them: Biscuit tin, top shelf. Every morning it comes to breakfast in my pocket, every night it goes home. Safest book on the ship.
them: Right. Back in the pocket. Have you had a biscuit today? Have one. Go on.

== beat 3
tone: heartfelt
where: Hydroponics garden
when: beat:halloran.2 time:evening
// FAVOUR emekaJokes (new): ask Yoon, Lemaire and Yilmaz for one terrible joke each (three short stops); done sets flag:halloran.jokes.done
hint: Walk round the garden with me? The tomatoes won't mind. I'd like the company.
mem: quiet
learn: Emeka's breakfast jokes are his late dad's: four hundred and twelve, numbered, in a book he carries every day.
them: Dad died a few years back. It was peaceful. I'm all right about it. Mostly.
them: He filled a room, my dad. You always knew which room. You could hear the groaning.   [laugh]
them: After, nobody groaned at breakfast any more. So I kept telling them. Somebody had to keep them going.
them: I send Mum one every week. She says they're not the same written down. You need the groan.
them: She says the kitchen's too still without it. She says it kindly. She says everything kindly.   [sigh]
? choice
* What if she heard a whole table groan?   flavour:practical favour:emekaJokes flag:halloran.jokes mem:table
  them: A whole table? Oh, she'd love that. But I couldn't ask people for jokes. Could I?
  + them: A whole table, groaning. Oh, she'd love that. I couldn't ask anyone. You'd do the asking? Ah, you're a treasure.
* So he's there every morning, at breakfast.   flavour:listen mem:mornings
  them: Every morning. And when I get to four hundred and twelve, I'll start again at one.
* Our house is never quiet. I miss that, here.   flavour:share mem:noisy
  them: Ah, then you know. A home wants a bit of noise in it. Ours had Dad.
them: Look at me, going on. The tomatoes have heard it all before. Have you eaten tonight?

== beat 4
tone: light
tier: friend
gapDays: 2
where: calm
when: beat:halloran.3
hint: Could I ask you something? It's a bit silly. Well. It's very silly.
mem: laugh
them: I don't ask people for things. You'll have noticed. I'm the one who says yes.
them: But I'm asking. I'm nearly at number two hundred and eighty-nine. It was Dad's favourite.
them: It's awful. The worst in the book. He told it on my birthday every year, and Mum groaned like a door.   [laugh]
them: Will you laugh? Properly. Even if it's dreadful. Especially if it's dreadful.
? choice
* I'll laugh. Promise.   flavour:listen mem:promise
  them: Not a polite laugh, mind. A proper one. From the boots.
* What if I groan instead?   flavour:cheer mem:groaninstead
  them: Even better. Dad would say that's the best laugh there is.
* I'll get there early and save you a seat.   flavour:practical mem:seat
  them: Ah. Nobody saves me a seat. I'm usually the one saving them.
  + them: Would you? Nobody saves me a seat. I'm always saving everyone else's. Oh, that's lovely. That's done me good.
them: There. That's me asked. It wasn't so bad. A bit like pulling a tooth.   [laugh]

== beat 5
// CRESCENDO rides on: breakfast at the Works tables (a weekday); day: from 15; cast: halloran-emeka, pell, yoon-elif, lemaire-nils, yilmaz-karin (if you collected their jokes), else kovac-zainab, torres-zeke; quiet ending: beat 6
// DAY: from 15
tone: resolution
tier: friend
gapDays: 0
where: meal
when: beat:halloran.4 time:morning day:15-
crescendo: meal:breakfast
cast: pell
quiet: 6
title: Breakfast with Halloran
invite: Number 289 | Breakfast tomorrow, the Works tables. A big one. Don't be late, and bring your best laugh. You'll need it. E.
hint: Breakfast? Works tables. It's a big one today. Number two hundred and eighty-nine.
mem: groan
mail: 4320 | From Coriel | Mum's written. She played it twice. She laughed till she cried, the good kind. The kitchen was loud all evening, she says. She's sending one back and won't say which. Have you eaten? E.
them: Morning, morning. Right. Is everyone settled? Number two hundred and eighty-
pell: Oi oi. Not today, Emeka. Today you're the audience. {me}, is it recording? Good.   [gesture]
if flag:halloran.jokes.done here:yoon-elif | yoon-elif: Sorry. Before you start. Why did the patient climb the ladder? I said take it one step at a time. Oh, I'm sorry.
if flag:halloran.jokes.done here:lemaire-nils | lemaire-nils: Why do stars never pay for tea? They're always out. That's two points to me.
if flag:halloran.jokes.done here:yilmaz-karin | yilmaz-karin: Why did the loaf join Works? It wanted to rise through the ranks. Treaty terms permitting.
if !flag:halloran.jokes.done | pell: Why don't pumps keep secrets? They always leak. Thank you, thank you.
if !flag:halloran.jokes.done here:kovac-zainab | kovac-zainab: Um. Why was the scrubber sad? It was a bit run down. That's it. That's the joke. Sorry.
if !flag:halloran.jokes.done here:torres-zeke | torres-zeke: What do you call a coil that tells jokes? Current comedy. Shocking, I know. Right, onward.
them: Oh, dear me. Oh, they're terrible. Stop. No, don't stop.   [laugh]
them: I can't. I can't breathe. Groaning means breathing, and I'm doing both.   [laugh]
them: Right. Fair's fair. Number two hundred and eighty-nine. How does the Wren say hello?
them: Hull-o.   [gesture]
them: Listen to that. The whole table, like one long note. Dad would be beside himself.
? choice
* (A long, loud groan)   flavour:cheer mem:biggroan
  them: That's the one. Mum'll hear that on Coriel without the recording.
* Here's one for your mum. What's a ship full of groaning? The Wren at breakfast.   flavour:share mem:yourjoke
  them: Ha! That's dreadful. That's perfect. Mum'll tell that one to the neighbours for a month.
* Let's send it to her now, while it's warm.   flavour:practical mem:sent
  them: Now? Yes. Off it goes. Coriel's a long way, but it'll get there groaning.
  + them: Now? Yes, let's. Off it goes, groans and all. You think of everything. Have you eaten? You have. Course you have.
them: Thanks ever so. Every one of you. Number two hundred and ninety's tomorrow. You've been warned.   [laugh]

== beat 6
// QUIET ENDING for beat 5: plays only if beat 5 was missed (Yoon got the table going anyway)
tone: light
tier: friend
gapDays: 0
where: calm
when: beat=halloran.4
hint: Oh, you missed a morning. Sit. You'll want all of it.
mem: missed
mail: 4320 | Coriel | Mum's had the recording. She says she laughed so much she had to sit on the stairs. She's sending one back. She says it's a good one. It won't be. E.
them: You missed a morning. Oh, you missed a morning.   [laugh]
them: Yoon had the whole table going before I'd sat down. One joke after another. I groaned myself hoarse.
them: Then I told two hundred and eighty-nine, and they all groaned at once. You'd have heard it on Deck 3.
them: Yoon recorded it for Mum. She's had it already. Lovely.
them: Don't look sorry. There's always tomorrow. Number two hundred and ninety. It's worse.   [laugh]

== beat 7
// AFTERGLOW: a breakfast a few days after beat 5 or its quiet ending (beat 6)
tone: light
tier: friend
gapDays: 2
where: meal
when: time:morning
follows: 5|6
hint: Breakfast? Mum sent one back. I've been holding it in since six.
mem: fromMum
keepsake: a scone tin with a dent in the lid
them: Morning, morning. Sit. Mum's sent one back. Her first ever. I've written it in the back of the book.
them: Number four hundred and thirteen. Her handwriting, next to his. Look at that.   [gesture]
them: Ready? Why do birds fly south? Because it's too far to walk.
them: It's the worst yet. She's very proud. I groaned so loud Brennan came out of the galley.   [laugh]
them: And this is for you. My scone tin. Don't ask about the dent. Long story, short drop.
? choice
* Your dad would've loved that one.   flavour:listen mem:loved
  them: He'd have pinched it. Told it every day for a week. Then said it was his.   [laugh]
* I'll bring the tin back full.   flavour:practical mem:refill
  them: You'll do no such thing. Well. If you insist.
  + them: Will you? Oh, that's how it works, isn't it. A tin goes round. Lovely. I'll eat whatever's in it.
* That's terrible. Tell me another.   flavour:cheer mem:another
  them: Tomorrow. One a day. Rules are rules. His, and mine, and Mum's now.
them: Right. Have you eaten? You have now.
