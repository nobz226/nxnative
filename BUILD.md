# Mario Kart 8 Deluxe (0100152000022000)

Source: NX2Apple 61374835 (upstream a662f29e) + anisotropic filtering (16x is a saved setting)

- Shader chain of the app: f3ceca86cac5
- Branch: game/0100152000022000 (e2fba1bc)
- Game version: v1441792

Host only (keeps the shaders):

    make -C dm/host GAME=0100152000022000 dmhost
    cp dm/host/dmhost ../0100152000022000.app/Contents/MacOS/dmhost
    codesign --force --sign - ../0100152000022000.app

Full game build: choose "This game's repo" under Build from in NX2Apple.

## Sky-High Sundae sky (far-plane depth), 2026-11-17

The host draws vertex shaders flagged `raster.far` with a depth bias past the far value and depth clamping (upstream 04ba572d, ported). This branch's
shader chain does not set the flag, so after a rebuild, add `"far": 1` to the `raster` object of each key in `dm/games/0100152000022000/far_plane_keys.tsv`
in the app's `Contents/Resources/msl/b-<chain>/<key>_b.json`, then re-sign the app.
