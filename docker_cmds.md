docker build -t mahi_test .

docker run --cap-add=NET_ADMIN --device /dev/net/tun --privileged -it mahi_test

src/experiments/test.py local --schemes cubic