#!/usr/bin/env bash

CURR_PATH="$(dirname $(readlink -f $0))"
GIT_RANGE="${1:-HEAD~1}"

git diff "${GIT_RANGE}" | awk -f "${CURR_PATH}/"git_diff_test_grab.awk