# continuous real time from D0 06:00 for ND days, drawing skipped; every frame on the hour: socialTick's parts timed
exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]; D0=int(sys.argv[2]); ND=int(sys.argv[3])
NAMES=os.environ.get('NAMES','socialTo,socialHour,shipDay').split(',')
WRAP=open('/tmp/pf/scripts/spike2.py').read().split('WRAP="')[1].split('"\nFR=')[0]
FR=open('/tmp/pf/scripts/hitch.py').read().split('FR=r"""')[1].split('"""')[0]
PUT=open('/tmp/pf/scripts/realtime.py').read().split('PUT=r"""')[1].split('"""')[0]
with sync_playwright() as pw:
    g=Game(pw,path,390,844); g.page.evaluate(REALNOW)
    g.ev(f"skipTo({(D0-1)*1440+6*60})"); g.ev(PUT); g.step(30)
    print('wrapped', g.page.evaluate("([s, n]) => window.__sc(s)(n)", [WRAP, NAMES]), flush=True)
    for b in range(int(os.environ.get('BATCH', ND*12))):
        r=g.page.evaluate("([s, a]) => window.__sc(s)(a)", [FR, [6000, 15]])
        for x in r['out']:
            if x[4]: print(x, flush=True)
    print('end', flush=True)
