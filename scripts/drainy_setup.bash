#!/usr/bin/env bash
# Initial environment setup for the Drainy workspace.
#
# Usage:
#   source drainy_setup.bash            # configure the current shell
#   source drainy_setup.bash --install  # also add it to ~/.bashrc so every new shell is configured

DRAINY_WS="${DRAINY_WS:-$HOME/ws/drainy_ws}"
DRAINY_ROS_DOMAIN_ID=32

# Environment changes only persist if the script is sourced
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  echo "[drainy_setup] This script must be sourced: source ${BASH_SOURCE[0]}" >&2
  exit 1
fi

if [[ "$1" == "--install" ]]; then
  _drainy_script="$(realpath "${BASH_SOURCE[0]}")"
  if ! grep -qF "$_drainy_script" "$HOME/.bashrc" 2>/dev/null; then
    echo "source $_drainy_script" >> "$HOME/.bashrc"
    echo "[drainy_setup] Added to ~/.bashrc"
  else
    echo "[drainy_setup] Already present in ~/.bashrc"
  fi
  unset _drainy_script
fi

if [[ -f "$DRAINY_WS/install/setup.bash" ]]; then
  source "$DRAINY_WS/install/setup.bash"
else
  echo "[drainy_setup] $DRAINY_WS/install/setup.bash not found, build the workspace first (colcon build --symlink-install)" >&2
fi

# Exported last so nothing sourced above can override it
export ROS_DOMAIN_ID=$DRAINY_ROS_DOMAIN_ID

echo "[drainy_setup] Workspace: $DRAINY_WS | ROS_DOMAIN_ID=$ROS_DOMAIN_ID"
