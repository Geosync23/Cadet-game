import sys
src = open('/tmp/rv13/fx13.html').read()
P = {
 'p1': ("['bank', !only && LINES[kind]]", "['bank', LINES[kind]]"),
 'p2': ("  if (pick.talk && pick.talk.first && !pick.answered) return;", ""),
 'p3': ("  if (talkOnlyOwn(p)) { for (const tk of TALKS.own[p.id] || [])", "  if (false) { for (const tk of TALKS.own[p.id] || [])"),
 'p4': ("ready.sort((a, b) => T.fired[a.id][0] - T.fired[b.id][0]);", "ready.sort((a, b) => T.fired[b.id][0] - T.fired[a.id][0]);"),
 'p5': ("hi = C.talk.pack && C.talk.pack.first ? null : talkSays", "hi = false ? null : talkSays"),
 'p6': ("  if (typeof talkOnlyOwn === 'function' && talkOnlyOwn(p)) return null;", ""),
 'p7': ("  const first = ((TALKS.own && TALKS.own[p.id]) || []).find(tk => tk.first && ok(tk))", "  const first = null && ((TALKS.own && TALKS.own[p.id]) || []).find(tk => tk.first && ok(tk))"),
}
for k,(a,b) in P.items():
    assert src.count(a) == 1, k
    open(f'/tmp/rv13/{k}.html','w').write(src.replace(a,b))
print('ok')
