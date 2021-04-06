#!/usr/bin/env bash
# https://pythonspeed.com/articles/system-packages-docker/
# Usage: ./install-packages.sh dependency1 dependency2 ...

set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get -y upgrade

# "$@" is the command-line arguments
apt-get -y install --no-install-recommends "$@"

apt-get clean
rm -rf /var/lib/apt/lists/*
