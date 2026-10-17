# "Jump, keep, match": jumps take the tile into your hand; drops; own same-mark clusters bank.
import random
from statistics import mean
MARKS=3
ORTH=((1,0),(-1,0),(0,1),(0,-1))
class R3:
    def __init__(s,**k):
        s.N=6; s.rows=2; s.steps='fwd3'; s.jumps='orth4'; s.drop='home'; s.target=7; s.rounds=14
        s.minc=3; s.layout='fixed'; s.tie='hand'; s.hand0=(0,0); s.dropmatch=True; s.shape='cluster'
        s.bankscore='each'; s.marks=3
        s.__dict__.update(k)
def setup(R,rng):
    N=R.N
    while True:
        b=[[None]*N for _ in range(N)]
        for r in range(R.rows):
            for x in range(N):
                m=(x+r)%R.marks if R.layout=='fixed' else rng.randrange(R.marks)
                b[r][x]=(0,m); b[N-1-r][N-1-x]=(1,m)
        if R.layout=='fixed' or not any(group(b,R,x,y) for y in range(N) for x in range(N) if b[y][x]): return b
def group(b,R,x,y):
    N=R.N; p,m=b[y][x]
    same=lambda c: c and c[0]==p and c[1]==m
    if R.shape=='cluster':
        seen={(x,y)}; st=[(x,y)]
        while st:
            cx,cy=st.pop()
            for dx,dy in ORTH:
                q=(cx+dx,cy+dy)
                if 0<=q[0]<N and 0<=q[1]<N and q not in seen and same(b[q[1]][q[0]]): seen.add(q); st.append(q)
        return seen if len(seen)>=R.minc else set()
    out=set()
    for dx,dy in ((1,0),(0,1)):
        cells=[(x,y)]
        for s in (1,-1):
            cx,cy=x+dx*s,y+dy*s
            while 0<=cx<N and 0<=cy<N and same(b[cy][cx]): cells.append((cx,cy)); cx+=dx*s; cy+=dy*s
        if len(cells)>=R.minc: out|=set(cells)
    return out
def SD(R,f):
    return {'fwd3':[(-1,f),(0,f),(1,f)],'diag':[(-1,f),(1,f)],'fwdside':[(0,f),(1,0),(-1,0)],'orth4':list(ORTH),
            'all8':[(a,c) for a in(-1,0,1) for c in(-1,0,1) if a or c]}[R.steps]
def JD(R,f):
    return {'orth4':list(ORTH),'diag4':[(1,1),(1,-1),(-1,1),(-1,-1)],'all8':[(a,c) for a in(-1,0,1) for c in(-1,0,1) if a or c],
            'fwd3':[(-1,f),(0,f),(1,f)]}[R.jumps]
def moves(st,R,p):
    b,hand=st; N=R.N; f=1 if p==0 else -1; out=[]
    for y in range(N):
        for x in range(N):
            c=b[y][x]
            if not c or c[0]!=p: continue
            for dx,dy in SD(R,f):
                nx,ny=x+dx,y+dy
                if 0<=nx<N and 0<=ny<N and not b[ny][nx]: out.append(('s',x,y,nx,ny))
            for dx,dy in JD(R,f):
                mx,my,nx,ny=x+dx,y+dy,x+2*dx,y+2*dy
                if 0<=nx<N and 0<=ny<N and not b[ny][nx] and b[my][mx] and b[my][mx][0]!=p: out.append(('j',x,y,nx,ny,mx,my))
    if hand[p]:
        rows=range(N) if R.drop=='any' else ((0,1,2) if p==0 else (N-1,N-2,N-3)) if R.drop=='half' else ((0,1) if p==0 else (N-1,N-2))
        for m in set(hand[p]):
            for y in rows:
                for x in range(N):
                    if not b[y][x]: out.append(('d',m,x,y))
    return out
def apply(st,R,p,mv):
    b,hand=st; b=[r[:] for r in b]; hand=[list(hand[0]),list(hand[1])]; g=0; ev=[]
    if mv[0]=='d':
        _,m,x,y=mv; hand[p].remove(m); b[y][x]=(p,m); at=(x,y); ev.append('drop')
    else:
        x,y,nx,ny=mv[1:5]; b[ny][nx]=b[y][x]; b[y][x]=None; at=(nx,ny)
        if mv[0]=='j':
            mx,my=mv[5],mv[6]; hand[p].append(b[my][mx][1]); b[my][mx]=None; ev.append('take')
    if mv[0]!='d' or R.dropmatch:
        cells=group(b,R,*at)
        if cells:
            g+=len(cells) if R.bankscore=='each' else (1+len(cells)-R.minc); ev.append('bank%d'%len(cells))
            for cx,cy in cells: b[cy][cx]=None
    return (b,hand),g,ev
def cnt(st,p): return sum(1 for r in st[0] for c in r if c and c[0]==p)+len(st[1][p])
def val(st,p): return 0.3*(cnt(st,p)-cnt(st,1-p))
def pick(kind,st,R,p,rng,sc):
    ms=moves(st,R,p)
    if not ms: return None
    if kind=='random' or (kind=='easy' and rng.random()<0.5): return rng.choice(ms)
    if kind=='easy': kind='greedy'
    if kind=='champ': return champ(st,R,p,rng,ms)
    bv=-1e9;best=None
    for m in ms:
        ns,g,ev=apply(st,R,p,m); v=g+val(ns,p)
        if kind=='greedy2':
            worst=-1e9
            for o in moves(ns,R,1-p):
                os_,og,_=apply(ns,R,1-p,o); w=og+val(os_,1-p)
                if w>worst: worst=w
            if worst>-1e9: v-=0.9*(worst-val(ns,1-p))
        v+=rng.random()*0.01
        if v>bv: bv=v;best=m
    return best
def game(R,kinds,rng):
    b=setup(R,rng); st=(b,[[rng.randrange(R.marks) for _ in range(R.hand0[0])],[rng.randrange(R.marks) for _ in range(R.hand0[1])]])
    sc=[0,0]; p=0; pl=0; hist=[]; evs=[]; endby='rounds'; last=-1
    while pl<R.rounds*2:
        m=pick(kinds[p],st,R,p,rng,sc)
        if m is None: endby='stuck'; break
        st,g,ev=apply(st,R,p,m); sc[p]+=g; evs+=ev; pl+=1; last = p if g else last; hist.append(tuple(sc)); p=1-p
        if R.target and max(sc)>=R.target: endby='target'; break
    if sc[0]!=sc[1]: w=0 if sc[0]>sc[1] else 1
    elif R.tie=='hand':
        a,c=cnt(st,0),cnt(st,1); w=-1 if a==c else (0 if a>c else 1)
    elif R.tie=='last':
        if last>=0: w=last
        else:
            a,c=cnt(st,0),cnt(st,1); w=-1 if a==c else (0 if a>c else 1)
    elif R.tie=='p2': w=1
    else: w=-1
    return w,pl,sc,hist,evs,endby
def stats(R,kinds,n=500,seed=11):
    rng=random.Random(seed); W={0:0,1:0,-1:0}; L=[]; cb=0; beh=0; ev={}; ends={}
    for i in range(n):
        w,pl,sc,h,evs,e=game(R,kinds,rng); W[w]+=1; L.append(pl); ends[e]=ends.get(e,0)+1
        for x in evs: k=x if not x.startswith('bank') else 'bank'; ev[k]=ev.get(k,0)+1
        if h:
            mid=h[len(h)//2]
            if mid[0]!=mid[1]:
                beh+=1; lead=0 if mid[0]>mid[1] else 1
                if w not in(-1,lead): cb+=1
    return dict(p1=W[0]/n,p2=W[1]/n,draw=W[-1]/n,plies=mean(L),cb=cb/max(1,beh),ev={k:round(v/n,2) for k,v in ev.items()},ends={k:round(v/n,2) for k,v in ends.items()})
def show(name,R,n=500,K=(('random','random'),('greedy','greedy'),('greedy2','greedy2'))):
    for kinds in K:
        s=stats(R,kinds,n)
        print(f"{name:30s} {kinds[0]:8s} p1 {s['p1']:.3f} p2 {s['p2']:.3f} d {s['draw']:.3f} plies {s['plies']:.1f} cb {s['cb']:.2f} {s['ev']} {s['ends']}",flush=True)

def champ(st,R,p,rng,ms):
    # Hard plus one more ply: my move, their best Hard-style reply, then my best immediate gain.
    bv=-1e9;best=None
    for m in ms:
        ns,g,_=apply(st,R,p,m); v=g+val(ns,p)
        om=moves(ns,R,1-p)
        if om:
            worst=1e9
            for o in om:
                os_,og,_=apply(ns,R,1-p,o)
                mine=max((apply(os_,R,p,x)[1] for x in moves(os_,R,p)),default=0)
                w=-og+0.9*mine+val(os_,p)-val(ns,p)
                if w<worst: worst=w
            v+=0.9*worst
        v+=rng.random()*0.01
        if v>bv: bv=v;best=m
    return best

# The page's exact rules (plans/tiles-plan.html): diagonal steps forward, diagonal jumps both ways,
# shuffled mirrored marks, dock after any step/jump/launch, first to 7, 14 turns each, ties to whoever docked last.
PAGE_RULES=dict(steps='diag',jumps='diag4',layout='random',tie='last',drop='home',target=7,rounds=14)

if __name__=='__main__':
    import sys
    n=int(sys.argv[1]) if len(sys.argv)>1 else 3000  # 3000 reproduces the page table exactly (seed 2026)
    R=R3(**PAGE_RULES)
    print('players            games  first-player  draws  turns  behind-at-half-won')
    for k,m in ((('random','random'),n),(('easy','easy'),n),(('greedy','greedy'),n),(('greedy2','greedy2'),max(1,n//2))):
        s=stats(R,k,m,seed=2026)
        print(f"{k[0]+' vs '+k[1]:18s} {m:5d}  {s['p1']*100:11.1f}%  {s['draw']*100:4.1f}%  {s['plies']:5.1f}  {s['cb']*100:5.0f}%")
    print('(easy = Easy, greedy = Medium, greedy2 = Hard, champ = the rejected champion level)')
