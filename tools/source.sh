#!/bin/bash

if [ -n "$ZSH_VERSION" ]; then
  # Zsh specific source detection
  _REL_PATH=$(dirname "${(%):-%x}")
elif [ -n "$BASH_VERSION" ]; then
  # Bash specific source detection
  _REL_PATH=$(dirname "${BASH_SOURCE[0]}")
else
  _REL_PATH="."
fi

export CROSS_COMPILER_ROOT="$(cd "$_REL_PATH" && pwd)"

function cross-compiler {
  local SCRIPT_DIR="$CROSS_COMPILER_ROOT"

  local COMPILE_SCRIPT="$SCRIPT_DIR/linux/compile.sh"
  local UPLOAD_SCRIPT="$SCRIPT_DIR/linux/upload.sh"
  local ERASE_SCRIPT="$SCRIPT_DIR/linux/erase.sh"

  # Resolve absolute paths (equivalent to [System.IO.Path]::GetFullPath)
  local BUILD_PATH
  BUILD_PATH=$(realpath "$SCRIPT_DIR/../build")
  local LAST_BUILD_LOG="$BUILD_PATH/lastbuild.txt"
  local LIBRARY_FOLDER_NAME="shared"
  local LIBRARY_PATH
  LIBRARY_PATH=$(realpath "$SCRIPT_DIR/../$LIBRARY_FOLDER_NAME")
  local GIT_PATH
  GIT_PATH=$(realpath "$SCRIPT_DIR/../.git")

  # Argument Handling
  if [[ $# -eq 0 ]]; then
    # Cyan color for usage
    echo -e "\033[0;36mUsage:  cross-compile <path>\033[0m"
    echo "Example: cross-compile ."
    return 1
  fi

  if [[ "$1" == "." ]]; then
    local current="$PWD"
    "$COMPILE_SCRIPT" "$current"

  elif [[ "$1" == "--upload" ]]; then
    if [[ ! -f "$LAST_BUILD_LOG" ]]; then
        echo -e "\033[0;31m[Error] No build log found at $LAST_BUILD_LOG\033[0m"
        return 1
    fi

    # Read first line and trim whitespace
    local last_build
    last_build=$(head -n 1 "$LAST_BUILD_LOG" | xargs)
    local last_build_path="$BUILD_PATH/$last_build"

    if [ ! -d "$last_build_path" ]; then
      echo -e "\033[0;31m[Error] build folder got corrupted, recompile and try again.\033[0m"
      return 1
    fi

    sudo "$UPLOAD_SCRIPT" "$last_build"

  elif [[ "$1" == "--reset" ]]; then
    "$ERASE_SCRIPT"

  elif [[ "$1" == "--clean-build" ]]; then
    # Check if path exists before removing to avoid errors
    if [[ -d "$BUILD_PATH" ]]; then
        rm -rf "$BUILD_PATH"
        echo "Build directory cleaned."
    fi

  # Handle --install
  elif [[ "$1" == "--install" ]] && [[ $# -eq 2 ]]; then
    local url="$2"
    # Regex match for owner/repo
    if [[ "$url" =~ [:/]([^/:]+)/([^/:]+?)(\.git)?$ ]]; then
        local owner="${BASH_REMATCH[1]}"
        local repo="${BASH_REMATCH[2]}"

        mkdir -p "$LIBRARY_PATH"

        # Calculate save path relative to the git root or absolute
        local save_path="$LIBRARY_PATH/$owner-$repo"

        git submodule add "$url" "$save_path"
    else
        echo "Invalid git URL format."
    fi

  # Handle --uninstall
  elif [[ "$1" == "--uninstall" ]] && [[ $# -eq 2 ]]; then
    local url="$2"
    if [[ "$url" =~ [:/]([^/:]+)/([^/:]+?)(\.git)?$ ]]; then
        local owner="${BASH_REMATCH[1]}"
        local repo="${BASH_REMATCH[2]}"

        local save_path="$LIBRARY_PATH/$owner-$repo"
        local git_remove_path="$GIT_PATH/modules/$LIBRARY_FOLDER_NAME/$owner-$repo"

        # Force deinit and removal
        git submodule deinit -f "$save_path"
        git rm -f "$save_path"
        rm -rf "$git_remove_path"
    else
        echo "Invalid git URL format."
    fi

  # Handle standard path argument
  elif [[ -d "$1" ]]; then
    # Remove trailing slash and resolve path
    local args_path
    args_path=$(realpath "${1%/}")
    "$COMPILE_SCRIPT" "$args_path"

  else
    echo "Invalid argument"
    return 1
  fi
}
