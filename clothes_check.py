# Starship Cadet: clothes and laundry check (section 21b, onboarding engineer 4, 0.42.40)
# Run:  CADET_CHROME=/opt/pw-browsers/chromium python3 clothes_check.py BUILD.html     (about 2 minutes)
# Uses cadet_test.py's Game (?nosave&debug) and switches clothes on (CLOTHES_ON; ?clothes in a real URL does the same).
# Checks, by real taps where a person would tap: the arrival's one spare outfit and the change on Day 1 (one minute,
# Settling-in's 'clothes' note), yesterday's clothes from 10:00 (hygiene drains faster, the status note, one toast a
# day), Day 2's empty wardrobe giving the hamper (the tip, the arrow to the laundry, the holding pose), Put down and
# picking it up again, a washer (busy and broken ones send you to a free one; all busy: which finishes first), the
# toast when it's done, taking it out, putting it away (the full kit: five outfits, and you change), the save round
# trip mid-wash, a new game by shuttle and on Monday, and that with clothes off nothing answers.
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'cadet_test.py')).read().split("a, shots = run(")[0])

fails = []
def check(ok, what):
    if not ok and 'E' in globals(): print('     toast:', repr(E("document.getElementById('toast').innerText"))[:200])
    print(('ok   ' if ok else 'FAIL ') + what)
    if not ok: fails.append(what)

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.step(30); E = g.ev
    toast = lambda: E("document.getElementById('toast').innerText")
    E("window.__toasts = []; { const t0 = toast; toast = (a, b) => { window.__toasts.push(a + ': ' + b); return t0(a, b); }; }")
    said = lambda: ' || '.join(E('window.__toasts.slice(-4)'))
    def scr(x, y, z): return E(f"(()=>{{const v=new THREE.Vector3({x},{y},{z}).project(camera); return [(v.x+1)*innerWidth/2, (1-v.y)*innerHeight/2]}})()")
    def until(cond, n=60):
        for _ in range(n):
            g.step(10)
            if E(cond): return True
        return False
    def tap_wardrobe():
        g.step(5); w = E("(()=>{const w=clothesWardrobe(); return [w.x,w.z]})()"); E("tap(%f,%f)" % tuple(scr(w[0], 1.2, w[1])))

    # off at test URLs: the wardrobe tap does what it did before, nothing is drained
    check(E("CLOTHES_ON") is False, 'clothes are off at ?nosave')
    E("SHIP.time.min = 11*60; FX_MIN = -1; SHIP.clothes.changed = -1")
    check(E("fxD(playerFx(), 'hygiene') === fxD(shipEffects(deckDef.num), 'hygiene')"), 'off: no extra hygiene drain')
    E("SHIP.time.min = 6*60+5; FX_MIN = -1")

    E("CLOTHES_ON = true; simNote('newGame', { arrival: true })")
    check(E("SHIP.clothes.clean === 1 && SHIP.clothes.kit === false && SHIP.clothes.changed === 0"), 'by shuttle: one spare outfit, no full kit')
    heard = E("(() => { window.__acts = []; onSim('act', n => window.__acts.push(n.act)); return true; })()")
    tap_wardrobe()
    check(until("!!ACT && ACT.kind === 'clothes'"), 'Day 1: a tap on the wardrobe starts changing')
    check(E("SHIP.clothes.clean === 0 && SHIP.clothes.changed === SHIP.time.day"), 'changed into the spare: none left')
    check('spare outfit' in toast() and 'laundry before tomorrow' in toast(), 'the toast: your one spare, laundry before tomorrow')
    check(E("window.__acts.includes('clothes')"), "the 'clothes' note for Settling-in")
    g.step(200); check(E("!ACT"), 'changing ends by itself')
    tap_wardrobe(); until('!!SHIP.clothes.hamper', 30)
    check(E("!!SHIP.clothes.hamper && SHIP.clothes.changed === SHIP.time.day"), 'none left: a second tap gives the hamper early (laundry before tomorrow)')
    E("SHIP.clothes.hamper = null; clothesGoal(null)")

    # yesterday's clothes
    E("SHIP.time.day = 2; SHIP.time.min = 9*60+50; FX_MIN = -1; updateClock()")
    check(E("!clothesYesterday()"), 'not yet before 10:00')
    E("SHIP.time.min = 10*60+1; FX_MIN = -1"); g.step(3)
    check(E("clothesYesterday() && Math.abs(fxD(playerFx(), 'hygiene') - CLOTHES_DRAIN * fxD(shipEffects(deckDef.num), 'hygiene')) < 1e-9"), "from 10:00: hygiene drains x" + str(E("CLOTHES_DRAIN")))
    check(E("playerFx().notes[0].text === \"In yesterday's clothes\""), 'the status note')
    check("yesterday's clothes" in said() and 'no clean ones left' in said(), 'one toast, pointing at the laundry')
    check(E("SHIP.clothes.told === 2"), 'told once today')

    # Day 2: the hamper
    E("SHIP.player.carry.push('relay')"); tap_wardrobe(); until("false", 30)
    check(E("!SHIP.clothes.hamper") and 'hands are full' in toast(), 'hands full: no hamper yet')
    E("SHIP.player.carry.length = 0"); tap_wardrobe()
    check(until("!!SHIP.clothes.hamper"), 'empty wardrobe: you take the hamper')
    check(E("SHIP.clothes.hamper.state === 'dirty' && hamperHeld()"), 'dirty, in your hands')
    check(E("!!IX_GOAL && IX_GOAL.label === 'Laundry' && IX_GOAL.deck === 4"), 'the arrow points to the laundry')
    check(E("SHIP.device.tipsSeen.laundry === true"), 'the laundry tip')
    g.step(3); check(E("player.holding === true"), 'the holding pose')
    check(E("putWhat()"), 'Put down shows')
    E("putDown()"); g.step(3)
    check(E("SHIP.clothes.hamper.at === 'floor' && HAMPER_LOOK && HAMPER_LOOK.visible"), 'Put down: on the floor, drawn')
    check(E("clothesFloorTap(new THREE.Vector3(SHIP.clothes.hamper.x, 0, SHIP.clothes.hamper.z))") and until("hamperHeld()"), 'a tap on it picks it up')
    check(E("!HAMPER_LOOK.visible"), 'and it is no longer drawn on the floor')

    # the washers
    E("player.obj.position.copy(cellPos(13,17)); player.stop(); target.copy(player.obj.position).setY(.7)"); g.step(30)
    E("MACH_RUN['4-washer-3'] = shipNow() + 20")
    wx, wy = scr(*E("(()=>{const c=cellPos(12,19); return [c.x, .6, c.z]})()")); E(f"tap({wx},{wy})"); until("false", 30)
    check(E("SHIP.clothes.hamper.at === 'hands'") and 'is free' in toast(), 'a busy washer sends you to a free one')
    E("for (const id of ['4-washer-1','4-washer-2','4-washer-4']) MACH_RUN[id] = shipNow() + 40")
    g.step(5); wx, wy = scr(*E("(()=>{const c=cellPos(12,19); return [c.x, .6, c.z]})()")); E(f"tap({wx},{wy})"); until("false", 30)
    check('finishes first' in toast() and ('Washer 3' in toast() or 'Number 3' in toast()), 'all busy: which finishes first')
    E("for (const k in MACH_RUN) delete MACH_RUN[k]")
    g.step(5); wx, wy = scr(*E("(()=>{const c=cellPos(12,19); return [c.x, .6, c.z]})()")); E(f"tap({wx},{wy})")
    check(until("SHIP.clothes.hamper.at === 'washer'"), 'a free washer: your washing goes in')
    check(E("SHIP.clothes.hamper.washer === '4-washer-3' && Math.abs(SHIP.clothes.hamper.until - shipNow() - WASH_MINS) < 2"), 'Washer 3, for ' + str(E("WASH_MINS")) + ' ship minutes')
    check(E("MACH_RUN['4-washer-3'] > shipNow()"), 'the washer runs (section 17)')
    check(E("window.__acts.includes('laundry')"), "the 'laundry' note")
    check(E("!hamperHeld() && !putWhat()"), 'hands free while it washes')
    # the save mid-wash
    s = E("(()=>{const s={ship:{},player:{}}; for (const f of SAVE_EXTRA) f(s); return JSON.stringify(s.clothes)})()")
    check(E("JSON.stringify(clothesLoad({ clothes: JSON.parse(%r) })) === %r" % (s, s)), 'the save round trip mid-wash')
    check(E("JSON.stringify(clothesLoad({ clothes: { clean: 'x', hamper: { state: 'odd' } } }).hamper) === 'null'"), 'a bad save reads back safely')
    check(E("clothesLoad({}).clean === CLOTHES_FULL && clothesLoad({}).changed === SHIP.time.day"), 'an older save: the full kit, changed today')
    E("SHIP.time.min += WASH_MINS + 1"); g.step(3)
    check("washing's done" in said() and 'Washer 3' in said(), 'the toast when it is done')
    g.step(5); wx, wy = scr(*E("(()=>{const c=cellPos(12,19); return [c.x, .6, c.z]})()")); E(f"tap({wx},{wy})")
    check(until("hamperHeld() && SHIP.clothes.hamper.state === 'clean'"), 'take it out: clean, in your hands')
    check(E("!!IX_GOAL && IX_GOAL.label === 'Your wardrobe'"), 'the arrow points back to your wardrobe')

    # back to Bunk 1
    E("player.obj.position.copy(cellPos(8,3)); player.stop(); target.copy(player.obj.position).setY(.7)"); g.step(30)
    tap_wardrobe(); check(until("!SHIP.clothes.hamper"), 'put it away at the wardrobe')
    check(E("SHIP.clothes.kit && SHIP.clothes.clean === CLOTHES_FULL - 1 && SHIP.clothes.changed === 2"), 'the full kit: five outfits, and you change into one')
    check('kit' in toast() and 'stores' in toast(), 'the toast says the kit came up from stores')
    E("FX_MIN = -1"); check(E("!clothesYesterday() && fxD(playerFx(), 'hygiene') === fxD(shipEffects(deckDef.num), 'hygiene')"), 'no longer in yesterday\'s clothes')
    check(E("!IX_GOAL || IX_GOAL.label !== 'Your wardrobe'"), 'the arrow is cleared')

    # the uniform's grime (0.42.46, Pillar 5's m2 page)
    E("window.__uni = []; onSim('uniform', n => window.__uni.push(n.state))")
    check(E("uniformState() === 'clean' && SHIP.clothes.grime === 0"), 'grime: clean to start')
    check(E("clothesGrime(.35) === .35 && uniformState() === 'clean'"), 'grime .35: still clean')
    check(E("clothesGrime(.3) === .65 && uniformState() === 'grubby'"), 'grime .65: grubby')
    check(E("window.__uni.includes('grubby')"), "simNote('uniform', { state: 'grubby' })")
    E("FX_MIN = -1")
    check(E("Math.abs(fxD(playerFx(), 'hygiene') - CLOTHES_DRAIN * fxD(shipEffects(deckDef.num), 'hygiene')) < 1e-9 && playerFx().notes[0].text === 'Your uniform is grubby'"), 'grubby drains hygiene like yesterday\'s clothes, with its note')
    E("SHIP.clothes.changed = SHIP.time.day - 1; SHIP.time.min = 11 * 60; FX_MIN = -1")
    check(E("Math.abs(fxD(playerFx(), 'hygiene') - CLOTHES_DRAIN * fxD(shipEffects(deckDef.num), 'hygiene')) < 1e-9"), 'grubby and yesterday\'s at once: one multiplier, not two')
    E("SHIP.clothes.changed = SHIP.time.day")
    check(E("clothesGrime(5) === 1 && clothesGrime(-9) === 0 && clothesGrime(.656) === .66"), 'grime clamps to 0-1, two decimals')
    s2 = E("(()=>{const s={ship:{},player:{}}; for (const f of SAVE_EXTRA) f(s); return JSON.stringify(s.clothes)})()")
    check(E("clothesLoad({ clothes: JSON.parse(%r) }).grime === .66" % s2), 'grime saves and loads')
    check(E("clothesLoad({ clothes: { clean: 3, changed: 2 } }).grime === 0 && clothesLoad({}).grime === 0 && clothesLoad({ clothes: { grime: 'x' } }).grime === 0"), 'an older or odd save loads clean')
    n_clean = E("SHIP.clothes.clean")
    tap_wardrobe(); until("SHIP.clothes.grime === 0", 40)
    check(E("SHIP.clothes.grime === 0 && SHIP.clothes.clean === %d - 1 && uniformState() === 'clean'" % n_clean), 'grubby: the wardrobe changes you though you changed today, and the grime goes')
    check(E("window.__uni[window.__uni.length - 1] === 'clean'"), "simNote('uniform', { state: 'clean' })")
    E("actEnd(true); SHIP.clothes.grime = .8; simAct('wash'); SHIP.player.needs.hygiene = 100"); g.step(5)
    check(E("SHIP.clothes.grime === .8 && uniformState() === 'grubby'"), 'a wash (the shower\'s note, hygiene full) leaves the grime')
    E("SHIP.clothes.grime = 0")

    # the cabin Mail and Day 1's arrows (0.42.48)
    E("SHIP.intro = introBlank(); SHIP.intro.on = true; SHIP.intro.done.bunk = 0; SHIP.clothes.said = {}; SHIP.mail = SHIP.mail || []")
    n0 = E("SHIP.mail.length"); E("clothesCabinMail(); clothesCabinMail()")
    check(E("SHIP.mail.length") == n0 + 1 and E("SHIP.mail.some(m => m.from === 'Zeke Torres')"), "Zeke's cabin Mail, once")
    E("clearGoal(); D1_ARROW = null; SHIP.time.day = 1; SHIP.time.min = 8 * 60 + 55; SHIP.intro.done['d1-briefing'] = 470; if (SHIP.career) SHIP.career.ci = 0")
    E("clothesDay1Arrows()"); check(E("!!IX_GOAL && IX_GOAL.label === 'Time clock'"), 'Day 1: after the briefing, the arrow to the time clock')
    E("SHIP.career = SHIP.career || {}; SHIP.career.ci = shipNow(); clothesDay1Arrows()")
    check(E("!!IX_GOAL && IX_GOAL.label === 'Job board'"), 'clocked in: the arrow to the job board')
    E("simNote('job', { step: 'take', id: 'x' }); clothesDay1Arrows()")
    check(E("!IX_GOAL || IX_GOAL.label !== 'Job board'"), 'a job taken: the board arrow goes')
    E("SHIP.time.min = 18 * 60 + 5; SHIP.intro.done['d1-dinner:said'] = 1; SHIP.player.tray = null; clothesDay1Arrows()")
    check(E("!!IX_GOAL && IX_GOAL.label === 'Servery'"), 'the cook says eat: the arrow to the servery')
    E("setGoal({ deck: 3, at: [1, 1], label: 'Someone else' }); D1_ARROW = null; clothesDay1Arrows()")
    check(E("IX_GOAL.label === 'Someone else'"), "never over another section's arrow")
    E("clearGoal(); simAct('eat', { with: 1 }); clothesDay1Arrows()")
    check(E("!IX_GOAL"), 'eaten: no arrow')
    E("SHIP.intro = introBlank(); clearGoal(); D1_ARROW = null")
    E("simNote('newGame', { arrival: false })")
    check(E("SHIP.clothes.clean === CLOTHES_FULL && SHIP.clothes.kit && !SHIP.clothes.hamper"), 'a new game on Monday: the full kit')
    E("CLOTHES_ON = false"); check(E("!clothesFloorTap(new THREE.Vector3(0,0,0)) && !hamperHeld() && clothesGrime(.5) === null && uniformState() === 'clean'"), 'off again: nothing answers')
    check(not g.errors, 'no errors: ' + ' | '.join(g.errors[:3]))
    g.close()
print('ALL OK' if not fails else str(len(fails)) + ' FAILED')
sys.exit(1 if fails else 0)
