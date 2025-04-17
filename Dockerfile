# Use Ubuntu 20.04 as base image
FROM ubuntu:20.04

# Avoid interactive prompts during package install
ENV DEBIAN_FRONTEND=noninteractive

# Install software-properties-common to get add-apt-repository
RUN apt-get update && apt-get install -y software-properties-common

RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git python3 python3-pip python3-venv \
    build-essential cmake \
    gcc-11 g++-11 python3 bpftrace \
    python3-pip \
    python3-venv \
    libgoogle-glog-dev libgflags-dev \
    libprotobuf-dev protobuf-compiler \
    libboost-all-dev libnl-3-dev libnl-genl-3-dev \
    libssl-dev libcurl4-openssl-dev libevent-dev \
    libncurses-dev pkg-config iptables apache2 \
    wget curl unzip dnsmasq apache2-dev \
    ntp ntpdate texlive \
    debhelper autotools-dev dh-autoreconf \
    sudo iproute2 iputils-ping libxcb1-dev libx11-dev libxcb-dri3-dev libxcb-present-dev libpango1.0-dev \
    && apt-get clean

# Make 'python' point to 'python3' and 'pip' to 'pip3'
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Set GCC-11 as default
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 100 && \
    update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 100

# Install Mahimahi
RUN apt-get install -y mahimahi
# RUN git clone https://github.com/ravinet/mahimahi.git && \
#     cd mahimahi && ./autogen.sh && \
#     ./configure && \
#     make && \
#     make install

RUN pip install matplotlib numpy tabulate pyyaml

# Clone Pantheon
RUN git clone https://github.com/StanfordSNR/pantheon.git && \
    cd pantheon && \
    git submodule sync && git submodule update --recursive --init

RUN cd pantheon/third_party/pantheon-tunnel && \
    ./autogen.sh && \
    ./configure && \
    make && \
    make install

# Set working directory
WORKDIR /pantheon

RUN apt-get install linux-headers-$(uname -r)

COPY src src
COPY ebpf ebpf

# RUN python src/experiments/setup_system.py --enable-ip-forward --set-all-mem --qdisc fq
RUN src/experiments/setup.py --install-deps --all

# Create a new user (e.g., "appuser") and give sudo if needed
RUN useradd -m -s /bin/bash appuser && \
    echo "appuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN chown -R appuser:appuser /pantheon

# Switch to the non-root user
USER appuser

# Use bash as default shell
CMD ["/bin/bash"]
