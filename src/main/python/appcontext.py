# SPDX-License-Identifier: GPL-2.0-or-later
# Minimal replacement for fbs_runtime's ApplicationContext.
import json
import os
import signal
import sys
from functools import cached_property

from PyQt5 import QtCore, QtGui, QtWidgets

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir))


def is_frozen():
    return getattr(sys, "frozen", False)


def platform_name():
    if sys.platform == "darwin":
        return "mac"
    if sys.platform.startswith("win"):
        return "windows"
    return "linux"


def load_build_settings():
    """ Merges src/build/settings/{base,<platform>}.json, the same way fbs did """
    settings = {}
    for profile in ["base", platform_name()]:
        path = os.path.join(PROJECT_DIR, "src", "build", "settings", profile + ".json")
        if os.path.exists(path):
            with open(path, "r") as inf:
                settings.update(json.load(inf))
    return settings


class ApplicationContext:

    def __init__(self):
        # Many Qt classes require a QApplication to have been instantiated
        self.app
        if not sys.platform.startswith("win"):
            self._install_sigint_handler()
        if self.app_icon:
            self.app.setWindowIcon(self.app_icon)

    @cached_property
    def app(self):
        result = QtWidgets.QApplication(sys.argv)
        result.setApplicationName(self.build_settings["app_name"])
        result.setApplicationVersion(self.build_settings["version"])
        return result

    @cached_property
    def build_settings(self):
        if is_frozen():
            with open(self.get_resource("build_settings.json"), "r") as inf:
                return json.load(inf)
        return load_build_settings()

    @cached_property
    def app_icon(self):
        # on macOS the icon comes from the .app bundle
        if sys.platform != "darwin":
            return QtGui.QIcon(self.get_resource("Icon.ico"))

    @cached_property
    def _resource_dirs(self):
        if is_frozen():
            return [sys._MEIPASS]
        resources = os.path.join(PROJECT_DIR, "src", "main", "resources")
        return [os.path.join(resources, "base"), os.path.join(resources, platform_name()),
                os.path.join(PROJECT_DIR, "src", "main", "icons")]

    def get_resource(self, *rel_path):
        for resource_dir in self._resource_dirs:
            path = os.path.join(resource_dir, *rel_path)
            if os.path.exists(path):
                return os.path.realpath(path)
        raise FileNotFoundError("Could not locate resource {}".format(os.path.join(*rel_path)))

    def _install_sigint_handler(self):
        # Python only runs signal handlers between bytecodes, which never happens while Qt's
        # event loop is idle; wake the interpreter periodically so Ctrl+C quits cleanly
        signal.signal(signal.SIGINT, lambda *_: self.app.exit(130))
        self._sigint_timer = QtCore.QTimer()
        self._sigint_timer.timeout.connect(lambda: None)
        self._sigint_timer.start(250)
