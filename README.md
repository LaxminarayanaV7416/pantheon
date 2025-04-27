# **Pantheon with Mahimahi - Docker Setup Guide**  

## **Overview**  
This repository provides a Dockerized environment for running network experiments using **Pantheon** and **Mahimahi**. Follow the steps below to set up and run the container.  

---

## **Prerequisites**  
- **Ubuntu OS** (tested on 20.04 LTS)  
- **Docker** (installed via official instructions)  
- **Git** (to clone this repository)  

---

## **Setup Instructions**  

### **1. Install Docker**  
Run the following commands to install Docker on Ubuntu:  
```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
```  
Verify the installation:  
```bash
docker --version
```  

### **2. Mandatory steps to achieve the run**
Run the following commands to enable congestion testing and allowing the three kernels, for this am using the source computer is Ubuntu 20.04 LTS supported version which comes with the kernel default installed where my idea is to volume the storage to the docker container such that It also can use it, make sure host ststem supports these kernels else you cannot do it.
```bash
sudo modprobe tcp_bbr
sudo modprobe tcp_vegas
sudo sysctl -w net.ipv4.tcp_allowed_congestion_control="reno cubic bbr vegas"
sudo sysctl -w net.core.default_qdisc=fq
sudo sysctl -w net.ipv4.ip_forward=1
```

### **3. Clone the Repository**  
Clone this repository and navigate to its directory:  
```bash
git clone <repository-url>
cd <repository-folder>
```  

### **4. Create trace files in the experiments directory**
```bash
for i in {1..60}; do echo 50 >> ./src/experiments/50mbps.trace; done && \
for i in {1..60}; do echo 1 >> ./src/experiments/1mbps.trace; done
```

### **5. Build the Docker Image**  
Build the image with the provided `Dockerfile`:  
```bash
docker build -t mahi_test .
```  

### **6. Run the Docker Container**  
Execute the container with the required permissions:  
```bash
docker run \
  --cap-add=NET_ADMIN \
  --cap-add=SYS_ADMIN \
  -v ./src/experiments/data:/pantheon/src/experiments/data \
  -v ./assignment_runs:/pantheon/assignment_runs \
  -v /lib/modules:/lib/modules \
  --device /dev/net/tun \
  --privileged \
  mahi_test
```  


#### Below are optional steps because I have developed a run.sh file in assignment_runs folder where it contains all commands, and docker file is set execute the bash script when you run the container.

### **7(Optional). Predefined Commands**  
All Docker-related commands are documented in **[docker_cmds.md](docker_cmds.md)** for reference. you can use them at your will by interactively opening the docker file from terminal using the flag `-it` in above run command does it for you, and you can test the commands by yourself.

### **8 (Optional). Running a test inside the container**  
As we have excuted the run command with -it which means interactive will straight end up in docker containers terminal where it will be pointing to the directory knownd as pantheon because we set that as working directory, from where we need to run test for which we can use the command below
```bash
src/experiments/test.py local \
--scheme "cubic vivace fillp" \
--data-dir='./src/experiments/data/highBandLowLatency' \
--uplink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.up' \
--downlink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.down' \
--extra-mm-link-args '--uplink-queue=codel --downlink-queue=codel --uplink-queue-args="target=512,interval=100,packets=100" --downlink-queue-args="target=512,interval=100,packets=100"'
```  
you can replace what you want to run based on the requirements, I have mentioned the whole command for reference

### **9(Optional). Generating the graphs**  
Generating graph is the easiest of all just need to run the analyze.py as shown below it will save the results to the data_dir mentioned below in the command
```bash
src/analysis/analyze.py \
--data-dir='./src/experiments/data/highBandLowLatency'
``` 

---

## **Notes**  
- Ensure your user has Docker permissions (or use `sudo`).  
- The container mounts:  
  - Experiment data (`./src/experiments/data`) for persistent logs.  
- The `--privileged` flag grants extended permissions for network emulation.  

For issues, check the [Mahimahi documentation](http://mahimahi.mit.edu/).  

--- 
