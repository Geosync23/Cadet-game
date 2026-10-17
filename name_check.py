# Starship Cadet: name check (the reviewers'; run it on every combine candidate)
# The game is one script: two sections that declare the same top-level name (const, let, var, function, class) make the
# whole file a SyntaxError, and nothing runs. Each branch alone is fine, so only a combine shows it. This finds it first.
#   python3 name_check.py BUILD.html
#       one file (a combined build): names declared twice at the top level, and a syntax check with node if it's installed
#   python3 name_check.py --branches BASE REF [REF ...]
#       git refs (e.g. origin/claude/ship-integration origin/claude/social origin/claude/arrival): the names each branch
#       adds over BASE, any name two branches both add (they will clash when combined), and any top-level name a
#       branch deletes but still uses (a ReferenceError at run time; node --check can't see it)
#   python3 name_check.py --branches LAST_REVIEWED NEW
#       re-reviewing one branch: the same, against its own last reviewed commit. Catches a helper deleting a name that
#       only ever existed on its branch (social f05d7db deleted socP and still called it)
# Top level means a declaration at the start of a line, which is how the game file is written (the code inside the one
# IIFE isn't indented). No browser needed; a second or two.
import re, subprocess, sys, tempfile, os

def declared(text):
    out = {}; cont = False                             # cont: the line before was a const/let/var line ending in ','
    for i, line in enumerate(text.split('\n')):
        m = re.match(r'^(?:async\s+)?(const|let|var|function\*?|class)\s+(.*)', line)
        if not m and cont:                              # a declarator carried on to the next line: const A = 1,\n      B = 2;
            m = re.match(r'^\s+()([A-Za-z_$][\w$]*\s*=(?!=).*)', line)
        if not m: cont = False; continue
        cont = bool(re.search(r',\s*(//.*)?$', line)) and (m.group(1) not in ('function', 'class'))
        kind, rest = m.group(1), m.group(2)
        if kind and (kind.startswith('function') or kind == 'class'):
            n = re.match(r'\*?\s*([A-Za-z_$][\w$]*)', rest)
            if n: out.setdefault(n.group(1), []).append(i + 1)
            continue
        depth, cur, parts, q = 0, '', [], None          # split the declarators: a = 1, b = [..], c = () => {..}
        for ch in rest:
            if q:
                cur += ch
                if ch == q: q = None
                continue
            if ch in '\'"`': q = ch
            elif ch in '([{': depth += 1
            elif ch in ')]}': depth -= 1
            if ch == ',' and depth == 0: parts.append(cur); cur = ''
            else: cur += ch
        parts.append(cur)
        for p in parts:
            n = re.match(r'\s*([A-Za-z_$][\w$]*)\s*(=|;|$)', p)
            if n: out.setdefault(n.group(1), []).append(i + 1)
            d = re.match(r'\s*[{\[]', p)                # const { a, b } = ...: destructuring
            if d:
                for nm in re.findall(r'([A-Za-z_$][\w$]*)\s*(?=[,}\]])', p.split('=')[0]): out.setdefault(nm, []).append(i + 1)
    return out

def script_of(html):
    js = re.findall(r'<script>(.*?)</script>', html, re.S)
    return max(js, key=len) if js else html

def one_file(path):
    html = open(path).read(); ok = True
    dup = {k: v for k, v in declared(script_of(html)).items() if len(v) > 1}
    for k, v in sorted(dup.items()):
        ok = False; print(f'  DECLARED TWICE: {k} at lines {v} (of the script)')
    try:
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as f: f.write(script_of(html)); tmp = f.name
        r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        if r.returncode: ok = False; print('  SYNTAX ERROR:', ' | '.join(l for l in r.stderr.split('\n') if l.strip())[:600])
        else: print('  node --check: the script parses')
        os.unlink(tmp)
    except FileNotFoundError:
        print('  (node not installed: syntax not checked)')
    return ok

def show(ref):
    return subprocess.run(['git', 'show', ref + ':starship-cadet.html'], capture_output=True, text=True, check=True).stdout

def branches(base, refs):
    b = declared(script_of(show(base))); seen = {}; ok = True
    for ref in refs:
        try: n = declared(script_of(show(ref)))
        except subprocess.CalledProcessError: print(f'  {ref}: no starship-cadet.html'); continue
        if subprocess.run(['git', 'merge-base', '--is-ancestor', ref, base]).returncode == 0:
            print(f'  {ref}: already in {base}, skipped'); continue
        added = [k for k in n if k not in b]
        print(f'  {ref}: {len(added)} new names')
        src = script_of(show(ref))                      # a name the branch deleted but still uses: a ReferenceError at run time
        for k in b:
            if k not in n and re.search(r'(?<![\w$.])' + re.escape(k) + r'(?![\w$])', src): ok = False; print(f'  {ref}: DELETED BUT STILL USED: {k}')
        for k in added: seen.setdefault(k, []).append(ref)
        for k, v in n.items():
            if len(v) > 1 and len(b.get(k, [])) < 2: ok = False; print(f'  {ref}: DECLARED TWICE inside the branch: {k} at {v}')
    for k, l in sorted(seen.items()):
        if len(l) > 1: ok = False; print(f'  CLASH when combined: {k} is new in {", ".join(l)}')
    return ok

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__ if __doc__ else 'usage: name_check.py BUILD.html | --branches BASE REF...'); sys.exit(2)
    ok = branches(a[1], a[2:]) if a[0] == '--branches' else all(one_file(p) for p in a)
    print('NAMES OK' if ok else 'NAMES CLASH')
    sys.exit(0 if ok else 1)
