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
    is_party_loaded = False
    aciton_result = None
    event_result = None

    def __init__(self, lang="en", debug=False):
        super().__init__(lang, debug)
        self.app = Flask(__name__, template_folder='flask')

    def display_debug_info(self):
        self.debug_info = f"<pre>&lt;Game runs in DEBUG mode&gt;\nlanguage: {self.lang}\nai module: {self.ai.getName()}</pre>"

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
        for i in range(self.party_size):
            name = request.form[f"name_{i+1}"]
            self.party.append(
                {"name": name, "health": const.GAME_DEFAULT_HEALTH_MAX})

    def get_player_choice(self):
        choice = 4
        if 'action' in request.form:
            choice = request.form['action']
        return int(choice)

    def quit(self):
        print("quit..")

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
            self.is_party_loaded = False
            self.reset_game()
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
            if not self.is_party_loaded:
                self.is_party_loaded = True
                self.get_party_members()

            self.action_result = None
            self.event_result = None
            choice = self.get_player_choice()
            if choice == 1:
                self.travel()
                self.random_event()
            elif choice == 2:
                self.rest()
            elif choice == 3:
                self.search()
            elif choice == 5:
                self.quit()
                return render_template('quit.html',
                                       lang=self.lang,
                                       title=self.__GAME_TITLE__,
                                       debug_info=self.debug_info,
                                       msg=self.msg_json['ui']['info_quit']
                                       )

            self.remove_dead_members()
            if self.check_game_over():
                return render_template('game_over.html',
                                       lang=self.lang,
                                       title=self.__GAME_TITLE__,
                                       debug_info=self.debug_info,
                                       act_result=self.action_result,
                                       evt_result=self.event_result,
                                       result=self.gameover_result
                                       )

            status_txt = f"{self.msg_json['ui']['date']}: {self.current_date} | {self.msg_json['ui']['supply']}: {self.supply} {self.msg_json['ui']['supply_unit']} | {self.msg_json['ui']['traveled']}: {self.ly_traveled} {self.msg_json['ui']['traveled_unit']}"

            percent = f"{(100*(self.ly_traveled/float(const.GAME_DESTINATION_DISTANCE))):.1f}"
            progress_txt = f"<label for='prog'>{self.msg_json['ui']['progress']}:</label><progress id='prog' value='{percent}' max='100'> {percent}% </progress> {percent}&percnt; {self.msg_json['ui']['complete']}</progress>"

            act_list = [
                self.msg_json['ui']['act_travel'],
                self.msg_json['ui']['act_rest'],
                self.msg_json['ui']['act_search'],
                self.msg_json['ui']['act_status'],
                self.msg_json['ui']['act_quit']
            ]

            print(f"mumu - {self.action_result}")
            print(f"haha - {self.event_result}")

            return render_template('game_screen.html',
                                   lang=self.lang,
                                   title=self.__GAME_TITLE__,
                                   debug_info=self.debug_info,
                                   status_title=self.msg_json['ui']['status'],
                                   status_txt=status_txt,
                                   progress_txt=progress_txt,
                                   party_title=self.msg_json['ui']['party'],
                                   health_txt=self.msg_json['ui']['health'],
                                   party=self.party,
                                   act_title=self.msg_json['ui']['choose_action'],
                                   act_list=act_list,
                                   act_txt=self.msg_json['input']['choose_action'],
                                   act_result=self.action_result,
                                   evt_result=self.event_result
                                   )

        self.app.run(debug=self.debug)
