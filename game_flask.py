"""This module defines a game UI class implemented with Flask"""

from flask import Flask, render_template
import os
from inspect import currentframe
import const

from game import IGameUI

flask_app = Flask(__name__, template_folder='flask')

class GameUI(IGameUI):
    """Class representing a game UI implemented with Flask"""
    __GAME_TITLE__ = "The Kepler Trail"
    debug_info = ""

    def __init__(self, lang="en", debug=False):
        print(f"-> {currentframe().f_lineno}")
        super().__init__(lang, debug)

    def display_debug_info(self):
        print(f"-> {currentframe().f_lineno}")
        self.debug_info = "<Game runs in DEBUG mode>" + f"language: {self.lang}" + f"ai module: {self.ai.getName()}"

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

@flask_app.route('/')
def home():
    print(GameUI.__GAME_TITLE__)
    return render_template('index.html', title=GameUI.__GAME_TITLE__, iframe="/title", debug_info=GameUI.debug_info)

@flask_app.route('/title')
def title():
    return render_template('title.html', title=GameUI.__GAME_TITLE__)

flask_app.run(debug=debug)
