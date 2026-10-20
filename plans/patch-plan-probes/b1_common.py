from pp import *
DLG = "(() => { if (!DIALOGUE) return null; const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(0); else dialogueNext(); return DIALOGUE ? DIALOGUE.id : 'end'; })()"
def to_day1(g, at=6*60):
    g.step(10); sign(g); g.secs(2)
    g.ev("(() => { introSkip(); SHIP.intro.ended = false; SHIP.intro.skipped = false; })()"); g.step(5)
    g.ev(f"(() => {{ goToDeck(4); player.obj.position.copy(cellPos(...DECKS[4].places.find(p => p.id === playerBed()).at)); sleepUntil({at}); nightT = nightAt(); }})()")
    g.step(10)
def tele(g, deck, tile):
    g.ev(f"(() => {{ if (deckDef.num !== {deck}) goToDeck({deck}); let c = {list(tile)}; if (!free(...c)) {{ const p = cellPos(...c); c = nearestOpen(p.x, p.z, player) || c; }} player.obj.position.copy(cellPos(...c)); player.path.length = 0; target.copy(player.obj.position).setY(.7); }})()")
    g.step(3)
GOAL = "(() => ({ t: clockText(), goal: IX_GOAL && (IX_GOAL.label + (IX_GOAL.trk ? ' [trk ' + IX_GOAL.trk + ']' : '')), introArrow: INTRO_UI.arrow, want: introArrowWant(Math.floor(shipNow())), clocked: careerClockedIn(1), dlg: DIALOGUE && DIALOGUE.id, room: roomAt(...player.here()), lab: document.getElementById('ixGoal').hidden ? '(hidden)' : document.getElementById('ixGoal').children[2].textContent }))()"
