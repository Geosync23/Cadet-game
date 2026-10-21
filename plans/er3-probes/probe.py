import sys, json, os
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium'); os.environ.setdefault('CADET_WORK','/tmp/cw-ct')
src=open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
build=sys.argv[1]; js=open(sys.argv[2]).read()
with sync_playwright() as pw:
    g=Game(pw, build)
    print(json.dumps(g.ev(js), indent=1, default=str)[:int(os.environ.get('LIM','20000'))])
    if g.errors: print('ERR', g.errors[:5])
    g.close()
