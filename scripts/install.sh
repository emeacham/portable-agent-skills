#!/bin/sh
# Link (or copy) a skill from this repo into the directories harnesses scan.
# POSIX sh; works on macOS and Linux.
#
# Usage: scripts/install.sh <skill-name> [--target claude|codex|cursor|copilot|agents|all]
#                                        [--copy] [--project] [--dry-run]
#   --target   which harness directory (default: all)
#   --copy     copy instead of symlink (symlink keeps the skill updated with git pull)
#   --project  install under the current directory (.claude/skills etc.) instead of $HOME
#   --dry-run  print what would happen

set -eu

REPO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SKILL=${1:-}
[ -n "$SKILL" ] || { echo "usage: $0 <skill-name> [--target ...] [--copy] [--project] [--dry-run]" >&2; exit 2; }
shift
SRC="$REPO_DIR/skills/$SKILL"
[ -d "$SRC" ] || { echo "no such skill: $SKILL (see $REPO_DIR/skills/)" >&2; exit 2; }

TARGET=all; MODE=link; BASE=$HOME; DRY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET=$2; shift ;;
    --copy) MODE=copy ;;
    --project) BASE=$(pwd) ;;
    --dry-run) DRY=1 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

dirs_for() {
  case "$1" in
    claude)  echo "$BASE/.claude/skills" ;;
    codex)   echo "$BASE/.agents/skills" ;;
    cursor)  echo "$BASE/.cursor/skills" ;;
    copilot) echo "$BASE/.github/skills" ;;   # project-level only in practice
    agents)  echo "$BASE/.agents/skills" ;;
    all)     printf '%s\n' "$BASE/.claude/skills" "$BASE/.agents/skills" "$BASE/.cursor/skills" \
             $( [ "$BASE" != "$HOME" ] && echo "$BASE/.github/skills" ) ;;
    *) echo "unknown target: $1" >&2; exit 2 ;;
  esac
}

dirs_for "$TARGET" | sort -u | while IFS= read -r dir; do
  [ -n "$dir" ] || continue
  dest="$dir/$SKILL"
  if [ "$DRY" -eq 1 ]; then
    echo "would $MODE $SRC -> $dest"; continue
  fi
  mkdir -p "$dir"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    echo "exists, skipping: $dest"; continue
  fi
  if [ "$MODE" = copy ]; then cp -R "$SRC" "$dest"; else ln -s "$SRC" "$dest"; fi
  echo "$MODE: $dest"
done
