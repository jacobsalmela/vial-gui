# -*- mode: python ; coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
#
# Build with:
#   pyinstaller --noconfirm --distpath target --workpath target/PyInstaller vial.spec
#
# Produces target/Vial.app on macOS and target/Vial/ elsewhere, the same layout `fbs freeze` used.
import glob
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = SPECPATH
sys.path.insert(0, os.path.join(ROOT, "src", "main", "python"))
from appcontext import load_build_settings  # noqa: E402

settings = load_build_settings()
app_name = settings["app_name"]

# Bundle the merged build settings so the frozen app can read them via get_resource()
gen_dir = os.path.join(workpath, "generated")
os.makedirs(gen_dir, exist_ok=True)
build_settings_path = os.path.join(gen_dir, "build_settings.json")
with open(build_settings_path, "w") as outf:
    json.dump(settings, outf, indent=4)

datas = [
    (build_settings_path, "."),
    (os.path.join(ROOT, "src", "main", "icons", "Icon.ico"), "."),
]
for resource in glob.glob(os.path.join(ROOT, "src", "main", "resources", "base", "*")):
    datas.append((resource, "."))


def generate_icns():
    """ Builds Icon.icns from src/main/icons/{base,mac}/*.png, the same way fbs did """
    iconset = os.path.join(workpath, "Icon.iconset")
    shutil.rmtree(iconset, ignore_errors=True)
    os.makedirs(iconset)
    for profile in ["base", "mac"]:
        for png in glob.glob(os.path.join(ROOT, "src", "main", "icons", profile, "*.png")):
            m = re.match(r"(\d+)(?:@(\d+)x)?$", os.path.splitext(os.path.basename(png))[0])
            size, scale = int(m.group(1)), int(m.group(2) or 1)
            name = "icon_{0}x{0}".format(size) + ("@{}x".format(scale) if scale != 1 else "")
            shutil.copy(png, os.path.join(iconset, name + ".png"))
    icns = os.path.join(workpath, "Icon.icns")
    subprocess.run(["iconutil", "-c", "icns", iconset, "-o", icns], check=True)
    return icns


a = Analysis(
    [os.path.join(ROOT, "src", "main", "python", "main.py")],
    pathex=[os.path.join(ROOT, "src", "main", "python")],
    datas=datas,
    noarchive=False,
)
if sys.platform.startswith("linux"):
    # Use the host's copies of these. Bundled ones break Popen() and GPU drivers on distros whose
    # libc/libstdc++ differ from the build machine (same list as fbs), and an old fontconfig cannot
    # parse newer distros' /etc/fonts (per the AppImage excludelist)
    host_libs = ("libstdc++.so", "libtinfo.so", "libreadline.so", "libdrm.so", "libfontconfig.so", "libfreetype.so")
    a.binaries = [b for b in a.binaries if not os.path.basename(b[0]).startswith(host_libs)]

pyz = PYZ(a.pure)

if sys.platform == "darwin":
    icon = generate_icns()
elif sys.platform.startswith("win"):
    icon = os.path.join(ROOT, "src", "main", "icons", "Icon.ico")
else:
    icon = None

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=app_name,
    debug=False,
    strip=False,
    upx=False,
    console=False,
    icon=icon,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name=app_name,
)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name=app_name + ".app",
        icon=icon,
        bundle_identifier=settings["mac_bundle_identifier"],
        version=settings["version"],
        info_plist={
            "CFBundleDisplayName": app_name,
            "CFBundleShortVersionString": settings["version"],
            "CFBundleVersion": settings["version"],
            "LSBackgroundOnly": "0",
            "NSPrincipalClass": "NSApplication",
            "NSHighResolutionCapable": True,
        },
    )
