###################
# IMPORTS
###################
import pygame as pg
import sys

import config
from ui import *
from cards import Cards
from engine import Engine

pg.init()
config.init_fonts()



###################
# WINDOW
###################
screen = pg.display.set_mode((config.WIDTH, config.HEIGHT))
pg.display.set_caption("WhiteJack")
pg.display.set_icon(pg.image.load(config.ICON_PATH))
clock = pg.time.Clock()



###################
# GAME LOOP
###################
SCREEN_BET = 0
SCREEN_GAME = 1

cards = Cards(config.CARD_PATH)
cards.load_imgs()
engine = Engine(cards)
buttons = create_game_buttons(screen, engine)
bet = ""
current_screen = 0
running: bool = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if current_screen == SCREEN_BET:
                if event.unicode.isdigit():
                    bet += event.unicode
                elif event.key == pg.K_BACKSPACE:
                    bet = bet[:-1]
                elif event.key == pg.K_RETURN and bet:
                    engine.start_round(int(bet))
                    bet = ""
                    current_screen = SCREEN_GAME
            elif current_screen == SCREEN_GAME:
                if engine.in_round:
                    # Player Controls
                    if event.key == pg.K_h:
                        engine.player_hit()
                    elif event.key == pg.K_s:
                        engine.player_stand()
                    elif event.key == pg.K_d:
                        engine.player_double()
                    elif event.key == pg.K_p:
                        engine.player_split()
                else:
                    # Round ended, press Enter to return to bet screen
                    if event.key == pg.K_RETURN:
                        current_screen = SCREEN_BET
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if current_screen == SCREEN_GAME and engine.in_round:
                mouse_pos = event.pos
                for btn in buttons:
                    if btn.enabled and btn.rect.collidepoint(mouse_pos):
                        btn.callback()

    if current_screen == SCREEN_BET:
        draw_bet_screen(screen, engine, bet)
    elif current_screen == SCREEN_GAME:
        draw_game_screen(screen, engine, buttons)

    pg.display.flip()
    clock.tick(config.FPS)

pg.quit()
sys.exit()