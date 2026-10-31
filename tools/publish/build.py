import sys
src=open(sys.argv[1]).read()
def rep(s,a,b):
    assert s.count(a)==1,(a,s.count(a)); return s.replace(a,b)
T='<title>Starship Cadet: CSV Wren</title>'
p=rep(src,T,'<title>Starship Cadet Playtest</title>')
open('play/starship-cadet-playtest.html','w').write(p)
DEV='<script>/* published Dev page: Dev mode always on (not in the repo) */try{if(!location.hash.slice(1).split(".").some(t=>(t.includes("-")?t.slice(0,t.indexOf("-")):t)==="dev"))history.replaceState(null,"",location.pathname+location.search+"#dev");}catch(e){}</script>'
d=rep(src,T,'<title>Starship Cadet Dev</title>')
d=rep(d,'<meta charset="utf-8">','<meta charset="utf-8">'+DEV)
open('dev/starship-cadet-dev.html','w').write(d)
