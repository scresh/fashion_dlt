

# --------------------------------------------------- SIGNING BUILD ----------------------------------------------------
FROM ubuntu:bionic as sawtooth-signing-builder

RUN apt-get update \
 && apt-get install gnupg -y

ENV VERSION=AUTO_STRICT

RUN echo "deb http://repo.sawtooth.me/ubuntu/ci bionic universe" >> /etc/apt/sources.list \
 && (apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 8AA7AF1F1091A5FD \
 || apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 8AA7AF1F1091A5FD) \
 && apt-get update \
 && apt-get install -y -q \
    git \
    python3 \
    python3-protobuf \
    python3-secp256k1 \
    python3-stdeb \
    python3-grpcio-tools \
    python3-grpcio

RUN cd / \
 && git clone https://github.com/hyperledger/sawtooth-core.git

RUN /sawtooth-core/bin/protogen \
 && cd /sawtooth-core/signing \
 && if [ -d "debian" ]; then rm -rf debian; fi \
 && python3 setup.py clean --all \
 && python3 setup.py --command-packages=stdeb.command debianize \
 && if [ -d "packaging/ubuntu" ]; then cp -R packaging/ubuntu/* debian/; fi \
 && dpkg-buildpackage -b -rfakeroot -us -uc
# ----------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------- PYTHON SKD BUILD --------------------------------------------------
FROM ubuntu:bionic as sawtooth-sdk-python-builder

RUN apt-get update \
 && apt-get install gnupg -y

ENV VERSION=AUTO_STRICT

RUN echo "deb http://repo.sawtooth.me/ubuntu/ci bionic universe" >> /etc/apt/sources.list \
 && (apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 8AA7AF1F1091A5FD \
 || apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 8AA7AF1F1091A5FD) \
 && apt-get update \
 && apt-get install -y -q \
    git \
    python3 \
    python3-colorlog \
    python3-protobuf \
    python3-stdeb \
    python3-grpcio-tools \
    python3-grpcio \
    python3-toml \
    python3-yaml

COPY --from=sawtooth-signing-builder /sawtooth-core/python3-sawtooth-signing*.deb /tmp

RUN cd / \
 && git clone https://github.com/hyperledger/sawtooth-core.git

RUN dpkg -i /tmp/python3-sawtooth-*.deb || true \
 && apt-get -f -y install \
 && /sawtooth-core/bin/protogen \
 && cd /sawtooth-core/sdk/python \
 && if [ -d "debian" ]; then rm -rf debian; fi \
 && python3 setup.py clean --all \
 && python3 setup.py --command-packages=stdeb.command debianize \
 && if [ -d "packaging/ubuntu" ]; then cp -R packaging/ubuntu/* debian/; fi \
 && dpkg-buildpackage -b -rfakeroot -us -uc
# ----------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------- PYTHON FASHION TP BUILD -----------------------------------------------
FROM ubuntu:bionic as python-fashion-tp-builder

RUN apt-get update \
 && apt-get install gnupg -y

ENV VERSION=AUTO_STRICT

RUN echo "deb http://repo.sawtooth.me/ubuntu/ci bionic universe" >> /etc/apt/sources.list \
 && (apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 8AA7AF1F1091A5FD \
 || apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 8AA7AF1F1091A5FD) \
 && apt-get update \
 && apt-get install -y -q \
    git \
    python3 \
    python3-cbor \
    python3-colorlog \
    python3-grpcio-tools \
    python3-grpcio \
    python3-protobuf \
    python3-stdeb

COPY --from=sawtooth-signing-builder /sawtooth-core/python3-sawtooth-signing*.deb /tmp
COPY --from=sawtooth-sdk-python-builder /sawtooth-core/sdk/python3-sawtooth-sdk*.deb /tmp

RUN cd / \
 && git clone https://github.com/hyperledger/sawtooth-core.git

RUN cd /sawtooth-core/sdk/examples/ \
 && git clone https://github.com/scresh/fashion_dlt.git

RUN cd /

RUN dpkg -i /tmp/python3-sawtooth-*.deb || true \
 && apt-get -f -y install \
 && /sawtooth-core/bin/protogen \
 && cd /sawtooth-core/sdk/examples/fashion_dlt/ \
 && if [ -d "debian" ]; then rm -rf debian; fi \
 && python3 setup.py clean --all \
 && python3 setup.py --command-packages=stdeb.command debianize \
 && if [ -d "packaging/ubuntu" ]; then cp -R packaging/ubuntu/* debian/; fi \
 && dpkg-buildpackage -b -rfakeroot -us -uc
# ----------------------------------------------------------------------------------------------------------------------


# ------------------------------------------- PYTHON FASHION TP DOCKER BUILD -------------------------------------------
FROM ubuntu:bionic

RUN apt-get update \
 && apt-get install -y \
 gnupg \
 systemd

COPY --from=sawtooth-signing-builder /sawtooth-core/python3-sawtooth-signing*.deb /tmp
COPY --from=sawtooth-sdk-python-builder /sawtooth-core/sdk/python3-sawtooth-sdk*.deb /tmp
COPY --from=python-fashion-tp-builder /sawtooth-core/sdk/examples/python3-sawtooth-fashion*.deb /tmp

RUN echo "deb http://repo.sawtooth.me/ubuntu/ci bionic universe" >> /etc/apt/sources.list \
 && (apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 8AA7AF1F1091A5FD \
 || apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 8AA7AF1F1091A5FD) \
 && apt-get update \
 && dpkg -i /tmp/python3-sawtooth-*.deb || true \
 && apt-get -f -y install
# ----------------------------------------------------------------------------------------------------------------------