import random, sys
N=6
def groups_ok(board):
    seen=set()
    for (r,c),(o,m) in board.items():
        if (r,c) in seen: continue
        g=flood(board,(r,c)); seen|=g
        if len(g)>=3: return False
    return True
def flood(board,s):
    o,m=board[s]; st=[s]; g={s}
    while st:
        r,c=st.pop()
        for dr,dc in((1,0),(-1,0),(0,1),(0,-1)):
            q=(r+dr,c+dc)
            if q in board and q not in g and board[q]==(o,m): g.add(q); st.append(q)
    return g
def deal(rng):
    while True:
        marks=[0,1,2]*4; rng.shuffle(marks); b={}
        for i,m in enumerate(marks):
            r,c=divmod(i,6); b[(r,c)]=(0,m); b[(5-r,5-c)]=(1,m)
        if groups_ok(b): return b
def moves(b,hold,p):
    fw=1 if p==0 else -1; home=(0,1) if p==0 else (4,5); out=[]
    for (r,c),(o,m) in list(b.items()):
        if o!=p: continue
        for dc in(-1,1):
            q=(r+fw,c+dc)
            if 0<=q[0]<N and 0<=q[1]<N and q not in b: out.append(('step',(r,c),q))
        for dr in(-1,1):
            for dc in(-1,1):
                a=(r+dr,c+dc); q=(r+2*dr,c+2*dc)
                if a in b and b[a][0]!=p and 0<=q[0]<N and 0<=q[1]<N and q not in b: out.append(('jump',(r,c),q,a))
    for i,m in enumerate(sorted(set(hold[p]))):
        for r in home:
            for c in range(N):
                if (r,c) not in b: out.append(('launch',m,(r,c)))
    return out
def apply(b,hold,p,mv,dock_any):
    b=dict(b); hold=[list(hold[0]),list(hold[1])]
    if mv[0]=='step': b[mv[2]]=b.pop(mv[1]); t=mv[2]
    elif mv[0]=='jump': b[mv[2]]=b.pop(mv[1]); hold[p].append(b.pop(mv[3])[1]); t=mv[2]
    else: hold[p].remove(mv[1]); b[mv[2]]=(p,mv[1]); t=mv[2]
    sc=0
    if dock_any or mv[0]=='launch':
        g=flood(b,t)
        if len(g)>=3:
            for q in g: del b[q]
            sc=len(g)
    return b,hold,sc
def pick(level,b,hold,p,ms,rng,dock_any):
    if level=='easy' and rng.random()<.5: return rng.choice(ms)
    best=None;bs=-1
    for mv in ms:
        _,_,sc=apply(b,hold,p,mv,dock_any)
        if sc>bs: bs=sc;best=mv
    if bs>0: return best
    js=[m for m in ms if m[0]=='jump']
    return rng.choice(js) if js else rng.choice(ms)
def game(rng,lv,dock_any):
    b=deal(rng); hold=[[],[]]; s=[0,0]; last=None; turns=0
    for t in range(28):
        p=t%2; ms=moves(b,hold,p)
        if not ms: break
        mv=pick(lv[p],b,hold,p,ms,rng,dock_any); b,hold,sc=apply(b,hold,p,mv,dock_any); turns+=1
        if sc: s[p]+=sc; last=p
        if s[p]>=7: return p,turns,s
    if s[0]!=s[1]: return (0 if s[0]>s[1] else 1),turns,s
    if last is not None: return last,turns,s
    n=[sum(1 for v in b.values() if v[0]==q)+len(hold[q]) for q in(0,1)]
    return (None if n[0]==n[1] else (0 if n[0]>n[1] else 1)),turns,s
for dock_any in (True,False):
  for lv in (('easy','easy'),('medium','medium')):
    rng=random.Random(1); w=[0,0,0]; T=0; capped=0
    G=2000
    for i in range(G):
        r,t,s=game(rng,lv,dock_any); w[2 if r is None else r]+=1; T+=t; capped+= (max(s)<7)
    print('dock after any move' if dock_any else 'dock only on launch', lv[0], 'P1 wins %.1f%% draws %.1f%% turns %.1f ended without 7: %.0f%%'%(100*w[0]/G,100*w[2]/G,T/G,100*capped/G))
