#!/usr/bin/env bash

# Note: run using "source" or "."
# Good:
#   . scripts/add-to-path
#   bash scripts/add-to-path
# Bad:
#   ./scripts/add-to-path
#   bash scripts/add-to-path

PATH="$(realpath bin):$PATH"
