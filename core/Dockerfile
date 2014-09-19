FROM ubuntu:14.04

MAINTAINER James R. Carr <james@zapier.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install git wget unzip -yq


RUN git clone https://github.com/jamescarr/mcrouter.git /tmp/mcrouter

RUN cd /tmp/mcrouter/mcrouter/scripts \
  && ./install_ubuntu_14.04.sh /usr/local/share

RUN ln -s /usr/local/share/install/bin/mcrouter /usr/local/bin/mcrouter

RUN mkdir -p /etc/mcrouter/mcrotuer.json

VOLUME ["/etc/mcrouter"]

CMD /usr/local/bin/mcrouter --config-file /etc/mcrouter//mcrouter.json

## Cleanup!
RUN sudo apt-get remove git unzip wget gcc-4.8 g++-4.8 libboost1.54-dev libboost-thread1.54-dev \
    libboost-filesystem1.54-dev libboost-system1.54-dev libboost-regex1.54-dev \
    libboost-python1.54-dev libboost-context1.54-dev ragel autoconf unzip \
    libsasl2-dev git libtool python-dev cmake libssl-dev libcap-dev libevent-dev \
    libgtest-dev libsnappy-dev scons flex bison libkrb5-dev binutils-dev make \
    libnuma-dev -yq
RUN apt-get clean
RUN rm -rf /tmp/*
ENV DEBIAN_FRONTEND newt
