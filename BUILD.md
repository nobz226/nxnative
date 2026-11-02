# The Legend of Zelda Breath of the Wild (01007EF00011E000)

Source: NX2Apple e6a02ea6 (upstream a662f29e) + same-pass feedback c692ba05 + depth copy + footprint controls and Deep footprints setting + anisotropic filtering. The settings row and its defaults are in dm/games/settings.tsv here.

- Shader chain of the app: f3ceca86cac5
- Branch: game/01007EF00011E000 (1ebcb80b)
- Game version: v1114112

Host only (keeps the shaders):

    make -C dm/host GAME=01007EF00011E000 dmhost
    cp dm/host/dmhost ../01007EF00011E000.app/Contents/MacOS/dmhost
    codesign --force --sign - ../01007EF00011E000.app

Full game build: choose "This game's repo" under Build from in NX2Apple.
