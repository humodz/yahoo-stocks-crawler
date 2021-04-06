#!/usr/bin/env bash

./scripts/start-redis.sh

DOTENV_FILE=test.env pytest "${@}"
