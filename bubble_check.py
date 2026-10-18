# Starship Cadet: speech bubble check (0.47.9; keep in the repo, next to cadet_test.py)
# The user (playtest, on a phone): "bubbles shake or jump between two spots". This runs the game at phone size (390 x 844,
# devicePixelRatio 3) with uneven frame times (17 and 33 ms, as a busy phone gives), you walking and the camera turning,
# and two bubbles up over crew near you. Every frame it checks:
#   1. each bubble's tail aims at its speaker as the frame is drawn: the bubble's anchor (b.ax, b.ay) against the speaker's
#      head projected with the camera the frame was drawn with, within 0.5 px (before 0.47.9 the bubbles were placed with the
#      previous frame's camera, so they lagged by however far the camera moved, and that changed with every uneven frame)
#   2. no shake: a bubble never moves one way and straight back on the next frame by more than 3 px beyond what its speaker's
#      head did, and never jumps more than 45 px beyond it in one frame (a change of layout slides in over a few frames)
#   3. no bubble is hidden and shown again within 30 frames (a re-show replays its pop-in)
#   4. two bubbles that overlap never swap sides or stacking from one frame to the next more than once a second
# Setup and environment as for cadet_test.py.  Run:  python3 bubble_check.py BUILD.html
import sys
exec(open(__file__.replace('bubble_check.py', 'cadet_test.py')).read().split('import sys, json, hashlib\nimport numpy')[0].replace('device_scale_factor=1', 'device_scale_factor=3'))   # a phone's pixel density

PICK = r"""(() => { const v = new THREE.Vector3(), P = player.obj.position;
  const C = DECK_CREW.filter(a => a.h && a.h.pos).map(a => { v.set(a.x, 1.6, a.z).project(camera); return [a, Math.abs(v.x) + Math.abs(v.y), Math.hypot(a.x - P.x, a.z - P.z)]; })
    .filter(x => x[1] < 1.1).sort((a, b) => a[2] - b[2]).slice(0, 2).map(x => x[0]);
  window.__BC = C; C.forEach((a, k) => bubbleSay(a.h, k ? 'And this is the second one, a reply.' : 'This is a speech bubble, a bit long.', 120)); return C.map(a => a.p.id); })()"""
# where the anchor should be: the speaker's head (as bubbles.place works it out) with the camera as drawn
MEASURE = r"""(() => { const v = new THREE.Vector3(); return bubbles.list.map(b => { const w = b.who, p = w.pos || (w.obj && w.obj.position) || w, h = w.h || 1;
  const seat = w.pos && w.pos.y >= .3 ? w.pos.y : 0; v.set(p.x, seat ? seat + 1.15 * h : (w.pos ? w.pos.y : w.obj ? w.obj.position.y : p.y || 0) + 2.0 * h, p.z).project(camera);
  const hx = (v.x + 1) / 2 * innerWidth, hy = (1 - v.y) / 2 * innerHeight, m = /translate3d\(([-\d.]+)px, *([-\d.]+)px/.exec(b.el.style.transform || '');
  const x = m ? +m[1] : parseFloat(b.el.style.left), y = m ? +m[2] : parseFloat(b.el.style.top);
  return { t: b.text.slice(0, 12), shown: b.el.style.display !== 'none', hx, hy, ax: b.ax, x, y }; }); })()"""

def run(path):
    errs = []
    with sync_playwright() as pw:
        g = Game(pw, path, w=390, h=844)
        g.ev("skipTo((2 - 1) * 1440 + 720)"); g.ev("goToDeck(3)"); g.step(5)
        g.ev("player.obj.position.set(21.5 - OX, 0, 10.5 - OZ)"); g.step(40)
        who = g.ev(PICK); print(f'  speakers: {who}')
        if len(who) < 2: errs.append('fewer than two crew near you to speak'); g.close(); return errs
        prev, worst, jump, shakes, hides, swaps, last_hide, last_order, last_swap, res = None, 0, 0, 0, 0, 0, {}, None, -99, {}
        for k in range(240):
            # you walk east then back; the camera follows and turns slowly; frames alternate 17 and 33 ms
            g.ev(f"player.obj.position.x += {.035 if (k // 60) % 2 == 0 else -.035}; azT += {.004 if k < 120 else -.004}")
            g.step(1, 1000 / 60 if k % 2 else 1000 / 30)
            cur = g.ev(MEASURE)
            for i, b in enumerate(cur):
                if b['shown']: worst = max(worst, abs(b['ax'] - b['hx']))
                if prev and i < len(prev):
                    p = prev[i]
                    if p['shown'] != b['shown']:
                        if b['shown'] and k - last_hide.get(b['t'], -99) < 30: hides += 1
                        if not b['shown']: last_hide[b['t']] = k
                    elif b['shown'] and p['shown']:
                        rx, ry = (b['x'] - p['x']) - (b['hx'] - p['hx']), (b['y'] - p['y']) - (b['hy'] - p['hy'])   # its own movement, beyond the speaker's
                        jump = max(jump, abs(rx) + abs(ry)); q = res.get(i)
                        if q and any(abs(u) > 3 and abs(w) > 3 and u * w < 0 for u, w in ((rx, q[0]), (ry, q[1]))): shakes += 1
                        res[i] = (rx, ry)
            if len(cur) == 2 and all(b['shown'] for b in cur):
                order = cur[0]['x'] < cur[1]['x']
                if last_order is not None and order != last_order:
                    if k - last_swap < 30: swaps += 1
                    last_swap = k
                last_order = order
            prev = cur
        print(f'  1. worst tail aim against the drawn speaker {worst:.2f} px (at most 0.5)')
        print(f'  2. shakes (there and straight back, over 3 px) {shakes} (none); largest move in a frame beyond the speaker\'s {jump:.1f} px (at most 45)')
        print(f'  3. hidden and shown again within 30 frames: {hides} (none)')
        print(f'  4. two bubbles swapping sides twice within 30 frames: {swaps} (none)')
        if worst > .5: errs.append(f'bubbles aim {worst:.1f} px off their speaker (placed with another frame\'s camera?)')
        if shakes: errs.append(f'{shakes} frames where a bubble shook (moved and came straight back)')
        if jump > 45: errs.append(f'a bubble jumped {jump:.1f} px more than its speaker moved')
        if hides: errs.append(f'{hides} bubbles hidden and re-shown within 30 frames')
        if swaps: errs.append(f'{swaps} bubble pairs swapped sides back and forth')
        if g.errors: errs.append('page errors: ' + ' | '.join(g.errors[:3]))
        g.close()
    return errs

if __name__ == '__main__':
    print('Speech bubbles at phone size, uneven frames, you walking and the camera turning')
    e = run(sys.argv[1])
    for x in e: print('  FAIL', x)
    print('BUBBLE CHECK ' + ('FAILED' if e else 'OK')); sys.exit(1 if e else 0)
