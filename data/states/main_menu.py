__author__ = 'justinarmstrong (modified)'

import pygame as pg
from .. import setup, tools
from .. import constants as c
from .. components import info, mario


class Menu(tools._State):
    def __init__(self):
        """Initializes the state"""
        tools._State.__init__(self)
        persist = {c.COIN_TOTAL: 0,
                   c.SCORE: 0,
                   c.LIVES: 3,
                   c.TOP_SCORE: 0,
                   c.CURRENT_TIME: 0.0,
                   c.LEVEL_STATE: None,
                   c.CAMERA_START_X: 0,
                   c.MARIO_DEAD: False,
                   'INVINCIBLE': False,
                   'PLAYER_MODE': 1}
        self.startup(0.0, persist)

    def startup(self, current_time, persist):
        """Called every time the game's state becomes this one."""
        self.next = c.CONTROLS_SCREEN
        self.persist = persist
        self.game_info = persist
        self.overhead_info = info.OverheadInfo(self.game_info, c.MAIN_MENU)

        self.sprite_sheet = setup.GFX['title_screen']
        self.setup_background()
        self.setup_mario()

        # Menu items: 0=PLAYER_1, 1=PLAYER_2, 2=LIVES, 3=INVINCIBLE
        self.selected = 0
        self.item_count = 4
        self.item_y_start = 280
        self.item_y_gap = 55

        # Settings
        self.lives = 3
        self.invincible = False
        self.player_mode = 1  # 1 = 1 player, 2 = 2 player

        # Read saved settings from persist
        if self.game_info.get('INVINCIBLE') is not None:
            self.invincible = self.game_info['INVINCIBLE']
        if self.game_info.get('LIVES_SETTING') is not None:
            self.lives = self.game_info['LIVES_SETTING']
        if self.game_info.get('PLAYER_MODE') is not None:
            self.player_mode = self.game_info['PLAYER_MODE']

        # Input debounce timers
        self.nav_timer = 0
        self.adj_timer = 0

        self.setup_cursor()

        # Fonts - smaller size for better layout
        self.font_title = pg.font.SysFont(None, 36)
        self.font_item = pg.font.SysFont(None, 28)
        self.font_setting = pg.font.SysFont(None, 22)
        self.font_arrow = pg.font.SysFont(None, 24)


    def setup_cursor(self):
        """Creates the mushroom cursor"""
        self.cursor = pg.sprite.Sprite()
        dest = (170, self.item_y_start)
        self.cursor.image, self.cursor.rect = self.get_image(
            24, 160, 8, 8, dest, setup.GFX['item_objects'])


    def setup_mario(self):
        """Places Mario at the beginning of the level"""
        self.mario = mario.Mario()
        self.mario.rect.x = 110
        self.mario.rect.bottom = c.GROUND_HEIGHT


    def setup_background(self):
        """Setup the background image to blit"""
        self.background = setup.GFX['level_1']
        self.background_rect = self.background.get_rect()
        self.background = pg.transform.scale(self.background,
                                   (int(self.background_rect.width*c.BACKGROUND_MULTIPLER),
                                    int(self.background_rect.height*c.BACKGROUND_MULTIPLER)))
        self.viewport = setup.SCREEN.get_rect(bottom=setup.SCREEN_RECT.bottom)

        self.image_dict = {}
        self.image_dict['GAME_NAME_BOX'] = self.get_image(
            1, 60, 176, 88, (170, 60), setup.GFX['title_screen'])


    def get_image(self, x, y, width, height, dest, sprite_sheet):
        """Returns images and rects to blit onto the screen"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(sprite_sheet, (0, 0), (x, y, width, height))
        if sprite_sheet == setup.GFX['title_screen']:
            image.set_colorkey((255, 0, 220))
            image = pg.transform.scale(image,
                                   (int(rect.width*c.SIZE_MULTIPLIER),
                                    int(rect.height*c.SIZE_MULTIPLIER)))
        else:
            image.set_colorkey(c.BLACK)
            image = pg.transform.scale(image,
                                   (int(rect.width*3),
                                    int(rect.height*3)))

        rect = image.get_rect()
        rect.x = dest[0]
        rect.y = dest[1]
        return (image, rect)


    def get_event(self, event):
        """Handle keyboard events for the menu"""
        if event.type != pg.KEYDOWN:
            return

        now = self.current_time
        key = event.key

        # Confirm selection: start game from any menu item
        if key in (pg.K_RETURN, pg.K_a, pg.K_s, pg.K_SPACE):
            self.reset_game_info()
            self.done = True
            return

        # Navigation
        if key == pg.K_DOWN:
            if now - self.nav_timer > 180:
                self.selected = (self.selected + 1) % self.item_count
                self.nav_timer = now
        elif key == pg.K_UP:
            if now - self.nav_timer > 180:
                self.selected = (self.selected - 1) % self.item_count
                self.nav_timer = now

        # Adjust settings with LEFT/RIGHT
        elif key == pg.K_LEFT:
            if self.selected == 1 and now - self.adj_timer > 120:
                self.player_mode = 1
                self.adj_timer = now
            elif self.selected == 2 and now - self.adj_timer > 120:
                self.lives = max(1, self.lives - 1)
                self.adj_timer = now
            elif self.selected == 3 and now - self.adj_timer > 300:
                self.invincible = not self.invincible
                self.adj_timer = now
        elif key == pg.K_RIGHT:
            if self.selected == 1 and now - self.adj_timer > 120:
                self.player_mode = 2
                self.adj_timer = now
            elif self.selected == 2 and now - self.adj_timer > 120:
                self.lives = min(99, self.lives + 1)
                self.adj_timer = now
            elif self.selected == 3 and now - self.adj_timer > 300:
                self.invincible = not self.invincible
                self.adj_timer = now


    def reset_game_info(self):
        """Resets the game info with current settings"""
        self.game_info[c.COIN_TOTAL] = 0
        self.game_info[c.SCORE] = 0
        self.game_info[c.LIVES] = self.lives
        self.game_info['INVINCIBLE'] = self.invincible
        self.game_info['LIVES_SETTING'] = self.lives
        self.game_info['PLAYER_MODE'] = self.player_mode
        self.game_info[c.CURRENT_TIME] = 0.0
        self.game_info[c.LEVEL_STATE] = None
        self.game_info[c.CAMERA_START_X] = 0
        self.game_info[c.MARIO_DEAD] = False
        self.persist = self.game_info


    def update(self, surface, keys, current_time):
        """Updates the state every refresh"""
        self.current_time = current_time
        self.game_info[c.CURRENT_TIME] = self.current_time
        self.overhead_info.update(self.game_info)

        # Handle held keys for continuous adjustment
        now = self.current_time
        if self.selected == 1 and keys[pg.K_LEFT] and now - self.adj_timer > 80:
            self.player_mode = 1
            self.adj_timer = now
        elif self.selected == 1 and keys[pg.K_RIGHT] and now - self.adj_timer > 80:
            self.player_mode = 2
            self.adj_timer = now
        elif self.selected == 2 and keys[pg.K_LEFT] and now - self.adj_timer > 80:
            self.lives = max(1, self.lives - 1)
            self.adj_timer = now
        elif self.selected == 2 and keys[pg.K_RIGHT] and now - self.adj_timer > 80:
            self.lives = min(99, self.lives + 1)
            self.adj_timer = now

        # Update cursor position - vertical layout starting at y=280, gap=45
        start_y = 280
        item_gap = 45
        self.cursor.rect.y = start_y + self.selected * item_gap

        # Draw everything
        surface.blit(self.background, self.viewport, self.viewport)
        surface.blit(self.image_dict['GAME_NAME_BOX'][0],
                     self.image_dict['GAME_NAME_BOX'][1])
        surface.blit(self.mario.image, self.mario.rect)
        surface.blit(self.cursor.image, self.cursor.rect)
        self.overhead_info.draw(surface)

        # Render menu
        self.render_menu(surface)


    def render_menu(self, surface):
        """Render menu items with settings - vertical layout"""
        center_x = c.SCREEN_WIDTH // 2
        left_x = 280
        start_y = 280
        item_gap = 45

        # Item 0: PLAYER 1
        y0 = start_y
        color0 = c.GOLD if self.selected == 0 else c.WHITE
        text0 = self.font_item.render('PLAYER 1', True, color0)
        rect0 = text0.get_rect(midleft=(left_x, y0))
        surface.blit(text0, rect0)
        if self.selected == 0:
            arr_l = self.font_arrow.render('<', True, c.GOLD)
            arr_r = self.font_arrow.render('>', True, c.GOLD)
        else:
            arr_l = self.font_arrow.render('<', True, c.GRAY)
            arr_r = self.font_arrow.render('>', True, c.GRAY)
        surface.blit(arr_l, arr_l.get_rect(midright=(left_x - 20, y0)))
        surface.blit(arr_r, arr_r.get_rect(midleft=(left_x + rect0.width + 15, y0)))

        # Item 1: PLAYER 2
        y1 = start_y + item_gap
        color1 = c.GOLD if self.selected == 1 else c.WHITE
        player_text = '1 PLAYER' if self.player_mode == 1 else '2 PLAYER'
        text1 = self.font_item.render(player_text, True, color1)
        rect1 = text1.get_rect(midleft=(left_x, y1))
        surface.blit(text1, rect1)
        if self.selected == 1:
            arr_l = self.font_arrow.render('<', True, c.GOLD)
            arr_r = self.font_arrow.render('>', True, c.GOLD)
        else:
            arr_l = self.font_arrow.render('<', True, c.GRAY)
            arr_r = self.font_arrow.render('>', True, c.GRAY)
        surface.blit(arr_l, arr_l.get_rect(midright=(left_x - 20, y1)))
        surface.blit(arr_r, arr_r.get_rect(midleft=(left_x + rect1.width + 15, y1)))

        # Item 2: LIVES
        y2 = start_y + item_gap * 2
        color2 = c.GOLD if self.selected == 2 else c.WHITE
        lbl2 = self.font_item.render('LIVES', True, color2)
        surface.blit(lbl2, lbl2.get_rect(midleft=(left_x, y2)))
        val2 = self.font_item.render(str(self.lives), True, color2)
        surface.blit(val2, val2.get_rect(midleft=(left_x + 120, y2)))
        if self.selected == 2:
            arr_l2 = self.font_arrow.render('<', True, c.GOLD)
            arr_r2 = self.font_arrow.render('>', True, c.GOLD)
        else:
            arr_l2 = self.font_arrow.render('<', True, c.GRAY)
            arr_r2 = self.font_arrow.render('>', True, c.GRAY)
        surface.blit(arr_l2, arr_l2.get_rect(midright=(left_x + 90, y2)))
        surface.blit(arr_r2, arr_r2.get_rect(midleft=(left_x + 150, y2)))

        # Item 3: INVINCIBLE
        y3 = start_y + item_gap * 3
        color3 = c.GOLD if self.selected == 3 else c.WHITE
        lbl3 = self.font_item.render('INVINCIBLE', True, color3)
        surface.blit(lbl3, lbl3.get_rect(midleft=(left_x, y3)))
        inv_str = 'ON' if self.invincible else 'OFF'
        inv_color = c.GREEN if self.invincible else c.RED
        val3 = self.font_item.render(inv_str, True, inv_color)
        surface.blit(val3, val3.get_rect(midleft=(left_x + 170, y3)))
        if self.selected == 3:
            arr_l3 = self.font_arrow.render('<', True, c.GOLD)
            arr_r3 = self.font_arrow.render('>', True, c.GOLD)
        else:
            arr_l3 = self.font_arrow.render('<', True, c.GRAY)
            arr_r3 = self.font_arrow.render('>', True, c.GRAY)
        surface.blit(arr_l3, arr_l3.get_rect(midright=(left_x + 150, y3)))
        surface.blit(arr_r3, arr_r3.get_rect(midleft=(left_x + 220, y3)))
