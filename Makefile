PYTHON ?= python3.12
VENV := venv

.PHONY: app clean

# Rebuild the standalone app from scratch (target/Vial.app on macOS, target/Vial/ elsewhere)
app: $(VENV)/.installed
	rm -rf target/Vial.app target/Vial target/PyInstaller
	$(VENV)/bin/pyinstaller --noconfirm --distpath target --workpath target/PyInstaller vial.spec

$(VENV)/.installed: requirements.txt
	test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt
	touch $@

clean:
	rm -rf target/Vial.app target/Vial target/PyInstaller
