// Red Dead Redemption's RPF6 archive tables, decrypted with the game's own cipher (tool mode, for the offline shader split).
// The archive code (main+0x148398 of the 1.0.7 main) reads the 16-byte big-endian header {"RPF6", entry count, debug data offset / 8, encryption}, reads the table of
// count × 20 bytes rounded up to 16 from +0x10, sets up its cipher from the encryption word (main+0x145d8c(ctx, flag), a context on the stack: no key or key schedule ever
// sits in memory, so it is white-box) and, for a non-zero flag, decrypts the table in place block by block (main+0x145c10(table, length, ctx + 8, main+0x145970)); then it
// byte-swaps the 32-bit words (five per entry). The three functions are pure computation (no calls out, no system instructions), so the host calls them directly.
// DM_RPF_DECRYPT=<output dir>: for each .rpf at the top of DM_ROMFS, writes <output dir>/<name>.toc (the decrypted table, still big-endian, as in the file) and exits.
#include "hle.h"
#include <dirent.h>
#include <string.h>

static const uint64_t K_INIT = 0x145d8c, K_DECRYPT = 0x145c10, K_BLOCK = 0x145970;

static uint32_t be32(const uint8_t *p) { return (uint32_t)p[0] << 24 | (uint32_t)p[1] << 16 | (uint32_t)p[2] << 8 | p[3]; }

void dm_rpf_decrypt_maybe(void) {
    const char *out = getenv("DM_RPF_DECRYPT"), *romfs = getenv("DM_ROMFS");
    if (!out || !*out) return;
    if (!romfs) die("DM_RPF_DECRYPT needs DM_ROMFS");
    extern module_t g_mod[]; extern int g_nmod;
    module_t *m = NULL; for (int i = 0; i < g_nmod; i++) if (!strcmp(g_mod[i].name, "main")) m = &g_mod[i];
    if (!m) die("DM_RPF_DECRYPT: no main module");
    void (*init)(void *, uint32_t) = (void (*)(void *, uint32_t))(m->base + K_INIT);
    void (*decrypt)(void *, uint32_t, void *, void *) = (void (*)(void *, uint32_t, void *, void *))(m->base + K_DECRYPT);
    void *block = m->base + K_BLOCK;
    DIR *dir = opendir(romfs); if (!dir) die("DM_RPF_DECRYPT: cannot open %s", romfs);
    int done = 0; struct dirent *de;
    while ((de = readdir(dir))) {
        size_t nl = strlen(de->d_name); if (nl < 5 || strcmp(de->d_name + nl - 4, ".rpf")) continue;
        char path[2048]; snprintf(path, sizeof path, "%s/%s", romfs, de->d_name);
        FILE *f = fopen(path, "rb"); if (!f) continue;
        uint8_t h[16]; if (fread(h, 1, 16, f) != 16 || memcmp(h, "RPF6", 4)) { fclose(f); LOG("[RED] %s: not RPF6", de->d_name); continue; }
        uint32_t count = be32(h + 4), flag = be32(h + 12), len = (count * 20 + 15) & ~15u;
        uint8_t *t = aligned_alloc(16, len ? len : 16); if (!t || fread(t, 1, len, f) != len) { fclose(f); free(t); LOG("[RED] %s: short table", de->d_name); continue; }
        fclose(f);
        uint8_t ctx[0x1000] __attribute__((aligned(16))); memset(ctx, 0, sizeof ctx);
        init(ctx, flag);
        if (flag) decrypt(t, len, ctx + 8, block);
        snprintf(path, sizeof path, "%s/%s.toc", out, de->d_name);
        FILE *o = fopen(path, "wb"); if (o) { fwrite(t, 1, len, o); fclose(o); }
        LOG("DM_RPF_DECRYPT: %s: %u entries, encryption %#x, table %u bytes → %s; first entry %08x %08x %08x %08x %08x", de->d_name, count, flag, len, path,
            be32(t), be32(t + 4), be32(t + 8), be32(t + 12), be32(t + 16));
        free(t); done++;
    }
    closedir(dir);
    LOG("DM_RPF_DECRYPT: %d archives done", done);
    exit(0);
}
