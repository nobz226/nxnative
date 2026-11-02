# The Legend of Zelda: Skyward Sword HD (01002DA013484000)

PORTED, NEVER BUILT. The installed app comes from the old sshd branch, whose source is lost. This is current nxnative (our main) plus what that branch did, recovered from notes and history.

Ported: gzip shader archives, DM_NPAD_JOYDUAL (Joy-Con pair for motion controls), NX_SKIP_GLSLC_CAPTURE.
Already in main, to be checked in play: logic ops, live image sharing, plain-player rumble, gyro.
Not ported: the old dual-source entry point. Current code has dual_want.tsv, filled by the host (DM_NVN_DUAL_WANT) and read by the next shader build, so the first run may need a second build. The old crash was in Apple's compiler on dual-source blending, so test that first.

Build: base + update v65536, NX_SKIP_GLSLC_CAPTURE=1. No profile: a provisional one comes from the survey.
env.txt: DM_OPMODE=1, DM_ANISO=4, DM_NPAD_JOYDUAL=1.
Old notes: ~/Desktop/nxnative-project/docs/games/skyward-sword-hd.md
