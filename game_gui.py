"""This module defines a game UI class implemented with Pygame"""

import pygame
import pygame_gui
from inspect import currentframe
import const

from game import IGameUI


class GameUI(IGameUI):
    """Class representing a game UI implemented with Pygame"""
    __GAME_TITLE__ = "The Kepler Trail"
    pygame_ = None
    debug_info = None
    is_running = False

    def __init__(self, lang="en", debug=False):
        super().__init__(lang, debug)
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("", 24)
        pygame.display.set_caption(self.__GAME_TITLE__)
        self.window_surface = pygame.display.set_mode((1280, 720))
        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('#000000'))
        self.manager = pygame_gui.UIManager((800, 600))
        self.hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                                         text='Say Hello',
                                                         manager=self.manager)
        self.clock = pygame.time.Clock()
        self.is_running = True

    def display_debug_info(self):
        self.debug_info = self.font.render(
            f"<Game runs in DEBUG mode>\nlanguage: {self.lang}\nai module: {self.ai.getName()}",
            True, (255, 255, 255)
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
        while self.is_running:
            time_delta = self.clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.hello_button:
                        print('Hello World!')

            self.manager.process_events(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            if (self.debug_info):
                self.window_surface.blit(self.debug_info, (20, 20))

            self.manager.draw_ui(self.window_surface)

            pygame.display.update()
