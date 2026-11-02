# Super Mario Odyssey (0100000000010000)

Source: NX2Apple d9909881 (upstream a662f29e) + Sand Kingdom pipe fix 6fe1927e + #612 bloom sampler patch, ported (DM_NVN_SAMPLER_SNAPSHOT_PROBE=1 in env.txt turns it on) + anisotropic filtering

- Shader chain of the app: f3ceca86cac5
- Branch: game/0100000000010000 (feb69d88)
- Game version: v393216

Host only (keeps the shaders):

    make -C dm/host GAME=0100000000010000 dmhost
    cp dm/host/dmhost ../0100000000010000.app/Contents/MacOS/dmhost
    codesign --force --sign - ../0100000000010000.app

Full game build: choose "This game's repo" under Build from in NX2Apple.
