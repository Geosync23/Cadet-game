# keepboth.py FILE : resolve row clashes: ours, then theirs' rows whose first cell isn't already in ours
import sys,pathlib
p=pathlib.Path(sys.argv[1]); L=p.read_text().split('\n')
key=lambda r: r.split('|')[1].strip() if r.startswith('|') else r
while '<<<<<<< HEAD' in L:
    a=L.index('<<<<<<< HEAD'); m=L.index('=======',a); b=next(i for i in range(m,len(L)) if L[i].startswith('>>>>>>> '))
    ours=L[a+1:m]; ok={key(r) for r in ours}
    add=[t for t in L[m+1:b] if key(t) not in ok]
    print(sys.argv[1], 'kept', len(ours), '+ added', [key(t) for t in add])
    L[a:b+1]=ours+add
p.write_text('\n'.join(L))
