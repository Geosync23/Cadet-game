import re,sys
L=open(sys.argv[1]).read().split('\n'); keys={}; inside=False
for n,l in enumerate(L,1):
    if re.match(r'^(const KIT = \{|Object\.assign\(KIT, \{)',l): inside=True; continue
    if inside and re.match(r'^\}\);?\s*$|^\};?\s*$',l): inside=False; continue
    if inside:
        m=re.match(r'^  ([A-Za-z_$][\w$]*)\s*(:|\()',l)
        if m: keys.setdefault(m.group(1),[]).append(n)
d={k:v for k,v in keys.items() if len(v)>1}
print('KIT keys:',len(keys),'duplicates:',d if d else 'none')
