import os
import pygame as pg
from random import shuffle

from config import *

class Cards:
    def __init__(self, card_path: str) -> None:
        self.card_path: str = card_path
        self.back = None
        self.cards = {}
        self.states = {}

    def load_imgs(self) -> None:
        file_name = os.path.join(self.card_path, "back.png")
        if os.path.exists(file_name):
            self.back = pg.image.load(file_name).convert_alpha()
            self.back = pg.transform.scale(self.back, (100, 145))
        else:
            raise FileNotFoundError(f"Cards::load_imgs()    -    {file_name} does not exist")
        
        for suit in SUITS:
            for rank in RANKS:
                file_name = os.path.join(self.card_path, f"{rank}_of_{suit}.png")
                if os.path.exists(file_name):
                    img = pg.image.load(file_name).convert_alpha()
                    img = pg.transform.scale(img, (100, 145))
                    self.cards[(rank, suit)] = img
                    self.states[(rank, suit)] = True
                else:
                    raise FileNotFoundError(f"Cards::load_imgs()    -    {file_name} does not exist")

    def get_card(self, rank: str, suit: str):
        try:
            if self.states[(rank, suit)] == True:
                return self.cards[(rank, suit)]
            else:
                return self.back
        except KeyError as e:
            print(f"Cards::get_card()    -    Error occured while accessing {rank} of {suit}")
            raise e
        
    def flip_card(self, rank: str, suit: str):
        if self.states[(rank, suit)] == True:
            self.states[(rank, suit)] = False
        else:
            self.states[(rank, suit)] = True

    def reset_states(self):
        for key in self.states.keys():
            self.states[key] = False

    def build_deck(self):
        
        deck = [(r, s) for s in SUITS for r in RANKS]
        shuffle(deck)
        return deck