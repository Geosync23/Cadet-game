import re
L = open('/tmp/claude-0/-home-user-Cadet-game/c1b02abe-9503-5276-8da1-eaa085c6ed9c/scratchpad/m/logs/times.txt').read().splitlines()
rows = []
for l in L:
    m = re.match(r'(\S+) lane=(\S+) rc=(\d+) (\d+) s :: (.*)', l)
    if m: rows.append((m[1], m[2], int(m[3]), int(m[4]), m[5]))
rows.append(('perf', 'alone', 1, 446, 'PERF CHECK: 1 problem (the known +2 geometries)'))
note = {'cadet': 'vs 0.64.6: differences as the 0.64.7 release round explained (First Light Cocoa moves the crew)', 'career': 'known: backlog row 12', 'day1': 'one day; a release runs Days 0-8', 'player': 'the longest check'}
rows.sort(key=lambda r: -r[3])
tot = sum(r[3] for r in rows)
md = ['| Check | Took | Result |', '| --- | --- | --- |'] + [f"| {n} | {s//60} min {s%60:02d} s | {res}{' (' + note[n] + ')' if n in note else ''} |" for n, lane, rc, s, res in rows]
md.append(f'| **all of them, one after another** | **{tot//3600} h {tot%3600//60:02d} min** | |')
mx = max(r[3] for r in rows)
html = ''.join(f'<div class="hb"><span class="l">{n}</span><span class="b{" alt" if n in ("player","intro") else ""}" style="width:{max(2, round(260*s/mx))}px"></span><span class="v">{s//60} min {s%60:02d} s</span></div>\n' for n, lane, rc, s, res in rows)
print('\n'.join(md)); print('TOTAL', tot); open('/tmp/claude-0/-home-user-Cadet-game/c1b02abe-9503-5276-8da1-eaa085c6ed9c/scratchpad/m/table.html', 'w').write(html)
