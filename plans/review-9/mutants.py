# PR9 (from PR8) (PR5's mutants.py): plant mutants in FR3's fix build and run its fridays_check; caught = the check exits 1
import sys, subprocess, pathlib
S = '/tmp/claude-0/-home-user-Cadet-game/c90be8f5-63df-55cd-b247-474233586f38/scratchpad'
H = pathlib.Path(S + '/wt_208581c'); src = (H / 'starship-cadet.html').read_text()
M = {
 'm6_notoday': ("  if (FRI.today && FRI.today[0] === d) {", "  if (false) {"),   # PR5's: friSpeech ignores FRI.today
 'm7_dur': ("e.tag === 'ev-captains-address' ? e.at + e.dur - t : e.dur", "e.dur"),   # PR5's: a late joiner stays e.dur
 'm11_nohook': ("    if (e && from < end && to >= end) friMissed(d, e, end);", "    if (false) friMissed(d, e, end);"),   # no SIM_ADVANCE path
 'm12_mailnow': ("friMissed(d, e, end);\n", "friMissed(d, e, to);\n"),   # the jump's Mail stamped at the jump's end
 'm13_nodip': ("  if (typeof playerShiftOn === 'function' && playerShiftOn(d) && typeof repAdd === 'function') repAdd(null, 0, { work: -2 }, 'address');\n  const A = friScript(d)", "  const A = friScript(d)"),   # the dip gone
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
