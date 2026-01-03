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

# Check if arduino-cli is installed
if ! command -v arduino-cli &> /dev/null; then
    echo -e "\033[0;31m[ERROR] arduino-cli is NOT in your PATH.\033[0m"
    echo "Please install it or add it to your PATH."
    exit 1
fi

# Load settings from config.sh
if [ -f "$SCRIPT_DIR/config.sh" ]; then
    source "$SCRIPT_DIR/config.sh"
else
    echo "Error: config.sh not found."
    exit 1
fi

INPUT_DIR=$(realpath "$SCRIPT_DIR/../../build/$1")
arduino-cli upload -p "$PORT" --fqbn "$BOARD_ID" --input-dir "$INPUT_DIR"
