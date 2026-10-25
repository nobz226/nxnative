#!/usr/bin/env python3
"""Summary of a session recorded by mac_perf_session.sh: writes <session>/summary.md and prints it.

Usage: scripts/perf/mac_perf_summary.py <session folder>
Reads macmon.jsonl (temperatures, power, clocks), proc.tsv (the host's CPU and memory), thermal.log and game.log
(the host's own 300-frame lines: power, frame interval, on-screen, frame step). Missing files are skipped.
"""
import json, re, statistics, sys
from pathlib import Path


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(p / 100 * (len(xs) - 1))))] if xs else float('nan')


def stats_row(name, xs, unit, fmt='{:.1f}'):
    if not xs: return f'| {name} | – | – | – | – |'
    f = lambda v: fmt.format(v)
    return f'| {name} | {f(statistics.fmean(xs))} | {f(pct(xs, 50))} | {f(pct(xs, 95))} | {f(max(xs))} {unit} |'


def macmon(d, out):
    p = d / 'macmon.jsonl'
    if not p.exists(): return
    rows = []
    for line in p.read_text().splitlines():
        try: rows.append(json.loads(line))
        except ValueError: pass
    rows = rows[5:] or rows   # the first seconds are the game starting up
    if not rows: return
    g = lambda k: [r[k] for r in rows if isinstance(r.get(k), (int, float))]
    t = lambda k: [r['temp'][k] for r in rows if r.get('temp', {}).get(k)]
    out += [f'## Heat and power ({len(rows)} s, after the first 5)', '',
            '| | mean | median | p95 | max |', '|---|---|---|---|---|',
            stats_row('CPU temperature', t('cpu_temp_avg'), '°C'),
            stats_row('GPU temperature', t('gpu_temp_avg'), '°C'),
            stats_row('CPU power', g('cpu_power'), 'W', '{:.2f}'),
            stats_row('GPU power', g('gpu_power'), 'W', '{:.2f}'),
            stats_row('CPU + GPU + ANE power', g('all_power'), 'W', '{:.2f}'),
            stats_row('whole system power', g('sys_power'), 'W', '{:.2f}'),
            stats_row('GPU load', [v * 100 for v in g('gpu_active_ratio')], '%'),
            stats_row('GPU clock', g('gpu_freq_mhz'), 'MHz', '{:.0f}'),
            stats_row('P-core load', [v * 100 for v in g('pcpu_active_ratio')], '%'),
            stats_row('P-core clock', g('pcpu_freq_mhz'), 'MHz', '{:.0f}'),
            stats_row('E-core load', [v * 100 for v in g('ecpu_active_ratio')], '%'), '']
    temps = t('cpu_temp_avg')
    if len(temps) >= 60:   # how the heat built up: the mean of each tenth of the session
        n = len(temps) // 10
        out += ['CPU temperature by tenth of the session: ' + ' → '.join(f'{statistics.fmean(temps[i * n:(i + 1) * n]):.0f}' for i in range(10)) + ' °C', '']


def proc(d, out):
    p = d / 'proc.tsv'
    if not p.exists(): return
    cpu, rss, th = [], [], []
    for line in p.read_text().splitlines()[1:]:
        f = line.split('\t')
        if len(f) == 4:
            try: cpu.append(float(f[1])); rss.append(float(f[2])); th.append(float(f[3]))
            except ValueError: pass
    if not cpu: return
    out += ['## The game process (dmhost)', '', '| | mean | median | p95 | max |', '|---|---|---|---|---|',
            stats_row('CPU (100 = one core)', cpu, '%', '{:.0f}'), stats_row('memory', rss, 'MB', '{:.0f}'),
            stats_row('threads', th, '', '{:.0f}'), '']


NUM = r'([\d.]+)'


def game(d, out):
    p = d / 'game.log'
    if not p.exists(): return
    text = p.read_text(errors='replace')
    lines = text.splitlines()
    power = [(float(a), float(b), float(c), float(e)) for a, b, c, e in
             re.findall(r'power up to frame \d+: CPU energy ' + NUM + r' W, ' + NUM + r' mJ per frame \(' + NUM + r' fps\); CPU ' + NUM + '%', text)]
    if power:
        out += ['## The game\'s own readings (every 300 frames)', '', '| | mean | median | p95 | max |', '|---|---|---|---|---|',
                stats_row('frame rate', [x[2] for x in power], 'fps'),
                stats_row('CPU energy (host view)', [x[0] for x in power], 'W', '{:.2f}'),
                stats_row('CPU energy per frame', [x[1] for x in power], 'mJ'),
                stats_row('CPU (100 = one core)', [x[3] for x in power], '%', '{:.0f}')]
        wk = [float(x) for x in re.findall(r'wakeups ' + NUM + '/s', text)]
        if wk: out.append(stats_row('wakeups', wk, '/s', '{:.0f}'))
        p99 = [float(x) for x in re.findall(r'frame interval up to frame \d+: .*?p99 ' + NUM + ' ms', text)]
        if p99: out.append(stats_row('frame interval p99', p99, 'ms'))
        drop = [int(x) for x in re.findall(r'on-screen up to frame \d+: \d+ frames, dropped (\d+)', text)]
        if drop: out.append(stats_row('frames dropped per 300', drop, '', '{:.0f}'))
        out.append('')
    steps = [l.split('] ', 2)[-1] for l in lines if 'frame step: hold' in l]
    if steps:
        out += [f'Frame-step changes: {len(steps)} (the host moved between 60 / 30 / 20 fps holds)', '']
        out += ['```'] + steps[-8:] + ['```', '']
    reds = [l for l in lines if '[RED]' in l]
    if reds:
        out += [f'Warnings ([RED] lines): {len(reds)}; the last few:', '', '```'] + [r[:240] for r in reds[-6:]] + ['```', '']


def thermal(d, out):
    p = d / 'thermal.log'
    if not p.exists(): return
    warn = sorted({l.strip() for l in p.read_text().splitlines() if 'level' in l.lower() and not l.strip().endswith('No thermal warning level has been recorded')
                   and not l.strip().endswith('No performance warning level has been recorded')})
    out += ['## macOS thermal warnings', ''] + ([f'- {w}' for w in warn] or ['none recorded']) + ['']


def main():
    d = Path(sys.argv[1]).expanduser()
    out = [f'# Performance session: {d.name}', '']
    info, env = d / 'info.txt', d / 'env.txt'
    if info.exists(): out += ['```', info.read_text().strip(), '```', '']
    if env.exists(): out += ['Settings (env.txt): ' + (', '.join(l for l in env.read_text().split() if '=' in l) or 'none'), '']
    for f in (macmon, proc, game, thermal): f(d, out)
    extra = [n for n in ('cpu-sample.txt', 'gpu.trace') if (d / n).exists()]
    if extra: out += ['Also recorded: ' + ', '.join(extra) + ' (open gpu.trace in Instruments).', '']
    (d / 'summary.md').write_text('\n'.join(out))
    print('\n'.join(out))


if __name__ == '__main__':
    main()
