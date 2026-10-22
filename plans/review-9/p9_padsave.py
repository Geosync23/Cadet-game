# PR9: P4's save rules: the pad used but nothing changed -> no 'pad' in the save; a change -> s.pad holds only it, and it
# loads back; back to normal -> gone; odd or old saves -> normal. Also: Settings with no pad seen, and after a press.
import sys, os, json
src = open('controller_check.py').read(); sys.argv = [sys.argv[0], 'starship-cadet.html', 'none']
exec(src.split('def part_off')[0].replace("__file__.replace('controller_check.py', 'cadet_test.py')", "'cadet_test.py'"))
from playwright.sync_api import sync_playwright
SAVE = "(() => { const decks = {}; const s = { v: SAVE_V, build: GAME_BUILD, time: { day: SHIP.time.day, min: SHIP.time.min }, player: { deck: player.deck, tile: player.here(), facing: player.face }, ship: { decks }, crew: {}, flags: SHIP.flags || {}, notes: SHIP.notes || [] }; for (const f of SAVE_EXTRA) f(s); return JSON.stringify({ pad: s.pad, keys: Object.keys(s).sort() }); })()"   # saveGame's own build-up (test URLs never save)
SETS = "(() => { deviceShow('settings'); return [...document.querySelectorAll('#devBody button')].some(b => /Controller settings/.test(b.textContent)); })()"
with sync_playwright() as pw:
    p = Pad(pw, ON)
    p.ev("deviceShow('home')"); p.step(3)
    print('no pad: Settings shows Controller settings?', p.ev(SETS), '| save:', p.ev(SAVE)[:200])
    base = json.loads(p.ev(SAVE)); p.ev('deviceClose()'); p.step(2)
    p.plug(); p.press('x'); p.log(); p.step(3)
    p.ev("deviceShow('home')"); p.step(3)
    print('pad used: Settings shows it?', p.ev(SETS))
    p.ev("deviceShow('padsettings')"); p.step(3)
    s1 = json.loads(p.ev(SAVE)); print('pad used, settings opened, nothing changed: save == no-pad save?', s1 == base, '| pad:', s1.get('pad'))
    p.ev("padSetAct('swap', true)"); p.ev("padSetAct('dead', .32)"); p.ev("padSetBind('y', 'x')")
    s2 = json.loads(p.ev(SAVE)); print('after swap + dead .32 + Y on X: s.pad =', json.dumps(s2.get('pad')))
    print('loads back:', p.ev(f"(() => {{ padSetLoad({json.dumps(s2.get('pad'))}); return JSON.stringify(padSetDiff()); }})()"))
    p.ev("padSetAct('normal')"); p.ev("padSetAct('normal')")
    s3 = json.loads(p.ev(SAVE)); print('after Everything back to normal (twice): pad key?', 'pad' in s3, '| == base', s3 == base)
    for odd in ['null', '5', '"x"', '{"map":{"a":"b"}}', '{"map":{"a":"zz","b":"a"},"dead":5,"zoom":"fast","swap":"yes","every":0}', '{"map":{"a":"b","b":"a"}}', '[1,2]']:
        print('load', odd, '->', p.ev(f"(() => {{ padSetLoad({odd}); return JSON.stringify(padSetDiff()) + ' ' + PAD_DEAD.stick + ' ' + PAD_MAPK.slice(0, 4).join(); }})()"))
    print('page errors', p.g.errors[:3]); p.close()
