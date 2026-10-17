@arc brennan
who: brennan
// Writer-commons, arc batch. From content/arcs/outlines.md, "6. Chef Auda Brennan". A new arc: beat 1 is a moment.
// Brennan's card: needs share. Her days off are Friday and Saturday (Lukas covers), so "Fridays" in beat 1 is Lukas
// cooking to her recipe. The fire: nobody was hurt, said firmly. Nell Arrowby and blue sage only from their beats.

== beat 1
tone: light
duty: true
hint: Come here, love. I need something from you. It won't hurt.
mem: book
them: Sit down, love. No, there. I've a question and I want a proper answer.
them: This is my book. Everyone aboard's in it. Their favourite dish. Holt's is in here. He'll never know I know.
them: What's yours? Your real favourite. Not the polite one. The one you'd want on a bad day.
? choice
* Something from home. The one my family makes on rest days.   flavour:share mem:home
  them: Then that's what goes in. I'll find out how they make it. I have ways.
  + them: Oh, love. The home ones are the best ones. Tell me every bit of it. I'm writing it down and underlining it twice.
* Honestly? Whatever you're cooking tonight.   flavour:cheer mem:tonight
  them: Flatterer. Good answer, though. Wrong, but good.   [laugh]
* Why do you keep a book like that?   flavour:listen mem:why
  them: Because everyone's a long way from home, love. A plate's the quickest way back.
them: There. Underlined twice. Fridays. Lukas does it, to my recipe. Don't tell anyone, they'll all want one.

== beat 2
tone: light
duty: true
when: beat:brennan.1
hint: Taste this. No, properly. Tell me what's wrong with it.
mem: sage
them: Taste. Go on. Mind, it's hot.
them: It's my mother's soup. I've made it ninety times on this ship and it's never been right. Not once.
them: It needs blue sage. A little grey-green leaf. Smells like a warm cupboard. The garden doesn't grow it.
them: I've tried without. Ninety times. You can taste the gap.   [sigh]
? choice
* I'll ask Tove Cruz about growing some.   flavour:practical mem:askedcruz favour:brennanSage flag:brennan.sage
  them: Would you? Tove won't say no to you. Tove says no to me. Politely. With a lot of soil.   [laugh]
* It tastes lovely to me.   flavour:cheer
  them: Bless you. You're wrong. But bless you.
* Tell me about your mother's cooking.   flavour:share mem:mother
  them: She taught me to cook by ear. A pan tells you everything, she says, if you'll only listen.
  + them: She taught me to cook by ear. Sings to her pans. I don't sing. The pans are relieved. Sit, love, I'll tell you.

== beat 3
tone: heartfelt
when: beat:brennan.2
hint: Stay a minute, love. The pans are put away. It's only me.
mem: fire
them: Got a letter. From Nell Arrowby. Old friend. She's got a restaurant on Hesper Dock, and she's offering it to me.
them: I had a place once. On Port Halloran. Twelve tables and a window on the harbour. I loved it.
them: There was a fire. In the kitchen. Late, on a busy night.   [sigh]
them: Nobody was hurt. I made sure of that. I counted them out the door. Twice.
them: After, I couldn't cook somewhere quiet. I needed a galley. Order. Seventy-five people who all eat at six.
them: And now Nell's offering me twelve tables again. And I don't know what I want.
? choice
* You counted them out twice. That's who you are.   flavour:listen mem:counted
  them: Once for them. Once for me. I still count, you know. Every dinner. Seventy-five.
* I'd eat at any restaurant of yours.   flavour:cheer mem:restaurant
  them: You eat at one every night, love. It's just got trays.   [laugh]
* I had a bad night once too. Want to hear it?   flavour:share mem:shared
  them: Go on. I'll put the kettle on.
  + them: Go on, love. The kettle's on. Tell me, and then I'll know you a bit better, and you'll know me. That's fair.
them: Thank you for sitting. I don't say that to many. Off you go. Eat something.

== beat 4
tone: heartfelt
gapDays: 2
when: beat:brennan.3
hint: I've cooked something. I need an honest mouth. Yours will do.
mem: tasting
them: Sit. Spoon. This is the first dish on the menu I'd serve on Hesper Dock.
them: I'm doing one a week. Honest verdict, love. If it's bad, I want to hear "bad".
them: The thing is, I don't know if I'm saying goodbye to it, or hello.
? choice
* It's wonderful. And it tastes a bit like goodbye.   flavour:listen mem:goodbye
  them: Does it? Hm. Maybe it does. Maybe that's the seasoning.
* Can I have seconds? That's my verdict.   flavour:cheer mem:seconds
  them: That's the only verdict a cook ever wants. Here.   [laugh]
* My family has a dish like this. Can I tell you about it?   flavour:share mem:family
  them: Go on.
  + them: Go on, love, tell me. I'll steal it. Cooks are thieves. The good ones, anyway.
them: Same time next week. Bring the same mouth.

== beat 5
tone: resolution
when: beat:brennan.4
hint: Dinner tonight. Soup. Don't ask why. Just come and eat it.
mem: soup
keepsake: a page from her book of favourite dishes, with yours on it
learn: Brennan ran a restaurant on Port Halloran until a fire (nobody was hurt). She turned Nell Arrowby down to stay.
them: Sit down, love. Eat that. Don't talk. Eat.
them: Blue sage. Tove grew it. Two weeks of fussing over one little pot. It's right. It's finally right. My mother's soup.
them: I've served it to the whole mess. Didn't tell anyone why. They don't need to know why. They just need to eat.
them: I wrote back to Nell. I said no.
them: My kitchen's here. It's got seventy-five people in it. And one of them's you.
? choice
* I'm so glad you're staying.   flavour:listen mem:staying
  them: Me too, love. Now eat. It's going cold, and I've waited ninety-one goes for this.
* Best soup on the Wren.   flavour:cheer
  them: Best soup in a good many places, love. Don't tell Nell.   [laugh]
* Will you teach me to make it?   flavour:share mem:teach
  them: Course I will. By ear. You'll hate it. Then you'll love it.
  + them: Oh, love. Yes. By ear, the way my mother taught me. You'll get it wrong ninety times. Then you won't.
them: Here. A page from my book. Your dish, underlined twice. Keep it. I know it by heart.
