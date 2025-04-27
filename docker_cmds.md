docker build -t mahi_test .

docker run --cap-add=NET_ADMIN --cap-add=SYS_ADMIN -v ./src/experiments/data:/pantheon/src/experiments/data  -v /lib/modules:/lib/modules --device /dev/net/tun --privileged -it mahi_test


src/experiments/test.py local --scheme "cubic vivace fillp" --data-dir='./src/experiments/data/cubic' --uplink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.up' --downlink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.down'

src/analysis/analyze.py --data-dir='./src/experiments/data/cubic'

src/experiments/test.py local --scheme "vivace" --data-dir='./src/experiments/data/vivace' --uplink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.up' --downlink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.down'

src/analysis/analyze.py --data-dir='./src/experiments/data/vivace'

src/experiments/test.py local --scheme "fillp" --data-dir='./src/experiments/data/fillp' --uplink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.up' --downlink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.down'

src/analysis/analyze.py --data-dir='./src/experiments/data/fillp'


src/experiments/test.py local --scheme "cubic vivace fillp" --data-dir='./src/experiments/data/highBandLowLatency' --uplink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.up' --downlink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.down' --extra-mm-link-args '--uplink-queue=codel --downlink-queue=codel --uplink-queue-args="target=512,interval=100,packets=100" --downlink-queue-args="target=512,interval=100,packets=100"'

src/analysis/analyze.py --data-dir='./src/experiments/data/highBandLowLatency'

src/experiments/test.py local \
--scheme "cubic bbr vegas" \
--runtime 60 \
--data-dir='./src/experiments/data/lowLatencyHighBandwidth' \
--uplink-trace='./src/experiments/50mbps.trace' \
--downlink-trace='./src/experiments/50mbps.trace' \
--prepend-mm-cmds "mm-delay 5"

src/analysis/analyze.py \
--data-dir='./src/experiments/data/lowLatencyHighBandwidth'


src/experiments/test.py local \
--scheme "cubic bbr vegas" \
--runtime 60 \
--data-dir='./src/experiments/data/highLatencyLowBandwidth' \
--uplink-trace='./src/experiments/1mbps.trace' \
--downlink-trace='./src/experiments/1mbps.trace' \
--prepend-mm-cmds "mm-delay 100"

src/analysis/analyze.py \
--data-dir='./src/experiments/data/highLatencyLowBandwidth'