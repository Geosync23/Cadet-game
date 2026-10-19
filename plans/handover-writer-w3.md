# Handover: rec deck writer W3

**Session:** session_01LbftuR6cNubo3CvAScTuv5 (2026-10-19, overnight). **Lead:** lead 19, session_01FsGspstkG61e9AWadSi36y
(was lead 18, session_01CBur9nrJ411pFkHopF96RL); check the latest brief on `claude/lead-pillar1`. **Branch:**
`claude/writer-rec`, from the 0.63.4 final **aa4f42c** (claude/p5-cand-s4). Build-table rows 0.48.117-0.48.127 (writers'
series; no HUD bump); the next is **0.48.128**. Brief: `plans/brief-recdeck.md` (claude/lead-pillar1), section "W3".

Read first: CLAUDE.md, the brief, `plans/handover-writer-w2.md` and `plans/handover-writer-p5.md` (claude/writer-p5:
tone, formats, gotchas), content/README.md, content/facts.md (its new section "The rec dec"), and **content/keys-rec.md**
(every key I wrote, who reads it, what's wired).

## Who's who
- RA, rec engineer A (crew use, the traditions engine): session_012mZrFQrGpbNeNWuRg4Bxyp, `claude/rec-crew`. It owns
  plans/trad-format.md, trad_parse.py, events_check, day_check. Its messages can arrive late.
- RB2, rec engineer B (machines, the leak trace, auditorium; took over from RB session_01PN7anFnvCzsMALwmWWEbhi):
  session_018cunWUG3yeKN8NzCPdRbTy, `claude/rec-works`.
- Reviewer R7: session_01HCwvy5w432bhz41UYxHYwq (was R6). Build master BM8: session_01YGy9FDmcbkySMJpVPYJaAo.
- Send every hash to the reviewer and the build master; the lead per finished piece, with memory %.

## What I built (all R6/R7 PASS through 4f2dcdc; 2cc8056 sent)
- **R12 words:** banks rec, disc, talent, talks, news-rec, mail-rec; overheard rec; reactions rec; own lines for 11 crew
  (blocks marked "W3, rec deck"); quiz q33-q40; Gran and Sam call scenes; facts.md "The rec dec".
- **Lightdisc:** `disc.charged/curve/point/win/lose` for rina, holt, vance, pell + banks/disc.lines. `disc.lose` (you
  win) isn't called by section 23b's discTalk yet. LD_TALK stays as the fallback (its comment reworded).
- **"Six decks" texts:** the five Deck directory ITs, the spine ladder, the lift tip, Halloran's roof.view fallback,
  torres-zeke walk.lift.2 all say seven. RB drew the sign and changed its own comment.
- **Naming (lead 18):** signs/formal "Recreation Deck" (directory "Recreation Deck (R)"); narration/Mail/news/UI "the
  rec deck"; crew speech "rec dec". The neon and the poster keep REC DEC (the deck's look). Deck R's own directory IT,
  the spine trunks and lockers ITs were changed; RA changes its recTap "closed till six" toast.
- **Machines:** content/works/faults-rec.lines (fault.name/shows/sign/still/tried for RB's 13 kinds; `still` = the line
  when you fitted THIS cause's part). content/works/rec.lines: rec.shut.float/net/belays/belay/route (wired), .pool (spare),
  trace.pool.goal/drip/up (wired; drip + ' ' + up), trace.symptom.pool (S2's traceTitle; {deck}).
- **Traditions:** content/traditions/rec-*.trad, k 486-498 (499 spare): rec-wso, rec-cup, rec-dawn-swim,
  rec-paddle-club, rec-regatta, rec-wall-night, rec-float-hour, rec-slow-stretch (Sun 08:00-08:45, lead 18),
  rec-wren-talk, rec-chiefs-talk, rec-film-night, rec-talent-night, rec-all-hands. **RA's REC_TRADS code holds the
  rules; the files give only the words** (from, mail/ask/here/thanks/chatter). The `flag: rec.on` gates, the place
  types and the "FOR RA" comments stay harmless; keep every where-line on deck 7.
- **Talks and talent night:** meetings talk.sato / talk.calder / talk.tomas / talk.esposito-yara / talk.you and
  rec.talent.you (RA opens them when present); the panel kinds talk.open ({title}) / talk.answer / talk.listen for
  nine speakers + a fallback; Ferreira's talent.ask / tune / joke / trick / watch.

## Loose ends
- Written but not wired yet (RA has no hook): rec.wso.up, rec.wso.win, mail.rec.allhands.night,
  mail.rec.talent.signup, mail.rec.talk.next; banks/talent.lines' show lines; rec.shut.pool.
- events_check FAILs on rec-all-hands (its first date, Day 92, is outside the check's days) until RA's next hash adds
  days 92/99 (lead 18's call). Not a writer fix.
- Talks after Day 29 (Holt 32, Maeve 36, Zeke 39, Brennan 43, Ferreira 46, then Pell, Rina, Saruth, Nandakumar) have
  only the panel lines, no meeting yet. Brief: "ship the first 4 talks; the rest come later".
- Not written: "Rec dec, is it?" for crew in the lift (no hook for crew talk in the lift).
- Small invented details, flagged to the lead: Maeve's nine minutes forty, Vance's 304 rings, the lone flipper, Calder's
  "decks 5 and 6 had a thousand labels" lore. Sato's Day 8 creature is unnamed on purpose.

## Gotchas
- `trad:` / `came:` conditions only accept tradition ids that are baked; write the .trad first, then the lines.
- trad_parse rejects extra `==` sections: put extras in banks as keys.
- `every 2 weeks ... week N` takes only 1 or 2; use `from day N` instead.
- Text keys cap at 90 characters unless `mail.` (400), `tip.`/`join.` (200), `works.ask` (140); split long toasts.
- Bake on the branch (`python3 content_gen.py`) so lines_check can PASS; the build master re-bakes on merge.
- interactions_check / events_check need three.js: `mkdir -p /tmp/cadet-work/three && cd /tmp/cadet-work/three && npm pack
  three@0.128.0 && tar xzf three-0.128.0.tgz`, `pip install playwright`, `CADET_CHROME=/opt/pw-browsers/chromium`, and
  a CADET_WORK of your own per run (DEV_NOTES "Testing").

## How to test
`python3 content_gen.py && python3 content_gen.py --check && python3 lines_check.py` (PASS);
`python3 plans/trad_parse.py` for the .trad files; `grep -i -c "six decks" starship-cadet.html` (0) and no "Deck 7" in
any text; interactions_check / events_check vs the base aa4f42c when texts on screen or traditions change.

## The user's answers (via lead 19, 2026-10-19 ~11:45)
- The small invented details stay.
- Later Wren talks get no full meetings: only the first four (talk.sato/calder/tomas/esposito-yara) and talk.you; the
  rest use RA's panel with the talk.open/answer/listen lines.
