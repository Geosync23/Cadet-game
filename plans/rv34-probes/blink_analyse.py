# RV34: compare blink traces: on vs off (same frames), calm vs off. Pulses, rate, size, return, draw calls.
import json, sys
A = json.load(open('/tmp/rv34/trace_off.json'))
for tag in sys.argv[1:]:
    B = json.load(open(f'/tmp/rv34/trace_{tag}.json'))
    for d in '1234567':
        a, b = A[d]['trace'], B[d]['trace']
        assert len(a) == len(b) and all(abs(x[0] - y[0]) < 1e-9 for x, y in zip(a, b)), 'frames differ'
        diff = [i for i, (x, y) in enumerate(zip(a, b)) if x[3:15] != y[3:15]]
        calls = [(x[15], y[15]) for x, y in zip(a, b) if x[15] is not None]
        ratio = [y[6] / x[6] for x, y in zip(a, b)]                       # hemi intensity, on / off
        dcol = [abs(y[5] - x[5]) for x, y in zip(a, b)]                    # hemi blue shift
        # pulses: rises of the hemi ratio past half its peak
        pk = max(ratio); thr = 1 + (pk - 1) / 2 if pk > 1.001 else None
        rises = []; up = False
        sig = ratio if thr else dcol; th = thr if thr else max(dcol) / 2
        for i, v in enumerate(sig):
            if v > th and not up: rises.append(b[i][0]); up = True
            elif v <= th: up = False
        span = (b[diff[0]][2], b[diff[-1]][2]) if diff else None
        print(tag, d, 'frames changed', len(diff), 'from se', span and round(span[0], 3), 'to', span and round(span[1], 3),
              '| last 60 frames identical', not any(i >= len(a) - 60 for i in diff), '| hemi x', round(pk, 3), 'blue +', round(max(dcol), 3),
              '| pulses', len(rises), [round(r, 2) for r in rises], '| calls same', all(x == y for x, y in calls), sorted(set(c[1] for c in calls)))
