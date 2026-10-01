#!/bin/bash

set -e

HERE=$(cd "$(dirname "$0")" && pwd)

cd "$HERE"
rm -rf output && mkdir -p output

cd "$HERE/../.."

docker build --platform linux/amd64 -t vialguibuilder:latest -f util/linux-builder/Dockerfile .
docker run --platform linux/amd64 --privileged --rm -v "$(realpath util/linux-builder/output)":/output vialguibuilder:latest bash /vial-gui/util/linux-builder/_builder.sh

cd "$HERE"
ls -lah output
