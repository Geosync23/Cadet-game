# 0.99.6 full round: R6's share (interactions_check whole)

- Candidate: claude/staging-0996 f3dbd11 (game same as 5ac6864 and b97cb98; the later commits are docs only), build 0.99.6.
- Game sha256: f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8 (matches BM24's GO).
- OLD: claude/integration 6475bb30, game sha256 93aed54f...5164 (checked; not needed, nothing failed).
- Setup: own CADET_WORK=/tmp/work-r6, CADET_CHROME=/opt/pw-browsers/chromium, three r128 and acorn via npm pack. Run alone, one browser.

| Check | Result | Key lines |
|---|---|---|
| interactions_check (whole) | OK, exit 0, about 53 min (16:18 to 17:11) | `INTERACTIONS CHECK OK`; draw-call peak while doing things 220; no FAIL lines |

No FAILs, so nothing to compare on OLD. Only a Python SyntaxWarning (an escape in a JS string at interactions_check.py:1262), harmless, as before.

R6: OK.
