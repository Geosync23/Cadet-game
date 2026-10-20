# TR1's shape/length parser for content/talkpack/*.talk (run from the repo root): python3 plans/talk-review-tools/tp.py shape | lines
import re,glob,os,collections,sys
D='content/talkpack'
talks=[]
for f in sorted(glob.glob(D+'/*.talk')):
    if f.endswith('smalltalk.talk'): continue
    who=None;topic=None;cur=None
    for i,l in enumerate(open(f),1):
        s=l.rstrip('\n')
        if s.startswith('@talks'): who=s.split()[1]
        elif s.startswith('topic:') and cur is None: topic=s.split(':',1)[1].strip()
        elif s.startswith('== '):
            cur={'file':os.path.basename(f),'line':i,'slug':s[3:].strip(),'who':who,'topic':topic,'when':'','them':[],'ask':None,'rep':{},'ans':{}}
            talks.append(cur); last=None
        elif cur is None: continue
        elif s.startswith('topic:'): cur['topic']=s.split(':',1)[1].strip()
        elif s.startswith('when:'): cur['when']=s[5:].strip()
        elif s.startswith('them:'): cur['them'].append((i,s[5:].strip()))
        elif s.startswith('ask:'): cur['ask']=(i,s[4:].strip())
        elif re.match(r'(listen|share|cheer):',s):
            k,v=s.split(':',1); cur['rep'][k]=(i,v.strip()); last=k
        elif s.startswith('  them:'): cur['ans'][last]=(i,s[7:].strip())
def txt(t): return re.sub(r'\s+#\w+$','',t)
def ln(t): return len(re.sub(r'\{\w+\}','x'*9,txt(t)))
mode=sys.argv[1] if len(sys.argv)>1 else 'shape'
if mode=='shape':
    ids=collections.Counter()
    for t in talks:
        tid=('pool.%s.%s'%(t['topic'],t['slug'])) if t['who']=='pool' else '%s.%s'%(t['who'],t['slug'])
        ids[tid]+=1
        if not(1<=len(t['them'])<=3) or not t['ask'] or set(t['rep'])!={'listen','share','cheer'} or set(t['ans'])!={'listen','share','cheer'}:
            print('SHAPE',t['file'],t['line'])
        for i,x in t['them']+[t['ask']]+list(t['ans'].values()):
            if ln(x)>90: print('LONG',t['file'],i,ln(x))
        for k,(i,x) in t['rep'].items():
            if len(x)>44 or '{' in x: print('REPLY',t['file'],i,len(x),x)
    print('talks',len(talks),'dupe ids',[k for k,v in ids.items() if v>1])
    print(collections.Counter(t['who']=='pool' for t in talks))
    tiers=collections.Counter()
    for t in talks:
        if t['who']=='pool':
            m=re.search(r'tier>=(\w+)',t['when']); tiers[m.group(1) if m else 'any']+=1
    print(tiers)
elif mode=='lines':
    for t in talks:
        for i,x in t['them']+[t['ask']]+list(t['rep'].values())+list(t['ans'].values()):
            print('%s:%d\t%s'%(t['file'],i,txt(x)))
