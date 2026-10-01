#!/bin/bash
# Packages the PyInstaller output in target/Vial into target/Vial-x86_64.AppImage

set -e

ROOT=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )/../.." &> /dev/null && pwd )
APPDIR=$ROOT/target/Vial.AppDir
RUNTIME=${APPIMAGE_RUNTIME:-/usr/local/share/appimage-runtime-x86_64}

rm -rf "$APPDIR"
mkdir -p "$APPDIR/opt"
cp -a "$ROOT/target/Vial" "$APPDIR/opt/Vial"

cat > "$APPDIR/AppRun" <<\APPRUN
#!/bin/sh
HERE=$(dirname $(readlink -f "${0}"))
export QT_QPA_PLATFORM=xcb
exec "${HERE}/opt/Vial/Vial" "$@"
APPRUN
chmod a+x "$APPDIR/AppRun"

cat > "$APPDIR/Vial.desktop" <<\DESKTOP
[Desktop Entry]
Name=Vial
Type=Application
Exec=Vial
Terminal=false
NoDisplay=false
Categories=Utility;
Version=1.0
Icon=Vial
DESKTOP

for icon in "$ROOT"/src/main/icons/base/*.png "$ROOT"/src/main/icons/linux/*.png; do
    size=$(basename "$icon" .png)
    mkdir -p "$APPDIR/usr/share/icons/hicolor/${size}x${size}/apps"
    cp "$icon" "$APPDIR/usr/share/icons/hicolor/${size}x${size}/apps/Vial.png"
done
cp "$ROOT/src/main/icons/linux/256.png" "$APPDIR/Vial.png"

ARCH=x86_64 appimagetool --runtime-file "$RUNTIME" "$APPDIR" "$ROOT/target/Vial-x86_64.AppImage"
