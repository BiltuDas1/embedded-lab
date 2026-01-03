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

# Define Paths and Variables
SOURCE_PATH="$1"

# Extract the folder name
# If the path is ".", we get the name of the current directory
# "realpath" ensures we get the absolute path first to get the correct name
FULL_SOURCE_PATH=$(realpath "$SOURCE_PATH")
FOLDER_NAME=$(basename "$FULL_SOURCE_PATH")

# Define Build and Library directories relative to this script
BUILD_DIR=$(realpath "$SCRIPT_DIR/../../build")
BUILD_FOLDER="$BUILD_DIR/$FOLDER_NAME"
SHARED_LIB_DIR=$(realpath "$SCRIPT_DIR/../../shared")

# Ensure build directory exists (good practice in Linux)
mkdir -p "$BUILD_FOLDER"

# Run the Compile Command
echo "Compiling $FOLDER_NAME..."

arduino-cli compile --fqbn "$BOARD_ID" "$FULL_SOURCE_PATH" \
  --libraries "$SHARED_LIB_DIR" \
  --warnings all \
  --output-dir "$BUILD_FOLDER"

# Check for success and update log
# $? stores the exit code of the last command
if [ $? -eq 0 ]; then
    echo "$FOLDER_NAME" > "$BUILD_DIR/lastbuild.txt"
    echo -e "\033[0;32mBuild Successful.\033[0m"
else
    echo -e "\033[0;31mBuild Failed.\033[0m"
    exit 1
fi
