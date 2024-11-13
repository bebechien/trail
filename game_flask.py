"""This module defines a game UI class implemented with Flask"""

from flask import Flask, render_template
import os
from inspect import currentframe
import const

from game import IGameUI


class GameUI(IGameUI):
    """Class representing a game UI implemented with Flask"""
    __GAME_TITLE__ = "The Kepler Trail"
    app = None
    debug_info = ""

    def __init__(self, lang="en", debug=False):
        super().__init__(lang, debug)
        self.app = Flask(__name__, template_folder='flask')

    def display_debug_info(self):
        self.debug_info = f"<pre>&lt;Game runs in DEBUG mode&gt;\nlanguage: {self.lang}\nai module: {self.ai.getName()}</pre>"

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
        @self.app.route('/')
        def home():
            return render_template('index.html',
                                   lang=self.lang,
                                   title=self.__GAME_TITLE__,
                                   debug_info=self.debug_info
                                   )

        @self.app.route('/get_party')
        def get_party():
            return render_template('get_party.html',
                                   lang=self.lang,
                                   title=self.__GAME_TITLE__,
                                   debug_info=self.debug_info,
                                   question=self.msg_json['input']['party_number']
                                   )

        self.app.run(debug=self.debug)
