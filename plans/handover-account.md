# Starship Cadet: handing the project to another account

Written by lead 46 on 2026-10-30, at the user's request ("prep the project for a hand over to another account").
This page is the starting point for whoever (or whichever Claude account) picks the project up next.
Everything that matters lives in this GitHub repository; nothing important lives only in a chat session.

## 1. Where things stand (0.99.3, live since 3:44 AM ET, Oct 30)

- **Latest release:** 0.99.3. Branch `claude/integration` = commit `9c0103e3` (game file sha256 `04c821fe...c2a9`).
  `claude/integration` is always the latest released game. **`main` is old** (0.63.2r, Oct 18) and has not been used
  since; see section 5.
- **The road to 1.0 (the user's rules):** every update now is a 0.99.x; **1.0 is only the user's own playtest notes**,
  nothing else. Each publish needs the user's OK unless they say otherwise for that one release.
- **Every game change runs the full round of checks before it is published** (`plans/testing-guide.md`, the user's
  rule since 2026-10-22). The round used in the 0.99.x releases is `plans/round-0990.md` on `claude/lead-46`
  (five shares; about 2.5 hours).
- **Open, not started (the user is still deciding):** a read-only code review for waste and inefficiency
  (about 4 reviewers by section, findings page to the user first; fixes would ship as a 0.99.x).
- **Small backlog notes from the 0.99.x work:** EV2-1 (Dev mode's formal dinner jump label is stale); after a reload
  mid-dinner, Zeke's chat itself is not replayed (left as it was; the Chief's welcome now does play).

## 2. The live links (claude.ai artifacts) and what changes with a new account

| Link | What | Current |
|---|---|---|
| https://claude.ai/artifact/7hQ14AcwZHCi5EvL1AKiMU | Playtest | Version 9 = 0.99.3 |
| https://claude.ai/artifact/KEyaHvon6ZaVHHFRdAe18m | Dev (Dev mode on) | Version 9 = 0.99.3 |
| https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq | The user's "current save" Dev link (0.92.2). **Never publish over it unless the user says so.** | Version 11 |
| https://claude.ai/artifact/YaJsaCgvpb3QXvcgestTSt | 0.99.1 on its own link | Version 1 |

**Important for an account change:**
- These pages belong to the account that published them. **A different account cannot update them** unless the
  owner shares them with edit access. The usual path: the new account publishes **new** Playtest and Dev links from
  `claude/integration` (the publisher steps are in `plans/handover-publisher-2.md` on `claude/publish-26`).
- **Saves live in the browser, per link.** A new link starts with no save. Before switching, open each link you play
  on and use **Saves > Download my save**; on the new link use **Saves > Load a save file**. Do this for the
  "current save" link (6daN) too.

## 3. How a new account picks it up (step by step)

1. Connect GitHub on the new claude.ai account and make sure it can reach the repository `Geosync23/Cadet-game`
   (the GitHub owner adds the account or installs the Claude app on the repository).
2. Start one Claude Code session on the repository as the **lead** (start it from claude.ai, not from another
   session). Give it this first message: *"You are the lead for Starship Cadet. Read CLAUDE.md, then
   plans/handover-account.md and plans/handover-lead46.md on branch claude/lead-46, then the bottom of TEAM.md on
   claude/lead-46. Make your branch claude/lead-47 from claude/lead-46."*
3. The new lead hires its own helpers (build master, reviewer, check runners, publisher). **None of the helper
   sessions listed in TEAM.md can be reached from another account**, but each left a handover note in `plans/`
   (section 4), so a fresh helper starts from its predecessor's note.
4. First release from the new account: publish new Playtest and Dev links from `claude/integration`, and give the
   user the new links.

## 4. Where everything is written down

- `CLAUDE.md`: the project rules (read first, every session).
- `DEV_NOTES.md`: how the build works, the rules that keep it working, testing, and "Next".
- `design-doc.md`: what the game is (single source of truth for the design).
- `plans/testing-guide.md`: the full round and how runners run their shares.
- `plans/roadmap-1.0.md` (on `claude/lead-44`): the user's road to 1.0.
- `plans/build-table.md`: every build, with what was in it and the test results.
- `TEAM.md` (bottom, on `claude/lead-46`): the running log of who did what and every user decision, with times.
- Handover notes from the latest seats:
  - lead: `plans/handover-lead46.md` (claude/lead-46)
  - build master: `plans/handover-bm21.md` (claude/handover-bm21)
  - reviewer: `plans/handover-rv26.md` (claude/review-rv26; RV27 continued from it on claude/review-rv27)
  - publisher: `plans/handover-publisher-2.md` (claude/publish-26)
  - sound: `plans/handover-sd3.md` (claude/mess-sound-0993)
  - render work: `plans/handover-rb1.md` (claude/opt-098-render)

## 5. Before switching: things the user may want to decide

- **Bring `main` up to date.** New sessions open the default branch, `main`, which is still 0.63.2r. Updating `main`
  to `claude/integration` (0.99.3) means a fresh session sees the current game and rules straight away. This changes
  the default branch on GitHub, so it waits for the user's OK.
- **Share or re-publish the links** (section 2), and **download saves** before switching.
- The hourly lead check-in (a scheduled task on this account) is switched off; it does not move to a new account.
