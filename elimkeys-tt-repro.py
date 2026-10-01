#!/usr/bin/env python3
"""
ElimKeys Elytra: TT(layer) keycodes are acknowledged but stored as KC_NO.

Requires: pip install hidapi
Run:      python3 elimkeys-tt-repro.py

Writes a few layer keycodes to layer 0, matrix row 2, col 0 (the Caps Lock
position) with VIA's dynamic_keymap_set_keycode (0x05), reads each back with
dynamic_keymap_get_keycode (0x04), then restores the original keycode.
Also checks whether QMK setting 20 (Tapping Toggle) is exposed over Vial.
"""
import struct
import hid

LAYER, ROW, COL = 0, 2, 0
KEYCODES = [
    ("MO(1)", 0x5221),
    ("TT(1)", 0x52C1),
    ("TG(1)", 0x5261),
    ("OSL(1)", 0x5281),
    ("LT1(KC_CAPS)", 0x4139),
]

info = next(d for d in hid.enumerate() if d["usage_page"] == 0xFF60 and d["usage"] == 0x61)
print("{} {} ({:04x}:{:04x}) {}".format(info["manufacturer_string"], info["product_string"],
                                         info["vendor_id"], info["product_id"], info["serial_number"]))
dev = hid.device()
dev.open_path(info["path"])


def send(msg):
    dev.write(b"\x00" + msg + b"\x00" * (32 - len(msg)))
    return bytes(dev.read(32, 1000))


def get_keycode():
    return struct.unpack(">H", send(struct.pack("BBBB", 0x04, LAYER, ROW, COL))[4:6])[0]


def set_keycode(kc):
    send(struct.pack(">BBBBH", 0x05, LAYER, ROW, COL, kc))


original = get_keycode()
try:
    for name, kc in KEYCODES:
        set_keycode(kc)
        stored = get_keycode()
        print("{:14} wrote 0x{:04X}  read back 0x{:04X}  {}".format(
            name, kc, stored, "OK" if stored == kc else "MISMATCH"))
finally:
    set_keycode(original)

# Vial: qmk_settings_get (0xFE 0x0A) for qsid 20 = Tapping Toggle; status byte 0 means supported
status = send(struct.pack("<BBH", 0xFE, 0x0A, 20))[0]
print("QMK setting 20 (Tapping Toggle): {}".format("supported" if status == 0 else "NOT supported (status 0x{:02X})"
                                                    .format(status)))
dev.close()
