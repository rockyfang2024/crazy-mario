__author__ = 'justinarmstrong'

import os
import pygame as pg
from . import constants as c

keybinding = {
    'action':pg.K_s,
    'jump':pg.K_a,
    'jump_alt':pg.K_SPACE,
    'jump_up':pg.K_UP,
    'left':pg.K_LEFT,
    'right':pg.K_RIGHT,
    'down':pg.K_DOWN
}

class Control(object):
    """Control class for entire project. Contains the game loop, and contains
    the event_loop which passes events to States as needed. Logic for flipping
    states is also found here."""
    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.done = False
        self.clock = pg.time.Clock()
        self.caption = caption
        self.fps = 60
        self.show_fps = False
        self.current_time = 0.0
        self.keys = pg.key.get_pressed()
        self.state_dict = {}
        self.state_name = None
        self.state = None
        self.paused = False
        self.paused_screen = None
        self.pause_font = pg.font.SysFont(None, 72)
        self.pause_sub_font = pg.font.SysFont(None, 32)

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self):
        self.current_time = pg.time.get_ticks()
        if self.done:
            return
        if self.paused:
            self.draw_pause_overlay()
            return
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.keys, self.current_time)

    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, persist)
        self.state.previous = previous


    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
                return
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
                # ESC to quit
                if event.key == pg.K_ESCAPE:
                    if self.paused:
                        self.paused = False
                    self.done = True
                    return
                # Enter to pause (only during gameplay)
                if event.key == pg.K_RETURN and self.state_name == c.LEVEL1:
                    if not self.paused:
                        self.paused = True
                        self.paused_screen = self.screen.copy()
                    else:
                        self.paused = False
                    return
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            if not self.paused:
                self.state.get_event(event)


    def toggle_show_fps(self, key):
        if key == pg.K_F5:
            self.show_fps = not self.show_fps
            if not self.show_fps:
                pg.display.set_caption(self.caption)


    def draw_pause_overlay(self):
        """Draw semi-transparent pause overlay"""
        if self.paused_screen:
            self.screen.blit(self.paused_screen, (0, 0))
        overlay = pg.Surface(c.SCREEN_SIZE)
        overlay.fill(c.BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        text = self.pause_font.render('PAUSED', True, c.WHITE)
        rect = text.get_rect(center=(c.SCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(text, rect)

        sub = self.pause_sub_font.render('Press ENTER to resume, ESC to quit', True, c.GRAY)
        sub_rect = sub.get_rect(center=(c.SCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(sub, sub_rect)


    def main(self):
        """Main loop for entire program"""
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)
            if self.show_fps:
                fps = self.clock.get_fps()
                with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
                pg.display.set_caption(with_fps)


class _State(object):
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}

    def get_event(self, event):
        pass

    def startup(self, current_time, persistant):
        self.persist = persistant
        self.start_time = current_time

    def cleanup(self):
        self.done = False
        return self.persist

    def update(self, surface, keys, current_time):
        pass



def load_all_gfx(directory, colorkey=(255,0,255), accept=('.png', 'jpg', 'bmp')):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name]=img
    return graphics


def load_all_music(directory, accept=('.wav', '.mp3', '.ogg', '.mdi')):
    songs = {}
    for song in os.listdir(directory):
        name,ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs


def load_all_fonts(directory, accept=('.ttf')):
    return load_all_music(directory, accept)


def load_all_sfx(directory, accept=('.wav','.mpe','.ogg','.mdi')):
    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx))
    return effects
