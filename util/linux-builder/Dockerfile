FROM ubuntu:18.04

RUN apt-get update && apt-get -y upgrade
# Python build deps, plus the libraries Qt needs to load and its xcb platform plugin needs at runtime,
# so PyInstaller can bundle them into the AppImage
RUN apt-get install -y build-essential wget file libffi-dev libssl-dev zlib1g-dev liblzma-dev libbz2-dev \
    libusb-1.0-0-dev libudev-dev \
    libglib2.0-0 libgl1 libegl1 libfontconfig1 libdbus-1-3 libx11-6 libx11-xcb1 libxext6 \
    libxkbcommon-x11-0 libxcb-glx0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
    libxcb-render-util0 libxcb-shape0 libxcb-sync1 libxcb-xinerama0 libxcb-xfixes0 libxcb-xkb1 libxcb-util1

# Build Python before copying the rest of the tree so source changes don't invalidate this layer
COPY util/setup_python.sh /vial-gui/util/setup_python.sh
RUN /vial-gui/util/setup_python.sh

ARG APPIMAGETOOL_SHA256=ed4ce84f0d9caff66f50bcca6ff6f35aae54ce8135408b3fa33abfc3cb384eb0
ARG RUNTIME_SHA256=2fca8b443c92510f1483a883f60061ad09b46b978b2631c807cd873a47ec260d
# Extract appimagetool so it runs without FUSE. Zeroing the AppImage magic bytes lets it also run
# under x86_64 emulation (e.g. Docker on Apple Silicon), which rejects them.
RUN cd /opt && \
    wget -O appimagetool.AppImage https://github.com/AppImage/appimagetool/releases/download/1.9.1/appimagetool-x86_64.AppImage && \
    echo "${APPIMAGETOOL_SHA256}  appimagetool.AppImage" | sha256sum -c - && \
    chmod +x appimagetool.AppImage && \
    dd if=/dev/zero of=appimagetool.AppImage bs=1 count=3 seek=8 conv=notrunc && \
    ./appimagetool.AppImage --appimage-extract && \
    mv squashfs-root appimagetool && rm appimagetool.AppImage && \
    ln -s /opt/appimagetool/AppRun /usr/local/bin/appimagetool && \
    wget -O /usr/local/share/appimage-runtime-x86_64 https://github.com/AppImage/type2-runtime/releases/download/20251108/runtime-x86_64 && \
    echo "${RUNTIME_SHA256}  /usr/local/share/appimage-runtime-x86_64" | sha256sum -c -

COPY . /vial-gui
