#!/bin/bash
if ! (dpkg -l | grep docker-compose > /dev/null); then
  sudo apt-get update
  sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo apt-key fingerprint 0EBFCD88
  sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"

  sudo apt-get update
  sudo apt-get install docker-ce

  sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose

  sudo groupadd docker
  sudo usermod -aG docker $USER
fi
docker-compose -f docker-compose.yaml down > /dev/null
yes | docker volume prune > /dev/null
docker-compose -f docker-compose.yaml up
