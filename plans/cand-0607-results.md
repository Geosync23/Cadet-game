# 0.60.7 check results

Built on claude/cand-0606 (from 0.60.6a c8685cf). One line per finished check (check, game commit, OK/FAIL, key numbers). A new build master reruns only what is missing here.

- trial: deck hook dba2627 + writer hook 7e4fb1e merge clean on cand-0606 (c8685cf + results), NAMES OK
- trial: writer c2b1b6a (0.48.81) merges clean; baked 8047 lines (was 7515); --check up to date; lines_check PASS (0 err, 2 warn); NAMES OK
- trial: arrival 31c6516f + writer 5916bd5 merge clean, bake 8084 lines, lines_check PASS, NAMES OK; KEY MISMATCH: code asks walk.train.<job>.<step> (31539) + walk.follow.N (31548), writer has walk.job.* + walk.talk.1-29
- trial: arrival 31c6516f + writer a76e232: keys match (walk.train.<9 jobs>.<take|fetch|make|at|done|turnin>, walk.follow.1-29), bake 8093 lines, lines_check PASS
- trial: arrival e2cd435e (0.42.32) + writer 2729ce1: clean, bake 8093, lines_check PASS, NAMES OK
- trial: deck hook + systems f351cc3 (0.33.40) + arrival e2cd435e + writer 2729ce1: build lines only, NAMES OK, machine OK, smoke OK
- trial (PE6 52839a6, deck hook, systems f351cc3, social 80116c5, arrival e2cd435e, writer 2729ce1): verify_merge 0, NAMES OK, smoke, social, device, interactions OK; cadet_test vs 0.60.6a: only i_tap0 2978 px (to explain on the full candidate)
- trial + deck 031c0e4 (0.38.24-27, tray return removed) + writer 5b57aa1: verify_merge 0, NAMES OK, bake 8091, food OK, day_check day 1 OK (deck alone doesn't break the tray walk)
- trial + traditions 317e24d (0.34.51): verify_merge 0 (all 7), bake 8091 lines / 34 traditions, NAMES OK, device OK; events FAIL only the known one: day 100 founding, 3-mess-12 shared jovanovic-petra/mbeki-bo 19:00
- trial of 8 (PE6 52839a6, deck 031c0e4, systems f351cc3, social d3e4d04, trad d27980f, ob3 e2cd435e, ob4 0ba0af8, writer 5b57aa1) + 068b8db social_check fix: verify_merge clean (ob3's 3 lines rewritten by ob4 to simNow), bake 8091, NAMES, smoke, newgame, clothes OK; events FAIL known day-100 seat; social FAIL 'Stop or the save wrong' (stop pts 1.5 vs m 1.2) = PE6 52839a6 + social d3e4d04 together (social alone OK)
- trial refresh (trad 6a203fd 0.34.52, ob4 22d88d3 0.42.42, writer bf99520): clean, bake 8268 lines, lines_check PASS, NAMES, smoke, tiles OK; events still FAILs the day-100 seat share (now social's item)
