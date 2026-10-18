import sys
# resrecord.py TIP: the Record app's first line when S (playerTier) and C (worksRecordHead) both change it
p='starship-cadet.html'; tip=sys.argv[1]; s=open(p).read()
k=s.index("  B.push((typeof worksRecordHead === 'function'"); a=s.rindex('<<<<<<< HEAD\n',0,k); c=s.index('\n>>>>>>> '+tip+'\n',k)
assert "playerTier" in s[a:k], 'unexpected Record conflict'
new="  B.push((typeof worksRecordHead === 'function' && worksRecordHead()) || { kind: 'text', text: 'Works technician, tier ' + (typeof playerTier === 'function' ? playerTier() : 1) + '.', mark: 'hot' });   // BM4 hand merge: C's head (0.44.x), S's playerTier fallback (0.33.45)"
s=s[:a]+new+s[c+len('\n>>>>>>> '+tip):]; open(p,'w').write(s); print('Record head resolved')
