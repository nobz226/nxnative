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
