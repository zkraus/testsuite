#!/usr/bin/env bash

GIT_RANGE="${1:-HEAD~1}"

git diff "${GIT_RANGE}" | awk -f git_diff_test_grab.awk