# Luigi's Mansion 3 (0100DCA0064A6000)

Source: upstream seedds/nxnative b55a3f07 (2026-10-25) plus the developer's GPU memory fix c484b13c ("Share physical storage for live NVN resolution variants"), ported:
- the tex_zero_fill conflict (depth / stencil clears) kept as the fix has it;
- tex_atomic_capable (native texture atomics, f8642c4, not in this base) is a stub returning 0.

Why this base: a build from upstream 5dfc86ae (2026-11-24) ran at 100+ °C on the M2 Air; this one runs at 60-65 °C, as the October build did (user, 2026-11-24).

- Game version: 1.4.0 (update v327680), with the Multiplayer Pack 2 DLC (v65536)
- Built 2026-11-24 in about 55 min (shaders 18.5 min; signing on the USB HDD 13 min) with NX2Apple's bundled Python; app 7.5 GB
- Settings (~/Library/Application Support/nxnative/0100DCA0064A6000/env.txt): DM_FPS_TARGET=0, DM_OPMODE=1, DM_ANISO=4, DM_PAD_LABELS=1, DM_FULLSCREEN=1, DM_METAL_HUD=1

Full build (this script has no --work-dir: the work folder is <input>/0100DCA0064A6000_build):

    export PATH="/Applications/NX2Apple.app/Contents/Resources/tools/bin:$PATH" DOTNET_ROOT=~/.dotnet PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
    /Applications/NX2Apple.app/Contents/Resources/python/bin/python3.13 scripts/build_ipa_from_nsp.py <input folder> \
      -k /Volumes/extSSD/Games/NXNative/system/keys.0/prod.keys --platform mac-app --progress lines -o ../0100DCA0064A6000.app

## Ghost Gallery fix (2026-11-24)

`dm/games/0100DCA0064A6000/patches.py` (CUTS on main 79e5950f…): the gallery camera's bone lookup (main+0x472334) skips a bone whose skeleton handle slot is free (odd value) or whose hash is not found, instead of crashing (seedds/nxnative #672). Applied to the installed app by hand (main.patched.bin, re-signed); the copy from before is `../main.patched.bin.before-gallery-fix`, undone by `../Revert Ghost Gallery fix.command`. A full build applies it through the rewriter.
