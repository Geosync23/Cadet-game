# Review: the time-jump pair, sim 2f6d8dd (0.26.27) + social 45b0595 (0.36.49)

Reviewer 1, 2026-10-17. On my full merge of arrival 1353f42 + sim 2f6d8dd (which carries section 17) + crew 98df62f + social 45b0595 + social B 31f8aea: name_check OK.

**Verdict: sim PASS. Social PASS WITH FIXES (a test-only fix).**

## Fixed (checked)
- `simNote` keeps a sender's time (`t` from `data.t` when finite), and section 17 stamps its notes with the machine hour.
- **The time-jump comparison now passes on the full merge:** `Two days in one jump the same as hour by hour (with bus notes): True`. My own run of the same comparison in a fresh page also comes out identical (no fields differ).

## 1. Social, SHOULD FIX (test only): social_check's purity test wipes the real bonds, so it fails on the full merge
- social_check (45b0595) on the full merge: `FAIL affBand, moodOf or purity wrong`. Each query, called on its own and checked with `socSave()` before and after, is pure. The failure is the test itself: at line 152 it sets test bonds and then `SHIP.social.bonds = {}` instead of putting the old ones back.
- Since 0.36.46, couples start at affinity 90, so with the crew designer's couples social B forms bonds within the first hours. After the two-day run: `navarro-mateo:yoon-elif`, `rahman-farah:hart-ravi`, `soto-marta:abara-rosa` and `chen-carmen:yilmaz-karin`, all `best`. The test then wipes them, and `pure` is false.
- Fix: `const B0 = SHIP.social.bonds;` before setting the test bonds, and `SHIP.social.bonds = B0;` after.
- Design note for social B (B6): the couples become `best` friends, not a `couple` bond. `bondOf(id, 'couple')` still answers from the roster's `partner`, but `{best}` lines will name a person's partner. Expected until B6 adds `couple` bonds.

## Still open (the sim engineer now owns section 17)
- **`kind` is still overwritten by `simNote`** (`Object.assign(copy, { kind, t })`), and the repair note still sends `kind: j.kind`. Every repair cue in play is `repair.repair`, so a writer's `cue('repair.oven')` never fires. The agreed fix: rename it to `mkind` in section 17, and have social's cue key read `machineById(d.machine).kind` first. See notes-bus-contract-0601.md, finding 1.
