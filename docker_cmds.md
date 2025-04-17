docker build -t mahi_test .

docker run --cap-add=NET_ADMIN --cap-add=SYS_ADMIN -v ./src/experiments/data:/pantheon/src/experiments/data --device /dev/net/tun --privileged -it mahi_test

src/experiments/test.py local --schemes cubic

src/experiments/test.py local --schemes "cubic bbr vegas" --uplink-trace ./src/experiments/12mbps.trace --downlink-trace ./src/experiments/12mbps.trace --data-dir ./src/experiments/data/trail_one


src/analysis/analyze.py --data-dir ./src/experiments/data/trail_one


src/experiments/test.py local --all -f=20 --data-dir='./src/experiments/data/att.lte.driving' --uplink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.up' --downlink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.down'


src/analysis/analyze.py --data-dir='./src/experiments/data/att.lte.driving'