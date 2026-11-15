# dlg.py [choiceIndex]: read a dialogue through with real taps on GO ON / a choice; prints each line
import sys, json, subprocess, os
pick = int(sys.argv[1]) if len(sys.argv) > 1 else 0
def c(cmds):
    r = subprocess.run(['python3', 'c.py', os.environ.get('PORT','7001'), '100000'], input=json.dumps(cmds), capture_output=True, text=True).stdout.strip().split('\n')
    return [json.loads(x) for x in r if x]
V = """(() => { if (!DIALOGUE) return null; const v = dialogueView(); const bs = [...document.querySelectorAll('#devDlg button, #devBody button, .dlg button')].filter(b => b.offsetParent).map(b => { const r = b.getBoundingClientRect(); return [b.innerText.trim(), r.left + r.width / 2, r.top + r.height / 2, Math.round(r.height)]; }); return [v && v.title, v && v.name, v && v.text, bs]; })()"""
for k in range(40):
    v = c([['ev', V]])[0]
    if not v: 
        c([['step', 40]]); v = c([['ev', V]])[0]
        if not v: print('(dialogue over)'); break
    print(f'{v[0]} | {v[1]}: {v[2]}', [b[0] + ' h' + str(b[3]) for b in v[3] if b[0] not in ('×',)])
    bs = [b for b in v[3] if b[0] not in ('×', 'BACK', 'HOME', 'CLOSE')]
    go = [b for b in bs if b[0].startswith('GO ON') or b[0].startswith('DONE') or b[0].startswith('OK')]
    b = go[0] if go else (bs[min(pick, len(bs) - 1)] if bs else None)
    if not b: print('no button'); break
    c([['tap', b[1], b[2]], ['step', 12]])
