FROM alpine:edge

WORKDIR /data

RUN apk -U add libgcc curl cargo portaudio-dev protobuf-dev \
 && cd /root \
 && curl -LO https://github.com/librespot-org/librespot/archive/master.zip \
 && unzip master.zip \
 && cd librespot-master \
 && cargo build --jobs $(grep -c ^processor /proc/cpuinfo) --release --no-default-features \
 && mv target/release/librespot /usr/local/bin \
 && cd / \
 && apk --purge del curl cargo portaudio-dev protobuf-dev \
 && apk add llvm-libunwind \
 && rm -rf /etc/ssl /var/cache/apk/* /lib/apk/db/* /root/master.zip /root/librespot-master /root/.cargo

COPY secrets .env

RUN export $(cat .env | sed 's/#.*//g' | xargs)

CMD librespot --name "$SPOTIFY_NAME" --bitrate "$SPOTIFY_BITRATE" --disable-audio-cache --enable-volume-normalisation --linear-volume --initial-volume=100 --zeroconf-port "$SPOTIFY_PORT" --backend pipe --device /audio/pipe --username "$SPOT_USER" --password "$SPOT_PASS" --autoplay --zeroconf-port 6969