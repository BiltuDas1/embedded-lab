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

# Check if esptool is installed
if ! command -v esptool &> /dev/null; then
    echo -e "\033[0;31m[ERROR] esptool is NOT in your PATH.\033[0m"
    echo "Please install esptool (pip install esptool) and try again."
    exit 1
fi

# Load settings from config.sh
if [ -f "$SCRIPT_DIR/config.sh" ]; then
    source "$SCRIPT_DIR/config.sh"
else
    echo "Error: config.sh not found."
    exit 1
fi

# Erase the flash
esptool --port "$PORT" erase-flash
