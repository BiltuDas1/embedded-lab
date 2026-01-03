#!/bin/bash

# Determine the directory where this script is located
if [ -n "$ZSH_VERSION" ]; then
    SCRIPT_PATH=$(dirname "${(%):-%x}")
elif [ -n "$BASH_VERSION" ]; then
    SCRIPT_PATH=$(dirname "${BASH_SOURCE[0]}")
else
    # Fallback for standard sh (cannot detect source path securely)
    SCRIPT_PATH="."
fi

SCRIPT_DIR="$(cd "$SCRIPT_PATH" && pwd)"

ENV_FILE="$SCRIPT_DIR/../../config.env"

if [ -f "$ENV_FILE" ]; then
    # 'set -a' automatically exports all variables defined in the sourced file
    set -a

    # We use sed to strip Windows carriage returns (\r) just in case the .env file
    # was edited on Windows, otherwise Bash might read values like "value\r"
    source <(sed 's/\r$//' "$ENV_FILE")

    set +a
else
    echo "Warning: config.env not found at $ENV_FILE"
fi
