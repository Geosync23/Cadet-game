import sys; tip=sys.argv[1]; p='starship-cadet.html'; s=open(p).read()
a=s.index('<<<<<<< HEAD\n'); b=s.index('>>>>>>> '+tip+'\n',a)+len('>>>>>>> '+tip+'\n')
blk=s[a:b]
if not ('bedText(text)' in blk and 'tipShow(id, tx)' in blk): sys.exit(1)
new="""    let tx = text; if (typeof text === 'function') { try { tx = text(); } catch (e) { tx = null; } }
    if (tipShow(id, bedText(tx))) { POP.tip = POP.card = now; return id; }   // a text may be read when shown (the head writer's, 0.72.5); Bunk 1 names your room (24 core)
"""
open(p,'w').write(s[:a]+new+s[b:])
