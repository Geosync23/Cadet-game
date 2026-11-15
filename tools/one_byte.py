#!/usr/bin/env python3
# tools/one_byte.py (FR1's review, A10): put the game's script in one-byte form. Run it LAST on a staging branch, after
# every word change is in; it can be run again at any time (a script already in one-byte form comes out unchanged).
#
#   python3 tools/one_byte.py [GAME.html]          convert in place, then prove it
#   python3 tools/one_byte.py --check [GAME.html]  say how many characters would change; change nothing (exit 1 if any)
#
# Why: the browser keeps the script's text in memory. One character outside Latin-1 (an arrow, a long dash, a star,
# a device glyph) anywhere in it makes the browser hold all 8.8 million characters at two bytes each: 17.7 MB instead
# of 8.85 MB (measured by a memory snapshot on 0.99.91). There were 161 such characters.
# What it does to the main script (the page's HTML and CSS before it are left alone):
#   - in a string, a template or a regular expression: the character becomes its \uXXXX escape (the same string);
#   - in a comment: plain words (-> for an arrow, ... for an ellipsis, - for a long dash), or U+XXXX;
#   - adds the mark "[one-byte script]" as the script's first line (a comment). With the mark, content_gen.py writes
#     baked words the same way and names_check.js fails on any new such character.
# Then it proves the script reads the same: every token of the script before and after must be equal, kind for kind
# and value for value; only a regular expression's own text may differ, and only by the escapes. And content_gen.py
# --check must say "up to date" on the result. On any failure the file is put back as it was and the exit code is 1.
# The build master still runs cadet_test (old against new: ALL IDENTICAL) and check_fast after it.
# Needs node and acorn in $CADET_WORK/acorn (as names_check.js does).
import sys, os, re, json, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACORN = os.path.join(os.environ.get('ACORN_DIR') or os.path.join(os.environ.get('CADET_WORK', '/tmp/cadet-work'), 'acorn/package'), 'dist/acorn.js')
MARK = '[one-byte script]'
MARK_LINE = '// ' + MARK + ' (tools/one_byte.py; FR1\'s review, A10): no character outside Latin-1 below. In a string write \\uXXXX; in a comment, plain words. names_check fails on one.\n'
PLAIN = {'→': '->', '←': '<-', '…': '...', '—': '-', '–': '-', '−': '-', '’': "'", '‘': "'", '“': '"', '”': '"', '↓': 'down', '↑': 'up', '≥': '>=', '≤': '<=', '×': 'x'}
COMMENTS_JS = "const fs=require('fs'),acorn=require(process.argv[1]);const src=fs.readFileSync(0,'utf8');const c=[];acorn.parse(src,{ecmaVersion:2022,sourceType:'script',onComment:(b,t,st,en)=>c.push([st,en])});console.log(JSON.stringify(c));"
TOKENS_JS = "const fs=require('fs'),acorn=require(process.argv[1]);const src=fs.readFileSync(0,'utf8');const o=[];for(const t of acorn.tokenizer(src,{ecmaVersion:2022}))o.push([t.type.label,t.value&&t.value.pattern!==undefined?t.value.pattern+'/'+t.value.flags:String(t.value)]);console.log(JSON.stringify(o));"

def node(js, text):
    return json.loads(subprocess.run(['node', '-e', js, ACORN], input=text, capture_output=True, text=True, check=True).stdout)

def bounds(html):
    i = html.index('<script>\n', html.index('three.min.js')) + 9
    return i, html.rindex('</script>')

def convert(src):
    if any(ord(ch) > 0xffff for ch in src): sys.exit('one_byte: a character beyond U+FFFF in the script; write it by hand as a \\u{...} escape')
    incom = bytearray(len(src))
    for a, b in node(COMMENTS_JS, src):
        incom[a:b] = b'\x01' * (b - a)
    out = []; nc = ns = 0
    for k, ch in enumerate(src):
        if ord(ch) < 256: out.append(ch)
        elif incom[k]: out.append(PLAIN.get(ch, 'U+%04X' % ord(ch))); nc += 1
        else: out.append('\\u%04x' % ord(ch)); ns += 1
    return ''.join(out), nc, ns

def main(argv):
    check = '--check' in argv; args = [a for a in argv if not a.startswith('--')]
    game = args[0] if args else os.path.join(ROOT, 'starship-cadet.html')
    html = open(game, encoding='utf8').read(); i, j = bounds(html); src = html[i:j]
    new, nc, ns = convert(src)
    if MARK not in new: new = MARK_LINE + new
    if check:
        print(f'one_byte: {nc + ns} character(s) outside Latin-1 in the script ({ns} in code, {nc} in comments); the mark is ' + ('there' if MARK in src else 'not there'))
        return 1 if nc + ns or MARK not in src else 0
    if new == src: print('one_byte: already in one-byte form, nothing to do'); return 0
    a, b = node(TOKENS_JS, src), node(TOKENS_JS, new); bad = []
    if len(a) != len(b): bad.append(f'token counts differ: {len(a)} before, {len(b)} after')
    else:
        esc = lambda t: re.sub(r'[^\x00-\xff]', lambda m: '\\u%04x' % ord(m.group(0)), t)
        rx = 0
        for x, y in zip(a, b):
            if x == y: continue
            if x[0] == y[0] == 'regexp' and esc(x[1]) == y[1]: rx += 1; continue
            bad.append(f'a token differs: {str(x)[:90]} -> {str(y)[:90]}')
        print(f'one_byte: {len(a)} tokens read the same' + (f' ({rx} regular expression(s) now hold an escape in their own text: the same match)' if rx else ''))
    if not bad:
        open(game, 'w', encoding='utf8').write(html[:i] + new + html[j:])
        r = subprocess.run([sys.executable, os.path.join(ROOT, 'content_gen.py'), '--check', game], capture_output=True, text=True)
        if r.returncode != 0: bad.append('content_gen.py --check on the result: ' + (r.stdout + r.stderr).strip()[:200])
    if bad:
        open(game, 'w', encoding='utf8').write(html)
        for x in bad[:8]: print('FAIL ' + x)
        print('one_byte: FAILED, the game file is as it was'); return 1
    print(f'one_byte: done: {ns} character(s) in code written as escapes, {nc} in comments as plain words, the mark added. Now run cadet_test (old against new) and check_fast.')
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
