# PR5: plant mutants in the head build and run fridays_check on each; a mutant is caught when the check exits 1
import sys, subprocess, pathlib, os
S = '/tmp/claude-0/-home-user/a4344e06-66ec-50a3-8125-a9cc15d32fe0/scratchpad'
H = pathlib.Path(S + '/w/' + os.environ.get('MH', 'head')); src = (H / 'starship-cadet.html').read_text()
M = {
 't1_nodip': ("repAdd(null, 0, { work: -2 }, 'address');", ";"),
 't2_dipleave': ("typeof playerShiftOn === 'function' && playerShiftOn(d) && typeof repAdd", "typeof repAdd"),
 't3_nodinner': ("return MEALS.dinner[0] + Math.round(50 * schedU(p.seed, d, 1184));", "return null;"),
 't4_flagsaved': ("delete save.flags.shortFriday;", ";"),
 't5_noflag': ("  flagSet('shortFriday');", "  ;"),
 't6_nightkeys': ("return SHORT_FRIDAY ? [k(1), k(2), k('friday.1'), k('friday.2'), k(3), k(4)]", "return false ? 0"),
 't7_reccap': ("m >= dayShiftEnd(d) || m < 540 ? REC_CAP.busy", "m >= 1020 || m < 540 ? REC_CAP.busy"),
 't8_nohu': ("FRI.hu = d; toast(", "FRI.hu = d; (() => 0)("),
}
names = sys.argv[1:] or list(M)
for n in names:
    a, b = M[n]; assert src.count(a) == 1, (n, src.count(a))
    d = pathlib.Path(S + '/mut9/' + n); d.mkdir(parents=True, exist_ok=True)
    for f in ('cadet_test.py', 'fridays_check.py'): (d / f).write_text((H / f).read_text())
    (d / 'starship-cadet.html').write_text(src.replace(a, b))
    r = subprocess.run(['python3', 'fridays_check.py', 'starship-cadet.html'], cwd=d, capture_output=True, text=True)
    fl = [l for l in r.stdout.splitlines() if 'FAIL' in l]
    print(n, 'CAUGHT' if r.returncode == 1 else 'MISSED (rc %d)' % r.returncode, fl[:4], flush=True)
