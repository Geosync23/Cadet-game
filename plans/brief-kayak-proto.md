# Kayak prototype brief ("White water"), lead 17 (session_016bN7x175WBwBL7S9xc2Lpb), 2026-10-19

**Overnight mode is ON** (the user is asleep until they check in and ask for the report). This is goal (4)'s first piece: the kayak mini-game **White water** as a **standalone prototype page**, the way Lightdisc was done (`lightdisc-proto.html`). It is NOT built into the game: the user tries it on its own link and approves it first; integration is a later, separate job. One seat.

**Read, in order:** CLAUDE.md; this brief (`git fetch origin claude/lead-pillar1 && git show origin/claude/lead-pillar1:plans/brief-kayak-proto.md`); the mini-games plan FINAL (`git show origin/claude/p5-design:plans/rec-minigames-plan.html`, 214f5b7 or later, https://claude.ai/artifact/Ubn2MJvidnuK1awcx2gKMP: "What all three share" and "Kayaks"); design-doc's "Rec dec traditions" paragraph (claude/p5-design); `plans/handover-lightdisc.md` (claude/lightdisc-proto); `lightdisc-proto.html` and `tools/lightdisc_proto_check.js` (in the base); the rec deck plan v5's river hall (`git show origin/claude/recdeck-plan:plans/recdeck-plan.html`, rooms and section 8 "kayak"); DEV_NOTES "Testing".

- **Branch:** new `claude/kayak-proto`, from the published 0.63.3 (`claude/p5-cand-pt1` 2bc08d5, which holds `lightdisc-proto.html` and its check) or a later build the lead names. You add only new files, so it can start any time (the lead says when).
- **Files (new only):** `kayak-proto.html` (the page) and `tools/kayak_proto_check.js` (its check), shots in `plans/shots-kayak/`, a short "Kayak prototype" section in DEV_NOTES. **Do not edit `starship-cadet.html`** or any other file.

## What to build (the agreed design; no gates)
- **One lap of the loop:** the slow channel, then the fast white-water run along the windows. About 60-90 s a go.
- **Steering:** the kayak heads where your thumb is (Lightdisc's steering); **tap for a strong stroke**. One thumb; mouse and keys on desktop.
- **The water is the challenge:** currents push you off your line; the standing waves at the wave gate shove you sideways; the bend at the bow end runs against you. Show the current with foam lines and ripples, and the calm **eddies** behind the rock banks.
- **Stamina meter** by your thumb: each strong stroke and every second fighting the current costs stamina; resting in an eddy or riding the current refills it; run it dry and you **drift with the current (safe, just slow)** until you get your breath back, with a tired slump.
- **No failing:** no capsizing for good, no clock you can lose to. **Bests in words** ("your best lap yet"), no times on screen.
- **The clock stops** for the go and its result: show the same kind of notice Lightdisc does (the game's ship clock isn't in the page; just show the notice, so the flow matches).
- **Crew beside you:** up to three crew kayaks on the same rules with a seeded autopilot at their own pace; "Race me?" turns it into a race. Their lap can also be worked out **on paper** (for the regatta later): `New`, `Step`, `Paper`, `Clone`, pure, fixed 60 Hz, one seeded stream, no `Math.random`, no DOM in the rules.
- **Progress to show (switchable on the menu, prototype only):** the slow loop only vs the fast run open (Holt opens it after three Paddle club visits), and Holt's wave gate turned up a notch; a regatta heat of four (one live go with three others) as a demo.
- **Look:** the live river hall in the game's style and colours (`col()`, sRGB, 1 unit = 1 tile), sized like the game's: `RIV = { x0: 3.0, x1: 13.6, z0: .5, z1: 5.6, in0: 4.6, in1: 12.0, iz0: 2.1, iz1: 4.0 }` (room-local; fast run on the north/window side, wave gate across it at the bow end), one opaque water like `RK.poolWater` plus foam on the fast run; the kayak, paddle and helmet like the game's (`recKayak`, the 1.3 m paddle). Camera: a chase view behind your kayak, eased in like Lightdisc's dolly-zoom; the stamina meter and stroke feedback are screen overlay (nothing on the water's plane).
- **Flow like Lightdisc's page:** a menu (paddle alone / with crew / race / regatta heat), How to play in two or three steps, the go, a result card (Again, Done).
- **Phones first:** portrait 390 × 844 and sideways; under 200 draw calls in a go (less is better); no new lights; no coplanar faces.

## Done when
The page plays a full lap on a phone with one thumb; currents, waves, eddies and stamina make the lap take some reading of the water; drifting when tired works and recovers; crew paddle beside you and a race and a heat work; a live go matches the same go on paper at 60, 30 and 20 fps; the check passes; shots taken.

## Checks (`tools/kayak_proto_check.js`, Node Playwright, like the Lightdisc one)
- A real thumb drag steers, a tap strokes, lifting the thumb holds the line; How to play advances.
- Stamina falls with strokes and fighting the current, refills in eddies, and empty means drifting, then recovery.
- Frame-rate match: a seeded go cloned and run at 60, 30 and 20 fps equals the go on paper.
- Seeded crew laps replay identically; a regatta heat's order is the same each time for the same seed.
- Draw calls under 200 in a go; no console errors; portrait and sideways shots (menu, how-to, mid-run in white water, drifting tired, result).
- Note: the Lightdisc check hard-codes `/home/user/Cadet-game/`; use this repo's real path.

## Rules
- Determinism: seeded streams only (when it's integrated later the game keys are 833-838, as the plan proposes; the lead confirms then). No `Math.random`.
- Plain language in everything the player reads; placeholder chat lines are fine (mark them as stand-ins, as `LD_TALK` does).
- **Report to lead 17** (send_message to session_016bN7x175WBwBL7S9xc2Lpb): one line when you start; one when the first playable version is pushed (hash, what, check results, memory %); at once if blocked or a design call is needed. No narration. The lead publishes the page as a **new artifact titled "Starship Cadet Kayak Prototype"** (its own link) and tells the user; the user approves before any integration.
- **Never** contact the user, start sessions, publish, or push outside `claude/kayak-proto`.
- **Long check runs** survive restarts (TEAM.md); **memory:** tell the lead at ~60%; at ~70% write `plans/handover-kayak-proto.md`, push, stop.

## Seat
| Seat | Session | Branch | Reads first |
|---|---|---|---|
| K kayak prototype engineer | (to start) | claude/kayak-proto | handover-lightdisc.md, lightdisc-proto.html |
- **Lead call (~06:55):** up to 2 crew kayaks beside you (the channels are ~1.6 m; keep the game's RIV numbers). Note: tools/lightdisc_proto_check.js hard-codes /home/user/Cadet-game/; use your clone path.
