import pygame as pg

import config

class Buttons:
    def __init__(self, screen, text, x, y, w, h, callback, enabled=True):
        self.screen = screen
        self.text = text
        self.rect = pg.Rect(x, y, w, h)
        self.callback = callback
        self.enabled = enabled
        self.hovered = False

    def draw(self, hand_x=None, hand_y=None, card_height=180):
        """
        Draws the button.
        If hand_x and hand_y are provided, button will appear below the hand.
        """
        # Base color
        if not self.enabled:
            base_color = (120, 120, 120)  # dark gray for disabled
            text_color = (50, 50, 50)
        else:
            base_color = (200, 200, 200)  # light gray
            text_color = (0, 0, 0)
        
        # Hover effect
        if self.hovered and self.enabled:
            base_color = (220, 220, 220)

        # Position below the current hand if given
        if hand_x is not None and hand_y is not None:
            self.rect.centerx = hand_x
            self.rect.top = hand_y + card_height + 20  # 20px margin below the cards

        # Draw button rectangle and border
        pg.draw.rect(self.screen, base_color, self.rect, border_radius=5)
        pg.draw.rect(self.screen, (0, 0, 0), self.rect, 2, border_radius=5)

        # Draw text
        txt_img = config.FONT.render(self.text, True, text_color)
        txt_rect = txt_img.get_rect(center=self.rect.center)
        self.screen.blit(txt_img, txt_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.enabled and self.rect.collidepoint(mouse_pos):
            self.callback()