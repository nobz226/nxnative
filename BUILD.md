# Bayonetta 2 (01007960049A0000)

Source: NX2Apple 46ea54c6 (upstream a662f29e) + anisotropic filtering

- Shader chain of the app: f3ceca86cac5
- Branch: game/01007960049A0000 (d8caa763)
- Game version: v65536

Host only (keeps the shaders):

    make -C dm/host GAME=01007960049A0000 dmhost
    cp dm/host/dmhost ../01007960049A0000.app/Contents/MacOS/dmhost
    codesign --force --sign - ../01007960049A0000.app

Full game build: choose "This game's repo" under Build from in NX2Apple.
