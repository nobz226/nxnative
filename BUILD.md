# Mario Kart 8 Deluxe (0100152000022000)

Source: NX2Apple 61374835 (upstream a662f29e) + anisotropic filtering (16x is a saved setting)

- Shader chain of the app: f3ceca86cac5
- Branch: game/0100152000022000 (e2fba1bc)
- Game version: v1441792

Host only (keeps the shaders):

    make -C dm/host GAME=0100152000022000 dmhost
    cp dm/host/dmhost ../0100152000022000.app/Contents/MacOS/dmhost
    codesign --force --sign - ../0100152000022000.app

## Before a full rebuild: read this

**Rebuild Mario Kart 8 Deluxe from the latest upstream nxnative (seedds/nxnative main), not from this branch.** Upstream's shader tools
flag the sky shaders themselves (04ba572d), so the Sky-High Sundae sky fix comes with the build and nothing else has to be done for it.
Check which of this branch's other changes (anisotropic filtering setting, Game Mode off in pack_app.py, the 2026-11-10 upstream ports) upstream
lacks and carry those over.

**If you do build from this branch** ("This game's repo" under Build from in NX2Apple), the sky fix is only half there: the engine part comes
with the build, but this branch's shader tools do not flag the sky shaders. After the build, run the rest of the fix:

    python3 dm/games/0100152000022000/apply_far_flags.py ../0100152000022000.app
    codesign --force --sign - ../0100152000022000.app

It must report 245 flagged (or already flagged) and 0 missing. Without it, Sky-High Sundae's sky shows red blocks again.

## Sky-High Sundae sky (far-plane depth), 2026-11-17

The host draws vertex shaders flagged `raster.far` with a depth bias past the far value and depth clamping (upstream 04ba572d, ported in 22cabd22).
This branch's shader chain does not set the flag: the 245 sky shaders upstream's `far_plane` finds in this game are listed in
`dm/games/0100152000022000/far_plane_keys.tsv`, and `apply_far_flags.py` flags them in a built app (see Before a full rebuild).
Backups of the pre-fix engine and reflection files: `dmhost.before-sky-fix` and `sky-fix-backup/` in the game folder.
