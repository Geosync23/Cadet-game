# PR5: plant mutants in the head build and run fridays_check on each; a mutant is caught when the check exits 1
import sys, subprocess, pathlib, os
S = '/tmp/claude-0/-home-user/a4344e06-66ec-50a3-8125-a9cc15d32fe0/scratchpad'
H = pathlib.Path(S + '/w/head'); src = (H / 'starship-cadet.html').read_text()
M = {
 'm1_nolead': ("  if (p.id === 'marrow') return at - 30;\n  const L", "  return at;\n  const L"),
 'm2_noring': ("used = new Set(FRI.ring.filter(r => r[0] < w && r[0] >= w - 6).flatMap(r => r.slice(1)));", "used = new Set();"),
 'm3_noheard': ("    FRI.heard = d;\n", "\n"),
 'm4_nohush': ("    if (typeof CHATTER_AT !== 'undefined') CHATTER_AT = simNow();   // the crowd hushes", "    // the crowd hushes"),
 'm5_saveoff': ("if (SHORT_FRIDAY) {\n  const s = SAVED && SAVED.fri", "SAVE_EXTRA.push(save => { save.fri = FRI; });\nif (SHORT_FRIDAY) {\n  const s = SAVED && SAVED.fri"),
 'm6_notoday': ("  if (FRI.today && FRI.today[0] === d) {", "  if (false) {"),
 'm7_dur': ("e.tag === 'ev-captains-address' ? e.at + e.dur - t : e.dur", "e.dur"),
 'm8_mailtwice': ("  if (FRI.heard === d || FRI.mailed === d) return;", "  if (FRI.heard === d) return;"),
 'm9_nolen': ("return ok && text.length <= max ? text : null;", "return ok ? text : null;"),
 'm10_vance_late': ("F.workEnd + (p.id === 'vance' ? 2 : 8)", "F.workEnd + (p.id === 'vance' ? 20 : 8)"),
}
names = sys.argv[1:] or list(M)
for n in names:
    a, b = M[n]; assert src.count(a) == 1, (n, src.count(a))
    d = pathlib.Path(S + '/mut/' + n); d.mkdir(parents=True, exist_ok=True)
    for f in ('cadet_test.py', 'fridays_check.py'): (d / f).write_text((H / f).read_text())
    (d / 'starship-cadet.html').write_text(src.replace(a, b))
    r = subprocess.run(['python3', 'fridays_check.py', 'starship-cadet.html'], cwd=d, capture_output=True, text=True)
    fl = [l for l in r.stdout.splitlines() if 'FAIL' in l]
    print(n, 'CAUGHT' if r.returncode == 1 else 'MISSED (rc %d)' % r.returncode, fl[:4], flush=True)
