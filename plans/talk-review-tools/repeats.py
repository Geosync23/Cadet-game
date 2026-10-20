# TR1: repeat and food counts across the whole Talk a while pack (run from the repo root):
#   python3 plans/talk-review-tools/repeats.py
import re, collections, os, sys
sys.argv = ['x', 'none']
exec(open(os.path.join(os.path.dirname(__file__), 'tp.py')).read().split("mode=")[0])
def norm(x): return re.sub(r'\W+', ' ', txt(x).lower()).strip()
def lines(t): return t['them'] + [t['ask']] + list(t['rep'].values()) + list(t['ans'].values())
c = collections.defaultdict(list)
for t in talks:
    for i, x in lines(t): c[norm(x)].append('%s:%d' % (t['file'].replace('.talk', ''), i))
dups = {k: v for k, v in c.items() if len(v) > 1}
print('talks', len(talks), '| word-for-word repeated lines:', len(dups))
for k, v in dups.items(): print('  DUP', k, v)
W = [t for t in talks if t['file'].startswith('work-')]
food = r'[Bb]iscuit|[Tt]oast|seconds|[Dd]inner|pudding|[Bb]reakfast|appetite|[Ss]oup|snack|\beat|food|helping|tea\b'
for name, T in (('work', W), ('pool+own', [t for t in talks if t not in W])):
    has = lambda t, p: any(re.search(p, x, re.I) for _, x in lines(t))
    print(f'{name}: {len(T)} talks; food/tea cheers {sum(bool(re.search(food, t["rep"]["cheer"][1])) for t in T)}; '
          f'biscuit talks {sum(has(t, "biscuit") for t in T)}; habit asks {sum(bool(re.search("habit", t["ask"][1], re.I)) for t in T)}; '
          f'"nobody knows/notices" {sum(has(t, r"never know|nobody (knows|notices|thinks)") for t in T)}')
