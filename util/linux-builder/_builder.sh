#!/bin/bash

set -e

cd /vial-gui
./util/python/prefix/bin/python3 -m venv docker_venv
. docker_venv/bin/activate
pip install -r requirements.txt
pyinstaller --noconfirm --distpath target --workpath target/PyInstaller vial.spec
deactivate
./util/linux-builder/make_appimage.sh
mv target/Vial-x86_64.AppImage /output/Vial-x86_64.AppImage
