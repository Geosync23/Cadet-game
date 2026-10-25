@arc teague
who: teague-theo
// "The last page" (content/arcs/outlines.md, Crew stories, C). SW2. Theo leaves on Day 21 (the Heron, the 15:00
// Tern); nothing here changes that. Blunt, quick, comic-strip beats (set-up, pause, punchline), never mean. Calder is
// a very tidy cloud; the playlist is always one song too long. needs: cheer (his voice card), so cheer replies get the
// warmer answer. His reason (new canon): eight stations before he was fourteen, always the new kid; he draws people so
// he gets to keep them; he leaves before a place gets used to him. Not used: transfer lists, his aunt, exams.
// Window Day 3 to Day 21, so the gates are lower than the defaults (each beat says).

== beat 1
// DAY: from 3 (may open in week 1)
when: day:3-
tone: light
tier: acquaintance
metDays: 1
where: Junior common room
hint: Oi. The comics wall. Go and look. I'll pretend I'm not watching.
mem: newone
them: New strip on the wall. Three panels. It's called "The New One". Go on.   [gesture]
them: Small figure. Big kitbag. Wrong spanner. It's you, before you ask.
them: It's a kind one. I don't do the other kind. Never have.
them: Panel two, you ask Calder for help. She's up in the corner. Very tidy cloud.   [laugh]
them: Panel three, you get it right. Everyone in panel three looks very surprised. Mostly you.
? choice
* It's brilliant. Can I have a copy?   flavour:cheer mem:copy
  them: No. The wall gets it first. You get a copy when you're famous.
  + them: Ha. No. Wall first. You get a copy when you're famous. Or when I'm gone. Whichever comes first.
* Why the wrong spanner?   flavour:listen mem:spanner
  them: Everyone's first week is the wrong spanner. Mine was. It's the law of comics.
* I did grab the wrong spanner. Tuesday. Don't tell anyone.   flavour:share mem:confessed
  them: Too late. It's on a wall. That's the trouble with walls.
them: Right. My tea's gone cold. That's not a comic. That's just sad.

== beat 2
// DAY: 3-21
when: beat:teague.1 day:3-21
// FAVOUR theoCloud (new): carry the smiling-cloud page to Calder's glass office; calder: Hm. Accurate.
tone: light
metDays: 4
where: Tea corner
hint: Need you for ten minutes. Sitting still. One of us has to manage it.
mem: cloud
them: Sit there. Chin up. No, your chin. Mine won't keep still. That's why I need yours.   [gesture]
them: Ten minutes. I've never managed ten minutes. I timed myself once. Four.
them: Done. Look. You, fixing the kettle. You look very serious. The kettle looks worried.   [laugh]
them: Want to see a thing? Nobody's seen it. Not Hart, not Abara. Here.
them: Calder. The tidy cloud. Only she's smiling. I saw it once. The board went green on a Friday. Three seconds.
them: I want her to have it. I can't hand it over. I got as far as her door once. Then I drew the door.   [sigh]
? choice
* I'll take it to her. You don't have to come.   flavour:practical favour:theoCloud mem:carried
  them: Would you? Don't say it's from me. She'll know. Say it anyway.
* That's her exactly. That's the three seconds.   flavour:listen mem:exactly
  them: Yeah. That's the hard bit. Drawing a smile on someone who saves them up.
* Give it to her at Friday tea. Make a show of it.   flavour:cheer mem:show
  them: A show. With Calder watching. She'd time my speech. I'd lose.
  + them: Ha. Picture it. Me, one page, the whole tea corner. She'd time my speech. I'd lose. Worth it, though.
them: Right. Cloud back in the folder. Folder under my arm. Arm back to work.

== beat 3
// DAY: 3-21, after Day 7 (Crossing the Line) if possible; evening
when: beat:teague.2 day:3-21
tone: heartfelt
tier: colleague
metDays: 7
where: Bow lounge
hint: Bar's quiet. Come and be quiet with me. I'll talk. You do the quiet bit.
mem: eight
learn: Theo moved stations eight times before he was fourteen. He draws people so he gets to keep them.
them: Blunt version first. I'm going. The Heron, on the twenty-first. Papers signed.
them: Long version. Eight stations before I was fourteen. Always the new kid. Every single time.
them: You get good at it. First week, you draw everyone. Then you've got them, whatever happens.
them: Here's the punchline. Ready? I like this ship.   [sigh]
them: Which is exactly when you go. Before it gets heavy. Before they get used to you.
? choice
* Go on. I'm listening.   flavour:listen mem:listened
  them: That's it, mostly. Eight stations, one kitbag, a lot of pencils. And now a ship I like. Annoying.
* Eight stations. That's a lot of comics walls.   flavour:cheer mem:walls
  them: Eight walls. Every page is in a box under my bunk.
  + them: Ha. Eight walls. All of it's in a box under my bunk. You'll go in the box. Near the top.
* I know being the new one. Not eight times. But I know it.   flavour:share mem:shared
  them: Yeah. You did it well, too. I watched. For the comic. Purely professional.
them: Right. That got heavy. See? This is what I mean.   [laugh]

== beat 4
// DAY: 18-20 (Day 20 is his farewell supper, Saturday 18:00 in the mess: the best place for it if the engine allows)
tone: heartfelt
tier: colleague
gapDays: 2
where: calm
when: beat:teague.3 day:18-20
hint: I need an editor. Five minutes. You're it. No pay.
mem: lastpanel
them: The Wren strip. Three months of it. Every panel's done but one. The last one.   [gesture]
them: I've drawn it six ways. All rubbish. Seven, with the one where the cloud cries. I don't count that one.
them: You pick. New hands see a place properly. Old hands just see the kettle.
them: So. What goes in the last panel?
? choice
* Me at the beam, with my name on it.   flavour:share mem:beam
  them: Big letters. You'll be the first name I've finished on this ship.
* The whole tea corner, on a Friday.   flavour:cheer mem:tea
  them: The whole lot. Calder, the mug rack, Halloran halfway through a joke. Big panel. I'll draw small.
  + them: The whole lot. Calder, the mug rack, Halloran halfway through a joke. I'll draw very small. Ha. That's the one.
* The Wren from outside. Small, and all lit up.   flavour:listen mem:wren
  them: From outside. Like from the Tern's window. Yeah. That's how I'll see her on Sunday.
them: Done, then. The strip's finished. Huh. I thought I'd like that more.   [sigh]

== beat 5
// CRESCENDO rides on: his send-off, the shuttle bay, 14:30-15:00 (he boards the 15:00 Tern); day: 21; cast: teague-theo, pell, torres-zeke; quiet ending: beat 6
// It's also his goodbye: the builders use it instead of his ordinary goodbye moment.
tone: resolution
tier: colleague
gapDays: 0
where: Shuttle bay
when: beat:teague.4
crescendo: farewell
quiet: 6
title: Theo's send-off
invite: Last day | The Tern goes at three tomorrow. Shuttle bay, half two. Pens packed last. Come and wave. Properly, with the whole arm. Theo
hint: Shuttle bay, half two. Don't be late. I'm never late for leaving.
mem: framed
keepsake: the last page of the Wren strip, signed, with you in it
them: There you are. Good. I had a speech. I drew it instead. Easier.   [gesture]
them > you: Here. The last page. Careful, the ink's two hours old.
them: Last panel's the one you picked. Look.
if mem:moment.teague.beam | them: Last panel. You at the beam, your name in big letters. Biggest letters I've got.
if mem:moment.teague.tea | them: Last panel. The tea corner on a Friday. Halloran mid-joke. Calder not laughing. Nearly.
if mem:moment.teague.wren | them: Last panel. The Wren from outside, every window lit. You're in the third one along.
them: Finished it. Don't frame it.   [nod]
them: Frame it.   [laugh]
if here:pell | pell: He drew me with a sandwich. Every panel. Every single one.   [laugh]
if here:torres-zeke | torres-zeke: Your new ship's lucky. Tell her coils I said hello. They'll know.
them: New ship, new playlist. Done. Fifteen songs. One too long. Obviously.
? choice
* I'll frame it. Promise.   flavour:cheer mem:promise
  them: Good. Somewhere Calder walks past. She'll straighten it.
  + them: Good. Hang it where Calder walks past. She'll straighten it every time. That's how you'll know she likes it.
* It was good, having you here.   flavour:listen mem:goodhere
  them: Don't. Yeah. You too. Stop it now, or I'll miss the Tern on purpose.
* Draw me a page from your new ship?   flavour:practical mem:heronpage
  them: First week. I'll draw everyone. Then a page for you, with a very small cloud in the corner. For the Chief.
them: Right. Ramp's down. That's me.   [nod]
them: Oi. From up here you all look very small. Good panel, that.   [gesture]
them: Laters, {me}. Don't do anything I'd draw.

== beat 6
// QUIET ENDING for beat 5: plays only if beat 5 was missed (Day 21 evening, the page on your bunk; he has gone)
tone: light
tier: colleague
gapDays: 0
where: visit
when: beat=teague.4
hint: Left you something on your bunk. Mind the ink.
mem: page
keepsake: the last page of the Wren strip, signed, with you in it
mail: 4320 | From the Heron | Day three, new ship. New kid: me. Wrong spanner: mine. Their Chief isn't a cloud. More of a hedge. A friendly one. I keep drawing a tidy cloud in the corner of every page anyway. Tell Calder. Don't tell her. Tell her. T.
them: You weren't at the bay. Fine. Drew you anyway.
them: That's the last page of the Wren strip. The last panel's yours. You'll know which.
them: Frame it. Don't argue. I can't hear you from out here.
them: Playlist's with O'Neill. Under protest. Fifteen songs. You know the rest.
them: Laters. T.
