# Bayonetta (010076F0049A2000)

Source: upstream seedds/nxnative b55a3f07 (2026-10-25, the code freeze), exactly as it was: no changes of our own. The game was built from this commit, detached, on 2026-10-26 06:08 (8½ min).

- Game version: 1.1 (update v65536), the version the profile is made for (full profile)
- Dumps: ExtHDD2/Games/Dumps/Bayonetta: [010076F0049A2000][v0] + [010076F0049A2800][v65536]
- Shaders: 458

## Settings (launch options, not code)

Written by `scripts/game-settings.sh` (nxnative-project) into `~/Library/Application Support/nxnative/010076F0049A2000/env.txt`:

    DM_OPMODE=1                 # docked
    DM_PRESENT_UPSCALE=metalfx  # MetalFX in the present
    DM_ANISO=4                  # 4x anisotropic filtering
    DM_PAD_LABELS=1             # Nintendo button labels

## Build

This commit's NSP script has no --work-dir: the work folder is <input folder>/010076F0049A2000_build.

    export PATH="/Applications/NX2Apple.app/Contents/Resources/tools/bin:$PATH" DOTNET_ROOT=~/.dotnet PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
    /Applications/NX2Apple.app/Contents/Resources/python/bin/python3.13 scripts/build_ipa_from_nsp.py <input folder> \
      -k <prod.keys> --platform mac-app --progress lines -o "../Bayonetta.app"
