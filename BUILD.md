# Metroid Prime Remastered (010012101468C000)

Source: Nobz main 8a40ffcc (upstream + our fixes, 2026-11-03) + light grid float view (a214d993) + sparse 3D tile shape (67ed43b9) + layered geometry keeps its reader (e962a3cf): the gunship lit (#783) + EQUAL on emulated D24 depth (floor edge strips without noise)

- Shader chain of the app: b-6b71f2c7dcb8
- Branch: game/010012101468C000
- Game version: v0 (1.0.0)
- App: Metroid_Prime_Remastered-58cde4fe.app

Host only (keeps the shaders):

    make -C dm/host GAME=010012101468C000 dmhost
    cp dm/host/dmhost ../Metroid_Prime_Remastered-58cde4fe.app/Contents/MacOS/dmhost
    codesign --force --sign - ../Metroid_Prime_Remastered-58cde4fe.app

Full game build: choose "This game's repo" under Build from in NX2Apple.
