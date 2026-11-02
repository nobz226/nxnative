# Metroid Dread (010093801237C000)

Source: NX2Apple d5b78230 (upstream 5d2bf73f) + anisotropic filtering

- Shader chain of the app: 373efc7add5f
- Branch: game/010093801237C000 (1da4db6d)
- Game version: v327680

Host only (keeps the shaders):

    make -C dm/host GAME=010093801237C000 dmhost
    cp dm/host/dmhost ../010093801237C000.app/Contents/MacOS/dmhost
    codesign --force --sign - ../010093801237C000.app

Full game build: choose "This game's repo" under Build from in NX2Apple.
