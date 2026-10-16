import re,sys
BUILD=sys.argv[1]
for p in ['starship-cadet.html','DEV_NOTES.md','deck_check.py','cadet_test.py']:
    try: s=open(p).read()
    except: continue
    if '<<<<<<<' not in s: continue
    out=[];i=0;L=s.split('\n');bad=False
    while i<len(L):
        if L[i].startswith('<<<<<<<'):
            j=i+1;ours=[]
            while not L[j].startswith('======='): ours.append(L[j]);j+=1
            j+=1;theirs=[]
            while not L[j].startswith('>>>>>>>'): theirs.append(L[j]);j+=1
            blk=ours+theirs
            if all('STARSHIP CADET: CSV Wren' in x for x in blk):
                out.append(re.sub(r'build \S+','build '+BUILD,ours[0]))
            elif all('GAME_BUILD' in x for x in blk):
                out.append(re.sub(r"'[0-9.]+'","'"+BUILD+"'",ours[0]))
            elif p=='DEV_NOTES.md':
                out+=ours+[x for x in theirs if x not in ours]
            else:
                print('UNRESOLVED',p,i+1); out+=L[i:j+1]; bad=True
            i=j+1
        else: out.append(L[i]);i+=1
    open(p,'w').write('\n'.join(out)); print('resolved',p,'(with leftovers)' if bad else '')
