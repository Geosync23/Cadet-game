# union.py TIP: M1's 24a-24d and M2's 24e/24f blocks (game file) and their mech_check PARTS: ours, then theirs
import sys; tip=sys.argv[1]
for p, start, sep in (('starship-cadet.html', '<<<<<<< HEAD\n// 24a ROUNDS', '\n\n// ---------------------------------------------------------------------\n'),
                      ('mech_check.py', '<<<<<<< HEAD\n# 24a rounds', '\n\n')):
    s = open(p).read()
    if start not in s: continue
    a = s.index(start); b = s.index('\n=======\n', a); c = s.index('\n>>>>>>> ' + tip + '\n', b)
    s = s[:a] + s[a+13:b] + sep + s[b+9:c] + s[c+len('\n>>>>>>> ' + tip):]
    open(p, 'w').write(s); print('union', p)
