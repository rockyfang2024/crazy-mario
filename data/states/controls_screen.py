__author__ = 'justinarmstrong (modified)'

import pygame as pg
from .. import setup, tools
from .. import constants as c


class ControlsScreen(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.next = c.LOAD_SCREEN

    def startup(self, current_time, persist):
        self.start_time = current_time
        self.persist = persist
        self.game_info = self.persist
        self.font_large = pg.font.SysFont(None, 60)
        self.font_medium = pg.font.SysFont(None, 38)
        self.font_small = pg.font.SysFont(None, 30)
        self.blink_timer = current_time
        self.show_prompt = True

    def get_event(self, event):
        """Proceed on any key/mouse press"""
        if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

    def update(self, surface, keys, current_time):
        self.current_time = current_time

        # Blink effect for "press any key" prompt
        if current_time - self.blink_timer > 500:
            self.show_prompt = not self.show_prompt
            self.blink_timer = current_time

        # Draw background
        surface.fill(c.BLACK)

        # Title
        title_surf = self.font_large.render('Controls', True, c.WHITE)
        title_rect = title_surf.get_rect(center=(c.SCREEN_WIDTH // 2, 80))
        surface.blit(title_surf, title_rect)

        # Separator line
        pg.draw.line(surface, c.GRAY,
                     (c.SCREEN_WIDTH // 2 - 180, 110),
                     (c.SCREEN_WIDTH // 2 + 180, 110), 1)

        # Controls list
        controls = [
            ('Space', 'Jump'),
            ('S', 'Action (Fireball / Run)'),
            ('Left / Right', 'Move'),
            ('Down', 'Crouch / Enter Pipe'),
            ('Enter', 'Pause'),
            ('ESC', 'Quit Game'),
        ]

        start_y = 155
        line_height = 50

        for i, (key, desc) in enumerate(controls):
            y = start_y + i * line_height

            # Key label with background
            key_surf = self.font_small.render(key, True, c.BLACK)
            key_rect = key_surf.get_rect(center=(c.SCREEN_WIDTH // 2 - 160, y))
            bg_rect = pg.Rect(0, 0, key_rect.width + 20, key_rect.height + 8)
            bg_rect.center = (c.SCREEN_WIDTH // 2 - 160, y)
            pg.draw.rect(surface, c.WHITE, bg_rect, border_radius=6)
            surface.blit(key_surf, key_rect)

            # Description
            desc_surf = self.font_medium.render(desc, True, c.WHITE)
            desc_rect = desc_surf.get_rect(midleft=(c.SCREEN_WIDTH // 2 - 50, y))
            surface.blit(desc_surf, desc_rect)

        # Separator line
        pg.draw.line(surface, c.GRAY,
                     (c.SCREEN_WIDTH // 2 - 180, start_y + len(controls) * line_height + 10),
                     (c.SCREEN_WIDTH // 2 + 180, start_y + len(controls) * line_height + 10), 1)

        # "Press any key to start" (blinking)
        if self.show_prompt:
            prompt_surf = self.font_medium.render('Press any key to start', True, c.GOLD)
            prompt_rect = prompt_surf.get_rect(center=(c.SCREEN_WIDTH // 2, 520))
            surface.blit(prompt_surf, prompt_rect)
