# Handover: lead 31

## START HERE (lead 32)
1. Read CLAUDE.md, this note, then the bottom of TEAM.md on `claude/lead-31` (from "~03:00 UTC: LEAD 31 took over").
2. Branch: start `claude/lead-32` from `claude/lead-31`. Push only there.
3. Make your own hourly check-in scheduled task (create_trigger, cron, into your session), then disable lead 31's `trig_01T2vpQXD1prT8LfmcBTfhQT` (update_trigger enabled=false).
4. Message every working seat below with your session id so they report to you (priority "now"; ask for a one-line acknowledgement). Tell lead 31 (session_0118SXBCdg87nDiXdtrGNVSR) you've taken over.
5. Tell the user in one short message that you've taken over.

Lead 31 = session_0118SXBCdg87nDiXdtrGNVSR, branch `claude/lead-31`, a fresh top-level session (chain depth 0). Took over 2026-10-23 ~03:00 UTC; handed over ~13:00 UTC (9 AM Eastern) at ~67% memory.

## The user's standing rules (new in bold)
- Plain language, no jargon, no emojis. Few messages to the user: published builds, questions only they can answer, milestone summaries; "Noted." for routine helper news. Phone notification (PushNotification) only for a published build, a milestone or a question.
- **Times for the user always in US Eastern time** (EDT now, UTC-4), never UTC (written into CLAUDE.md). Team notes may keep UTC.
- Whenever next steps are discussed, remind the user of everything still built but switched off (now: the controller, Crossing the Line).
- **Deadlines are goals, not deadlines: quality first; nothing gets dropped or rushed for a time** (the user, 2026-10-22 night).
- **Overnight mode** when the user goes to bed: no messages or phone pings; decisions wait for the morning; one morning summary.
- Hire whatever is needed, don't waste. Full round on six runners for every game change. Memory: judge from ~60%, never above 80%.

## Pages for the user
- Playtest https://claude.ai/artifact/Wn6mUGcxatoWVqhCNTa1vs and Dev https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq: **Version 9 = 0.92.0** (claude/integration 685af944, game sha256 f2329b620c113b0a585d6129ef70a3cbb8f8112c6ef9d19a13587fb996271ebd; POINT_ON + GUIDE_ON true, PAD_ON + EV_LINE_ON false). PUB1 republishes from a named commit + sha.
- Fresh-eyes findings https://claude.ai/artifact/7GFQ8pZZxmZnTW3o6RHd6k: **v22** (batch 2 Done; 25 Not a problem; 14 note). Always read the live page first (Artifact read the url; then read with path "index.html" to get an editable local copy; edit the state JSON; publish with url). FE2's findings go here as they come.
- Game preview PDF (PW1): claude/game-preview 513d9a4 (plans/starship-cadet-preview.pdf, updated for 0.92.0) sent to the user; also a text-only version (110 KB) sent, built from plans/preview/starship-cadet-preview.html with images/styles stripped and printed with Chromium (not committed).

## What 0.92.0 contains (published 12:06 UTC / 8:06 AM Eastern)
Teaching arrows ON (Settings: Always / First times / Off); breakfast back; Zeke's new Day 0 front end (17:15 arrival, walk-and-talk, 15 hand-over bubbles, Mail "Before you land", clock hold, wardrobe arrow); diners leave gradually at every meal (Day 0 table full to the goodnight, FX5's kept-seat fix); booth arrow + Tracked booth row; shower once per 6 ship h, basin refills only the toilet's take; tiles partner sits; Dev-mode career arrow; tip-clear; FB1 tap guard; FX3 fix 19; FX4 m7 + Wait here; FX7 gym-bike floor-tap crash fix. Known in its round: KC1/KC2 (controller-only lift ring in a crowded lobby), KS1 (save size, being trimmed), KP1 (Line ceremony 335 draw calls, accepted), backlog 14/23/32; reach partial (controller off).

## User decisions this session (all in TEAM.md)
- No bag safety net: player must always stow the bag (Monday put-away removed; exception agreed by lead: skipping the intro/"I know my way around"/week's end stows it quietly; user not yet asked about the week's-end case, mention it).
- Day 0 table: keep as is (full ~1 h after the goodnight, thins by ~20:05); lead read "Yes" as keep: confirm if the user brings it up.
- Zeke tour notes (washroom line only if you linger; slow player misses the arrival Sunday table; "Ship traditions tomorrow" Mail in the bunk room): no change for now.
- Hygiene rule approved; late tweaks (booth arrow, hygiene, tiles, dev arrow) shipped.
- **Open question to the user: switch Crossing the Line on in 0.92.1?** (FX6's check passed; see below). Not answered yet.

## 0.92.1 (in progress; build master BM15 session_01EH5qkoYriK2Gsrp7hHRoso, staging claude/staging-0.92.1)
- AC3 54169e4c: join notices never dropped (TQ_KEEP) + check test hook (LEAD31-3, LEAD31-2): **RV10 PASS, merged on staging (c6601dce)**; lead signed off section 18 on RV10's review.
- FX4 claude/fx4-save-trim 06a989e6 (LEAD31-4; Day 30 2700 B, Day 120 2816 B; old saves trimmed on load): with RV10.
- FX7 gym bike tap at camera turn 2 (LEAD31-1): building.
- DS1 claude/bag-no-net (local, not pushed; on hold for the lift fix) → RV9.
- **DS1 claude/zeke-lift-fix (priority):** FE2's Day 0 blocker: the Works-door step only counts you "there" on the 2-tile lift-lobby spot Zeke stands on; a player beside him in the haulway waits until 19:05. OLD bug (also in 0.91.0). Fix (a): counted there within 2 tiles of Zeke once his 2 Works lines are said + an intro_check "stand beside him" walker; check other tour steps for the same trap; a tap on Zeke during the tour shows his card; walk.more.3 reworded to "Forget my name? Tap me. I won't be offended. Much." (ZW1); introAsk.meet line to check; shuttle-bay talk-in-place (~16 real-time ship min) → walk while talking if too long. Reviewer RV9. Workaround told to the user and FE2: step one tile east into the lift lobby beside him.
- If the user says yes, Crossing the Line ON goes in too (EV_LINE_ON; FX6's check: all fine; backlog LEAD31-5 Line supper over-cooks).

## Controller follow-up (controller stays off)
CP5 session_01Un47TDkZfRL6cvcLwE3Zcy (claude/controller-follow2 from 685af944): map deck buttons (D-pad can't reach 6 of 7 on Maps / Appointments > Pick on the map), KC1, KC2, 21 of 44 mess seats, B cases. CTT4 session_013PsHo9ueLbqRuDYitNjX6K (claude/controller-tests-4): confirm map/B, resumable reach sweep, check CP5's fixes. Reviewer to be named when CP5 pushes (RV10 or a fresh one).

## Seats (session ids)
- Build: BM15 session_01EH5qkoYriK2Gsrp7hHRoso; BM14 session_016mhGtsCxEgPCFn9C767yjq (~55%, answers BM15 then stops). PUB1 session_01GnpjFR6oumvuvTrmcXSqeg.
- Runners: CR1 session_01CsWNjCsy8u5mrHJgTVgCst, CR2 session_01BgMQaB1LQmhfU1rSJ2ATvv, CR3 session_016oCbvvzgcqzzCTsBFCkYRB, CR4 session_01636CfY2MhB3DzrzZ59dhXz, CR5 session_01CHoEsvv7zMPZDr1ir7uAiz, CR6 session_01B1FwE5sMmHnMPWsGn23nrk (all idle).
- Builders: DS1 session_01MZBSf7MZeb9C89wpoavLko (zeke-lift-fix, bag-no-net); AC3 session_01DiLRzrXgkeoAZCoX1mVJn9 (arrows-c owner, idle ~48%); FX4 session_01BueJ4UzQkn8HcC1TXd1KrW (save trim); FX5 session_01LGRr55ZQCd11PuqhJEn9Jj (idle ~45%); FX6 session_01VVgFPg2QfrvjGSfxf7QsQw (idle; did the Line check); FX7 session_01UrZGjRKXhLrWFfDJXVDhBN (gym bike); FX3 session_01UZWrZRivwQJPKL3x7c8Ft9 (idle); DV1 session_01GewvUTCXkDVkHsz53ex71o (idle); CP5 (controller).
- Writers: ZW1 session_01QY7V7HVtAbiX64cyVKL1Am (Zeke words); PW1 session_01Kpg4fqV2FgfYYeGuQTU5NV (preview; idle).
- Reviewers: RV9 session_01E31oZQU7DFbZnh2BesWsnM (~50%; DS1's pieces, then done); RV10 session_01XeJ6bvySekD1V8Sfh1tzgb (~22%; 0.92.1 reviews).
- Testers: FE2 session_01FYu2AXA4x4P4x5XVC66Qcz (playing Days 0-8 on 0.92.0; batch 1 = the lift stall; send findings to the page); CTT4 (controller).
- Stopped this session: lead 30, SC1, IM1, RV7, RV8, FB1, CTT3 (handover notes on their branches).

## Backlog added (lead 31)
- LEAD31-1 gym bike 3-gym-17 floor tap at camera turn 2 (FX7, in 0.92.1).
- LEAD31-2 test hook so checks show pop-ups at once (AC3, done).
- LEAD31-3 join notices never dropped (AC3, done).
- LEAD31-4 save trim (FX4, in review).
- LEAD31-5 Line supper over-cooks (+20 cooked / +21 wasted with the Line on; section 16).
- FE2 batch 1 smaller items: "You wake in Bunk 1" card behind the manifest (FE1 item 7 again); single floor taps beyond the shuttle-bay rail don't move you (press-and-hold does).

## Gotchas learned this session
- **With the arrows on, toasts go through a pop-up queue (guideToast → guideTick replays toast()); any check reading toasts or IX_GOAL directly needs the shared pattern (AC3's; now the LEAD31-2 hook).** Isolate arrows-caused failures by running a copy with POINT_ON/GUIDE_ON false.
- **Checks that walk to exact spots hide real-player stalls** (the Day 0 lift); FE2's real-time play found what fast-frame checks couldn't. Prefer "stand where a player would" walkers.
- **A seat whose tool call is declined may silently stop** (AC3 held 3 h asking in its own session). Look at quiet seats' session status (get_session / list_events), not just messages. Rule sent to all: report declined calls at once and carry on.
- Two helpers given the same fix by mistake twice (FX4/FB1 garden line, FX7/FX5 booth line): before assigning a fix, check who owns the line.
- Long background runs stop at 2 h (CR4's reach); use resumable/detached runs.
- Repo .gitignore ignores *.png; the stop hook wants no untracked files in this checkout (delete temp copies after sending files).
