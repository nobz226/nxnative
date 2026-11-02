# Donkey Kong Country Tropical Freeze (0100C1F0051B6000)

Source: nobz-fixes at 4612aa67: Vorbis lengths, audio catch-up, boot fix a1b9a2ae, depth copy, aniso. The installed host also has the unused DM_NVN_NO_GPU_OPT switch, removed from this source.

- Shader chain of the app: b7cd656abd7c
- Branch: game/0100C1F0051B6000 (4612aa67)
- Game version: v131072

Host only (keeps the shaders):

    make -C dm/host GAME=0100C1F0051B6000 dmhost
    cp dm/host/dmhost ../0100C1F0051B6000.app/Contents/MacOS/dmhost
    codesign --force --sign - ../0100C1F0051B6000.app

Full game build: choose "This game's repo" under Build from in NX2Apple.
