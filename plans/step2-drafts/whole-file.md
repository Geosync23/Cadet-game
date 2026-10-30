# Draft: keeping the whole one-file game (not applied)

The user's rule (2026-10-20): before the next step, keep the last version of the whole game so it can always be fetched in one piece. With no cut, the file stays whole anyway; this keeps a fixed copy of the rec deck build as the reference point for step 2's changes (slots, the build master's numbering) and for Dev mode.

When lead 20 says the rec deck is published (its final hash, 0.64.x):
1. **Archive copy:** `cp starship-cadet.html archive/starship-cadet-0.64.x-whole.html` in a commit on the shared branch, with its sha256 in the commit message and in DEV_NOTES (`sha256sum`). Never edited afterwards.
2. **Frozen branch:** `claude/whole-file-0.64.x` at the published commit, never pushed to again. Helper sessions can only push to their own branch, so the lead starts a short session on that branch name (or the build master's session creates it from its own branch with `git push origin <hash>:refs/heads/claude/whole-file-0.64.x` if its permissions allow; tags are refused, as the split plan found). A GitHub Release tag stays skipped (the user's call).
3. **Check:** `git show claude/whole-file-0.64.x:starship-cadet.html | sha256sum` equals the archive copy's and the published page's.
4. Note both in TEAM.md and the roadmap's step 2 checklist.

Size: the archive copy adds ~5.1 MB (the file at 0.64.2) to the repository once (git stores it as one object; later edits to the live file don't touch it).
