#!/usr/bin/env bash

set -euo pipefail

# package repository into tar.gz file
tarfile=$(basename "$(git config --get remote.origin.url)" .git).tar.gz
git archive --verbose --format tar.gz --output "$tarfile" HEAD



# upload to buildkite artifactory (for reference only)
buildkite-agent artifact upload "$tarfile"
