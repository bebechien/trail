"""This module defines game related classes"""

import abc
import random
import datetime
import json
import const


class IGameAI(metaclass=abc.ABCMeta):
    """Interface Class representing a game AI"""
    app = None
    name = "IGameAI"

    def __init__(self, app, name):
        self.app = app
        self.name = name

    def get_name(self):
        """Returns the name of AI"""
        return self.name

    @abc.abstractmethod
    def random_event(self):
        """Function generating a random event"""
        raise NotImplementedError


class IGameUI(metaclass=abc.ABCMeta):
    """Interface Class representing a game UI"""
    supply = const.GAME_DEFAULT_SUPPLY
    ly_traveled = 0
    current_date = const.GAME_DEFAULT_START_DATE
    party = []
    ai = None
    lang = "en"
    debug = False
    msg_json = {}
    game_cleared = False
    gameover_result = "Unknown"

    def __init__(self, lang="en", debug=False):
        """Sets initial game values."""
        self.lang = lang
        self.debug = debug
        self.load_text_res()

    def load_text_res(self):
        with open(f"locale/{self.lang}.json", "r", encoding="utf-8") as f:
            self.msg_json = json.load(f)

    def reset_game(self):
        """Reset in-game values"""
        self.supply = const.GAME_DEFAULT_SUPPLY
        self.ly_traveled = 0
        self.current_date = const.GAME_DEFAULT_START_DATE
        self.party = []
        self.game_cleared = False
        self.gameover_result = "Unknown"

    def set_game_ai(self, ai):
        """Sets a game AI module"""
        self.ai = ai
        if self.debug:
            self.display_debug_info()

    def travel(self):
        """Handles the 'travel' action."""
        days_traveled = random.randint(3, 7)
        lys = random.randint(1, 4) * const.GAME_DEFAULT_TRAVEL_SPEED
        # Consume supply based on party size
        self.supply -= days_traveled * \
            const.GAME_DEFAULT_CONSUME_TRAVEL * len(self.party)
        for member in self.party:
            # Potential individual health decrease
            member["health"] -= random.randint(0,
                                               const.GAME_DEFAULT_HEALTH_MAX // 5)
        self.ly_traveled += lys
        self.current_date += datetime.timedelta(days=days_traveled)
        self.display_travel_result(lys, days_traveled)

    def rest(self):
        """Handles the 'rest' action."""
        days_rested = random.randint(2, 5)
        # Consume supply based on party size
        self.supply -= days_rested * \
            const.GAME_DEFAULT_CONSUME_REST * len(self.party)
        for member in self.party:
            # Increase health, but not beyond the maximum
            member["health"] = min(
                const.GAME_DEFAULT_HEALTH_MAX, member["health"] + 1)
        self.current_date += datetime.timedelta(days=days_rested)
        self.display_rest_result(days_rested)

    def search(self):
        """Handles the 'search' action."""
        days_searching = random.randint(2, 5)
        # Increase supply supply based on party size
        earned_supply = const.GAME_DEFAULT_SUPPLY_SEARCH * len(self.party)
        self.supply += earned_supply
        for member in self.party:
            # Potential individual health decrease
            member["health"] -= random.randint(0, 1)
        self.current_date += datetime.timedelta(days=days_searching)
        self.display_search_result(days_searching, earned_supply)

    def remove_dead_members(self):
        """Removes dead members from the party."""
        # Keep only members with health > 0
        self.party = [member for member in self.party if member["health"] > 0]

    def random_event(self):
        """Generate a random event"""
        # 100% chance of a random event if debug mode
        if self.debug:
            self.ai.random_event()
            return

        # 30% chance of a random event
        if random.random() < const.GAME_DEFAULT_RANDOM_EVENT:
            self.ai.random_event()

    def update_value(self, supply, health, day):
        """Update class values"""
        if supply is not None:
            self.supply += supply

        if health is not None:
            target = random.choice(self.party)
            target['health'] = min(
                const.GAME_DEFAULT_HEALTH_MAX, target['health'] + health)

        if day is not None:
            self.current_date += datetime.timedelta(days=day)

    def check_game_over(self):
        """Checks game over conditions"""
        if self.ly_traveled >= const.GAME_DESTINATION_DISTANCE:
            self.game_cleared = True
            self.gameover_result = self.msg_json['ui']['end_reached']
            return True
        elif self.supply <= 0:
            self.gameover_result = self.msg_json['ui']['end_no_supply']
            return True
        # Check if all member has 0 health
        elif all(member["health"] <= 0 for member in self.party):
            self.gameover_result = self.msg_json['ui']['end_all_died']
            return True
        elif self.current_date >= const.GAME_DEFAULT_END_DATE:
            self.gameover_result = self.msg_json['ui']['end_time_over']
            return True
        return False

    def display_debug_info(self):
        """Prints debug information"""
        print("<Game runs in DEBUG mode>")
        print(f"language: {self.lang}")
        print(f"ai module: {self.ai.get_name()}")

    def display_travel_result(self, lys, days):
        """Display travel result."""
        print(self.msg_json['ui']['info_traveled'].format(
            lys=lys, days=days))

    def display_random_event(self, desc, effect):
        """Display travel result."""
        print(self.msg_json['ui']['info_event'].format(
            desc=desc, effect=effect))

    def display_rest_result(self, days):
        """Display rest result."""
        print(self.msg_json['ui']['info_rested'].format(days=days))

    def display_search_result(self, days, supply):
        """Display search result."""
        print(self.msg_json['ui']['info_searched'].format(
            days=days, supply=supply))

    @abc.abstractmethod
    def get_party_members(self):
        """Gets the number of party member and names."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_player_choice(self):
        """Gets and validates player input."""
        raise NotImplementedError

    @abc.abstractmethod
    def quit(self):
        """Quit the game"""
        raise NotImplementedError

    @abc.abstractmethod
    def main_loop(self):
        """Main game loop"""
        raise NotImplementedError
