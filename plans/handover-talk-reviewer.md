# Handover: the Talk a while reviewer (TR1)

**Role:** TR1, the careful reviewer of the "Talk a while" pack, started by lead 20 (session_019UJSCUCdtC1kTpYiABWKhs).
Report to the lead with `send_message`; never contact the user; never touch main, the main game link or the writer's
files. **Branch:** `claude/talk-pack-review` (push only there). My session: session_01T93VUcBukQwhBLu8vCNUhV.
**Others:** writer TW1 (session_019ek4xmi5Yp9xijbzuAo2kN, `claude/talk-pack`); talk engineer TE1
(session_01MnQHVrsK5wnTwfEi2QFm4W, `claude/talk-wire`).

## What I reviewed (all on this branch, under `plans/`)

| File | What | Verdict |
| --- | --- | --- |
| `talk-pack-review.md` | the first pack (160 talks: 100 shared pool, 15 × 4 own, small talk) at f6005cf, and its plan | 7 blockers, 38 should-fix, 30 nits; TW1 folded them in (95bb299) |
| `work-pools-review.md` | TW1's work-pools plan page (6de6a87) | 0 blockers, 13 should-fix, 12 nits; folded in (1235f51); the user then chose every recommendation (c9357b3) |
| `talk-wire-review.md` | TE1's wiring T1-T3 (f053df0) and, as an addendum, T4 work pools (ebd69b6) | PASS WITH FIXES (both) |
| `work-pools-content-review.md` | the nine work pools (120 talks) at 7d88673 | 0 blockers, 22 should-fix, 12 nits |

## Open items (as of 2026-10-20, 15:20)

1. **TW1: the 22 should-fixes and 12 nits** in `work-pools-content-review.md` (P1-P22, N1-N12). The big three: the
   friend tier turned into a formula (the habit, "who do you do it for" and "nobody knows it was me" talks in every pool:
   P1-P4); 8 word-for-word repeats across the pack and three talks that restate own/shared talks (P5, P6); food in 57 of
   120 work cheers and biscuits in 25 work talks (P7). Then ~15 fact/condition fixes (P8-P22).
2. **TE1: W1** (`talk-wire-review.md`): the "We've talked about everything" small-talk opener can come while talks are
   only waiting (tier-gated). Fix: `const left = TALK_SOURCES.some(s => s.talks(p).some(tk => !T.fired[tk.id]));` and
   `done = !left && ...`. **W7:** `talk_check.py` crashes once work files are baked (`KeyError` at line 131, part (d)
   builds its condition table from pool + own only) and counts work talks as "own". Nits W2-W6, W8.
3. **Lead's questions** (answered or pending with the lead): `TALK_PACK_ON` committed on (confirm it's by decision);
   parking the old `talk.<topic>.*` lines now as a marking only (my answer: yes, keep the keys: the switch-off path uses
   them).
4. **My last job (the lead's, 15:20):** a quick re-check of TW1's fixes when they land: spot-check repeats and food
   with `repeats.py`, not a full re-read. Then stop.

## Tools (in `plans/talk-review-tools/`; copies of my scratch scripts)

- `tp.py`: parses every `.talk` file (`talks` list with file, line, slug, who, topic, when, them, ask, replies,
  answers). `python3 plans/talk-review-tools/tp.py shape` checks the shape, card lines ≤ 90 (a placeholder counts 9),
  replies ≤ 44 with no `{...}`, unique ids; `... lines` prints every line as `file:line<TAB>text`.
- `repeats.py`: word-for-word repeated lines across the whole pack; food/tea cheers, biscuit talks, "habit" asks and
  "nobody knows" talks, for work pools and for the rest. **This is the re-check tool.** Run from the repo root on a
  checkout of `claude/talk-pack`.
- `phone_lines.py WORKTREE`: every line of every talk (own, shared, work) and every small-talk line on the real chat
  card at 390 × 844, plus each ask with its three buttons: reports cards off screen, clipped buttons, the tallest card
  and talks no one can fill. Needs a built game in WORKTREE (content_gen run) with TE1's wiring.
- `turns.py WORKTREE`: plays 20 days of picks for six people and prints the source order (own → work/shared taking
  turns → small talk).
- `done_check.py WORKTREE OUTDIR`: reproduces W1 (a stranger's "done" openers while pool talks wait) and screenshots the
  longest greeting + opener card.
- These three use `cadet_test.py`'s `Game` (exec'd from the worktree), so run them with
  `CADET_CHROME=/opt/pw-browsers/chromium CADET_WORK=/tmp/cadet-work/<lane>`.

## Gotchas

- **Setting up the checks in a fresh cloud session:** `pip install playwright`; `CADET_CHROME=/opt/pw-browsers/chromium`
  (never `playwright install`); `CADET_WORK` needs `three/` (`npm pack three@0.128.0`, untar) and `acorn/`
  (`npm pack acorn@8.12.1`, untar), as DEV_NOTES "Testing" says. check_fast takes 4-8 minutes.
- To test the pack in the game, I merge `claude/talk-pack` into a detached worktree of `claude/talk-wire`
  (`git worktree add <scratch>/wire origin/claude/talk-wire`, then `git merge origin/claude/talk-pack`,
  `python3 content_gen.py starship-cadet.html`), never pushing it.
- Ids are frozen once baked (`pool.<topic>.<slug>`, `<crewId>.<slug>`, `work.<pool>.<slug>`): rewording keeps an id;
  replacing a talk with a different one needs a new slug (before release, renaming was fine).
- Canon to check against: `content/facts.md` (sections 3, 4d, 5, 6, 9-11), the roster in the game (`ROSTER` JSON rows,
  incl. `thread`, `habits`, `aboard` and `ROSTER_ROTATIONS`: who leaves when), the voice cards, `content/arcs/*.arc`
  and `outlines.md` (what each beat tells), `content/themes/*.arc` (the struggle themes' beats), `design-doc.md` (no
  lunch; two meals). The player's family is fixed: Mum, Gran, Jo (older sibling), Sam (best friend).
- The talk pack's own decisions: once per save (the user, 2026-10-20); work and shared take turns; friend-tier work
  talks are about what the job means, ending warm; Works treats you as a workmate.

## How I rate

Blocker = spoils an arc or theme early, repeats an arc beat word for word, or broken text for many crew. Should fix =
a fact that contradicts the game or canon, a condition missing, a repeat the player will notice, voice drift. Nit =
wording, small consistency. Each finding has `file:line` and a proposed replacement in the speaker's voice.

## Final state (TR1, 2026-10-20 15:25): the spot-check of TW1's fixes (df61ae2)

`repeats.py` on `claude/talk-pack` df61ae2: 280 talks, ids unique, shape clean. Word-for-word repeats **8 → 2**: "Who
said it?" (button text, kept on purpose, N2) and "The first hour of shift, before it's busy." (`work-bridge:103` and
`work-watch:213`: the second came from my own P2 suggestion; change one). Work-pool cheers about food or tea **57 → 24**
of 120; biscuit talks **25 → 5**; "habit" asks **6 → 3**; "nobody knows" talks **10 → 6**. Spot-checked fact fixes are in:
`!moved:` for Lindqvist, Zamora and Ueda; onions, tea-corner and bay-quiet skips; night-survey is Ibarra's; Thursday
checks `!rank:junior`; Hart's first watering; the player's gran's marrows; the engine-room line. TE1 fixed W1 and W7
(910c257, 838aef0) and is adding `!moved:` to `talkPackFits`. Nothing open for TR1. I've stopped.
