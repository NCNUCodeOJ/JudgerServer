FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
COPY build/java_policy /etc
RUN buildDeps='software-properties-common git libtool cmake python-dev python3-pip python-pip libseccomp-dev curl' && \
    apt-get update && apt-get -y install python3 $buildDeps && \
    add-apt-repository ppa:ubuntu-toolchain-r/test && add-apt-repository ppa:openjdk-r/ppa && \
    add-apt-repository ppa:longsleep/golang-backports && \
    apt-get update && apt-get install -y gcc-9 g++-9 openjdk-11-jdk golang-go && \
    pip3 install psutil &&\
    cd /tmp && git clone -b newnew  --depth 1 https://github.com/NCNUCodeOJ/Judger.git && cd Judger && \
    mkdir build && cd build && cmake .. && make && make install && \
    cd ../bindings/Python && python3 setup.py install && \
    apt-get purge -y --auto-remove $buildDeps && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 40 && \
    update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 40 && \
    mkdir -p /code && \
    useradd -u 12001 compiler && useradd -u 12002 code && \
    useradd -u 12003 spj && usermod -a -G code spj
RUN mkdir /log
WORKDIR /code