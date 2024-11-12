"""This module defines a game UI class implemented with Pygame"""

import abc
import pygame
from pygame.locals import *
import pygame_gui
from inspect import currentframe
import const

from game import IGameUI

class IGameScreen(metaclass=abc.ABCMeta):
    """Interface Class representing a game UI screen"""

    def __init__(self, game_ui):
        self.game_ui = game_ui

    @abc.abstractmethod
    def process_events(self, event):
        """Handles events"""
        raise NotImplementedError

    @abc.abstractmethod
    def draw_ui(self, surface):
        """Draws UI elements"""
        raise NotImplementedError


class TitleScreen(IGameScreen):
    """Class representing a title screen UI"""

    def __init__(self, game_ui):
        super().__init__(game_ui)
        self.title_img = pygame.transform.scale(pygame.image.load("static/title.jpg"), (self.game_ui.__GAME_WIDTH__, self.game_ui.__GAME_HEIGHT__))
        self.title_txt = pygame.font.SysFont("", 64).render(self.game_ui.__GAME_TITLE__, True, self.game_ui.__COLOR_WHITE__)

    def process_events(self, event):
        if event.type == MOUSEBUTTONUP:
            print(event)
            if event.button == 1:
                self.game_ui.next_screen = 1            

    def draw_ui(self, window_surface):
        window_surface.blit(self.title_img, (0, 0))
        window_surface.blit(self.title_txt, (40, 100))


class GetPartyMember(IGameScreen):
    """Class representing a title screen UI"""

    def __init__(self, game_ui):
        super().__init__(game_ui)
        self.question_txt = pygame.font.SysFont("", 64).render(self.game_ui.msg_json['input']['party_number'], True, self.game_ui.__COLOR_WHITE__)
        self.text_entry = pygame_gui.elements.UITextEntryLine(pygame.Rect((40, 200), (200, -1)), self.game_ui.manager, container=self)
        self.text_entry.set_allowed_characters('numbers')

    def process_events(self, event):
        pass

    def draw_ui(self, window_surface):
        window_surface.blit(self.question_txt, (40, 100))


class GameUI(IGameUI):
    """Class representing a game UI implemented with Pygame"""
    __GAME_TITLE__ = "The Kepler Trail"
    __GAME_WIDTH__ = 1280
    __GAME_HEIGHT__ = 720
    __COLOR_WHITE__ = (255,255,255)
    pygame_ = None
    debug_info = None
    game_screen = []
    next_screen = 0
    is_running = False

    def __init__(self, lang="en", debug=False):
        super().__init__(lang, debug)
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("", 24)
        pygame.display.set_caption(self.__GAME_TITLE__)
        self.window_surface = pygame.display.set_mode((self.__GAME_WIDTH__, self.__GAME_HEIGHT__))
        self.background = pygame.Surface((self.__GAME_WIDTH__, self.__GAME_HEIGHT__))
        self.background.fill(pygame.Color('#000000'))
        self.manager = pygame_gui.UIManager((self.__GAME_WIDTH__, self.__GAME_HEIGHT__))
        self.clock = pygame.time.Clock()

        self.game_screen.append(TitleScreen(self))
        self.game_screen.append(GetPartyMember(self))

        self.is_running = True

    def display_debug_info(self):
        self.debug_info = self.font.render(
            f"<Game runs in DEBUG mode>\nlanguage: {self.lang}\nai module: {self.ai.getName()}",
            True, self.__COLOR_WHITE__
        )
        
    def display_status(self):
        print(f"-> {currentframe().f_lineno}")

    def display_travel_result(self, lys, days):
        print(f"-> {currentframe().f_lineno}")

    def display_rest_result(self, days):
        print(f"-> {currentframe().f_lineno}")

    def display_search_result(self, days, supply):
        print(f"-> {currentframe().f_lineno}")

    def get_party_members(self):
        print(f"-> {currentframe().f_lineno}")

    def get_player_choice(self):
        print(f"-> {currentframe().f_lineno}")
        return 5

    def check_game_over(self):
        print(f"-> {currentframe().f_lineno}")

    def quit(self):
        print(f"-> {currentframe().f_lineno}")

    def main_loop(self):
        cur_screen_idx = 0
        while self.is_running:
            time_delta = self.clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                self.manager.process_events(event)
                self.game_screen[cur_screen_idx].process_events(event)

            self.manager.update(time_delta)

            # clear screen
            self.window_surface.blit(self.background, (0, 0))

            self.game_screen[cur_screen_idx].draw_ui(self.window_surface)
            if (self.debug_info):
                self.window_surface.blit(self.debug_info, (20, 20))

            self.manager.draw_ui(self.window_surface)

            if(self.next_screen != cur_screen_idx):
                cur_screen_idx = self.next_screen

            pygame.display.update()
