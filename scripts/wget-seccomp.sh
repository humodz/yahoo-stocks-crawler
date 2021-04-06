#!/usr/bin/env bash

# Downloads a seccomp profile that allows running chrome on docker without --no-sandbox

wget -O 'docker/seccomp-chrome.json' 'https://raw.githubusercontent.com/Zenika/alpine-chrome/master/chrome.json'
