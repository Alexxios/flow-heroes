import os

from utils import load_image

_BASE_DIR = "assets/gamekit/3 Icons"
_load = lambda x : load_image(os.path.join(_BASE_DIR, x))

HOME_ICON       = _load("Icons_01.png")
INFO_ICON       = _load("Icons_04.png")
RIGHT_ICON      = _load("Icons_25.png")
LEFT_ICON       = _load("Icons_26.png")
STORE_ICON      = _load("Icons_32.png")
SETTINGS_ICON   = _load("Icons_39.png")
QUIT_ICON       = _load("Icons_50.png")
COIN_ICON       = _load("Icons_61.png")
SWORD_ICON      = _load("Icons_63.png")
SPELL_ICON      = _load("Icons_64.png")