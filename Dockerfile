FROM ubuntu:14.04

MAINTAINER James R. Carr <james.r.carr@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install wget git-core unzip -yq

## Install FBThrift
RUN apt-get install -yq \
    g++ \
    automake \
    autoconf \
    autoconf-archive \
    libtool \
    libboost-all-dev \
    libevent-dev \
    libdouble-conversion-dev \
    libgoogle-glog-dev \
    libgflags-dev \
    liblz4-dev \
    liblzma-dev \
    libsnappy-dev \
    make \
    zlib1g-dev \
    binutils-dev \
    libjemalloc-dev

RUN git clone https://github.com/jamescarr/fbthrift.git /tmp/fbthrift
RUN apt-get install -yq \
      flex \
      bison \
      libkrb5-dev \
      libsasl2-dev \
      libnuma-dev \
      pkg-config \
      libssl-dev

RUN cd /tmp/fbthrift/thrift && chmod +x deps.sh && ./deps.sh && make install

## Install mcrouter

RUN git clone https://github.com/facebook/mcrouter.git /tmp/mcrouter
RUN cd /tmp/mcrouter \
  && autoreconf --install \
  && ./configure \
  && make \
  && make install \

## Cleanup!
RUN rm -rf /tmp/*
ENV DEBIAN_FRONTEND newt
