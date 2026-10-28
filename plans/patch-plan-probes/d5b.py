from pp import *
g = start('?nosave&debug')
g.step(10)
g.ev("player.obj.position.copy(cellPos(20,15)); target.copy(player.obj.position).setY(.7)"); g.step(40)
def scr(x,y,z): return g.ev(f"(() => {{ const v = new THREE.Vector3({x},{y},{z}).project(camera); return [ (v.x+1)/2*innerWidth, (1-v.y)/2*innerHeight ]; }})()")
p = g.ev("(() => { const e = EDGES.get('h,20,14'); const a = cellPos(20,14); return [a.x, a.z - .5]; })()")
s = scr(p[0], .08, p[1]); print(s)
g.page.mouse.click(s[0], s[1]); g.step(20)
print(g.ev(STATE))

# the ladder itself behind glass
q = g.ev("(() => { const a = cellPos(20,13); return [a.x, a.z]; })()")
s = scr(q[0], 1.0, q[1]); g.page.mouse.click(s[0], s[1]); g.step(20); print(g.ev(STATE))
g.snap('05-ladder-hatch'); g.close()
