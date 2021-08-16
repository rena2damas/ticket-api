#!/usr/bin/env bash

set -euo pipefail

# package repository into tar.gz file
tar=$(git archive --format tar HEAD | gzip > archive-HEAD.tar.gz)

# upload to buildkite artifactory
buildkite-agent artifact upload <<< "$tar"
