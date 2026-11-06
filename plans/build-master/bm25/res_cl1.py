# res_cl1.py : CL1's two game clashes (RV33's recipe)
import pathlib
p=pathlib.Path('starship-cadet.html'); L=p.read_text().split('\n'); out=[]; i=0; n=0
while i<len(L):
    if L[i].startswith('<<<<<<< '):
        m=L.index('=======',i); e=next(j for j in range(m,len(L)) if L[j].startswith('>>>>>>> ')); o,t=L[i+1:m],L[m+1:e]
        if t and t[-1].startswith('const CAL997_ON'):
            assert o[0].startswith('const TRAD995_ON') and t[0].startswith('const TRAD995_ON'); out += t + o[1:]
        elif t and 'cl997LeadMinute' in t[-1]:
            assert len(o)==1 and 'eventsDecor(now)' in o[0]; out += o + t[1:]
        else: raise SystemExit('unknown block at %d' % i)
        n+=1; i=e+1
    else: out.append(L[i]); i+=1
p.write_text('\n'.join(out)); print('blocks', n)
