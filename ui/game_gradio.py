"""This module defines a game UI class implemented with Gradio"""

import gradio as gr
import os
from inspect import currentframe
import const

from game import IGameUI


class GameUI(IGameUI):
    """Class representing a game UI implemented with Gradio"""
    __GAME_TITLE__ = "The Kepler Trail"
    gradio_app = None

    def __init__(self, lang="en", debug=False):
        print(f"-> {currentframe().f_lineno}")
        print(os.getcwd())
        super().__init__(lang, debug)

        with gr.Blocks(title=self.__GAME_TITLE__) as self.gradio_app:
            gr.Markdown(f"# {self.__GAME_TITLE__}")
            gr.Markdown("![title](gradio_api/file=static/title.jpg)")
            with gr.Row():
                inp = gr.Textbox()

    def display_debug_info(self):
        print(f"-> {currentframe().f_lineno}")
        self.gradio_app.launch(allowed_paths=["static"])

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
