# Handover: lead 47 -> lead 48 (written 2026-10-31 ~19:15 UTC / 3:15 PM ET, at ~72% memory)

Lead 47 = session_014zyJYM4mt9ZDCD5H9JZDtN, branch claude/lead-47 (TEAM.md log is current to the minute; read its bottom from "LEAD 47 started").
Read first: CLAUDE.md, this note, plans/handover-account.md (account move notes from lead 46), plans/patch-0995.md (the user's 19 notes, seats, decisions), the bottom of TEAM.md on claude/lead-47.

## Where things stand
- **0.99.4 LIVE** (crew stories stage 2: Zeke, Calder, Raman, Kowalczyk + new Tomas story) on NEW links on this account:
  Playtest https://claude.ai/artifact/CqUGjQXerhSKxuu4umhK41 (v1), Dev https://claude.ai/artifact/Sm86UjQMH1NmBj5ybNnB2b (v1).
  claude/integration = main = 596712bc (game a01d1a4c...bc4a). Old-account links (7hQ1, KEya, 6daN, YaJs) untouched; never publish over them.
- **0.99.5 (the user's 19-note playtest patch) is in its final gates.** BM23 (session_014zyJYPpetpQqNvn9pkGrig) on claude/staging-0995 /
  claude/bm23-wip: candidate game sha256 5733867d19550eddbc02d3c1ab5f9d22aaa58cf6c56e48b8fe1d291ae190b102 (after PL2's office fix 75e22d2).
  Re-gates started 18:04 UTC (check_fast, intro whole, day 2, player, promo, career, interactions whole, cadet vs 0.99.4); GO ETA ~19:30 UTC.
  Then BM23 sends the GO to R1-R4 itself (R5 = BM23). Round plan: plans/round-0995.md on claude/staging-0995. OLD = 0.99.4 596712bc.
- **The user PRE-APPROVED publishing 0.99.5: "Notify and publish 99.5 when ready."** So: all five shares OK -> BM23 round record + final GO ->
  lead verifies the game sha256 and that claude/integration fast-forwards -> GO to PUB3 (session_014zyJYQ6fZqmqTjgzdCaumh, already briefed:
  update the SAME two new pages to v2, {downloads}, scan, 390x844 test) -> push 596712bc..candidate to claude/integration and main ->
  PushNotification to the user (they asked to be notified) with the links.
- **THEN, only after 0.99.5 is published, the user wants the project prepared to move to another account** (TEAM ~17:13 UTC). Do: update
  plans/handover-account.md (current links on this account = CqUG / Sm86; saves are per link: Saves > Download my save, then Load a save file
  on the new account's page; a new account cannot update these pages; the next account publishes NEW links from claude/integration using
  plans/handover-publisher-3.md on claude/publish-pub3), make sure every seat's handover note is pushed (list below), write your own lead
  handover, disable the hourly check-in trigger, and tell the user in plain words what to do before switching.

## What's in 0.99.5 (all reviewed and passed; switches ON in the candidate)
JB2 jobs (14, 15, 18) + SW4 tour words; PL2 seats/doors/talk (3, 12, 13; note 13 narrowed to cabins + bedrooms after the Day 2 office
regression); CT5 controller (2, 5, 6); SD5 sound (9, 4 MESS_SCALE on = user's pick, 17 SND_LONG on, SND_BUF_ON on = user's pick);
TB3 traditions (19 Spice, 10 tea = standing spot moved only, 8 beam, milestones, Off the Tern, two-trads, toasts) + TB5 spice follow-up;
OB2 onboarding (1, 7, 11, 16); TB4 the eight 0.92.6 traditions + SW4 words; SW4 milestone words + three Mails reworded (user: change the Mail).
User answers (traditions page https://claude.ai/artifact/UfwLXgfSzGx7Eic1iyEfPE, murmur page https://claude.ai/artifact/E4ykNVcBpJjPxLgZxu3oWf):
meals only Spice; rec deck's nine: no tap; Mails changed to match; tea: move the spot; murmur proposed; buffer on.

## Seats (session ids) and state
| Seat | Session | State |
|---|---|---|
| BM23 build master | session_014zyJYPpetpQqNvn9pkGrig | running 0.99.5 gates, then R5 share + round record + final GO |
| R1-R4 runners | R1 session_014zyJYQ4EiB7CipGp4HsYV8, R2 session_014zyJYMsL5YqKnLb9Q6Lvyz, R3 session_014zyJYPN2WU6wpJgghsXiAe, R4 session_014zyJYNRijQBB389vXWxWNJ | set up, waiting for BM23's GO (branches claude/checks-0995-rN) |
| PUB3 publisher | session_014zyJYQ6fZqmqTjgzdCaumh | briefed for 0.99.5; handover claude/publish-pub3 |
| RV29 reviewer | session_014zyJYM3D7UBkZN49CsZVuA | ~47%, idle after PL2 PASS |
| RV30 reviewer | session_014zyJYNFR7ewWJGvEQNUAHr | idle, moderate memory |
| Builders (done, handovers pushed) | ST1, SW4, SD5, CT5, OB2, JB2, PL2, TB3, TB4, TB5, TR1, BM22, RV28 | idle; plans/handover-<seat>.md on their branches |
Hourly check-in trigger: trig_01W67fhJjcRCn6ahnaNdc351 (fires into lead 47's session): disable it and make your own.

## Backlog added today (next 0.99.x)
BM22-1 stories_check default 36 (ST1 7c875a26 ready), BM22-2 player_check Saving temp file/timing, BM22-3 devmode "real" flake, JB2-1 tour
last-stop line, TB3-1 chatter over a cheer, TB3-2 hosts who don't come (planner), TB4-1 Open house Mail says "Deck 2", TB5-1 tea walk-in,
RV29-1 tap in a tradition's last ~7 min, PL2-1/PL2-2 (talk social 15 vs 30; other locked rooms incl. reactor permit open from outside),
CT5-1..3 controller check-side issues. Still open, not started (the user decides): the read-only code review for waste and inefficiency.

## Gotchas learned
- Messages between sessions often arrive late or cross: restate decisions; check the builder's latest commit before sending a GO.
- Sessions go idle with checks running in the background: nudge with get_session at each check-in.
- Builders' own gates must include intro_check WHOLE for anything touching doors, walking or first-week scenes (missed on PL2 once).
- stories_check needs 36 days (the 30 default false-FAILs). player_check/devmode flakes under load: re-run alone.
- Verify every game sha256 yourself before a GO; never let BM or helpers push to claude/integration/main (the lead does, after publish).
