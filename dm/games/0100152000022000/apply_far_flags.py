#!/usr/bin/env python3
# Sky-High Sundae sky fix, step 2 of 2 after a build from this branch (see BUILD.md): sets raster.far = 1 in the reflection JSON of every vertex
# shader listed in far_plane_keys.tsv, in the app's Contents/Resources/msl/b-<chain>/. The host (nvn_mtl.m draw, upstream 04ba572d port) then
# draws those sky shaders with a depth bias past the far value and depth clamping. Re-sign the app afterwards.
# Usage: apply_far_flags.py <path to 0100152000022000.app>
import json, os, sys, glob
app = sys.argv[1]
keys = [l.strip() for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'far_plane_keys.tsv')) if l.strip() and not l.startswith('#')]
dirs = glob.glob(os.path.join(app, 'Contents/Resources/msl/b-*'))
if len(dirs) != 1: sys.exit(f'[RED] expected one msl/b-<chain> folder in {app}, found {len(dirs)}')
done = already = missing = 0
for k in keys:
    p = os.path.join(dirs[0], k + '_b.json')
    if not os.path.exists(p): missing += 1; continue
    j = json.load(open(p))
    if j.get('stage') != 'vs': sys.exit(f'[RED] {k} is not a vertex shader')
    if j.setdefault('raster', {}).get('far') == 1: already += 1; continue
    j['raster']['far'] = 1
    open(p, 'w').write(json.dumps(j, indent=1)); done += 1
print(f'flagged {done}, already flagged {already}, missing {missing} of {len(keys)} (expected: 245 flagged or already flagged, 0 missing)')
print(f'now re-sign: codesign --force --sign - "{app}"')
