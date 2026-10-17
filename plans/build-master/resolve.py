#!/usr/bin/env python3
"""Resolve merge-conflict hunks that are only build-number differences.
usage: resolve.py FILE BUILD [--union]
 - build lines (header 'build x.y.z', GAME_BUILD, HUD) are set to BUILD on both sides
 - equal after that -> taken; one side contained in the other -> the larger taken
 - --union (DEV_NOTES): ours then theirs' extra lines
Anything else is left as a conflict and reported."""
import re, sys
path, build = sys.argv[1], sys.argv[2]
union = '--union' in sys.argv
src = open(path).read().split('\n')
pat = [(re.compile(r"(build )\d+\.\d+\.\d+"), r"\g<1>" + build),
       (re.compile(r"(GAME_BUILD = ')\d+\.\d+\.\d+"), r"\g<1>" + build)]
def norm(l):
    for p, r in pat:
        if p.search(l): l = p.sub(r, l).rstrip()
    return l
def key(l):
    return re.sub(r'\s+', ' ', l) if any(p.search(l) for p, _ in pat) else l
def contains(big, small):
    big, small = [key(x) for x in big], [key(x) for x in small]
    n = len(small)
    return any(big[i:i+n] == small for i in range(len(big) - n + 1))
out, i, left = [], 0, 0
while i < len(src):
    l = src[i]
    if l.startswith('<<<<<<< '):
        a, b, j = [], [], i + 1
        while not src[j].startswith(('=======', '|||||||')): a.append(src[j]); j += 1
        if src[j].startswith('|||||||'):
            while not src[j].startswith('======='): j += 1
        j += 1
        while not src[j].startswith('>>>>>>> '): b.append(src[j]); j += 1
        na, nb = [norm(x) for x in a], [norm(x) for x in b]
        if [key(x) for x in na] == [key(x) for x in nb]: out += na
        elif contains(na, nb): out += na
        elif contains(nb, na): out += nb
        elif union: out += na + [x for x in nb if x not in na]
        else:
            left += 1; print(f'left at line {len(out)+1}: ours {len(a)} / theirs {len(b)}')
            out += [src[i]] + a + ['======='] + b + [src[j]]
        i = j + 1
    else:
        out.append(l); i += 1
open(path, 'w').write('\n'.join(out))
print(path, 'unresolved hunks:', left)
