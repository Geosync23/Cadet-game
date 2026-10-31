# RV28: a crew story big scene in the real game (stage 2). Dev jump to the scene's day before it, the story put just
# before its crescendo (earlier beats told, the person a good friend), then the game runs: storyTick books it, the
# player (standing where the scene is) taps the teller once momentReady offers it, plays a few cards, saves, reloads
# the page mid-scene, and plays it again to the end. Logs who is in the room, the booking, the bridge door, errors.
# Run from a worktree:  CADET_WORK=... python3 PATH/st_scene.py WORKTREE BUILD.html tomas|kowalczyk|calder [OUTDIR]
import sys, os, json, pathlib
WT, BUILD, WHO = sys.argv[1], sys.argv[2], sys.argv[3]
OUT = pathlib.Path(sys.argv[4] if len(sys.argv) > 4 else '.')
sys.argv = [sys.argv[0], BUILD]
src = open(WT + '/devmode_check.py').read().split("\ndef part_off")[0].replace("__file__.replace('devmode_check.py', 'cadet_test.py')", repr(WT + '/cadet_test.py'))
exec(src)
CFG = {
  'tomas':     dict(day=21, at=17 * 60 + 15, deck=5, room='Shuttle bay', told=[5, 6, 7], beat=8, cast=['tomas', 'bramwell-basil', 'torres-zeke', 'holt'], end='18:20'),
  'kowalczyk': dict(day=24, at=5 * 60 + 5, deck=1, room='Bridge', told=[1, 2, 3], beat=4, cast=['kowalczyk', 'takahashi-wen', 'mensah'], end='06:40'),
  'calder':    dict(day=26, at=18 * 60 + 15, deck=5, room='Tea corner', told=[1, 2, 3, 4], beat=5, cast=['calder', 'halloran-emeka', 'torres-zeke', 'pell'], end='19:40'),
}[WHO]
ID = {'tomas': 'tomas', 'kowalczyk': 'kowalczyk', 'calder': 'calder'}[WHO]
PRE = """(() => { const R = DECKS[%d].rooms, k = Object.keys(R).find(c => R[c] && R[c].name === %s); return k; })()""" % (CFG['deck'], json.dumps(CFG['room']))
SETUP = """(() => { const id = %s; socInit(); const C = storyCS(); C.told[id] = %s; C.skip[id] = []; delete C.book[id];
  for (let i = 0; i < 40; i++) relAdd(id, 'chat', 5); const r = relGet(id); r.arc = Math.max(r.arc || 0, %d);
  if (%s === 'calder' && SHIP.works) { SHIP.works.rank = 'specialist'; SHIP.works.tier = 4; for (let i = 0; i < 40 && repBand('works') !== 'well' && repBand('works') !== 'trusted'; i++) repAdd('works', 5, { work: 1 }, 'job'); }
  return { tier: relTier(id), arc: r.arc, rank: SHIP.works && SHIP.works.rank, rep: repBand('works'), next: momentNextId(socP(id)) }; })()""" % (json.dumps(ID), json.dumps(CFG['told']), max(CFG['told']), json.dumps(WHO))
S = """(() => { const id = %s, p = socP(id), C = storyPeekCS(), t = shipNow();
  const crew = %s.map(c => { const q = socP(c), w = q && whereIs(q, t), a = DECK_CREW.find(x => x.p && x.p.id === c);
    return [c, w ? (w.deck + ':' + (storyRoom(q, t) || (w.moving ? 'moving' : '?')) + ':' + w.act + ':' + (w.tag || '')) : null, a ? roomAt(...cellAt(a.x, a.z)) : 'off-deck']; });
  const v = DIALOGUE && dialogueView();
  return { t: hhmm(t %% 1440), day: Math.floor(t / 1440) + 1, deck: deckDef.num, room: roomAt(...player.here()), book: C.book[id] || null, told: C.told[id] || [], skip: C.skip[id] || [],
    ready: momentReady(p, t), cday: C.cday, door: typeof storyDoorOpen === 'function' ? storyDoorOpen() : null, dlg: v ? (v.name || '') + ': ' + (v.text || '') + (v.choices ? ' [choice]' : '') : null,
    dlgId: DIALOGUE ? DIALOGUE.id : null, crew, why: (() => { try { const mid = momentNextId(p), d = mid && momentDef(mid); if (!d || !d.crescendo) return null; const day = Math.floor(t / 1440) + 1, sl = storySlots(d.crescendo, p, day, d.lead || 0, d);
      const w = {}; for (const k in (d.when || {})) { try { w[k] = !!linesOk({ [k]: d.when[k] }, p, momentCtx(p, sl[0] ? sl[0].from : t, mid)); } catch (e) { w[k] = 'err'; } }
      return { slots: sl.map(x => hhmm(x.from %% 1440) + '-' + hhmm(x.to %% 1440)), gates: sl[0] ? storyGates(p, d, mid, sl[0].from, sl[0].trad) : null, goes: sl[0] ? storyGoes(p, d, sl[0], t) : null, tier: relTier(id), met: metDays(id, t), rep: typeof repBand === 'function' ? repBand('works') : null, when: w, held: STORIES2_ON ? storyDayHeld(id, d, day) : null }; } catch (e) { return 'err ' + e.message; } })(), goal: IX_GOAL ? IX_GOAL.label : null,
    mail: SHIP.social.mail.filter(m => m.from === p.name).map(m => m.subject + '@' + hhmm(m.at %% 1440)).slice(-3) }; })()""" % (json.dumps(ID), json.dumps(CFG['cast']))
NEXT = "(() => { const v = dialogueView(); if (!v) return null; if (v.choices) dialogueChoose(0); else dialogueNext(); return true; })()"
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    rk = pg.ev(PRE); print('room key', rk)
    r = pg.ev("devmodeRun('Jump', () => devmodeSetCareerTo(%d, { day: %d, at: %d, where: { deck: %d, room: %s } }))" % (CFG['day'], CFG['day'], CFG['at'], CFG['deck'], json.dumps(rk))); pg.step(10)
    print('jump', r); print('setup', pg.ev(SETUP))
    phase, cards, reloaded, said = 'wait', 0, False, []
    for i in range(400):
        pg.step(30)
        try: s = pg.ev(S)
        except Exception as e: print('state err', str(e)[:200]); break
        if i % 4 == 0 or s['dlg'] or s['ready']: print(json.dumps(s)[:1100])
        if phase == 'wait' and s['ready'] and str(s['ready']).endswith(':' + str(CFG['beat'])):
            print('TAP ->', pg.ev("(() => { const p = socP(%s); chatOpen(p, false, null, { tap: true }); const l = chatLine ? null : null; return momentShow(%s) ? 'shown' : 'not shown'; })()" % (json.dumps(ID), json.dumps(s['ready'])))); phase = 'scene'
            pg.shot(str(OUT / f'{WHO}_start.png')); continue
        if phase == 'wait' and s['dlgId'] and not str(s['dlgId']).startswith('moment:') and os.environ.get('ST_PLAY_OTHER'): print('OTHER', s['dlgId'], (s['dlg'] or '')[:120]); pg.ev(NEXT); continue   # another scene on screen: play it as a player would
        if phase == 'scene':
            if s['dlg']:
                said.append(s['dlg']); cards += 1
                if cards == 4 and not reloaded:
                    pg.shot(str(OUT / f'{WHO}_mid.png'))
                    print('SAVE', pg.ev('(() => { saveGame(); return !!localStorage.getItem("starship-cadet-save-dev"); })()'))
                    pg.reload(); reloaded = True; phase = 'wait'; print('RELOADED', json.dumps(pg.ev(S))[:1100]); continue
                pg.ev(NEXT)
            elif s['dlgId'] is None and cards and str(CFG['beat']) and CFG['beat'] in s['told']:
                print('TOLD', json.dumps(s)[:1100]); pg.shot(str(OUT / f'{WHO}_end.png')); phase = 'done'
        if phase == 'done' or s['t'] >= CFG['end']: break
    print('LINES', len(said)); [print('  ', x[:160]) for x in said]
    print('errors', pg.errors[:5])
    b.close()
