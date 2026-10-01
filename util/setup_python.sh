#!/bin/bash
# Builds a shared-library CPython into util/python/prefix, for PyInstaller builds on old glibc

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

set -e

PYTHON_VERSION=3.12.15
PYTHON_SHA256=c2c4321961fab0fb999d66e0cecf521c2ab3994c7992873ea99e306c1094fd5a
PREFIX=$SCRIPT_DIR/python/prefix

cd "$SCRIPT_DIR"
rm -rf python && mkdir -p python

pushd python

wget "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz"
echo "${PYTHON_SHA256}  Python-${PYTHON_VERSION}.tar.xz" | sha256sum -c -
tar xf Python-${PYTHON_VERSION}.tar.xz

pushd Python-${PYTHON_VERSION}
./configure --enable-shared --prefix=$PREFIX LDFLAGS="-Wl,-rpath,$PREFIX/lib"
make -j$(nproc)
make install
popd

popd
