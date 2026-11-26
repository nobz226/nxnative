# Bayonetta 3 (01004A4010FEA000)

Source: upstream seedds/nxnative b55a3f07 (2026-10-25, the code freeze), exactly as it was: no changes of our own. The game was built from this commit, detached, on 2026-10-26 13:02 (15 min).

- Game version: 1.2.0 (update v131072), the version the profile is made for (full profile)
- Dumps: ExtHDD2/Games/Dumps/Bayonetta 3: Bayonetta 3.xci + [01004A4010FEA800][v131072]
- Shaders: 6,424; 2 failed, the two DS_Vanish05 domain shaders the developer's notes list (a vanish effect may not draw)

## Settings (launch options, not code)

Written by `scripts/game-settings.sh` (nxnative-project) into `~/Library/Application Support/nxnative/01004A4010FEA000/env.txt`:

    DM_OPMODE=1                 # docked
    DM_PRESENT_UPSCALE=metalfx  # MetalFX in the present
    DM_ANISO=4                  # 4x anisotropic filtering
    DM_PAD_LABELS=1             # Nintendo button labels

## Build

This commit's NSP script has no --work-dir: the work folder is <input folder>/01004A4010FEA000_build.

    export PATH="/Applications/NX2Apple.app/Contents/Resources/tools/bin:$PATH" DOTNET_ROOT=~/.dotnet PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
    /Applications/NX2Apple.app/Contents/Resources/python/bin/python3.13 scripts/build_ipa_from_nsp.py <input folder> \
      -k <prod.keys> --platform mac-app --progress lines -o "../Bayonetta 3.app"
