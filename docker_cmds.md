docker build -t mahi_test .

docker run --cap-add=NET_ADMIN --cap-add=SYS_ADMIN -v ./src/experiments/data:/pantheon/src/experiments/data  -v /lib/modules:/lib/modules --device /dev/net/tun --privileged -it mahi_test


src/experiments/test.py local --scheme "cubic vivace fillp" --data-dir='./src/experiments/data/cubic' --uplink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.up' --downlink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.down'

src/analysis/analyze.py --data-dir='./src/experiments/data/cubic'

src/experiments/test.py local --scheme "vivace" --data-dir='./src/experiments/data/vivace' --uplink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.up' --downlink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.down'

src/analysis/analyze.py --data-dir='./src/experiments/data/vivace'

src/experiments/test.py local --scheme "fillp" --data-dir='./src/experiments/data/fillp' --uplink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.up' --downlink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.down'

src/analysis/analyze.py --data-dir='./src/experiments/data/fillp'
