# METAL GEAR SOLID 4 (0100D0B01C4F4000, program 2)

PORTED, NEVER BUILT. The installed app comes from the old mgs4 branch, whose source is lost. This is current nxnative (our main) plus what that branch did, recovered from notes and history.

Ported: NX_PROGRAM_INDEX, VPAK shaders, the profile values (4 GB layout), DM_LAUNCH_PARAM, PopOpenUsers hand-over, Manual button in the browser.
Already in main, to be checked in play: audio catch-up fix (FMVs), plain-player rumble, gyro.
Missing: the profile's shader tables, which the first build makes.

Build: NX_PROGRAM_INDEX=2, update v262144 and the two DLCs in the folder.
env.txt: DM_OPMODE=1, DM_ANISO=4, DM_LAUNCH_PARAM=-region us -lan en -selfregion NA -resolution 0 -launcherpath 0
Old notes: ~/Desktop/nxnative-project/docs/games/metal-gear-solid-4.md
