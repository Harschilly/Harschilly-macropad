# Tutorials came in clutch
import board
import busio
import time
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_ssd1306

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.extensions.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC

# Emoji thingys

ICON_COPY = bytearray([
    0x00,0x00,0x3E,0x22,0x22,0x3E,0x20,0x20,
    0x3E,0x22,0x22,0x3E,0x00,0x00,0x00,0x00
])

ICON_PASTE = bytearray([
    0x00,0x1C,0x14,0x14,0x1C,0x00,0x3E,0x22,
    0x22,0x22,0x3E,0x00,0x00,0x00,0x00,0x00
])

ICON_CUT = bytearray([
    0x00,0x22,0x14,0x08,0x14,0x22,0x00,0x22,
    0x14,0x08,0x14,0x22,0x00,0x00,0x00,0x00
])

ICON_UNDO = bytearray([
    0x00,0x08,0x18,0x28,0x08,0x08,0x1C,0x22,
    0x22,0x1C,0x00,0x00,0x00,0x00,0x00,0x00
])

ICON_REDO = bytearray([
    0x00,0x10,0x18,0x14,0x10,0x10,0x1C,0x22,
    0x22,0x1C,0x00,0x00,0x00,0x00,0x00,0x00
])

ICON_PLAY = bytearray([
    0x00,0x08,0x18,0x38,0x78,0x38,0x18,0x08,
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00
])

ICON_NEXT = bytearray([
    0x00,0x22,0x36,0x3E,0x36,0x22,0x20,0x20,
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00
])

ICON_PREV = bytearray([
    0x00,0x20,0x20,0x22,0x36,0x3E,0x36,0x22,
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00
])

ICON_VOL = bytearray([
    0x00,0x06,0x0E,0x1E,0x3E,0x1E,0x0E,0x06,
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00
])

ICON_MUTE = bytearray([
    0x00,0x3E,0x22,0x14,0x08,0x14,0x22,0x3E,
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00
])

# The keypad

keyboard = KMKKeyboard()
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Matrix
keyboard.col_pins = (board.GP29, board.GP4, board.GP3)
keyboard.row_pins = (board.GP26, board.GP27, board.GP28)

keyboard.extensions.append(MediaKeys())

# spinny thingy

encoder = EncoderHandler()
encoder.pins = (
    (board.GP4, board.GP5, board.GP1),  # A, B, Switch
)
encoder.map = (
    ((KC.VOLD, KC.VOLU, KC.MUTE),),
)
keyboard.extensions.append(encoder)

# OLED stuff

displayio.release_displays()

i2c = busio.I2C(board.GP7, board.GP6)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

display = adafruit_ssd1306.SSD1306(
    display_bus,
    width=128,
    height=32,
)

display.fill(0)
display.show()

# OLED Features

volume = 50
muted = False
anim_frame = 0

def show_icon(icon, text):
    display.fill(0)
    display.bitmap(0, 8, icon, 16, 16, 1)
    display.text(text, 20, 10, 1)
    display.show()

def show_volume(vol, mute=False):
    display.fill(0)
    display.bitmap(0, 8, ICON_MUTE if mute else ICON_VOL, 16, 16, 1)

    bar = int((vol / 100) * 100)
    display.rect(20, 26, bar, 4, 1)
    display.text(f"{vol}%", 20, 8, 1)
    display.show()

def oled_animation():
    global anim_frame
    display.rect(anim_frame % 128, 0, 10, 3, 1)
    anim_frame += 4

# Keymap

keyboard.keymap = [
    [
        KC.LCTL(KC.C), KC.LCTL(KC.V), KC.LCTL(KC.X),
        KC.LCTL(KC.Z), KC.LCTL(KC.Y), KC.LALT(KC.TAB),
        KC.MEDIA_PLAY_PAUSE, KC.MEDIA_NEXT_TRACK, KC.MEDIA_PREV_TRACK,
    ]
]

# what each key does

@keyboard.on_press
def key_pressed(key):
    if key == KC.LCTL(KC.C):
        show_icon(ICON_COPY, "COPY")
    elif key == KC.LCTL(KC.V):
        show_icon(ICON_PASTE, "PASTE")
    elif key == KC.LCTL(KC.X):
        show_icon(ICON_CUT, "CUT")
    elif key == KC.LCTL(KC.Z):
        show_icon(ICON_UNDO, "UNDO")
    elif key == KC.LCTL(KC.Y):
        show_icon(ICON_REDO, "REDO")
    elif key == KC.MEDIA_PLAY_PAUSE:
        show_icon(ICON_PLAY, "PLAY")
    elif key == KC.MEDIA_NEXT_TRACK:
        show_icon(ICON_NEXT, "NEXT")
    elif key == KC.MEDIA_PREV_TRACK:
        show_icon(ICON_PREV, "PREV")


@keyboard.before_matrix_scan
def before_scan():
    oled_animation()

keyboard.go()
