# res_cl1_docs.py : CL1's design-doc clash (Saturday run cut + TB6's loaf) and the backlog rows
import pathlib
p=pathlib.Path('design-doc.md'); L=p.read_text().split('\n')
a=L.index('<<<<<<< HEAD'); m=L.index('=======',a); e=next(j for j in range(m,len(L)) if L[j].startswith('>>>>>>> '))
o,t=L[a+1:m],L[m+1:e]; assert len(o)==1 and len(t)==1 and 'cut 2026-11-06' in t[0] and 'Your loaf to eat' in o[0]
loaf = o[0][o[0].index(' **Your loaf to eat**'):]
L[a:e+1]=[t[0] + loaf]; assert '<<<<<<< HEAD' not in L; p.write_text('\n'.join(L))
