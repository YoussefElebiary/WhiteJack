import pygame as pg

import config
from engine import Engine
from buttons import Buttons

def draw_text(screen, text: str, x: int, y: int, center: bool = False, font = None):
    if font is None:
        font = config.FONT
    img = font.render(text, True, (255, 255, 255))
    rect= img.get_rect()
    rect.topleft = (x, y)
    if center:
        rect.center = (x, y)
    screen.blit(img, rect)

def draw_card(screen, img, x, y):
    shadow = pg.Surface((img.get_width() + 10, img.get_height() + 10), pg.SRCALPHA)
    pg.draw.rect(shadow, config.WHITE, shadow.get_rect(), border_radius=8)
    screen.blit(shadow, (x - 5, y - 5))
    screen.blit(img, (x, y))

def draw_bet_screen(screen, engine, bet_input):
    screen.fill(config.GREEN)
    draw_text(screen, "WhiteJack", config.WIDTH//2, 100, center=True, font=config.BIG_FONT)
    draw_text(screen, f"Balance: ${engine.balance}", config.WIDTH//2, 200, center=True)
    draw_text(screen, "Enter Bet:", config.WIDTH//2, 300, center=True)
    draw_text(screen, bet_input + "_", config.WIDTH//2, 350, center=True)
    draw_text(screen, "Press ENTER or Click START to begin", config.WIDTH//2, 450, center=True)

def draw_game_screen(screen, engine, buttons):
    screen.fill(config.GREEN)
    # Top-left balance and bet
    draw_text(screen, f"Balance: ${engine.balance}", 10, 10)
    draw_text(screen, f"Current Bet: ${engine.bet}", 10, 40)
    
    # Dealer
    draw_text(screen, "Dealer", config.WIDTH // 2, 50, True)
    x_offset = config.WIDTH//2 - (len(engine.dealer_cards) * 60)
    for i, card in enumerate(engine.dealer_cards):
        img = engine.cards.get_card(*card)
        draw_card(screen, img, x_offset + i * 120, 100)
    
    # Player hands
    hand_spacing = 200
    y_base = 400
    x_offsets = []
    for h_index, hand in enumerate(engine.hands):
        x_offset = config.WIDTH//2 - ((len(engine.hands)-1) * hand_spacing)//2 + h_index * hand_spacing
        hand_width = len(hand) * 120
        start_x = x_offset - hand_width//2
        for i, card in enumerate(hand):
            draw_card(screen, engine.cards.get_card(*card), start_x + i*120, y_base)
        draw_text(screen, f"Hand {h_index+1} Value: {Engine.hand_value(hand)}", x_offset, y_base-30, center=True)
        if h_index == engine.current_hand and engine.in_round:
            draw_text(screen, "-> Current Hand <-", x_offset, y_base-60, center=True)
        x_offsets.append(x_offset)

    # Update buttons enabled state
    current_hand = engine.hands[engine.current_hand] if engine.hands else []
    for btn in buttons:
        if btn.text == "Split":
            btn.enabled = len(current_hand) == 2 and current_hand[0][0] == current_hand[1][0] and engine.balance >= engine.bet
        elif btn.text == "Double":
            btn.enabled = engine.in_round and engine.balance >= engine.bet
        else:
            btn.enabled = engine.in_round

    # Position buttons dynamically below current hand
    if engine.in_round and engine.hands and 0 <= engine.current_hand < len(engine.hands):
        button_width = 100
        spacing = 20
        x_center = x_offsets[engine.current_hand]
        button_y = y_base + 180  # below cards
        total_width = len(buttons) * (button_width + spacing) - spacing
        start_x = x_center - total_width // 2

        mouse_pos = pg.mouse.get_pos()
        for i, btn in enumerate(buttons):
            btn.rect.topleft = (start_x + i*(button_width + spacing), button_y)
            btn.check_hover(mouse_pos)
            btn.draw()

    # Draw result overlay if round ended
    if engine.result:
        overlay = pg.Surface((config.WIDTH, config.HEIGHT), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # semi-transparent dark overlay
        screen.blit(overlay, (0, 0))
        draw_text(screen, engine.result, config.WIDTH//2, 250, center=True, font=config.BIG_FONT)
        draw_text(screen, "Press ENTER to continue", config.WIDTH//2, 300, center=True)

def create_game_buttons(screen, engine):
    button_width = 100
    button_height = 40
    spacing = 30
    y_pos = 370  # above player cards
    x_center = config.WIDTH // 2
    buttons = []

    # Hit
    buttons.append(Buttons(screen, "Hit", x_center - button_width*2 - spacing, y_pos, button_width, button_height,
                          lambda: engine.player_hit()))
    # Stand
    buttons.append(Buttons(screen, "Stand", x_center - button_width//2, y_pos, button_width, button_height,
                          lambda: engine.player_stand()))
    # Double
    buttons.append(Buttons(screen, "Double", x_center + button_width + spacing - button_width, y_pos, button_width, button_height,
                          lambda: engine.player_double()))
    # Split
    buttons.append(Buttons(screen, "Split", x_center + button_width*2 + spacing - button_width, y_pos, button_width, button_height,
                          lambda: engine.player_split()))

    return buttons