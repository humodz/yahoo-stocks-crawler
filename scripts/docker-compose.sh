#!/usr/bin/env bash

docker-compose -p yahoo-stocks-crawler -f docker/docker-compose.yml "$@"
