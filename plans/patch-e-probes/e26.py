# patch #26 probe: First Light Cocoa. GAME=..., Q='&firstlight&mug'
import sys, os; sys.path.insert(0, '/home/user/Cadet-game/plans/patch-plan-probes')
from pp import *
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
g = start('?nosave&debug' + os.environ.get('Q', '')); g.step(5)
print('on Day 1:', g.ev("eventsOn(1).map(e => e.id + ' ' + hhmm(e.from % 1440) + '-' + hhmm(e.to % 1440))"))
print('raman, zeke, tomas plans:', g.ev("['raman', 'torres-zeke', 'tomas', 'holt'].map(id => { const p = schedPeople().find(x => x.id === id); return id + ': ' + planDay(p, 1).filter(s => /^ev-/.test(s.tag || '')).map(s => s.tag + ' ' + hhmm(s.from % 1440) + ' ' + s.placeId).join(', '); })"))
g.ev("skipTo(18*60+20)"); g.ev("goToDeck(3)"); g.step(5)
z = g.ev("(() => { const a = DECK_CREW.find(a => a.p.id === 'torres-zeke'); return a ? [a.x, a.z, a.goalId] : null; })()"); print('Zeke at dinner:', z)
if z: g.ev(f"(() => {{ const c = nearestOpen({z[0]} + .8, {z[1]} + .8, player); player.obj.position.copy(cellPos(...c)); target.copy(player.obj.position).setY(.7); }})()")
g.secs(2)
print('invite:', g.ev("({ asked: flag('firstlight.asked'), appts: SHIP.device.appts.filter(a => a.trad === 'first-light').map(a => [a.by, hhmm(a.at % 1440), a.status, a.where]), bubble: [...document.querySelectorAll('.bubble, #bubbles div')].map(b => b.innerText).filter(Boolean).slice(0, 3) })"))
g.page.screenshot(path=OUT + '/26-invite.png')
g.ev("skipTo(20*60+5)"); g.ev("goToDeck(3)"); g.step(5)
g.ev("(() => { const t = (ROOM_TILES['L'] || []).find(c => free(...c) && !occupiedBy(player).has(K(c))); player.obj.position.copy(cellPos(...t)); target.copy(player.obj.position).setY(.7); })()"); g.secs(3)
print('in the lounge:', g.ev("({ on: !!tradOn('first-light'), here: DECK_CREW.filter(a => /^ev-first-light/.test(a.tag || '')).map(a => a.p.id + (a.settled ? '' : '~')).slice(0, 16), dim: FLC_DIM })"))
print('join:', g.ev("(() => { const a = DECK_CREW.find(a => a.p.id === 'raman') || DECK_CREW.find(a => /^ev-first-light/.test(a.tag || '')); return a ? [a.p.id, tradJoinTap(a)] : null; })()"))
g.secs(4)
print('after join:', g.ev("({ joined: SHIP.events.joined.slice(-2), dlg: DIALOGUE && DIALOGUE.id, who: DIALOGUE && [...new Set(MEETING_SCRIPTS['firstLightCocoa.today'].lines.map(l => l.who))], drink: SHIP.player.drink, act: ACT && ACT.kind, pose: ACT && ACT.o && ACT.o.pose, dim: +FLC_DIM.toFixed(2), bed: IX_GOAL && IX_GOAL.label })"))
g.page.screenshot(path=OUT + '/26-joined.png')
g.secs(15); g.page.screenshot(path=OUT + '/26-seated.png')
print('seated:', g.ev("DECK_CREW.filter(a => /^ev-first-light/.test(a.tag || '') && a.settled).map(a => a.p.id + ':' + crewPose(a)).slice(0, 12)"))
print('light now / without the dim:', g.ev("(() => { const a = +hemi.intensity.toFixed(3); const k = FLC_DIM; FLC_DIM = 0; applyLight(nightT); const b = +hemi.intensity.toFixed(3); FLC_DIM = k; applyLight(nightT); return [a, b]; })()"))
steps = []
for k in range(25):
    v = g.ev("(() => { const v = DIALOGUE && dialogueView(); return v ? JSON.stringify(Object.keys(v)) + ' ' + (v.who || '') + ': ' + (v.text || '').slice(0, 40) + ' | ' + (v.choices || []).map(c => JSON.stringify(c).slice(0, 60)).join(' / ') : null; })()")
    if not v: break
    steps.append(v)
    if '"choices"' in v and ' / ' in v:
        g.ev("dialogueStep(1)")
    else:
        g.ev("dialogueStep()")
    g.step(3)
print('script:'); [print('  ', x[:160]) for x in steps]
print('after:', g.ev("({ dlg: DIALOGUE && DIALOGUE.id, raman: relGet('raman').pts, tomas: relGet('tomas').pts, mem: (SHIP.rel.raman && SHIP.rel.raman.known || []).slice(-3), dimSoon: FLC_DIM })"))
g.secs(5); print('dim after:', g.ev("FLC_DIM"), 'bed arrow:', g.ev("IX_GOAL && IX_GOAL.label"))
print('errors', g.errors[:5]); g.close()
