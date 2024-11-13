"""This module defines a game UI class implemented with Flask"""

from flask import Flask, render_template, request
import os
from inspect import currentframe
import const

from game import IGameUI


class GameUI(IGameUI):
    """Class representing a game UI implemented with Flask"""
    __GAME_TITLE__ = "The Kepler Trail"
    __MAX_PARTY_NUMBER__ = 4
    app = None
    debug_info = ""
    party_size = 1

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

        @self.app.route('/get_party', methods=['GET', 'POST'])
        def get_party():
            if request.method == 'POST':
                self.party_size = int(request.form['party_size'])

            return render_template('get_party.html',
                                   lang=self.lang,
                                   title=self.__GAME_TITLE__,
                                   debug_info=self.debug_info,
                                   question_num=self.msg_json['input']['party_number'],
                                   question_name=self.msg_json['input']['member_name'],
                                   max_party=self.__MAX_PARTY_NUMBER__,
                                   party_size=self.party_size
                                   )

        @self.app.route('/game_screen', methods=['POST'])
        def game_screen():
            if request.method == 'POST':
                names = ""
                for i in range(self.party_size):
                    names += request.form[f"name_{i+1}"]
                return render_template('game_screen.html',
                                       lang=self.lang,
                                       title=self.__GAME_TITLE__,
                                       debug_info=self.debug_info,
                                       names=names
                                       )

        self.app.run(debug=self.debug)
