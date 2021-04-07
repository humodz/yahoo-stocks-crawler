#!/usr/bin/env bash

./scripts/docker-compose.sh up -d redis

uvicorn app.main:app --reload
