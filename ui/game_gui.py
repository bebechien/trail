"""This module defines a game UI class implemented with Pygame"""

import abc
import pygame
import pygame_gui
from inspect import currentframe
import const

from game import IGameUI


class IGameScreen(metaclass=abc.ABCMeta):
    """Interface Class representing a game UI screen"""

    def __init__(self, game_ui):
        self.game_ui = game_ui

    def load_screen(self):
        """Loads required resources for this UI screen"""

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
        self.title_img = pygame.transform.scale(pygame.image.load(
            game_ui.__IMG_TITLE__), (game_ui.__GAME_WIDTH__, game_ui.__GAME_HEIGHT__))
        self.title_txt = pygame.font.SysFont(game_ui.__GAME_FONT__, 64).render(
            game_ui.__GAME_TITLE__, True, game_ui.__COLOR_WHITE__)

    def process_events(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.game_ui.next_screen = 1

    def draw_ui(self, surface):
        surface.blit(self.title_img, (0, 0))
        surface.blit(self.title_txt, (40, 120))


class GetPartyMember(IGameScreen):
    """Class representing a title screen UI"""

    __MAX_PARTY_SIZE__ = 4
    party_size = 1
    member_name = []

    def __init__(self, game_ui):
        super().__init__(game_ui)
        self.bg_img = pygame.transform.scale(pygame.image.load(
            game_ui.__IMG_GET_PARTY__), (game_ui.__GAME_WIDTH__, game_ui.__GAME_HEIGHT__))

        self.question_txt = pygame.font.SysFont(game_ui.__GAME_FONT__, game_ui.__DEFAULT_FONT_SIZE__).render(
            game_ui.msg_json['input']['party_number'], True, game_ui.__COLOR_WHITE__)

        for i in range(const.GAME_MAX_PARTY_NUMBER):
            self.member_name.append(pygame.font.SysFont(game_ui.__GAME_FONT__, game_ui.__DEFAULT_FONT_SIZE__).render(
                game_ui.msg_json['input']['member_name'].format(idx=i+1), True, game_ui.__COLOR_WHITE__))

    def load_screen(self):
        party_number = []
        for i in range(const.GAME_MAX_PARTY_NUMBER):
            party_number.append(str(i+1))
        self.num_of_party = pygame_gui.elements.UIDropDownMenu(party_number, '1', pygame.Rect(
            (40, 120+self.game_ui.__DEFAULT_FONT_SIZE__*2), (50, 30)), self.game_ui.manager)

    def process_events(self, event):
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.num_of_party:
                self.party_size = int(event.text)

    def draw_ui(self, surface):
        surface.blit(self.bg_img, (0, 0))
        surface.blit(self.question_txt, (40, 120))
        for i in range(self.party_size):
            surface.blit(
                self.member_name[i], (400, 120+i*self.game_ui.__DEFAULT_FONT_SIZE__*2))


class GameUI(IGameUI):
    """Class representing a game UI implemented with Pygame"""
    __GAME_TITLE__ = "The Kepler Trail"
    __GAME_FONT__ = "malgungothic"
    __GAME_WIDTH__ = 1280
    __GAME_HEIGHT__ = 720
    __COLOR_WHITE__ = (255, 255, 255)
    __DEFAULT_FONT_SIZE__ = 18

    __IMG_TITLE__ = "ui/static/title.jpg"
    __IMG_GET_PARTY__ = "ui/static/get_party.jpg"

    debug_info = None
    game_screen = []
    next_screen = 0
    is_running = False

    def __init__(self, lang="en", debug=False):
        super().__init__(lang, debug)
        pygame.init()
        pygame.font.init()
        # print(pygame.font.get_fonts())
        if lang=="ja":
            self.__GAME_FONT__ = "meiryo"

        pygame.display.set_caption(self.__GAME_TITLE__)
        self.window_surface = pygame.display.set_mode(
            (self.__GAME_WIDTH__, self.__GAME_HEIGHT__))
        self.background = pygame.Surface(
            (self.__GAME_WIDTH__, self.__GAME_HEIGHT__))
        self.background.fill(pygame.Color('#000000'))
        self.manager = pygame_gui.UIManager(
            (self.__GAME_WIDTH__, self.__GAME_HEIGHT__))
        self.clock = pygame.time.Clock()

        self.game_screen.append(TitleScreen(self))
        self.game_screen.append(GetPartyMember(self))

        self.is_running = True

    def display_debug_info(self):
        self.debug_info = pygame.font.SysFont(self.__GAME_FONT__, self.__DEFAULT_FONT_SIZE__).render(
            f"<Game runs in DEBUG mode>\nlanguage: {self.lang}\nai module: {self.ai.get_name()}\nfont: {self.__GAME_FONT__}",
            True, self.__COLOR_WHITE__
        )

    def get_party_members(self):
        # TODO
        print("get party member")

    def get_player_choice(self):
        # TODO
        return 5

    def quit(self):
        print("quit..")

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
                self.window_surface.blit(self.debug_info, (10, 10))

            self.manager.draw_ui(self.window_surface)

            if (self.next_screen != cur_screen_idx):
                cur_screen_idx = self.next_screen
                self.game_screen[cur_screen_idx].load_screen()

            pygame.display.update()
