#!/bin/bash

# Install tools specified in mise.toml
#
mkdir -p /root/.ssh
cp /tmp/.ssh/id_rsa /root/.ssh/id_rsa
chmod 600 /root/.ssh/id_rsa

cd /workspaces/real-time-ml-system-cohort-4
mise trust
mise install
echo 'eval "$(/usr/local/bin/mise activate bash)"' >> ~/.bashrc
source ~/.bashrc