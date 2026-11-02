# Super Mario 3D World + Bowser's Fury (010028600EBDA000)

Source: NX2Apple 46ea54c6 (upstream a662f29e) + anisotropic filtering

- Shader chain of the app: f3ceca86cac5
- Branch: game/010028600EBDA000 (41af9a21)
- Game version: v262144

Host only (keeps the shaders):

    make -C dm/host GAME=010028600EBDA000 dmhost
    cp dm/host/dmhost ../010028600EBDA000.app/Contents/MacOS/dmhost
    codesign --force --sign - ../010028600EBDA000.app

Full game build: choose "This game's repo" under Build from in NX2Apple.
