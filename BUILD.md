# Super Mario Bros. Wonder (010015100B514000)

Source: NX2Apple 6c5c1344 (upstream 5d2bf73f) + anisotropic filtering

- Shader chain of the app: 373efc7add5f
- Branch: game/010015100B514000 (87a25045)
- Game version: v327680

Host only (keeps the shaders):

    make -C dm/host GAME=010015100B514000 dmhost
    cp dm/host/dmhost ../010015100B514000.app/Contents/MacOS/dmhost
    codesign --force --sign - ../010015100B514000.app

Full game build: choose "This game's repo" under Build from in NX2Apple.
