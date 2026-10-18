import sys
p='starship-cadet.html'; tip=sys.argv[1]; s=open(p).read()
a=s.index('<<<<<<< HEAD\n'); b=s.index('\n=======\n',a); c=s.index('\n>>>>>>> '+tip+'\n',b)
ours=s[a+len('<<<<<<< HEAD\n'):b]; theirs=s[b+len('\n=======\n'):c]
assert ours.startswith('// 24. WORK') and theirs.startswith('// 24g.'), 'unexpected conflict'
sep='// =====================================================================\n'
s=s[:a]+ours+'\n\n'+sep+theirs+s[c+len('\n>>>>>>> '+tip):]
assert '<<<<<<<' not in s; open(p,'w').write(s); print('24 core + 24g/24k resolved')
