# Astral Chain (01007300020FA000)

Source: NX2Apple d5b78230 (upstream 5d2bf73f) + anisotropic filtering

- Shader chain of the app: 373efc7add5f
- Branch: game/01007300020FA000 (4dd0eb1f)
- Game version: v65536

Host only (keeps the shaders):

    make -C dm/host GAME=01007300020FA000 dmhost
    cp dm/host/dmhost ../01007300020FA000.app/Contents/MacOS/dmhost
    codesign --force --sign - ../01007300020FA000.app

Full game build: choose "This game's repo" under Build from in NX2Apple.
