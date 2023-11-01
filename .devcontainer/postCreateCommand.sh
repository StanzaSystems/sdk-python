#!/bin/bash

sudo apt-get update
DEBIAN_FRONTEND=noninteractive \
    sudo apt-get -y install --no-install-recommends \
    apt-utils dialog dnsutils

# Because I'm tired of remembering to do this everytime I rebuild my devcontainer
echo '-w "\\n"' > ~/.curlrc
echo 'alias ll="ls -l"' >> ~/.bashrc
source ~/.bashrc