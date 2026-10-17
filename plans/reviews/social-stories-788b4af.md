# Review: social B2's device_check fix (claude/social-stories 788b4af, test only)

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS.**

- "Mail: From home, Play on a recorded message": with section 20c's real `mailPlayable`, Play shows only while Gran
  has a waiting recorded message. The check now sets `homeC('gran').msg = { day, i: 0, done: false }` when Gran is a
  home contact, and puts `SHIP.social.stories.home` back afterwards (or deletes it if there was none). With 20c but
  no home data, it only checks that plain mail has no Play. Sound.
- On the 0.60.3 candidate's page (claude/cand-0603 eb75e1a), this device_check: the "From home" case now **passes**.
  The only failure left is "heads-up: as it starts, once", the known Late-piano window case fixed by device 24f1920.
- Note: this device_check can't run against claude/social-stories' own page (build 0.39.22): it stops at
  `devHeadsReset is not defined`, because that page has no device heads-ups. It's meant for combined builds, which is fine.
- build master 2 carries the same fix (and 24f1920's three heads-up lines) on claude/cand-0603. Who carries it to
  claude/device is for the lead: reviewers don't write to other seats' branches.
