import re,sys
p=sys.argv[1]; t=open(p).read()
pat=re.compile(r'<<<<<<< HEAD\n((?:const (?:GAME_BUILD|SHIP_RATE)[^\n]*\n)+)=======\n((?:const (?:GAME_BUILD|SHIP_RATE)[^\n]*\n)+)>>>>>>> [^\n]*\n')
t,n=pat.subn(lambda m:m.group(1),t); open(p,'w').write(t); print('fixed',n)
