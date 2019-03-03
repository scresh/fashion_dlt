#!/bin/bash
if ! (dpkg -l | grep docker-compose > /dev/null); then
  yes | sudo apt-get update
  yes | sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
  yes | curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  yes | sudo apt-key fingerprint 0EBFCD88
  yes | sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"

  yes | sudo apt-get update
  yes | sudo apt-get install docker-ce

  yes | sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  yes | sudo chmod +x /usr/local/bin/docker-compose

  yes | sudo groupadd docker
  yes | sudo usermod -aG docker $USER
fi
sudo docker-compose -f docker-compose.yaml down > /dev/null
yes | sudo docker volume prune > /dev/null
yes | sudo docker-compose -f docker-compose.yaml up
