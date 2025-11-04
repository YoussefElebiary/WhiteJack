import os
import sys
import pygame as pg

def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource, compatible with PyInstaller.
    - In PyInstaller executable, sys._MEIPASS points to the temporary folder
      where files are extracted.
    - In normal Python execution, it uses the current working directory.
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



WIDTH, HEIGHT = 1000, 650
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 254, 255)
GREEN = (34, 139, 34)
YELLOW = (255, 215, 0)
RED = (200, 50, 50)
BUTTON_HOVER = (255, 100, 100)

FONT = None
BIG_FONT = None

ASSETS_PATH = resource_path("./assets")
ICON_PATH = os.path.join(ASSETS_PATH, "icon.png")
CARD_PATH = os.path.join(ASSETS_PATH, "cards")

SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
SCORE = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10, 'king': 10, 'queen': 10,
    'jack': 10, 'ace': 11
}

def init_fonts():
    global FONT, BIG_FONT
    FONT = pg.font.SysFont("arial", 24)
    BIG_FONT = pg.font.SysFont("arial", 40, bold=True)