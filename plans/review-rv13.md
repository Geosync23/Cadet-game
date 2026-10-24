# RV13 review notes

Reviewer RV13 (session_016ioWtxM6NJRV4Ck3ADwozc), branch claude/review-rv13 (notes only), under lead 32.
Base for 0.92.3 pieces: claude/integration 364c80cb (0.92.2). Verdicts go to LEAD 32 and BM15.

Queue (patch 0.92.3, plans/patch-0.92.3.md on claude/lead-32):
- DV1: items 13 + 23 (Name on the beam: no signing until people arrive, explaining bubbles; your name with the others)
- FX10: items 21, 24, 29 (more science-area work; many rotating repair jobs; board pointer for hauling/stores)
- FX11: items 17, 25 (pool swim camera; light disc players visible)
- FX13: item 15 wiring (Talk a while: own line pools for the Captain + main characters; the Captain's first welcome)

Each: diff does only what it says; new check lines FAIL without the fix, PASS with it (planted fault); area checks,
check_fast, cadet_test (every pixel diff explained); nothing else changes.

## Status
- Set up ~03:30 UTC: playwright, three r128, acorn 8.12.1 in /tmp/cadet-work. Waiting for shas.
