@arc rina
who: rina
// Writer-commons, arc batch. From content/arcs/outlines.md, "5. Rina Deshi". Beats 1-4 are already in the game
// (STORY_ARCS.rina: Gran's Tiles, Gran in hospital, two days without news, Gran home and cheating). Rina's card:
// needs cheer. She never says how she feels straight out; she stays dry even in beat 7.

== beat 5
tone: light
when: beat:rina.4
hint: Make yourself useful. Sit down and pick a journal.
mem: quiz
them: You caught me. I'm reading the pillow. Don't tell anyone. It ruins the effect.
them: Quiz me. Any page. And if you say "easy" I'll beat you at Tiles for a month.
them: Bet you a game I can't name three bones of the hand. Go on. Take the bet.
them: Scaphoid, lunate, triquetral, pisiform, trapezium, trapezoid, capitate, hamate. That's the wrist. I'm warming up.
them: Five metacarpals. Fourteen phalanges. Twenty-seven. Honestly. You owe me a game.
? choice
* That was brilliant. Properly.   flavour:cheer mem:brilliant
  them: It was all right. It was quite good. Fine. It was brilliant. Don't make it a thing.
  + them: Ha. Fine. It was. Same time tomorrow? I've got a whole journal on lungs, and you've got no excuse.
* Why do you know all this?   flavour:listen mem:why
  them: I want to be a ship's doctor. One day. Don't look at me like that. Drink some water.
* I'll quiz you again. Any time.   flavour:practical mem:again flag:rina.quizzes
  them: Careful. I'll hold you to that. I hold everyone to everything.

== beat 6
tone: heartfelt
when: beat:rina.5
hint: Talk to me about something stupid. Anything. Go.
mem: nextquarter
them: My sister's sent another exam date. The qualifying exam. She sends one every quarter. Like a dentist.
them: I've said "next quarter" four quarters running. The infirmary's busy. Very convenient, the infirmary.   [sigh]
them: If I sit it and fail, she was right. About me. About all of it. And I'm not doing that again.
them: I'm not scared. I'd just rather not. There's a difference. There isn't. Don't say anything.
? choice
* Anyone who names every bone in the hand for a bet isn't failing anything.   flavour:cheer mem:bones
  them: Twenty-seven, hand and wrist. Get it right if you're going to flatter me.   [laugh]
  + them: Twenty-seven. Ha. You're all right, you. Fine. I'll look at the date. Look. Not book.
* "Again"? You said "again".   flavour:listen mem:again
  them: Did I. Hm. Long story. A hard year, at home. Another time. Not tonight.
* Dr. Nandakumar would help you get ready. I could ask her.   flavour:practical mem:nandakumar
  them: Don't you dare. ...She might, though. Let me think about it.
them: Right. Enough of that. Tiles. I need to beat someone.

== beat 7
tone: resolution
when: beat:rina.6
hint: Walk with me. I've done something. Don't make a fuss.
mem: booked
flag: rina.exam
keepsake: a Tiles piece, the one her gran always cheated with
learn: Rina's booked the qualifying exam at last. The year before the Wren, she held everything together at home.
mail: 4320 | First part | Passed the first part. Don't make a fuss. Fine. A small fuss. Rina
them: I've booked it. The exam. It's in the calendar. I can't take it back. I checked. You can't.
them: Nandakumar's sitting with me for it. She says she'll bring biscuits. I said that's not how exams work. She said it is now.
them: I told Gran. Do you know what she said? "Cheat if you have to." She meant every word.   [laugh]
them: The year before the Wren, everything at home went wrong at once. All of it. And I was the one holding it together.   [sigh]
them: I didn't sleep for about a year. Then I came here, and someone said "drink some water", and I did. Stupid. It helped.
them: That's it. That's the whole story. I've told it once. That's my limit.
? choice
* Thank you for telling me.   flavour:listen mem:told
  them: Don't. You'll make me nice. Nobody wants that.
* You're going to be a brilliant doctor. Honestly.   flavour:cheer mem:doctor
  them: "Honestly." Steal my word, would you. ...Thanks.
  + them: Using my own word against me. Fine. Thank you. Really. Don't tell anyone I said "really".
* I'll quiz you every night till then.   flavour:practical mem:quiznight
  them: Every night. Lungs first. Don't be late.
them: Take this. Gran's Tiles piece. The one she cheats with. For luck. Don't you dare use it against me.
