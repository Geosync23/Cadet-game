# OR2: draw the REC DEC sign's canvas (recBigSign's own code) N times in one page; are the pixels the same each time?
import sys
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0])
from playwright.sync_api import sync_playwright
JS = r"""(() => { const hs = [], cvs = [];
  for (let k = 0; k < 12; k++) { const cv = document.createElement('canvas'); cv.width = 1024; cv.height = 300; const c = cv.getContext('2d'), w = 1024, h = 300;
    c.fillStyle = '#120b1c'; c.fillRect(0, 0, w, h); c.strokeStyle = '#50e6ff'; c.lineWidth = 8; c.shadowColor = '#50e6ff'; c.shadowBlur = 24; c.strokeRect(16, 16, w - 32, h - 32);
    c.textAlign = 'center'; c.font = '900 168px system-ui,sans-serif'; c.shadowColor = '#ff4fd8'; c.shadowBlur = 40;
    c.lineWidth = 10; c.strokeStyle = '#ff4fd8'; c.strokeText('REC DEC', w / 2, 192); c.fillStyle = '#ffe3fa'; c.fillText('REC DEC', w / 2, 192);
    c.shadowBlur = 16; c.shadowColor = '#50e6ff'; c.fillStyle = '#bff6ff'; c.font = '700 34px system-ui,sans-serif'; c.fillText('THE RECREATION DECK  ·  OPEN 06:00 TO MIDNIGHT', w / 2, 258);
    cvs.push(cv); }
  for (const cv of cvs) { const s = cv.toDataURL(); let x = 0; for (let i = 0; i < s.length; i++) x = (x * 31 + s.charCodeAt(i)) | 0; hs.push(x); }
  return hs; })()"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    for r in range(3): hs = g.ev(JS); print('distinct drawings of 12:', len(set(hs)), hs[:4]); g.ev('goToDeck(7)'); g.step(3)
    g.close()
