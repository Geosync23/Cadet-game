#!/usr/bin/env python3
"""lines_check.py: checks the writers' files under content/ before they're baked (writers run it before every push).

    python3 lines_check.py [GAME.html] [--strict] [--quiet]
    python3 lines_check.py --day [GAME.html]     the voice budget in the game itself (a browser; a few minutes)

Errors (exit 1): a file content_gen.py can't read; an unknown {token} or condition value; a line too long; an
unknown crew id; the banned list (romance and flirting, swearing beyond the ship's mild "blast", real-world brands
and politics, things the game doesn't have); #serious lines not behind tier>=friend or an arc beat; the baked
blocks in the game file out of date (re-run content_gen.py).
Warnings: names that aren't crew, guests or ship words; the same line in two places; American spellings; a habit:
condition in someone's own file for a habit they don't have; hard-to-read files (reading ease under 60).
Reports: coverage per person and kind against the targets in the plan (story crew about 200 lines, Works crew and your
bunkmates about 60, everyone else about 30 of their own); --strict turns missing coverage into errors (wave 2 on),
and the voice budget's numbers for a ship day (the rules section 22 enforces, and what the banks can supply).
The vocabulary it checks against is content_gen.py's COND_KEYS and content/README.md.
"""
import json, os, re, sys
import content_gen as cg

ROOT = os.path.dirname(os.path.abspath(__file__))

TOKENS = {'hi', 'bye', 'yes', 'thanks', 'wow', 'sigh', 'nick'}
PLACEHOLDERS = {'me', 'name', 'first', 'friend', 'best', 'rival', 'partner', 'mentor', 'mentee', 'boss', 'thing', 'trad',
                'machine', 'room', 'deck', 'dish', 'weekday', 'home', 'family', 'hobby', 'since', 'other',
                'kin', 'lost', 'hobbyNoun', 'missed',
                'time', 'hours', 'n', 'max', 'part', 'shelf', 'drink', 'answer',
                'mech', 'job', 'tools', 'skill', 'title', 'rank', 'band', 'next', 'shows', 'drill', 'host',
                'system', 'dept', 'day', 'word', 'where', 'when', 'from', 'to', 'place'}   # Pillar 5 Step 3 texts (keys-p5.md "Step 3")   # Pillar 5 texts (content/works/keys-p5.md)   # 0.60.7 texts (keys-0607.md): the engineer fills these   # kin, lost: "my gran", "my wife" (with the my); hobbyNoun: "knitting", "the piano"
PAIR_WORDS = {'same', 'bunk', 'friend', 'rival', 'senior', 'couple', 'best', 'mentor', 'mentee'}   # section 22's linePair
NEEDS = {'home', 'family', 'hobby', 'since', 'kin', 'lost', 'hobbyNoun'}   # what a theme beat's needs: can name
TRAD_PLACEHOLDERS = {'trad', 'host', 'names', 'first', 'season', 'weekday', 'time'}   # tradition texts: only these (plans/trad-format.md, tradFill)
VALUES = {
    'warmth': {'cold', 'warm'},
    'bond': {'best', 'friends', 'friend', 'rivals', 'rival', 'mentor', 'mentee', 'drifting', 'couple', 'partner', 'missed'},   # section 20's BOND_KINDS and bondOf's aliases 'mood': {'low', 'ok', 'high'},
    'rep': {'new', 'known', 'well', 'theirs'}, 'ship.work': {'low', 'ok', 'high'}, 'ship.kindness': {'low', 'ok', 'high'},
    'ship.spirit': {'low', 'ok', 'high'}, 'week1': {'true', 'false'}, 'leaving': {'soon', 'you'}, 'newhere': {'true', 'false'},
    'guide': {'true', 'false'},
    'time': {'morning', 'afternoon', 'evening', 'night'}, 'weekday': {'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'},
    'season': {'sowing', 'greening', 'harvest', 'lanterns'}, 'birthday': {'me', 'you'},
    'dept': {'command', 'helm', 'comms', 'works', 'watch', 'survey', 'infirmary', 'galley', 'garden', 'store', 'civilian', 'guest'},
    'rank': {'junior', 'officer', 'senior', 'chief', 'xo', 'captain', 'guest'},
    'act': {'work', 'breakfast', 'dinner', 'meal', 'gym', 'wash', 'sleep', 'leisure', 'off', 'free', 'event', 'shop', 'call'},
}
BUBBLE_KINDS = {'smalltalk', 'rumour', 'overheard'}        # spoken over heads: 60 characters (90 at most)
LONG_KINDS = ('story', 'arc', 'moment', 'note', 'trad', 'career', 'works.ask', 'inspect.mail')    # chat lines, moments, Mail: 140
CARD = 90
HOME_IDS = {'mum', 'gran', 'jo', 'sam'}                  # your people back home (content/home/<id>.call)
NAME_W = 9                                                 # a filled-in name counts as this many characters

BANNED = [
    # romance and flirting with anyone (the user: no romance with the player; couples live quietly in the background)
    r'\bkiss\w*', r'\bflirt\w*', r'\bdarling\b', r'\bsweetheart\b', r'\bbabe\b', r'\bsexy\b', r'\bgorgeous\b', r'\bcrush\b',
    r'\bromanc\w*', r'\bdate night\b', r'\bon a date\b', r'\blove you\b', r'\bmy love\b', r'\bhandsome\b', r'\bcutie\b', r'\bsnog\w*',
    # swearing (the ship's "blast" is fine)
    r'\bdamn\w*', r'\bhell\b', r'\bbloody\b', r'\bcrap\w*', r'\bshit\w*', r'\bfuck\w*', r'\bbastard\w*', r'\bpiss\w*',
    r'\barse\w*', r'\bass\b', r'\bbollocks\b', r'\bgod\b', r'\bjesus\b', r'\bchrist\b',
    # real-world brands and politics
    r'\bcoca[- ]?cola\b', r'\bpepsi\b', r'\biphone\b', r'\bgoogle\b', r'\bfacebook\b', r'\bapple\b(?! pie)', r'\bnike\b',
    r'\bstarbucks\b', r'\bamazon\b', r'\bnetflix\b', r'\bdisney\b', r'\bmcdonald\w*', r'\bdemocrat\w*', r'\brepublican\w*',
    r'\bbrexit\b', r'\btory\b', r'\btories\b', r'\bparliament\b', r'\bpresident\b', r'\belection\w*',
    # things the game doesn't have (the social plan's writers' rules)
    r'\bphotos?\b', r'\bphotograph\w*', r'\bcamera\b', r'\bselfie\w*', r'\bguns?\b', r'\bweapons?\b', r'\bblaster\w*',
    r'\bphone\b', r'\binternet\b',
]
# romance said to you (the user: none with the player). Crew couples may speak of each other in overheard conversations,
# so these are errors in every player-facing line (chat, moments, replies, meetings, Mail) but not in overheard banks
BANNED_PLAYER = [r'\bin love\b', r'\bfall(?:ing|en)? for you\b', r'\bfell for you\b', r'\bmarry me\b', r'\bwill you marry\b', r'\bmy heart\b',
                 r'\bsoulmate\w*', r'\bbe mine\b', r'\bdate me\b', r'\bgo out with me\b', r'\bsweet on\b', r'\bhold my hand\b',
                 r'\bboyfriend\b', r'\bgirlfriend\b', r'\bpropos(?:e|al) to you\b', r'\bdating\b', r'\bgoing out\b',
                 r'\bseeing (?:each other|anyone|someone|somebody)\b',
                 r'\b(?:fancy|want|like) a date\b', r'\bask(?:ed)? (?:you|me) out\b']   # "married", "wedding": family lines need them
# aimed at you: banned even in lines about crew couples
BANNED_AT_YOU = [r'\bfall(?:ing|en)? for you\b', r'\bfell for you\b', r'\bbe mine\b', r'\bdate me\b', r'\bgo out with me\b',
                 r'\bhold my hand\b', r'\bmarry me\b', r'\bin love with you\b', r'\blove you\b']
US = {'color': 'colour', 'favorite': 'favourite', 'favor': 'favour', 'center': 'centre', 'realize': 'realise',
      'organize': 'organise', 'gray': 'grey', 'mom': 'mum', 'honor': 'honour', 'neighbor': 'neighbour', 'theater': 'theatre',
      'apologize': 'apologise', 'recognize': 'recognise', 'traveled': 'travelled', 'cozy': 'cosy', 'defense': 'defence',
      'labor': 'labour', 'humor': 'humour', 'flavor': 'flavour', 'meter': 'metre', 'pajamas': 'pyjamas', 'cookie': 'biscuit'}
# capitalised words that aren't people (ship words, places, days, the Veyli...): names checks skip them
SHIP_WORDS = set('''I I'm I'll I've I'd OK Wren CSV Works Watch Survey Comms Helm Command Galley Infirmary Store Garden Deck Decks
Bridge Captain Commander Chief Chef Doctor Dr Envoy Cadet Officer Lieutenant Ensign Veyli Tiles Hesper Dock Mail Monday Tuesday
Wednesday Thursday Friday Saturday Sunday Sowing Greening Harvest Lanterns Board Mess Lounge Gym Shuttle Tern Coil Oi Ta
Mum Dad Gran Grandad Grandma Grandpa Nan Uncle Auntie Aunt Morning Evening Afternoon Night Hey Hi Hello Good Right Well
Admiral Moro Brenner Gull Bunk Engine Specialist Reactor Valo Coriel Lisk Kesh Marra Station Ostrander Tevan Port Halloran
New Aberdeen Halcyon Gerald Varga Fenn Arrowby Rook Midtour Year Lantern Jo Sam'''.split())   # Jo, Sam: your people back home


POSES = {'sigh', 'laugh', 'listen', 'nod', 'gesture', 'play'}   # the talk poses (section 8b) a meeting or moment line may ask for
MAX_REPLIES = 3
COMMON = set('''scanner patrol relay sweep telescope treadmill coffee ship odd somebody whose fridays mondays tuesdays wednesdays
thursdays saturdays sundays someone anybody everybody nobody nothing everything morning tonight tomorrow yesterday today
lunch dinner breakfast tea supper week weekend station deck dock rumour word news'''.split())   # ordinary words a line may start with


def roster(game):
    with open(game, encoding='utf-8') as f:
        html = f.read()
    people = {}
    for name in ('ROSTER', 'ROSTER_GUESTS', 'GUESTS'):     # crew, guests living aboard, and event guests and visitors
        m = re.search(r'^const ' + name + r' = \[\n(.*?)^\];', html, re.M | re.S)
        for l in (m.group(1).split('\n') if m else []):
            l = l.strip().rstrip(',')
            if l.startswith('{"id"'):
                p = json.loads(l)
                people[p['id']] = p
    return people, html


def flesch(text):
    words = re.findall(r"[A-Za-z']+", text)
    if not words:
        return 100.0
    sents = max(1, len(re.findall(r'[.!?]+', text)))
    syl = 0
    for w in words:
        w = w.lower().strip("'")
        groups = re.findall(r'[aeiouy]+', w)
        n = len(groups) - (1 if w.endswith('e') and len(groups) > 1 and not w.endswith('le') else 0)
        syl += max(1, n)
    return 206.835 - 1.015 * len(words) / sents - 84.6 * syl / len(words)


def main(argv):
    strict, quiet = '--strict' in argv, '--quiet' in argv
    args = [a for a in argv if not a.startswith('--')]
    game = args[0] if args else os.path.join(ROOT, 'starship-cadet.html')
    errors, warns = [], []
    try:
        out = cg.bake()
    except cg.GenError as e:
        print('ERROR ' + str(e))
        print('lines_check: FAIL (content_gen.py can\'t read content/)')
        return 1
    people, html = roster(game)
    # trait: and you: values, with _ for a space (trait:dry_humour, you:night_owl): the roster's traits, section 20's REP_TAGS
    m = re.search(r'^const REP_TAGS = \[(.*?)\];', html, re.M | re.S)
    VALUES['you'] = {t.replace(' ', '_') for t in re.findall(r"\['([^']+)'", m.group(1))} if m else None
    VALUES['trait'] = {t.replace(' ', '_') for p in people.values() for t in p.get('traits', [])} or None
    # trad: and came: values: section 18's traditions (SHIP_TRADITIONS) and the baked ones, plus today / any
    m = re.search(r'^const SHIP_TRADITIONS = \[\n(.*?)^\];', html, re.M | re.S)
    trads = set(re.findall(r"^  \{ id: '([^']+)'", m.group(1), re.M)) if m else set()
    trads |= {t['id'] for t in out['TRADITIONS'] if t.get('id')}
    VALUES['trad'] = (trads | {'today'}) if trads else None
    VALUES['came'] = (trads | {'any'}) if trads else None
    for k in ('you', 'trait', 'trad', 'came'):
        if not VALUES[k]:
            del VALUES[k]                                  # an older build without them: not checked
    names = set()
    for p in people.values():
        names.update(w.strip('.') for w in p['name'].split())
    known_words = SHIP_WORDS | names
    facts = os.path.join(cg.CONTENT, 'facts.md')       # the head writer's canon sheet: every capitalised word in it is known
    if os.path.exists(facts):
        known_words |= set(re.findall(r"\b[A-Z][a-z]+\b", open(facts, encoding='utf-8').read()))

    # every line, with where it came from: (where, kind, entry, speaker id or None, source)
    allx = []
    for cid, card in out['VOICE'].items():
        if cid not in people:
            errors.append(f'VOICE "{cid}": no such crew member or guest')
        for kind, es in card.get('lines', {}).items():
            allx += [(f'lines/{cid}', kind, e, cid, 'own') for e in es]
    for tpl, card in out['VOICE_TEMPLATES'].items():
        for kind, es in card.get('lines', {}).items():
            allx += [(f'template {tpl}', kind, e, None, 'tpl') for e in es]
    for kind, es in out['LINES'].items():
        allx += [('bank', kind, e, None, 'bank') for e in es]
    for c in out['CONVOS']:
        if all(l['who'] == 'A' for l in c['lines']):       # one speaker (a call home, a mutter): nobody else is in it
            bad = [k for k in ('pair', 'with') if c.get(k)] + (['{other}'] if any('{other}' in l['text'] for l in c['lines']) else [])
            if not (c.get('place') or c.get('act')):
                errors.append(f'overheard {c["topic"]} "{c["lines"][0]["text"]}": a one-speaker conversation needs place: or act: (where, or what they are doing)')
            if bad:
                errors.append(f'overheard {c["topic"]} "{c["lines"][0]["text"]}": a one-speaker conversation has no other person ({", ".join(bad)})')
        for l in c['lines']:
            allx.append((f'overheard {c["topic"]}', 'overheard', dict(c, text=l['text']), None, 'convo'))
    for tr in out['TRADITIONS']:                           # the traditions engineer's shape: text: { kind: [{ t, tone }] }
        for sec, es in tr.get('text', {}).items():
            allx += [(f'tradition {tr["id"]}', 'trad.' + sec, {'text': e.get('text', e.get('t')), 'tone': e.get('tone', 'light'), 'id': tr['id']}, None, 'trad') for e in es]
    # moments (story arcs and themes): every script line, the hint, keepsake, learn and Mail; when: values like a line's
    def moment_beats():
        for mid, b in out['MOMENTS'].items():
            yield f'arc {b["thread"][4:]} beat {b["beat"]}', b, b['who']
        for th, bs in out['MOMENT_THEMES'].items():
            for b in bs:
                yield f'theme {th} beat {b["beat"]}', b, 'them'
        for mid, b in out['HOME_MOMENTS'].items():
            yield f'call {b["thread"][4:]} beat {b["beat"]}', b, b['who']
    home_ids = {c['id'] for c in out['HOME_CONTACTS'].values()}   # the player's people back home: home:mum, ...
    for k, c in out['HOME_CONTACTS'].items():
        if k not in HOME_IDS:                              # content_gen makes sure its who: is home:<k>
            errors.append(f'call home.{k}: no such person back home (the contacts are {", ".join(sorted(HOME_IDS))})')
    known_words |= {w for c in out['HOME_CONTACTS'].values() for w in c.get('name', '').split()}
    for where, b, who in moment_beats():
        src = 'home' if where.startswith('call ') else 'moment'
        # a roster word used in a theme beat must be in its needs: (else social lets in people without it, and those lines
        # drop: a loss beat for someone who lost nobody); in story arcs (one known person) only {lost} must be
        if src == 'moment':
            texts = [b.get(k) or '' for k in ('hint', 'keepsake', 'learn')] + [(b.get('after') or {}).get('mail', {}).get('body', '')]
            for l in b['lines']:
                texts += [l['text']] if 'text' in l else [c[r]['text'] if r in ('reply', 'warm') else c['text'] for c in l['choice'] for r in ('text', 'reply', 'warm') if r == 'text' or r in c]
            used = set(re.findall(r'\{(home|since|kin|lost|hobbyNoun)\}', ' '.join(texts)))
            want = used if where.startswith('theme ') else used & {'lost'}
            for n in sorted(want - set(b.get('needs') or [])):
                errors.append(f'{where}: uses {{{n}}} but its needs: lacks {n} (people without it would get this beat with the line missing)')
        for n in b.get('needs') or []:
            if n not in NEEDS:
                errors.append(f'{where}: needs: {n} is not one of {", ".join(sorted(NEEDS))}')
            elif src == 'moment' and n in ('family', 'hobby'):
                errors.append(f'{where}: needs: {n}: use {"kin or lost" if n == "family" else "hobbyNoun"} (short, line-ready; the roster\'s {n} is a description)')
        if who not in people and who != 'them' and who not in home_ids:
            errors.append(f'{where}: who "{who}" is not a crew member or guest')
        allx.append((where, 'hint', {'text': b['hint'], 'id': where}, None, src)) if b.get('hint') else None
        for k in ('keepsake', 'learn'):
            if b.get(k):
                allx.append((where, 'moment', {'text': b[k], 'id': where}, None, src))
        if b.get('after', {}).get('mail'):
            allx.append((where, 'letter', {'text': b['after']['mail']['body'], 'id': where}, None, src))
        if b.get('when'):
            allx.append((where, 'moment', dict(b['when'], text='', id=where), None, src))
        for l in b['lines']:
            for x in ([l] if 'text' in l else [c for c in l['choice']] + [c[r] for c in l['choice'] for r in ('reply', 'warm') if r in c]):
                if x.get('who') and x['who'] not in people and x['who'] not in ('you', 'them') and x['who'] not in home_ids:
                    errors.append(f'{where}: speaker "{x["who"]}" is not a crew member, guest, them or you')
                allx.append((where, 'moment', {'text': x['text'], 'id': where}, None, src))
    for cid, es in out['HOME_SEND'].items():                # what you can tell them, and their reactions
        for e in es:
            allx.append((f'call home.{cid} send', 'moment', e, None, 'home'))
            if e.get('reply'):
                allx.append((f'call home.{cid} send', 'moment', {'text': e['reply']['text'], 'id': e['id']}, None, 'home'))
    for cid, cs in out['HOME_CHAT'].items():                # everyday calls
        for n, c in enumerate(cs, 1):
            if c.get('when'):
                allx.append((f'call home.{cid} chat {n}', 'moment', dict(c['when'], text='', id=f'{cid}.chat{n}'), None, 'home'))
            if any(x.get('send') for x in c['lines']):     # calls are one-sided since 0.62.0 (the user): you never tell them anything
                warns.append(f'call home.{cid} chat {n}: a "? send" line (calls are one-sided now; it is left out)')
            for x in c['lines']:
                if 'text' in x:
                    allx.append((f'call home.{cid} chat {n}', 'moment', {'text': x['text'], 'id': f'{cid}.chat{n}'}, None, 'home'))
    # poses and the number of replies, in moments and meetings
    scripts = [(w, b['lines']) for w, b, _ in moment_beats()] + [(f'meeting {k}', v['lines']) for k, v in out['MEETINGS_BAKED'].items()] \
        + [(f'call home.{k} chat', [x for c in cs for x in c['lines'] if 'text' in x]) for k, cs in out['HOME_CHAT'].items()]
    for where, ls in scripts:
        for l in ls:
            if 'choice' in l and len(l['choice']) > MAX_REPLIES:
                errors.append(f'{where}: {len(l["choice"])} replies in one choice (at most {MAX_REPLIES})')
            for x in ([l] if 'text' in l else [c[r] for c in l.get('choice', []) for r in ('reply', 'warm') if r in c]):
                if x.get('pose') and x['pose'] not in POSES:
                    errors.append(f'{where}: pose [{x["pose"]}] is not one of {", ".join(sorted(POSES))}')
    for mid, sc in out['MEETINGS_BAKED'].items():
        for l in sc['lines']:
            for x in ([l] if 'text' in l else [c for c in l['choice']] + [c['reply'] for c in l['choice'] if 'reply' in c]):
                allx.append((f'meeting {mid}', 'moment', {'text': x['text'], 'id': mid}, None, 'meet'))

    allowed = set()                                    # line ids the head writer has approved past the romance check
    al = os.path.join(cg.CONTENT, 'allow.list')
    if os.path.exists(al):
        for l in open(al, encoding='utf-8'):
            l = l.split('#')[0].strip()
            if l:
                allowed.add(l.split()[0])
    vocab = set()
    for x in allx:
        vocab.update(re.findall(r"\b[a-z][a-z']+\b", x[2]['text']))
    seen = {}
    for where, kind, e, cid, src in allx:
        t, tag = e['text'], f'{where} [{kind}] "{e["text"][:50]}"'
        if not t and src not in ('moment', 'home'):
            continue
        if src == 'moment' and re.search(r'\{(family|hobby)\}', t):   # story arcs and themes: the roster's descriptions don't fit a sentence
            errors.append(f'{tag}: {{family}} / {{hobby}} read as descriptions ("late wife, who I still talk about"): use {{kin}} or {{lost}} ("my gran") or {{hobbyNoun}} ("knitting")')
        if re.search(r'\bmy \{(kin|lost)\}', t, re.I):
            errors.append(f'{tag}: {{kin}} and {{lost}} include the "my" ("my gran"): write {{kin}}, not "my {{kin}}"')
        for tok in re.findall(r'\{([^}]*)\}', t):
            if (tok not in TRAD_PLACEHOLDERS) if kind.startswith('trad.') else (tok not in TOKENS | PLACEHOLDERS):
                errors.append(f'{tag}: unknown token {{{tok}}}')
        if t.count('{') != t.count('}'):
            errors.append(f'{tag}: unbalanced braces')
        # conditions' values
        for scope in (e, e.get('not', {})):
            for k, v in scope.items():
                if k in VALUES:
                    for x in (v if isinstance(v, list) else [v]):
                        for alt in str(x).split('|'):
                            if (alt.replace(' ', '_') if k in ('you', 'trait') else alt) not in VALUES[k]:
                                errors.append(f'{tag}: {k}:{alt} is not one of {", ".join(sorted(VALUES[k]))}')
                if k == 'aff':
                    for x in (v if isinstance(v, list) else [v]):
                        for alt in str(x).split('|'):
                            band = alt.rsplit(':', 1)
                            if band[-1] not in {'rival', 'neutral', 'friend'} or (len(band) == 2 and band[0] not in people):
                                errors.append(f'{tag}: aff is aff:rival|neutral|friend or aff:<crewId>:<band>')
                if scope is e and (k, v) in (('rep', 'new'), ('ship.work', 'low'), ('ship.kindness', 'low'), ('ship.spirit', 'low')):
                    warns.append(f'{tag}: {k}:{v} is always true ("at least {v}"); for "only {v}" write !{k}:{"known" if k == "rep" else "ok"}')
                if k == 'cue':
                    for x in (v if isinstance(v, list) else [v]):
                        for alt in str(x).split('|'):
                            if '@' in alt and alt.split('@', 1)[1] not in ('me', 'dept'):
                                errors.append(f'{tag}: cue:{alt}: after @ only "me" or "dept"')
                if k in ('who', 'with'):
                    for x in (v if isinstance(v, list) else [v]):
                        for alt in str(x).split('|'):
                            if alt not in people:
                                errors.append(f'{tag}: {k}:{alt} is not a crew id')
                if k == 'pair':
                    for x in (v if isinstance(v, list) else [v]):
                        for alt in str(x).split('|'):
                            if '+' not in alt and alt not in PAIR_WORDS:
                                errors.append(f'{tag}: pair:{alt} is not x+y or one of {", ".join(sorted(PAIR_WORDS))}')
                            for side in (alt.split('+') if '+' in alt else []):
                                if side not in people and side not in VALUES['dept'] and side not in VALUES['rank'] and side != 'any':
                                    errors.append(f'{tag}: pair:{alt}: "{side}" is not a department, rank, crew id or any')
                if k == 'moved':
                    for x in (v if isinstance(v, list) else [v]):
                        if x not in people:
                            errors.append(f'{tag}: moved:{x} is not a crew id')
                if k in ('beat', 'beatIs'):
                    for x in (v if isinstance(v, list) else [v]):
                        if not re.fullmatch(r'[\w.-]+\.\d+', x):
                            errors.append(f'{tag}: beat is like beat:tomas.3 (arc id, a dot, beats told)')
        # length, with names filled in
        n = len(re.sub(r'\{[^}]*\}', 'x' * NAME_W, t))
        lim = 90 if kind in ('trad.chatter', 'trad.ask', 'trad.here') else 200 if kind in ('trad.mail', 'trad.thanks') or kind.startswith(('tip.', 'join.')) else 400 if kind == 'letter' or kind.startswith('mail.') or kind in ('promo.announce.mail', 'promo.mail', 'promo.captain') else 60 if kind in BUBBLE_KINDS else 140 if kind.startswith(LONG_KINDS) else CARD
        if not e.get('old'):
            if n > (90 if kind in BUBBLE_KINDS else lim):
                errors.append(f'{tag}: {n} characters (at most {lim})')
            elif n > lim:
                warns.append(f'{tag}: {n} characters (a bubble wants {lim} or fewer)')
        low = t.lower()
        bonds = ' '.join(str(x) for x in (e.get('bond') if isinstance(e.get('bond'), list) else [e.get('bond', '')]))
        # couple words are allowed only in an overheard conversation between a couple (pair:couple or bond:couple) or a line
        # gated on bond:couple, and never in a line with any reference to the player ({me}, {nick}, the new hand, cadet,
        # newcomer, you, your), whatever the kind
        couple = 'couple' in bonds or 'partner' in bonds or 'couple' in str(e.get('pair', ''))
        at_you = re.search(r"\{me\}|\{nick\}|\bnew (?:hand|cadet)\b|\bcadets?\b|\bnewcomer\b|\byou(?:r|rs|rself)?\b", low)
        about_crew = couple and not at_you
        # calls home: only family warmth is exempt (a plain "love you", "I love you"); every other romance word stays an
        # error ("I'm still in love with you" fails on "in love")
        family = [x for x in BANNED_PLAYER + BANNED_AT_YOU if x != r'\blove you\b']
        romance = [] if e.get('id') in allowed else family if src == 'home' else BANNED_AT_YOU if about_crew else BANNED_PLAYER
        for b in (BANNED if src != 'home' else [x for x in BANNED if x != r'\blove you\b']) + romance:
            m = re.search(b, low)
            if m:
                errors.append(f'{tag}: "{m.group(0)}" is on the banned list' + (' (no romance with the player: reword, or ask the head writer to add the line id ' + str(e.get('id')) + ' to content/allow.list)' if b in BANNED_PLAYER + BANNED_AT_YOU else ''))
        for us, uk in US.items():
            if re.search(r'\b' + us + r's?\b', low):
                warns.append(f'{tag}: American spelling "{us}" (British: "{uk}")')
        mems = [str(x) for x in (e.get('mem') if isinstance(e.get('mem'), list) else [e.get('mem')]) if x]
        if e.get('tone') == 'serious' and not ((e.get('tier') and e['tier'][0] >= 3) or e.get('beat') or e.get('beatIs') or any(m.startswith('moment') for m in mems)
                                               or 'soon' in str(e.get('leaving', '')) or kind.startswith(('story', 'arc', 'moment'))):
            errors.append(f'{tag}: #serious needs tier>=friend, a beat:, mem:moment or leaving:soon (serious moments are earned)')
        if cid and e.get('habit'):
            have = set(people.get(cid, {}).get('habits', [])) | {h.get('add') for h in people.get(cid, {}).get('habitShifts', []) if h.get('add')}
            for h in (e['habit'] if isinstance(e['habit'], list) else [e['habit']]):
                if not set(h.split('|')) & have:
                    warns.append(f'{tag}: {cid} doesn\'t have the habit "{h}"')
        # names: capitalised words mid-sentence that aren't crew, guests or ship words
        for m in re.finditer(r'(?<![.!?]\s)(?<!^)(?<!["(])\b([A-Z][a-z]+)\b', t):
            w = m.group(1)
            if w not in known_words and w.lower() not in vocab and w.lower() not in COMMON and m.start() > 0 and not re.search(r'[.!?:]\s*$', t[:m.start()]):
                warns.append(f'{tag}: "{w}" isn\'t a crew member, guest or ship word (a name only from the roster)')
        for m in re.finditer(r"\b([A-Z][a-z]+)(?:'s\b| says\b| said\b| told\b| thinks\b| wants\b| is\b| was\b| and I\b)", t):
            if m.group(1) not in known_words and m.group(1).lower() not in vocab and m.group(1).lower() not in COMMON and m.group(1) not in ('It', 'That', 'This', 'There', 'What', 'Who', 'Everyone', 'Nobody', 'Someone', 'Here', 'He', 'She', 'Today', 'Tomorrow', 'Dinner', 'Breakfast', 'Lunch', 'Food', 'Nothing', 'Something', 'Life', 'Home', 'Work',
                                                                       'Or', 'How', 'Why', 'When', 'Where', 'Which', 'Everything', 'Anyone', 'Anything', 'Mine', 'Yours',
                                                                       'His', 'Her', 'Their', 'Our', 'Your', 'My', 'One', 'Each', 'Now', 'Then', 'So', 'Yes', 'No', 'Yesterday'):
                warns.append(f'{tag}: "{m.group(1)}" looks like a name that isn\'t crew or a guest')
        key = (kind, t)
        if key in seen and src not in ('convo', 'moment', 'home') and t:
            warns.append(f'{tag}: the same line is also in {seen[key]}')
        seen.setdefault(key, where)

    # reading ease per file
    byfile = {}
    for where, kind, e, cid, src in allx:
        byfile.setdefault(where, []).append(e['text'])
    ease = {w: flesch(' '.join(ts)) for w, ts in byfile.items()}
    for w, s in sorted(ease.items()):
        if s < 60:
            warns.append(f'{w}: reading ease {s:.0f} (aim for 60 or more: short words, short sentences)')

    # the baked blocks are up to date
    new = html
    for name, body in cg.blocks(out).items():
        try:
            new = cg.splice(new, name, body)
        except cg.GenError as e:
            errors.append(str(e))
    if new != html:
        errors.append('the baked blocks in the game file are out of date: run python3 content_gen.py')

    # coverage per person (their own lines) against the plan's targets
    crew = [p for p in people.values() if p.get('rank') != 'guest']
    story = {p['id'] for p in crew if p.get('story')} | {'torres-zeke', 'calder', 'brennan', 'kovac-zainab'}
    def target(p):
        if p['id'] in story:
            return 200
        if p.get('dept') == 'works' or (p.get('bed') or '').startswith('4-B1'):
            return 60
        return 30
    cov, kinds_seen = [], set()
    for p in crew:
        card = out['VOICE'].get(p['id'], {})
        n = sum(len(v) for v in card.get('lines', {}).values())
        kinds_seen.update(card.get('lines', {}).keys())
        cov.append((p['id'], n, target(p), 'words' in card, sorted(card.get('lines', {}).keys())))
    with_card = sum(1 for c in cov if c[3])
    short = [c for c in cov if c[1] < c[2]]
    if strict:
        for c in short:
            errors.append(f'{c[0]}: {c[1]} lines of their own (target {c[2]})')
        for c in cov:
            if not c[3]:
                errors.append(f'{c[0]}: no voice card')

    # the voice budget for a ship day: the rules (section 22 and 20 enforce them) and what the banks can supply
    serious = sum(1 for x in allx if x[2].get('tone') == 'serious')
    budget = [
        'one bubble or one overheard conversation on screen at a time; none while a chat card or meeting is open',
        'at most one #serious line a day (ship-wide); reactions once per person per kind per day',
        'overheard conversations and reactions never repeat to you within 7 ship days (the saved ring)',
        f'supply: {len(out["CONVOS"])} overheard conversations (a week of evenings wants about 30), '
        f'{len(out["LINES"].get("cue", []))} reaction lines, {serious} #serious lines',
    ]

    print(f'lines_check: {len(allx)} lines in {len(byfile)} places; {len(out["VOICE"])} voice cards '
          f'({with_card} with words) for {len(crew)} crew; {len(out["CONVOS"])} conversations; '
          f'{len(out["MOMENTS"])} moments; {len(out["MOMENT_THEMES"])} themes; {len(out["MEETINGS_BAKED"])} meetings; {len(out["TRADITIONS"])} traditions')
    if not quiet:
        print('coverage (own lines / target), people with any:')
        for c in cov:
            if c[1] or c[3]:
                print(f'  {c[0]:<18} {c[1]:>4} / {c[2]:<4} card: {"yes" if c[3] else "no "}  kinds: {", ".join(c[4])}')
        print(f'  {len(short)} of {len(crew)} crew below their target (expected until the writers start)')
        print('voice budget (a ship day):')
        for b in budget:
            print('  ' + b)
        print('reading ease: ' + ', '.join(f'{w} {s:.0f}' for w, s in sorted(ease.items())))
    for w in warns:
        print('warn  ' + w)
    for e in errors:
        print('ERROR ' + e)
    print(f'lines_check: {"FAIL" if errors else "PASS"} ({len(errors)} errors, {len(warns)} warnings)')
    return 1 if errors else 0


# ---- the voice budget, played (0.43.19): --day runs the real game in a browser (cadet_test.py's Game: a virtual
# clock, frames stepped by hand) through a ship day's busy places with the player standing among the crew, logs every
# speech bubble (section 8b's bubbleSay, wrapped), and checks the budget's rules: at most two bubbles on screen, one
# conversation at a time and no other talk while it plays, nothing new while a chat card or meeting is open, at most one
# #serious conversation or reaction a day, nobody reacting to a kind twice a day, nothing from the ring said twice.
DAY_VISITS = [   # deck, ship minute of Day 1, what to stand by (a crowd, or someone doing this), real seconds
    (3, 7 * 60 + 10, 'crowd', 90), (5, 10 * 60, 'work', 60), (4, 13 * 60, 'crowd', 60), (3, 18 * 60 + 10, 'crowd', 120),
    (3, 19 * 60 + 30, 'callhome', 60), (3, 20 * 60 + 40, 'crowd', 90)]
DAY_WRAP = r"""(() => {
  window.__B = []; window.__R = 0;
  const say = bubbleSay; bubbleSay = (who, text, secs) => { const b = say(who, text, secs);
    const a = DECK_CREW.find(x => x.h === who);
    if (b) __B.push({ t: Math.floor(shipNow()), who: a ? a.p.id : '?', text, ovh: OVH ? OVH.lines.id : null, react: __R, chat: !!CHAT,
      dlg: typeof DIALOGUE !== 'undefined' && !!DIALOGUE, on: bubbles.list.length }); return b; };
  const lr = linesReact; linesReact = (...a) => { __R = 1; try { return lr(...a); } finally { __R = 0; } };
})()"""
DAY_STAND = r"""(F => { const c = DECK_CREW.filter(a => a.h); let best = F === 'crowd' ? null : c.find(a => (whereIs(a.p, shipNow()) || {}).act === F), n = -1;
  if (!best) for (const a of c) { const k = c.filter(b => Math.hypot(a.x - b.x, a.z - b.z) < 3).length; if (k > n) { n = k; best = a; } }
  if (best) { player.obj.position.set(best.x + 1, 0, best.z + 1); target.copy(player.obj.position).setY(.7); }
  return best ? best.p.id : null; })"""


def voice_day(game):
    import pathlib
    here = os.path.dirname(os.path.abspath(__file__))
    src = open(os.path.join(here, 'cadet_test.py'), encoding='utf-8').read().split('a, shots = run(')[0]
    env = {'__name__': 'cadet_day'}
    exec(src, env)
    errors, notes = [], []
    with env['sync_playwright']() as pw:
        g = env['Game'](pw, game)
        if not g.ev("typeof linesTick === 'function' && typeof CONVOS !== 'undefined'"):
            print('lines_check --day: this build has no overheard conversations (section 22 before 0.43.12)'); g.close(); return 1
        g.ev(DAY_WRAP)
        peak, overlap = 0, 0
        for n, (deck, at, focus, secs) in enumerate(DAY_VISITS):
            g.ev(f'goToDeck({deck}); skipTo({at});'); g.step(30)
            who = g.ev(DAY_STAND + f"('{focus}')")
            for k in range(secs):
                if n == 3 and k == secs // 2:      # a chat card mid-dinner: nothing new while it's open, and a conversation stops
                    g.ev("(() => { const a = DECK_CREW.find(a => a.h); if (a) chatOpen(a.p); })()")
                if n == 3 and k == secs // 2 + 10:
                    g.ev('chatClose()')
                g.step(30)
                r = g.ev("[bubbles.list.length, OVH ? OVH.lines.id : null, bubbles.list.filter(b => OVH && !OVH.bub.includes(b)).length]")
                peak = max(peak, r[0])
                if r[1] and r[2]:
                    overlap += 1
            notes.append(f'visit {n + 1}: Deck {deck} {at // 60:02d}:{at % 60:02d} by {who or "nobody"}')
        B = g.ev('__B')
        L = g.ev('SHIP.lines')
        serious = g.ev("(SHIP.lines.ring || []).filter(([id]) => (CONVOS.find(c => c.id === id) || (LINES.cue || []).find(e => e.id === id) || {}).tone === 'serious').length")
        errs = g.errors
        g.close()
    convs = sorted({b['ovh'] for b in B if b['ovh']})
    reacts = [b for b in B if b['react']]
    other = [b for b in B if not b['ovh'] and not b['react']]
    if peak > 2:
        errors.append(f'{peak} bubbles on screen at once (at most two)')
    if serious > 1:
        errors.append(f'{serious} #serious conversations or reactions in a day (at most one)')
    if overlap:
        errors.append(f'other talk on screen during a conversation ({overlap} seconds)')
    for b in B:
        if b['chat'] or b['dlg']:
            errors.append(f'a bubble while a chat card or meeting was open: {b["who"]}: {b["text"]}')
    ids = [r[0] for r in L.get('ring', [])]
    if len(ids) != len(set(ids)):
        errors.append('a conversation or reaction was heard twice in a day: ' + ', '.join(sorted({i for i in ids if ids.count(i) > 1})))
    for pid, r in (L.get('reacted') or {}).items():
        if len(r['kinds']) != len(set(r['kinds'])):
            errors.append(f'{pid} reacted to the same kind twice in a day')
    if errs:
        errors += ['game: ' + e for e in errs[:5]]
    for x in notes:
        print('  ' + x)
    print(f'  {len(convs)} conversations, {len(reacts)} reactions, {len(other)} other bubbles (section 20\'s chatter); peak {peak} bubbles')
    for b in B[:400]:
        print(f'    {b["t"] // 60 % 24:02d}:{b["t"] % 60:02d} {"conv " if b["ovh"] else "react" if b["react"] else "other"} {b["who"]}: {b["text"]}')
    for e in errors:
        print('ERROR ' + e)
    print(f'lines_check --day: {"FAIL" if errors else "PASS"} ({len(errors)} errors)')
    return 1 if errors else 0


if __name__ == '__main__':
    if '--day' in sys.argv:
        a = [x for x in sys.argv[1:] if not x.startswith('--')]
        sys.exit(voice_day(os.path.abspath(a[0]) if a else os.path.join(ROOT, 'starship-cadet.html')))
    sys.exit(main(sys.argv[1:]))
