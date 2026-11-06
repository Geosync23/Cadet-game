# RV33 SC1 probe: chat card buttons, Get to know, wants-a-word arrow once a day, host +4. Phone size 390x844.
import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
path, tag = sys.argv[1], sys.argv[2]
BTN = "[...document.querySelectorAll('#chat button')].map(b=>b.textContent.trim())"
with sync_playwright() as pw:
    g = Game(pw, path, w=390, h=844)
    g.ev('localStorage.clear()'); g.ev("newGameStart(true)"); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.locator('form button').first.click(); g.step(10)
    g.ev("introSkip()"); g.step(3)
    # week 1 has gates; let the clock reach Day 9 evening and warm the core crew, as a few days of play would
    found = g.ev("""(() => { socInit(); for (const id of ['tomas','pell','torres-zeke','saad-amira','kovac-zainab','brennan','rina','halloran-emeka']) if (SOC.idx.has(id)) { relAdd(id, 'talk', 60); SHIP.rel[id].met = 0; }
      for (let t = 8*1440 + 7*60; t < 14*1440; t += 30) { const r = SOC.crew.filter(p => { try { return storyIdx().beats.has(p.id) && !!momentReady(p, t); } catch (e) { return false; } });
        if (r.length) { setShipNow(t); return { t, ids: r.map(p => p.id) }; } } return null; })()""")
    print(tag, 'first ready:', found)
    if not found: sys.exit(0)
    g.step(3)
    pid = found['ids'][0]; t0 = found['t']
    def near(pid):
        g.ev(f"(() => {{ const p = socP('{pid}'), w = whereIs(p, shipNow()), pl = w && w.placeId && schedData().byId.get(w.placeId), dk = pl ? pl.deck : (w && w.deck); if (dk && player.deck !== dk) goToDeck(dk); }})()"); g.step(6)
        return g.ev(f"(() => {{ const a = DECK_CREW.find(x => x.p.id === '{pid}'); if (!a) return 'not on deck ' + player.deck; player.obj.position.set(a.x + .9, 0, a.z); return 'beside, deck ' + player.deck; }})()")
    print(tag, 'move:', near(pid))

    g.ev("GUIDE.list.length = 0; storyArrows(shipNow())")
    arrow = lambda: g.ev(f"GUIDE.list.filter(e => e.id === 'story:word:{pid}').length")
    print(tag, 'arrow before talking:', arrow(), 'tier', g.ev(f"relTier('{pid}')"), 'intro', g.ev('SHIP.intro && SHIP.intro.step'), 'ready now', g.ev(f"!!momentReady(socP('{pid}'), shipNow())"))
    g.ev(f"chatOpen(socP('{pid}'))"); g.step(2)
    print(tag, 'card shown:', g.ev("!document.getElementById('chat').hidden"))
    print(tag, 'card buttons:', g.ev(BTN))
    g.page.screenshot(path=f'/tmp/rv33/sc1/story_card_{tag}.png')
    # Say hello (the 'chat' button) then the row again
    g.ev("chatDo('chat')"); g.step(2)
    print(tag, 'after Say hello:', g.ev(BTN), '| line:', g.ev("CHAT && CHAT.line && CHAT.line.kind"))
    g.ev("chatClose()"); g.step(1)
    # arrow re-asked over the rest of the day?
    n = 0
    for k in range(1, 40):
        t = t0 + k * 10
        if t // 1440 != t0 // 1440: break
        g.ev(f"setShipNow({t}); storyArrows({t}); guideLive({t})")
        n += arrow()
    print(tag, 'arrow re-shown checks later that day (sum over 10-min samples):', n)
    nd = (t0 // 1440 + 1) * 1440 + 12 * 60
    ready_next = g.ev(f"!!momentReady(socP('{pid}'), {nd})")
    g.ev(f"setShipNow({nd}); storyArrows({nd})")
    print(tag, 'next day noon: ready', ready_next, 'arrow', arrow())
    # Get to know plays the beat
    g.ev(f"setShipNow({t0})"); g.step(2); print(tag, 'move again:', near(pid)); g.ev(f"chatOpen(socP('{pid}'))"); g.step(2)
    b = g.page.locator('#chat button', has_text='Get to know')
    if b.count():
        b.first.click(); g.step(3)
        print(tag, 'after Get to know: dialogue', g.ev("typeof DIALOGUE!=='undefined' && DIALOGUE ? (DIALOGUE.id||'open') : null"))
        g.page.screenshot(path=f'/tmp/rv33/sc1/story_beat_{tag}.png')
    else: print(tag, 'no Get to know button')
    # note 39: host warms to you
    host = g.ev("(() => { for (let d = 1; d < 15; d++) for (const e of eventsOn(d)) if (typeof e.ev.host === 'string' && SOC.idx.has(e.ev.host)) return [e.id, e.ev.host, d]; return null; })()")
    print(tag, 'a hosted tradition:', host)
    if host:
        eid, h, d = host; at = (d - 1) * 1440 + 20 * 60
        r0 = g.ev(f"relGet('{h}').pts")
        g.ev(f"socApply('tradition', {{ id: '{eid}', day: {d}, at: {at}, came: [], you: true, host: '{h}' }}, {at})"); r1 = g.ev(f"relGet('{h}').pts")
        g.ev(f"socApply('tradition', {{ id: '{eid}', day: {d}, at: {at+5}, came: [], you: true, host: '{h}' }}, {at+5})"); r2 = g.ev(f"relGet('{h}').pts")
        g.ev(f"socApply('tradition', {{ id: '{eid}', day: {d}, at: {at}, came: [], you: false, host: '{h}' }}, {at})"); r3 = g.ev(f"relGet('{h}').pts")
        print(tag, f'host {h}: before {r0}, joined {r1}, joined again same day {r2}, not joined {r3}')
    print(tag, 'errors', g.errors[:5])
