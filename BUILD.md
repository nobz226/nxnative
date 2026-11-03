# Super Smash Bros. Ultimate (01006A800016E000)

Source: smash-nu-barrier b66a2fdd: Vorbis lengths, boot fix, aniso, DM_NU_BARRIER. Crash stopgap: DM_NU_BARRIER=2 in env.txt. The crash cause is unknown.

- Shader chain of the app: b7cd656abd7c
- Branch: game/01006A800016E000 (b66a2fdd)
- Game version: v2031616

Host only (keeps the shaders):

    make -C dm/host GAME=01006A800016E000 dmhost
    cp dm/host/dmhost ../01006A800016E000.app/Contents/MacOS/dmhost
    codesign --force --sign - ../01006A800016E000.app

Full game build: choose "This game's repo" under Build from in NX2Apple.

## Crash stopgap (issue #768)

The host makes the movie audio stream's pending buffer 16 KB (`dm/host/probe.c`, on by default for this game; `DM_768_PAD=0` turns it off). The crash after the tutorial movie stopped with it in 2 runs (18 and 12 minutes); the real cause is still open. `DM_NU_BARRIER` is not needed.

## Final fixes (2026-11-03, user-confirmed: every menu, every mode, attract cycles)

- `0daca28d` #768 stopgap: the movie audio stream's pending buffer is 16 KB (on by default).
- `7696239e` oe: SwitchLcdBacklightOff / On answered on the host (crash backing out of menus).
- `98a5fe5e` capture services (caps:*) served (PR #495, crash entering Spirits matches).
- `fe4c08c1` a command memory callback with no allocator is treated as absent (crash leaving the Spirits map).
