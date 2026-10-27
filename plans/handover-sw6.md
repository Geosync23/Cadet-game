# Handover: SW6 (ending writer A)

**Role:** writer A for the ending, under lead 39 (session_019V68fz33UFv4cK5Z4iCDvi); reviewer RV21
(session_01AmTyMHLr5UuCY9zo3nQcwS). Builders EN1 (offer, goodbye, end page) and EN2 (crossing back, endgame).
Writer B has the endgame pool (content/ending/endgame.lines), not me.
**Branch:** `claude/ending-words-a`, from claude/staging-0.93.3 d9c7e5f0. Content files plus the baked blocks
(content_gen.py) only. Spec: plans/ending-spec.html on claude/p5-specs, section 9.

## The user's answers (2026-10-26, via lead 39)
No way back from the end page (only "Start a new game"; the ended save shows the page again; no "Before the goodbye").
Change your mind until the Captain's address at the Line. The post is worded by your answer to Calder.

## What's written (batch 1, 6dd03f57)
- `content/banks/event-crossingBack.lines`: the crossing back's notices, chatter, Saruth at the glass, Sunday's
  banner and gathering words, plaque by Basil's answer, the certificate's second date, the Line supper by stay/go.
- `content/ending/*.meet`: the staged scenes (meetings). Variants are separate files (as captainAllClear.*).
  The oath you lead uses one-reply choices so the words are yours.
- `content/ending/offer.lines`, `friends.lines`, `goodbye.lines`, `ui.lines`. Mails are `mail.ending.*` (so the
  checker allows 400). Bubble-meant kinds (chatter, Calder's walk, rumour, crowd, waves, breakfast) are kept to 60
  by hand; the checker only knows its own bubble kinds.
- Flags read: end.offer, end.now.<stay|go|unsure>, end.stay / end.go, end.calder.<engines|bridge|teach|unsure>,
  end.zeke.friday, back.answer.<feel|colonies|slow>. Proposed to lead 39; builders may rename.

## How to check
`python3 content_gen.py starship-cadet.html`, `python3 lines_check.py starship-cadet.html` (PASS),
`CADET_WORK=/tmp/cadet-work node names_check.js`, `bash check_fast.sh` (setup as in plans/handover-sw2.md:
acorn and three from registry.npmjs.org tarballs into /tmp/cadet-work, `pip install playwright`). Duplicates:
CS1's tools/near_dupes.py from claude/crew-stories-pitch. Don't re-bake while check_fast is running.

## Open
RV21 review 1 (FIXES NEEDED) answered in batch 2: daughter removed from the offer, slower-career versions (crossingBackAddress.plain, endingTell.unsure.slow, endingAsk.slow, slow Mails), friends talks neutral, nits. End page: two buttons, Keep this ending and Start a new game (lead 39's correction).
