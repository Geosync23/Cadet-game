# Handing the project to another Claude account (a handoff, not shared work)

Written by lead 10, 2026-10-18. For the case where the user switches to a different Claude account to share usage: one account works at a time, the other rests. Never both at once (they'd fight over the same branches).

## Is extra documentation needed?
Mostly no. The project already explains itself in the repository: `CLAUDE.md` (the rules), `DEV_NOTES.md` (how the build works, testing, the build table), `design-doc.md` (what the game is), `TEAM.md` (who's who), `plans/handover-lead.md` (the lead's running handover; read the last "HANDOVER TO LEAD n" section), the plan pages, and a `plans/handover-<role>.md` for every role. A fresh lead on any account can start from those. What the files can't carry is **what belongs to the old account**, listed below; this page covers that.

## What carries over (it's in the repository)
- All code, branches, tests, plans, notes, decisions (`plans/overnight-decisions.md`) and handover notes.
- The rules, the merge order, the build numbering, the release steps.

## What does NOT carry over (it belongs to the old account)
| Thing | What the new account does |
|---|---|
| **Running helper sessions** (builders, build master, reviewer) | Can't message or close them. Before switching, the old lead makes every helper push its work and handover note, then stops them. The new lead starts its own fresh helpers, each reading its predecessor's note. |
| **Scheduled check-ins** | Belong to the old account. The old lead disables its own; the new lead creates its own. |
| **Published links** (the game https://claude.ai/artifact/SmL8Na1iTB2JQZDP4dYdou, the plan pages) | The new account can't update them in place. Either the user shares them with the new account with edit access (from each page's Share menu), or the new lead publishes to new links and the user bookmarks those. The game file itself is always in the repo (`starship-cadet.html` on `claude/ship-integration`), so nothing is lost. |
| **Usage allowance** | Separate per account (that's the point of switching). |
| **GitHub access** | The new account must connect GitHub (claude.ai → Settings → Connectors / the GitHub app) with a login that can push to `Geosync23/Cadet-game`, or the user adds that login as a collaborator on the repository. |
| **Environment** | The new account needs a cloud environment with the same setup (network access to cdnjs and npm for three.js; Chromium/Playwright is pre-installed). |

## Steps
**On the old account (the outgoing lead), before switching:**
1. Finish or pause at a quiet point (between merges, never mid check run).
2. Every helper pushes its work and handover note; the build master pushes `plans/cand-<build>-results.md`.
3. Write the "HANDOVER TO LEAD n" section in `plans/handover-lead.md`, noting "new account" and every live link.
4. Disable the old lead's scheduled check-in; stop (archive) the helpers.

**On the new account:**
1. Connect GitHub; make sure the repo `Geosync23/Cadet-game` is reachable.
2. Start one session (it will be at depth 0) on branch `claude/lead-pillar1` with:
   > You are lead N for Starship Cadet, on a new Claude account (a handoff to share usage). Work on branch claude/lead-pillar1. Read CLAUDE.md, then the last "HANDOVER TO LEAD" section of plans/handover-lead.md, then plans/handover-new-account.md, TEAM.md and DEV_NOTES.md. The old account's helpers and scheduled check-ins are gone: start your own as needed (helpers never start sessions; you do). Put your session id and depth in TEAM.md, set up an hourly check-in, and say hello to me in plain language.
3. The new lead re-hires only the seats the next step needs, each reading its predecessor's `plans/handover-<role>.md`.

## The session chain rule (same on any account)
Leads are always level 0 (started by the user) or level 1 (started by a level-0 lead); a level-1 lead never starts another lead (it asks the user). Helpers are started only by the lead, never by helpers.
