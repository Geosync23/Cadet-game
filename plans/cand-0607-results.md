# 0.60.7 check results

Built on claude/cand-0606 (from 0.60.6a c8685cf). One line per finished check (check, game commit, OK/FAIL, key numbers). A new build master reruns only what is missing here.

- trial: deck hook dba2627 + writer hook 7e4fb1e merge clean on cand-0606 (c8685cf + results), NAMES OK
- trial: writer c2b1b6a (0.48.81) merges clean; baked 8047 lines (was 7515); --check up to date; lines_check PASS (0 err, 2 warn); NAMES OK
- trial: arrival 31c6516f + writer 5916bd5 merge clean, bake 8084 lines, lines_check PASS, NAMES OK; KEY MISMATCH: code asks walk.train.<job>.<step> (31539) + walk.follow.N (31548), writer has walk.job.* + walk.talk.1-29
- trial: arrival 31c6516f + writer a76e232: keys match (walk.train.<9 jobs>.<take|fetch|make|at|done|turnin>, walk.follow.1-29), bake 8093 lines, lines_check PASS
- trial: arrival e2cd435e (0.42.32) + writer 2729ce1: clean, bake 8093, lines_check PASS, NAMES OK
