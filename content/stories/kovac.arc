@arc kovac
who: kovac-zainab
// "Four, please" (content/arcs/outlines.md, section 10). The Works writer, arc batch. Small, funny and kind. She
// tells the lift-club meetings (everyone rides the lift; they hold the rail) rather than staging them, so no other cast has to be present. needs: listen.
// The lift isn't admitted until beat 2. Marra Station's night is told only in beat 3.
// Crew stories (SW1, 2026-10-24, from outlines.md "E. Zainab Kovac"): beats 1-3 kept word for word. Beat 4 is the
// crescendo at the Deck 5 lift doors before the Friday address; beat 5 its quiet ending; beat 6 the afterglow, where
// her keepsake is now a knitted spanner grip (Zeke's is the only scarf). A line starting "if <conditions> |" plays
// only when they hold (for the builders).

== beat 1
tone: light
where: calm
hint: Oh. Hi. I'm a bit wobbly. It's nothing.
mem: ladder
them: Oh. Hi. Sorry. Bit wobbly. The lift, from Deck 5. I held the rail the whole way.
them: Tove Cruz was in it too. Eyes shut. They said, "Lovely lift." I said, "Lovely lift."
them: Then Davi Keane got in at Four. Both hands on the rail. "Lovely lift." Nobody said anything else.   [laugh]
? choice
* Lifts can be a lot.   flavour:cheer mem:verygood
  them: They can. Not that I. Um. It's a lovely lift. Yes.
* Do you not like the lift?   flavour:listen mem:askedlift
  them: It's fine. It's. Um. The rail's good.
  + them: It's fine. Mostly. Um. Ask me another day. I might tell you a thing. Maybe.   [sigh]
them: Anyway. Nine and a half minutes, the scrubber this morning. I timed it.

== beat 2
tone: light
when: beat:kovac.1
where: calm
hint: Can I tell you something? It's very small. Sorry.
mem: club
them: Can I tell you something? It's small. I'm afraid of the lift. There. Said it.
them: Not a lot. Just. All of it. The doors. The bit between floors.
them: Oh. Oh no. Cruz. And Keane. That's why they hold the rail like that.   [laugh]
them: We're a club. Oh no. We're a club. I'm delighted. That's awful. I'm delighted.
? choice
* Thank you for telling me. I won't say a word.   flavour:listen mem:keptsecret
  them: I know you won't. That's why I told you.
  + them: I know. That's why it was you. Thank you, {me}. Um. That's twice I've said thank you. Sorry. Three.   [laugh]
* The lift club. You need badges.   flavour:cheer mem:badges
  them: Don't. I'll knit them. You know I'll knit them.
them: Right. Back to the scrubbers. Scrubbers don't have doors.

== beat 3
tone: heartfelt
when: beat:kovac.2
where: calm
hint: Sit with me? I want to tell you the why. If that's all right.
mem: night
them: When I was small, on Marra Station, a lift stuck between floors. I was in it. On my own.
them: A whole night. Nobody came till the morning shift. The lights stayed on, at least.
them: I counted the bolts in the ceiling. There were a hundred and twelve. I counted them all night.   [sigh]
them: I'm fine. Really. I just don't like the counting. It starts again in there.
? choice
* That sounds so lonely. I'm glad you told me.   flavour:listen mem:listened
  them: It was. It's less now. Telling you made it smaller, somehow.
  + them: It was. It's smaller now. I didn't think saying it would do that. Thank you for sitting still for it.   [nod]
* We could service the lift's brakes together. You'd see how it works.   flavour:practical flag:kovac.liftjob favour:liftBrakes mem:brakes
  them: Inside it? Every bolt? Um. That's terrifying. And. Yes. I think yes.
* I'm scared of the reactor door. Not the same. A bit the same.   flavour:share mem:shared
  them: Everyone's scared of the reactor door. That's sensible. But thank you. It helps.
them: Right. That's enough of that. Tea? I'll walk. The long way.

== beat 4
// CRESCENDO rides on: the lift up to the Captain's Friday address (the Deck 5 lift lobby, about 15:50-16:00; the scene plays at the doors, before they ride); day: 19 (preferred) or 26; cast: kovac-zainab and you (Keane only if there: he's on nights; Cruz no longer in it, lead 36 for RV16, 2026-10-25); quiet ending: beat 5
tone: resolution
when: beat:kovac.3 weekday:fri trad:captains-address day:19-26
crescendo: trad:captains-address
quiet: 5
lead: 28
title: The lift with Kovac
invite: Friday | Before the address tomorrow. The Deck 5 lift lobby, {at}. Will you come? Sorry. I mean, please. Zainab
where: Lift lobby
hint: Walk with me? Just to the lift. Well. Into it.
mem: doors
flag: kovac.rode
them: Oh. You came. It's just us today. Well. Us and the lift.
if here:keane-davi | keane-davi: Hiya. Engine room floor's spotless today, by the way. Anyway. The address. Big one, I hear.
if flag:liftBrakes | them: Here it comes. Brake shoes, four. Guide rollers, twelve. I tightened every one. I know where they all are.
them: Doors. Okay. Okay.   [sigh]
them: Four, please.   [nod]
them: We're going to the rec deck, I know. I just wanted to say it. You said it, your first night. I've been practising.   [laugh]
if here:keane-davi | keane-davi: Lovely lift.
them: Lovely lift. It is, actually.
them: I'm not holding the rail. Look. No, don't look. I'm not looking.
if here:keane-davi | them: Very brave, all three.
if !here:keane-davi | them: Very brave, both of us.
? choice
* You did it. I'm so proud of you.   flavour:listen mem:proud
  them: I did it. Oh. I did it. My knees are shaking. I did it.
  + them: I did it. My knees are shaking. Don't tell anyone they're shaking. Thank you, {me}. For all of it.   [laugh]
* Again on the way down?   flavour:cheer mem:again
  them: Don't push it. After the address. Maybe after the address.   [laugh]
* Same time next Friday? A standing order.   flavour:practical mem:friday
  them: Fridays. The lift club rides on Fridays. I'll tell Cruz. Cruz will nod. That's a yes.
them: Rec deck. That's us. Mind the... is there a gap? There's no gap. Good.

== beat 5
// QUIET ENDING for beat 4: plays only if beat 4 was missed (they still rode up together)
tone: light
when: beat:kovac.3
where: Tea corner
hint: Oh. Hi. We did a thing. Can I tell you? It's quick.
mem: weride
flag: kovac.rode
mail: 30 | We did it | All three of us rode up to the address. Nobody held the rail. Cruz kept their eyes open the whole way. Sorry. You should have been there. Next Friday? Zainab
them: Oh. Hi. We did it. Friday. The lift. All three of us.
them: Nobody held the rail. Not once. Cruz kept their eyes open the whole way up.
them: You should have seen Cruz's face. Sorry. You should have been there. That's what I mean.
them: Next Friday? There's room. Well. It's a lift. There's always room.   [laugh]
? choice
* Next Friday. I'll be at the doors.   flavour:listen mem:nextfriday
  them: At the doors. Good. Um. I'll count you in. I count everyone in.
  + them: At the doors. Good. I'll count you in. That's the only counting I do in there now. Thanks, {me}.   [nod]
* I'm sorry I missed it. Tell me Cruz's face.   flavour:cheer mem:cruzface
  them: Like a seed that's just come up. Surprised to be there. Pleased about it. That's how Cruz would put it.
* I'll ride with you before then. Any deck you like.   flavour:practical mem:anydeck
  them: Any deck. Oh. That's a lot of decks. Two. Let's say two. Then we'll see.
them: Right. Scrubbers. I like scrubbers. They never surprise me.

== beat 6
// AFTERGLOW: plays after beat 4 or its quiet ending, beat 5
// JOY LINE (for when the stories switch is on): add to content/lines/kovac-zainab.lines, under == joy:
//   ? mem:moment.kovac.grip
//   - Orange and green, on a spanner. My only two-colour piece. You know which one.   #warm
// The old scarf line there (? mem:moment.kovac.fourplease) stays for the old story; this story's beat 4 sets
// mem: doors, not fourplease, so the scarf line never plays with it.
tone: light
gapDays: 1
when: flag:kovac.rode
follows: 4|5
where: Tea corner
hint: I made you a thing. It's small. Sorry. It's very small.
mem: grip
keepsake: a knitted grip for your spanner, in Works orange and garden green
learn: Zainab Kovac was stuck in a lift as a child. She serviced the Wren's lift brakes, and now the lift club rides without the rail.
them: Oh. Hi. I made you something. Sorry. It's small. It's very small.
them: A grip. For your spanner. Orange and green. I measured your spanner while you were at lunch. Sorry about that too.   [laugh]
them: So you've got something to hold. Not that you need it.
them: Forty-two rows. I counted. Obviously. I unpicked two and did them again. They were fine. They weren't perfect.
? choice
* It's perfect. Thank you, Zainab.   flavour:listen mem:perfect
  them: Oh. Um. You're welcome. It fits. I made sure it would.
  + them: It fits. I made sure it would. You stood by the doors with us. That counted. I count things. That one counted most.   [nod]
* Will you show me how to make one?   flavour:share mem:showme
  them: Oh. Yes. Tea corner, after shift. Small needles. I'll go slowly. Slower than with Zeke. Sorry, Zeke.
* I'll use it every day.   flavour:cheer mem:everyday
  them: Every day. Okay. Then I'll make a spare. Wool wears. I'll know when.
them: Right. Scrubbers. I'll be at the tea corner after, knitting. If you want. No fuss.
