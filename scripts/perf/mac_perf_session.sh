#!/bin/zsh
# Records a performance and heat session of an nxnative Mac app while you play, then writes a summary.
#
# Start it before (or while) the game runs; it waits for the game's host (dmhost), records until the game
# quits or you press Ctrl+C, then runs mac_perf_summary.py on the session.
#
# What it records, in ~/Developer/perf-sessions/<date>-<label>/:
#   macmon.jsonl   CPU and GPU temperature, CPU / GPU / package power, clocks and load, every second (macmon, no sudo)
#   proc.tsv       the host's CPU %, memory and thread count, every 2 s
#   thermal.log    macOS thermal and performance warnings (pmset -g therm), every 10 s
#   game.log       the game's own log for this run (power, frame interval, on-screen, frame step, memory lines)
#   env.txt        the settings file the run used
#   cpu-sample.txt with --sample: a 10 s CPU call-graph sample of the host, 60 s in
#   gpu.trace      with --trace <s>: an Instruments Metal System Trace of <s> seconds, 90 s in (open it in Instruments)
#   summary.md     what mac_perf_summary.py makes of it all
#
# Usage: scripts/perf/mac_perf_session.sh [label] [--title <title ID>] [--sample] [--trace <seconds>]
#   label   a short name for the session, for example "docked-30-fxaa" (default: "session")
#   --title the game's title ID (default: Breath of the Wild, 01007EF00011E000)
# Needs: brew install macmon. The summary: python3 (any 3.x). --trace: Xcode.

set -u
HERE=${0:A:h}
LABEL=session TITLE=01007EF00011E000 SAMPLE=0 TRACE=0
while (( $# )); do
  case $1 in
    --title) TITLE=$2; shift 2 ;;
    --sample) SAMPLE=1; shift ;;
    --trace) TRACE=$2; shift 2 ;;
    -h|--help) sed -n '2,21p' $0; exit 0 ;;
    *) LABEL=$1; shift ;;
  esac
done
command -v macmon >/dev/null || { echo "macmon not found: brew install macmon"; exit 1; }

OUT=~/Developer/perf-sessions/$(date +%Y%m%d-%H%M)-$LABEL
mkdir -p $OUT
SUPPORT=~/Library/Application\ Support/nxnative/$TITLE
LOG=~/Library/Logs/nxnative/$TITLE.log
[ -f "$SUPPORT/env.txt" ] && cp "$SUPPORT/env.txt" $OUT/env.txt
{ echo "label: $LABEL"; echo "title: $TITLE"; echo "started: $(date)"
  echo "mac: $(sysctl -n hw.model) ($(sysctl -n machdep.cpu.brand_string)), macOS $(sw_vers -productVersion)"
  echo "nxnative: $(git -C $HERE/../.. rev-parse --short HEAD 2>/dev/null) ($(git -C $HERE/../.. branch --show-current 2>/dev/null))"; } > $OUT/info.txt

echo "session folder: $OUT"
echo "waiting for the game to start (dmhost) ..."
until PID=$(pgrep -nx dmhost); do sleep 1; done
echo "game running (pid $PID): recording; quit the game or press Ctrl+C to stop"
echo "game pid: $PID" >> $OUT/info.txt

# The log is rewritten at each start: follow it from its beginning, from this run on
tail -n +1 -F "$LOG" > $OUT/game.log 2>/dev/null & P_LOG=$!
macmon pipe -i 1000 > $OUT/macmon.jsonl 2>/dev/null & P_MAC=$!
{ printf 'time\tcpu_pct\trss_mb\tthreads\n'
  while kill -0 $PID 2>/dev/null; do
    ps -o %cpu=,rss= -p $PID | awk -v t=$(date +%s) -v th=$(ps -M -p $PID | tail -n +2 | wc -l | tr -d ' ') '{printf "%s\t%s\t%.0f\t%s\n", t, $1, $2/1024, th}'
    sleep 2
  done; } > $OUT/proc.tsv & P_PROC=$!
{ while kill -0 $PID 2>/dev/null; do echo "== $(date +%T)"; pmset -g therm 2>/dev/null | grep -v '^$'; sleep 10; done; } > $OUT/thermal.log & P_THERM=$!

stop() {
  kill $P_LOG $P_MAC $P_PROC $P_THERM 2>/dev/null
  wait 2>/dev/null
  echo "ended: $(date)" >> $OUT/info.txt
  python3 $HERE/mac_perf_summary.py $OUT && echo && echo "summary: $OUT/summary.md"
  exit 0
}
trap stop INT TERM

if (( SAMPLE )); then
  ( sleep 60; kill -0 $PID 2>/dev/null && sample $PID 10 -file $OUT/cpu-sample.txt >/dev/null 2>&1 ) &
fi
if (( TRACE > 0 )); then
  ( sleep 90; kill -0 $PID 2>/dev/null && xcrun xctrace record --template 'Metal System Trace' --attach $PID \
      --time-limit ${TRACE}s --output $OUT/gpu.trace >/dev/null 2>&1 ) &
fi

while kill -0 $PID 2>/dev/null; do sleep 2; done
echo "the game quit"
stop
