"""This module defines a game UI class implemented with Gradio"""

import gradio as gr
import os
from inspect import currentframe
import const

from game import IGameUI


class GameUI(IGameUI):
    """Class representing a game UI implemented with Gradio"""
    __GAME_TITLE__ = "The Kepler Trail"
    __IMG_TITLE__ = "ui/static/title.jpg"

    __MAX_PARTY_NUMBER__ = 4

    app = None
    debug_info = ""
    party_size = 1

    action_result = None
    event_result = None

    def __init__(self, lang="en", debug=False):
        super().__init__(lang, debug)

        with gr.Blocks(title=self.__GAME_TITLE__) as self.app:
            gr.Markdown(f"# {self.__GAME_TITLE__}")
            gr.Markdown(f"![title](gradio_api/file={self.__IMG_TITLE__})")
            with gr.Row():
                inp = gr.Textbox()

    def display_debug_info(self):
        self.debug_info = f"<pre>&lt;Game runs in DEBUG mode&gt;\nlanguage: {self.lang}\nai module: {self.ai.get_name()}</pre>"

    def display_travel_result(self, lys, days):
        self.action_result = self.msg_json['ui']['info_traveled'].format(
            lys=lys, days=days)

    def display_random_event(self, desc, effect):
        self.event_result = self.msg_json['ui']['info_event'].format(
            desc=desc, effect=effect)

    def display_rest_result(self, days):
        self.action_result = self.msg_json['ui']['info_rested'].format(
            days=days)

    def display_search_result(self, days, supply):
        self.action_result = self.msg_json['ui']['info_searched'].format(
            days=days, supply=supply)

    def get_party_members(self):
        print(f"-> {currentframe().f_lineno}")

    def get_player_choice(self):
        print(f"-> {currentframe().f_lineno}")
        return 5

    def quit(self):
        print("quit..")

    def main_loop(self):
        self.app.launch(allowed_paths=["ui/static"])
