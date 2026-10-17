#!/usr/bin/env python3
"""The Voices sampler (the head writer, Pillar 4 check-in A): plans/voices-sampler.html, made from content/.

    python3 tools/voices_sampler.py            # writes plans/voices-sampler.html

For each of the story crew: who they are, how they talk (their voice card), what they call you as you get closer, and
their own lines so far (up to 12, spread over tiers and kinds), plus the arrival evening's scenes. Placeholders are
filled with sample values so the page reads as the game would. Re-run after each merged batch; nothing is hand-edited.
"""
import html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import content_gen  # noqa: E402

OUT = os.path.join(ROOT, 'plans', 'voices-sampler.html')
ME = 'Kit'   # a sample name for you
TIERS = ['Stranger', 'Acquaintance', 'Colleague', 'Friend', 'Close friend']
CAST = [   # id, name, role, one line on who they are to you, their story in a sentence (opens as you grow close)
    ('torres-zeke', 'Zeke Torres', 'Works engine officer', 'Meets you off the shuttle and trains you in your first week.',
     'Passed over twice for promotion, he wonders if he\'s ready for more; later, his father back home is losing his memory.'),
    ('calder', 'Chief Ines Calder', 'Head of Works, your boss', 'Exact, fair, dry. Gives you your first solo job.',
     'Her first chief never once said "well done". Now that chief has written to her, and she hasn\'t answered.'),
    ('tomas', 'Tomas Lind', 'Watch rating, your bunkmate', 'Arrived a week before you, and is very glad not to be the newest.',
     'Homesick, a little lost, eyeing a transfer home; he finds his place, and meets the next new arrival himself.'),
    ('pell', 'Pell Okafor', 'Works technician, two years ahead', 'Your friend next door. Can fix anything except his sleep.',
     'His mum wants him home to run the family repair shop; and the certification practical he wants more than anything.'),
    ('rina', 'Rina Deshi', 'Infirmary aide', 'Dry, steady, undefeated at Tiles, and keeps count.',
     'Wants to be a ship\'s doctor, and keeps putting off the exam; her gran (who cheats at Tiles) has been ill.'),
    ('brennan', 'Chef Auda Brennan', 'Runs the galley and mess', 'Calls everyone "love". Asks if you\'ve eaten first.',
     'An old friend offers her a restaurant of her own again, years after a fire closed her last one.'),
    ('vance', 'Commander Teo Vance', 'Executive Officer', 'By the book, every page of it. Keeps the leaderboards.',
     'Two messages from his father wait unopened; and he secretly writes the ship newsletter\'s worst poems.'),
    ('marrow', 'Captain Odile Marrow', 'Captain', 'Calm, curious, quietly funny. Asks a junior the truth.',
     'Responsible for everyone and friends with no one; her daughter rarely writes; she wonders about stepping down.'),
    ('holt', 'Chief Bram Holt', 'Head of Watch', 'Gruff, testing, dependable. Doesn\'t trust the Veyli, and says so.',
     'One bad day years ago, and a slow thaw toward the Envoy next door, which he\'ll deny.'),
    ('kovac-zainab', 'Zainab Kovac', 'Works technician', 'Shy, exact, knits perfect scarves. Your first favour.',
     'Secretly afraid of the lift; a small, funny, kind story about it.'),
]
SAMPLE = {'me': ME, 'name': '', 'first': '', 'friend': 'Pell', 'best': 'Rina', 'rival': 'Teague', 'partner': 'their partner',
          'mentor': 'Torres', 'mentee': 'Kit', 'boss': 'Calder', 'other': 'Pell', 'thing': 'the lamp', 'trad': 'quiz night',
          'machine': 'the scrubber', 'room': 'the tea corner', 'deck': 'Deck 5', 'dish': 'the stew', 'weekday': 'Thursday',
          'home': 'home', 'family': 'family', 'hobby': 'knitting', 'since': 'two years'}
KIND_NAMES = {'greet': 'hello', 'bye': 'goodbye', 'chat': 'chat', 'near': 'where they are', 'feel': 'how they feel',
              'life': 'their life', 'joy': 'what they love', 'week1': 'your first week', 'invite': 'an invitation',
              'callback': 'remembering', 'cue': 'reacting', 'hint': 'a moment is ready'}
TONE = {None: 'light', 'funny': 'funny', 'warm': 'warm', 'serious': 'serious'}


def fill(text, card, tier):
    w = card.get('words', {})
    def word(k):
        v = w.get(k) or ['']
        return v[0]
    nick = (w.get('nick') or [None] * 5)[tier] or ('cadet' if tier == 0 else ME)
    text = re.sub(r'\{(hi|bye|yes|thanks|wow|sigh)\}', lambda m: word(m.group(1)), text)
    text = text.replace('{nick}', nick.replace('{me}', ME))
    return re.sub(r'\{(\w+)\}', lambda m: SAMPLE.get(m.group(1), m.group(0)), text)


def conds(l):
    skip = {'text', 'id', 'tone', 'tier', 'w', 'odds'}
    out = []
    for k, v in l.items():
        if k in skip:
            continue
        if k == 'not':
            out += ['not ' + kk for kk in v]
            continue
        out.append(f'{k}: {v}' if not isinstance(v, list) else f'{k}: ' + ', '.join(map(str, v)))
    return out


def day0(l):
    """A Day 0 line: a walking line (flag:walk.<step>) or an arrival-evening chat line (Sunday evening of week 1)."""
    f = l.get('flag')
    return (isinstance(f, str) and f.startswith('walk.')) or (l.get('weekday') == 'sun' and l.get('week1'))


def pick(card, n=12):
    """Up to n of their own lines, round-robin over kinds so the sample is varied (Day 0 lines go to the arrival)."""
    kinds = [k for k in card.get('lines', {}) if not k.startswith('old')]
    pools = {k: [l for l in card['lines'][k] if not day0(l)] for k in kinds}
    got = []
    while len(got) < n and any(pools.values()):
        for k in kinds:
            if pools[k] and len(got) < n:
                got.append((k, pools[k].pop(0)))
    return got


def esc(s):
    return html.escape(str(s), quote=True)


def scene(sc, names):
    rows = []
    for l in sc['lines']:
        if 'choice' in l:
            opts = ''.join(f'<li><span class="you">You:</span> {esc(c["text"])}'
                           + (f'<div class="reply"><b>{esc(names.get(c["reply"]["who"], c["reply"]["who"]))}:</b> {esc(fill(c["reply"]["text"], {}, 1))}</div>' if c.get('reply') else '')
                           + '</li>' for c in l['choice'])
            rows.append(f'<li class="choice"><div class="choose">You choose one:</div><ul>{opts}</ul></li>')
        else:
            who = names.get(l['who'], l['who'])
            rows.append(f'<li><b>{esc(who)}:</b> {esc(fill(l["text"], {}, 1))}</li>')
    return '<ol class="scene">' + ''.join(rows) + '</ol>'


def main():
    out = content_gen.bake()
    V = out['VOICE']
    names = {c[0]: c[1].split(' ')[-1] if c[0] in ('calder', 'brennan', 'vance', 'marrow', 'holt') else c[1].split(' ')[0] for c in CAST}
    names.update({'calder': 'Calder', 'torres-zeke': 'Torres', 'tomas': 'Tomas', 'you': 'You'})
    nav, secs = [], []
    # the arrival evening
    sc_html = ''
    for mid, label in (('introBunk', 'At your bunk (17:53, Day 0)'), ('introChief', 'Dinner: the Chief stops by (about 18:30)')):
        sc = out['MEETINGS_BAKED'].get(mid)
        if sc:
            sc_html += f'<h3>{esc(label)}</h3>' + scene(sc, names)
    walk, steps = V.get('torres-zeke', {}).get('lines', {}).get('week1', []), []
    for l in walk:
        f = l.get('flag')
        if isinstance(f, str) and f.startswith('walk.'):
            st = f[5:]
            if not steps or steps[-1][0] != st:
                steps.append((st, []))
            steps[-1][1].append(fill(l['text'], V['torres-zeke'], 1))
    STEP = {'hello': 'At the shuttle ramp', 'haulway': 'The haulway', 'works': 'The Works bay door', 'lift': 'The lift',
            'wing': 'The junior wing', 'toMess': 'Off to dinner', 'servery': 'The servery', 'free': 'After dinner',
            'call': 'If you wander off'}
    if steps:
        sc_html = ('<h3>Torres, as you walk (speech bubbles)</h3><ol class="scene">' + ''.join(
            f'<li><b>{esc(STEP.get(st, st))}:</b> ' + ' '.join(f'"{esc(t)}"' for t in ts) + '</li>' for st, ts in steps)
            + '</ol>') + sc_html
    for cid, label in (('pell', 'Pell joins your table at dinner (if you tap him)'), ('tomas', 'Tomas finds you after dinner (if you tap him)')):
        ls = [l for k, v in V.get(cid, {}).get('lines', {}).items() for l in v if day0(l)]
        if ls:
            sc_html += f'<h3>{esc(label)}</h3><ol class="scene">' + ''.join(
                f'<li><b>{esc(names.get(cid, cid))}:</b> {esc(fill(l["text"], V[cid], 1))}</li>' for l in ls) + '</ol>'
    secs.append(f'<section id="arrival"><h2>The arrival evening</h2><p>Your first evening aboard: Torres\'s lines as he walks you '
                f'through the ship, the two scenes that play in the dialogue panel, and what Pell and Tomas say if you talk to them. '
                f'You walk yourself the whole way.</p>{sc_html}</section>')
    nav.append('<a href="#arrival">Arrival</a>')
    for cid, name, role, who, story in CAST:
        card = V.get(cid, {})
        w = card.get('words', {})
        nick = [(n or ('cadet' if i == 0 else ME)).replace('{me}', ME) for i, n in enumerate(w.get('nick') or [None] * 5)]
        ladder = ''.join(f'<li><span>{TIERS[i]}</span><b>{esc(nick[i])}</b></li>' for i in range(5))
        words = ' · '.join(f'<i>{esc(" / ".join(w[k]))}</i>' for k in ('hi', 'bye', 'thanks') if w.get(k))
        jokes = ''.join(f'<li>{esc(j)}</li>' for j in card.get('jokes', []))
        lines = pick(card)
        lrows = ''.join(
            f'<li><p>{esc(fill(l["text"], card, (l.get("tier") or [1])[0]))}</p><div class="meta">'
            f'<span class="tag">{esc(TIERS[(l.get("tier") or [0])[0]])}{"+" if (l.get("tier") or [0, 0])[1] > (l.get("tier") or [0, 0])[0] else ""}</span>'
            f'<span class="tag">{esc(KIND_NAMES.get(k, k))}</span><span class="tag tone-{esc(TONE.get(l.get("tone"), l.get("tone")))}">{esc(TONE.get(l.get("tone"), l.get("tone")))}</span>'
            + ''.join(f'<span class="tag cond">{esc(c)}</span>' for c in conds(l)) + '</div></li>'
            for k, l in lines)
        if not lines:
            lrows = '<li class="empty"><p>Their lines are being written (batch 1).</p></li>'
        secs.append(f'''<section id="{cid}">
<header class="who"><h2>{esc(name)}</h2><div class="role">{esc(role)}</div></header>
<p class="lede">{esc(who)}</p>
<div class="cols">
<div><h3>How they talk</h3><p>{esc(card.get("talk", ""))}</p>
<h3>Says</h3><p class="words">{words}</p>
<h3>Running jokes</h3><ul>{jokes}</ul>
<h3>What they call you</h3><ul class="ladder">{ladder}</ul>
<h3>Their story</h3><p class="story">{esc(story)}</p></div>
<div><h3>Their lines</h3><ul class="lines">{lrows}</ul></div>
</div></section>''')
        nav.append(f'<a href="#{cid}">{esc(name.replace("Chief ", "").replace("Commander ", "").replace("Captain ", "Capt. ").replace("Chef ", ""))}</a>')
    page = PAGE.replace('{{NAV}}', ''.join(nav)).replace('{{SECTIONS}}', '\n'.join(secs)).replace('{{ME}}', ME)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(page)
    print('wrote', os.path.relpath(OUT, ROOT), '|', ', '.join(f'{c[0]} {sum(len(v) for k, v in V.get(c[0], {}).get("lines", {}).items())}' for c in CAST))


PAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Wren Voices Sampler</title>
<style>
:root{--bg:#f6f3ec;--panel:#fffdf8;--ink:#1f2a30;--muted:#5d6b70;--line:#e2dccf;--accent:#1f7a6e;--accent-ink:#ffffff;--chip:#e9f3f1;--chip-ink:#1d5c53;
--funny:#f6e7c1;--funny-ink:#6b4c00;--warm:#f7dcd3;--warm-ink:#7a2e17;--serious:#dde3f3;--serious-ink:#29386b;--cond:#efece6;--cond-ink:#5d5a52}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121a22;--panel:#18232d;--ink:#e6eef0;--muted:#9aaab0;--line:#2a3944;--accent:#4cc3b5;--accent-ink:#0f1a20;--chip:#1d3437;--chip-ink:#a9e5dc;
--funny:#3d3420;--funny-ink:#f1d891;--warm:#3f2a24;--warm-ink:#f2b9a4;--serious:#252e45;--serious-ink:#b9c6ef;--cond:#22292f;--cond-ink:#aab3b8}}
:root[data-theme="dark"]{--bg:#121a22;--panel:#18232d;--ink:#e6eef0;--muted:#9aaab0;--line:#2a3944;--accent:#4cc3b5;--accent-ink:#0f1a20;--chip:#1d3437;--chip-ink:#a9e5dc;
--funny:#3d3420;--funny-ink:#f1d891;--warm:#3f2a24;--warm-ink:#f2b9a4;--serious:#252e45;--serious-ink:#b9c6ef;--cond:#22292f;--cond-ink:#aab3b8}
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--bg);color:var(--ink);font:15px/1.55 "Avenir Next","Segoe UI",system-ui,sans-serif}
.top{max-width:1080px;margin:0 auto;padding:22px 16px 6px}
h1{font-size:24px;margin:0 0 4px;font-weight:650}
.sub{color:var(--muted);margin:0;max-width:760px}
nav{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line)}
nav div{display:flex;gap:6px;overflow-x:auto;padding:8px 16px;max-width:1080px;margin:0 auto}
nav a{flex:none;text-decoration:none;color:var(--ink);border:1px solid var(--line);background:var(--panel);padding:5px 11px;border-radius:999px;font-size:13px}
nav a:hover,nav a:focus-visible{border-color:var(--accent);outline:none}
main{max-width:1080px;margin:0 auto;padding:4px 16px 48px}
section{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:16px 0;scroll-margin-top:60px}
h2{margin:0;font-size:19px;font-weight:650}
h3{margin:14px 0 4px;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:600}
.who{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px}
.role{color:var(--muted);font-size:14px}
.lede{margin:6px 0 0;font-size:15.5px}
.cols{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);gap:8px 28px}
@media (max-width:760px){.cols{grid-template-columns:1fr}}
p{margin:4px 0}
ul{margin:4px 0;padding-left:18px}
.words i{font-style:normal;background:var(--chip);color:var(--chip-ink);border-radius:6px;padding:1px 6px}
.ladder{list-style:none;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:4px}
.ladder li{border:1px solid var(--line);border-radius:8px;padding:4px 6px;text-align:center;font-size:12px;color:var(--muted)}
.ladder b{display:block;color:var(--ink);font-size:13.5px;font-weight:600;overflow-wrap:anywhere}
@media (max-width:480px){.ladder{grid-template-columns:repeat(2,minmax(0,1fr))}}
.story{color:var(--muted);font-style:italic}
.lines{list-style:none;padding:0;margin:4px 0}
.lines li{border-left:3px solid var(--accent);padding:6px 10px;margin:0 0 8px;background:var(--bg);border-radius:0 8px 8px 0}
.lines li p{font-size:15.5px}
.lines li.empty{border-left-color:var(--line);color:var(--muted)}
.meta{margin-top:3px;display:flex;flex-wrap:wrap;gap:4px}
.tag{font-size:11.5px;border-radius:999px;padding:1px 8px;background:var(--chip);color:var(--chip-ink)}
.tag.tone-light{display:none}
.tag.tone-funny{background:var(--funny);color:var(--funny-ink)}
.tag.tone-warm{background:var(--warm);color:var(--warm-ink)}
.tag.tone-serious{background:var(--serious);color:var(--serious-ink)}
.tag.cond{background:var(--cond);color:var(--cond-ink)}
.scene{list-style:none;padding:0;margin:6px 0 12px}
.scene>li{padding:5px 0;border-bottom:1px dashed var(--line)}
.scene .choice{background:var(--bg);border-radius:8px;padding:8px 10px;margin:4px 0;border:1px solid var(--line)}
.choose{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.choice ul{list-style:none;padding:0}
.choice li{margin:6px 0}
.you{color:var(--accent);font-weight:600}
.reply{margin:2px 0 0 18px;color:var(--muted)}
.ask{border:1px solid var(--accent);background:var(--chip);color:var(--chip-ink);border-radius:12px;padding:10px 14px;margin:14px 0 0}
</style>
</head>
<body>
<div class="top">
<h1>The Wren's voices: a sampler</h1>
<p class="sub">How the ten main characters talk, before the bulk of the dialogue is written. Each one shows their voice card, what they
call you as you get to know them, and a sample of their own lines. Your name in these samples is "{{ME}}".</p>
<div class="ask"><b>What we'd like from you:</b> for each person, does this sound like them? Keep, change or cut any line or detail.
Tags show when a line can be said (how well they know you, what's happening) and its tone (funny, warm, serious; plain lines aren't tagged).</div>
</div>
<nav><div>{{NAV}}</div></nav>
<main>
{{SECTIONS}}
</main>
</body>
</html>
'''

if __name__ == '__main__':
    main()
