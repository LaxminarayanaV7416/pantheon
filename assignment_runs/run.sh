#!/bin/sh -x

echo $(pwd)

src/experiments/test.py local \
--scheme "cubic bbr vegas" \
--runtime 60 \
--data-dir='./src/experiments/data/highLatencyLowBandwidth' \
--uplink-trace='./src/experiments/1mbps.trace' \
--downlink-trace='./src/experiments/1mbps.trace' \
--prepend-mm-cmds "mm-delay 100"

src/analysis/analyze.py \
--data-dir='./src/experiments/data/highLatencyLowBandwidth'

src/experiments/test.py local \
--scheme "cubic bbr vegas" \
--runtime 60 \
--data-dir='./src/experiments/data/lowLatencyHighBandwidth' \
--uplink-trace='./src/experiments/50mbps.trace' \
--downlink-trace='./src/experiments/50mbps.trace' \
--prepend-mm-cmds "mm-delay 5"

src/analysis/analyze.py \
--data-dir='./src/experiments/data/lowLatencyHighBandwidth'