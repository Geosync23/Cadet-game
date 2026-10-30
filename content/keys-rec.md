# Rec deck keys (W3, writer; claude/writer-rec)

The words for the rec deck (plans/recdeck-plan.html v5 section 9; plans/rec-traditions-plan.html FINAL). Keys are
proposals until the seat that reads them confirms; renames are adopted and logged here.

| What | Keys / files | Read by |
| --- | --- | --- |
| Everyday rec dec talk | banks/rec.lines (chat, smalltalk, near with deck:7 / place:pool, river_hall, float_room, stands, auditorium, feel); overheard/rec.lines | the dialogue engine (as is) |
| Own lines | `== chat` / `== smalltalk` blocks marked "W3, rec deck R12" in lines/pell, rina, holt, vance, brennan, calder, oduya, tomas, volkov-maeve, ferreira, nandakumar | as is |
| Lightdisc talk | `disc.charged`, `disc.curve`, `disc.point`, `disc.win` (the opponent wins the game), `disc.lose` (you win; new, for 23b) in lines/rina, holt, vance, pell; banks/disc.lines for anyone else | section 23b's discTalk (lineFor(opp, 'disc.<kind>')); LD_TALK stays as the fallback |
| Quiz | quiz.q33-q40 (banks/quiz.lines; a1 right) | Tomas's quiz (as is) |
| Calls home | gran.call and sam.call: two `== chat` scenes each (swimming; Lightdisc) | as is |
| News | banks/news-rec.lines (news.works, news.notice, news.gossip, news.crew). news.trad by rec tradition id | the News feed |
| Mail | banks/mail-rec.lines: mail.rec.film.moved, mail.rec.bellboard ({text} = names), mail.rec.bellboard.you, mail.rec.regatta.won ({name}), mail.rec.cup.won ({name}), mail.rec.talent.signup, mail.rec.talk.next ({name}, {title}), mail.rec.talk.you | RA (section 18): wired film.moved, bellboard(.you), regatta.won, cup.won, talk.you ({weekday}); not yet: talent.signup, talk.next, allhands.night |
| Traditions | content/traditions/rec-*.trad (lead 18: W3 writes them in the existing format): rec-wso 486, rec-cup 487, rec-dawn-swim 488, rec-paddle-club 489, rec-regatta 490, rec-wall-night 491, rec-float-hour 492, rec-slow-stretch 493 (Sun 08:00), rec-wren-talk 494, rec-chiefs-talk 495, rec-film-night 496 (flag rec.film.moved), rec-talent-night 497, rec-all-hands 498; 499 spare. Every one but film night waits on `flag: rec.on` (set it when REC_DECK is on). What the format can't say is in each file's `FOR RA:` comment. Place types rec:lane, rec:kayak, rec:belay, rec:float are RA's to make. Extra words: rec.wso.up, rec.wso.win, mail.rec.allhands.night (banks/mail-rec.lines) | RA (section 18) |
| Reactions | reactions/rec.lines: cue:tradition.<rec id> and .you for each | social's cue (as is) |
| Wren talks | meetings talk.sato (Day 8, chief's), talk.calder (Day 18, chief's), talk.tomas (Day 25, small), talk.esposito-yara (Day 29, small), talk.you (your talk); each choice sets `mem:talk.<id>.asked` | RA: the meetings are opened when present, else its panel with talk.* kinds |
| Talk panel (RA) | talk.open ({title}) / talk.answer / talk.listen: banks/talks.lines (anyone) and own lines for sato, calder, tomas, esposito-yara, holt, volkov-maeve, torres-zeke, brennan, ferreira; Ferreira's talent.ask / talent.tune / talent.joke / talent.trick / talent.watch | RA (section 18 REC_TRADS); or the meetings below |
| Talent night | banks/talent.lines: talent.open, talent.intro ({name}, {thing}), talent.act.song/piano/duet/juggle/poem/trick/joke, talent.after, talent.close, talent.crowd; meeting rec.talent.you (your act's choice card) | RA (show) / RB (recShow) |
| Machine faults | content/works/faults-rec.lines: fault.name/shows/sign/still/tried.<kind>.<cause> for RB's 13 rec kinds | section 17 / the scanner (as is) |
| Works texts | content/works/rec.lines: rec.shut.float/net/belays/belay/pool, trace.pool.goal/drip/up (wired: .drip + ' ' + .up), trace.symptom.pool; rec.shut.float/net/belays/belay/route wired (RB2 0ab43cd, 0.84.12), .pool spare | RB2 (section 15r, the leak trace) |
| "Six decks" | game texts: the five Deck directory ITs, the spine ladder, the lift tip, Halloran's roof.view fallback; torres-zeke walk.lift.2 | — |
| Canon | facts.md "The rec dec" | writers |
