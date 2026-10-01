### vial-gui

# Docs and getting started

### Please visit [get.vial.today](https://get.vial.today/) to get started with Vial

Vial is an open-source cross-platform (Windows, Linux and Mac) GUI and a QMK fork for configuring your keyboard in real time.


![](https://get.vial.today/img/vial-win-1.png)


---


#### Releases

Visit https://get.vial.today/ to download a binary release of Vial.

#### Development

Python 3.12 is recommended.

Install dependencies:

```
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To launch the application afterwards:

```
source venv/bin/activate
python src/main/python/main.py
```

To build a standalone app (`target/Vial.app` on macOS, `target/Vial/` elsewhere; the Linux AppImage is built with `util/linux-builder/build-in-docker.sh`):

```
source venv/bin/activate
pyinstaller --noconfirm --distpath target --workpath target/PyInstaller vial.spec
```

To run the tests:

```
source venv/bin/activate
pip install -r test-requirements.txt
pytest src/main/python/test
```
