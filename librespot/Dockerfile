FROM alpine:edge

WORKDIR /data

RUN echo https://dl-cdn.alpinelinux.org/alpine/edge/testing >>  /etc/apk/repositories

RUN apk -U add librespot

CMD librespot --name "$SPOTIFY_NAME" --bitrate "$SPOTIFY_BITRATE" --disable-audio-cache --enable-volume-normalisation --initial-volume=100 --backend pipe --device /audio/pipe --username "$SPOTIFY_USER" --password "$SPOTIFY_PASS" --autoplay --zeroconf-port 6969