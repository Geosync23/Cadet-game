# unionall.py TIP FILE...: every conflict -> ours then theirs (whole blocks both kept); for adjacent new blocks only
import sys
tip = sys.argv[1]
for p in sys.argv[2:]:
    s = open(p).read(); n = 0
    while '<<<<<<< HEAD\n' in s:
        a = s.index('<<<<<<< HEAD\n'); b = s.index('\n=======\n', a); c = s.index('\n>>>>>>> ' + tip + '\n', b)
        s = s[:a] + s[a+13:b] + '\n' + s[b+9:c] + s[c+len('\n>>>>>>> ' + tip):]; n += 1
    open(p, 'w').write(s); print('union', p, n)
