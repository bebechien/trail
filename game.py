"""This module defines game related classes"""

import random
import datetime
import json
import const


class IGameAI:
    """Interface Class representing a game AI"""
    app = None

    def __init__(self, app):
        self.app = app

    def random_event(self):
        """Function generating a random event"""


class GameApp:
    """Class representing a game application"""
    supply = const.GAME_DEFAULT_SUPPLY
    ly_traveled = 0
    current_date = const.GAME_DEFAULT_START_DATE
    party = []
    ai = None
    lang = "en"
    msg_json = {}

    def initialize_game(self, ai, lang="en"):
        """Sets initial game values."""
        self.ai = ai
        self.lang = lang
        with open(f"locale/{lang}.json", "r", encoding="utf-8") as f:
            self.msg_json = json.load(f)

        party_size = int(input(self.msg_json['input']['party_number']))
        for i in range(party_size):
            name = input(self.msg_json['input']['member_name'].format(idx=i+1))
            self.party.append(
                {"name": name, "health": const.GAME_DEFAULT_HEALTH_MAX})

    def print_travel_progress(self):
        """Prints travel progress bar"""
        percent = f"{(100*(self.ly_traveled/float(const.GAME_DESTINATION_DISTANCE))):.1f}"
        filled_length = int(const.GAME_UI_PROGRESS_BAR_LENGTH * self.ly_traveled //
                            const.GAME_DESTINATION_DISTANCE)
        prog_bar = "█" * filled_length + "-" * \
            (const.GAME_UI_PROGRESS_BAR_LENGTH - filled_length)
        print(
            f"{self.msg_json['ui']['progress']}: |{prog_bar}| {percent}% {self.msg_json['ui']['complete']}")

    def display_status(self):
        """Displays the current game status."""
        print(f"\n--- {self.msg_json['ui']['status']} ---")
        print(
            f"{self.msg_json['ui']['date']}: {self.current_date} | {self.msg_json['ui']['supply']}: {self.supply} {self.msg_json['ui']['supply_unit']} | {self.msg_json['ui']['traveled']}: {self.ly_traveled} {self.msg_json['ui']['traveled_unit']}")
        self.print_travel_progress()
        print(f"--- {self.msg_json['ui']['party']} ---")
        for member in self.party:
            print(
                f"{member['name']}: {self.msg_json['ui']['health']} - {member['health']}")

    def get_player_choice(self):
        """Gets and validates player input."""
        while True:
            print(f"--- {self.msg_json['ui']['choose_action']} ---")
            print(f"1. {self.msg_json['ui']['act_travel']} | 2. {self.msg_json['ui']['act_rest']} | 3. {self.msg_json['ui']['act_search']} | 4. {self.msg_json['ui']['act_status']} | 5. {self.msg_json['ui']['act_quit']}")
            try:
                choice = int(input(f"{self.msg_json['input']['choose_action']}"))
                if 1 <= choice <= 5:
                    return choice
                else:
                    print(f"{self.msg_json['err']['invalid_choice']}")
            except ValueError:
                print(f"{self.msg_json['err']['invalid_input']}")

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
                                               const.GAME_DEFAULT_HEALTH_MAX / 5)
        self.ly_traveled += lys
        self.current_date += datetime.timedelta(days=days_traveled)
        print(self.msg_json['ui']['info_traveled'].format(lys=lys, days=days_traveled))

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
        print(self.msg_json['ui']['info_rested'].format(days=days_rested))

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
        print(self.msg_json['ui']['info_searched'].format(days=days_searching, supply=earned_supply))

    def check_game_over(self):
        """Checks if game over conditions are met."""
        if self.ly_traveled >= const.GAME_DESTINATION_DISTANCE:
            print(self.msg_json['ui']['end_reached'])
            return True
        elif self.supply <= 0:
            print(self.msg_json['ui']['end_no_supply'])
            return True
        # Check if all member has 0 health
        elif all(member["health"] <= 0 for member in self.party):
            print(self.msg_json['ui']['end_all_died'])
            return True
        elif self.current_date >= const.GAME_DEFAULT_END_DATE:
            print(self.msg_json['ui']['end_time_over'])
            return True
        return False

    def remove_dead_members(self):
        """Removes dead members from the party."""
        # Keep only members with health > 0
        self.party = [member for member in self.party if member["health"] > 0]

    def random_event(self):
        """Generate a random event"""
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

    def quit(self):
        print(self.msg_json['ui']['info_quit'])
