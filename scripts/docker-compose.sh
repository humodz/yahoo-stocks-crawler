#!/usr/bin/env bash
# Helper script for docker-compose
# Usage:
#     ./scripts/docker-compose.sh build
#     ./scripts/docker-compose.sh up
#     ./scripts/docker-compose.sh exec app sh
# Etc ...

docker-compose -p yahoo-stocks-crawler -f docker/docker-compose.yml "$@"
