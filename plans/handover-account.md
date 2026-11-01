# Starship Cadet: handing the project to another account

First written by lead 46 (2026-10-30); brought up to date by lead 48 on 2026-11-01 (~9:30 PM ET Oct 31), right after
0.99.5 was published, at the user's request ("Only after 99.5 is published prepare the project to move to another
account"). This page is the starting point for whoever (or whichever Claude account) picks the project up next.
Everything that matters lives in this GitHub repository; nothing important lives only in a chat session.

## 1. Where things stand (0.99.5, live since ~9:13 PM ET, Oct 31)

- **Latest release:** 0.99.5 (the user's 19-note playtest patch). `claude/integration` = `main` = commit `6475bb30`
  (game file `starship-cadet.html` sha256 `93aed54fa9296e75c308ae199cbac32465c776c650161fe41bf22535839a5164`).
  Keep `claude/integration` and `main` equal: after each release, fast-forward both to the published commit.
- **Repository:** GitHub now names it `Geosync23/Cadet-game` (the old `geosync23/cadet-game` address redirects).
- **The road to 1.0 (the user's rules):** every update now is a 0.99.x; **1.0 is only the user's own playtest notes**.
  Each publish needs the user's OK unless they say otherwise for that one release.
- **Every game change runs the full round of checks before it is published** (`plans/testing-guide.md`). The round
  used for 0.99.5 is `plans/round-0995.md` (five shares: four runners + the build master; about 2.5-3 hours).
- **Next 0.99.x backlog** (`plans/backlog.md`, and the list in `plans/handover-lead48.md`): first P5-1 (the first
  Senior Officer "follow the line" puzzle can be skipped for good if the line reads low at that moment; old, both
  builds), then JB2-2 (the gym locker job's marker sits on a treadmill), JB2-3 (fewer repairs since 0.99.5, so
  puzzles come a little less often: ask the user whether to raise the rate), TB5-1, RV29-1, PL2-1/PL2-2, TB3-1/TB3-2,
  TB4-1, BM22-1..3, JB2-1, CT5-1..3.
- **Open, not started (the user decides):** a read-only code review for waste and inefficiency.

## 2. The live links (claude.ai artifacts) and what changes with a new account

On the CURRENT account (the one that ran leads 46-48):

| Link | What | Current |
|---|---|---|
| https://claude.ai/artifact/CqUGjQXerhSKxuu4umhK41 | Playtest | Version 2 = 0.99.5 |
| https://claude.ai/artifact/Sm86UjQMH1NmBj5ybNnB2b | Dev (Dev mode on) | Version 2 = 0.99.5 |

On the OLDER account (before 0.99.4; never publish over these):

| Link | What | Current |
|---|---|---|
| https://claude.ai/artifact/7hQ14AcwZHCi5EvL1AKiMU | old Playtest | 0.99.3 |
| https://claude.ai/artifact/KEyaHvon6ZaVHHFRdAe18m | old Dev | 0.99.3 |
| https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq | the user's "current save" Dev link (0.92.2, Version 11) | never publish over it unless the user says so |
| https://claude.ai/artifact/YaJsaCgvpb3QXvcgestTSt | 0.99.1 on its own link | Version 1 |

**Important for an account change:**
- A page belongs to the account that published it. **A different account cannot update it** (unless the owner shares
  it with edit access). So the new account publishes **new** Playtest and Dev links from `claude/integration`, using
  the publisher steps in `plans/handover-publisher-3.md` (branch `claude/publish-pub3`).
- **Saves live in the browser, per link.** A new link starts with no save. Before switching, open each link you play
  on and use **Saves > Download my save**; on the new link use **Saves > Load a save file**. Do it for every link
  whose save you want to keep (CqUG, Sm86, and the old 6daN "current save" link if it still matters).
- The old pages keep working after the switch (they stay on the account that made them); they just can't be updated.

## 3. How a new account picks it up (step by step)

1. Connect GitHub on the new claude.ai account and make sure it can reach the repository `Geosync23/Cadet-game`
   (the GitHub owner adds the account, or installs the Claude GitHub app on the repository).
2. Start one Claude Code session on the repository as the **lead** (from claude.ai/code, not from another session).
   Give it this first message:
   *"You are lead 49 for Starship Cadet, on a new account. Read CLAUDE.md, then plans/handover-account.md and
   plans/handover-lead48.md on branch claude/lead-48, then the bottom of TEAM.md on claude/lead-48. Make your branch
   claude/lead-49 from claude/lead-48. No helper sessions from the old account can be reached: hire fresh ones from
   their handover notes. Publish new Playtest and Dev links from claude/integration when the user says so."*
3. The new lead hires its own helpers (build master, reviewers, check runners, publisher). **None of the helper
   sessions listed in TEAM.md can be reached from another account**, but each left a handover note (section 4).
4. First thing from the new account: publish new Playtest and Dev links of 0.99.5 from `claude/integration`, give the
   user the links, and the user loads their downloaded saves there.
5. CLAUDE.md names the user's "current save" Dev link (6daN, old account). Once the user has moved their save to a
   new link, ask whether CLAUDE.md should name the new one instead.

## 4. Where everything is written down

- `CLAUDE.md`: the project rules (read first, every session).
- `DEV_NOTES.md`: how the build works, the rules that keep it working, testing, and "Next".
- `design-doc.md`: what the game is (single source of truth for the design).
- `plans/testing-guide.md`: the full round and how runners run their shares; `plans/round-0995.md`: the last round.
- `plans/build-table.md`: every build, with what was in it and the test results. `plans/backlog.md`: open items.
- `plans/patch-0995.md` (claude/lead-47 and later): the user's 19 playtest notes and who did what.
- `TEAM.md` (bottom, on `claude/lead-48`): the running log of who did what and every user decision, with times.
- Handover notes from the latest seats:
  - lead: `plans/handover-lead48.md` (claude/lead-48); before it `plans/handover-lead47.md`
  - build master: `plans/handover-bm23.md` (claude/handover-bm23)
  - publisher: `plans/handover-publisher-3.md` (claude/publish-pub3)
  - reviewers: `plans/handover-rv30.md` (claude/review-rv30), `plans/handover-rv29.md` (claude/review-rv29)
  - check runners' results for 0.99.5: `plans/checks-0995-r1.md` .. `-r4.md` (claude/checks-0995-r1 .. r4)
  - the 0.99.5 builders (ST1, SW4, SD5, CT5, OB2, JB2, PL2, TB3, TB4, TB5, TR1): `plans/handover-<seat>.md` on their
    branches (listed in plans/handover-lead47.md)

## 5. Before switching: what the user does

- **Download your saves** from every link you play on (section 2).
- The hourly lead check-in (a scheduled task on this account) is switched off; it does not move to a new account.
- Nothing else is needed on the old account: all the work is pushed to GitHub.
