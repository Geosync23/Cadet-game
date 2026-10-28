# rec64.py TIP: resolve starship-cadet.html conflicts in the 0.64.0 combine. Default keep both (HEAD then TIP);
# the recTap Lightdisc lines: RB2's net-down refusal, then RA's Cup/WSO and queue lines; the climbing wall: RA's
# free-belay route pick (r0 -> r), then RB2's z line with sh = recShut() and its two refusals on that r
import sys, re; tip = sys.argv[1]; p = 'starship-cadet.html'; s = open(p).read()
pat = re.compile(r'<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> ' + re.escape(tip) + r'\n', re.S)
def fix(m):
    a, b = m.group(1), m.group(2); al, bl = a.splitlines(True), b.splitlines(True)
    if 'recShut().court' in a and 'recCupTap' in b: print('  court'); return al[0] + b
    if 'recShut().court' in b and 'recCupTap' in a:  print('  court (sides swapped)'); return bl[0] + a
    if 'recBelaysFree' in a and 'rec.shut.route' in b: print('  wall'); return al[0] + al[1] + bl[1] + bl[2] + bl[3]
    if 'recBelaysFree' in b and 'rec.shut.route' in a: print('  wall (sides swapped)'); return bl[0] + bl[1] + al[1] + al[2] + al[3]
    print('  keep both:', a.splitlines()[0][:70]); return a + b
s, n = pat.subn(fix, s); open(p, 'w').write(s); print('resolved', n)
