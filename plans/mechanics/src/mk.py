import sys,re
body,out=sys.argv[1],sys.argv[2]
src=open(body).read()
m=re.match(r'TITLE:(.*)\nH1:(.*)\nSUB:(.*)\nNAV:(.*)\n',src); title,h1,sub,nav=[x.strip() for x in m.groups()]; rest=src[m.end():]
css=open(sys.argv[3]).read()
navh=''.join('<a href="#%s">%s</a>'%tuple(x.split('=',1)) for x in nav.split('|'))
html=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
{css}</style>
</head>
<body>
<header>
  <h1>{h1}</h1>
  <div class="sub">{sub}</div>
</header>
<nav><div>{navh}</div></nav>
<main>
{rest}
</main>
</body>
</html>
'''
open(out,'w').write(html); print(out,len(html))
