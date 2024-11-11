"""This module defines a game UI class implemented with Terminal"""

import const

from game import IGameUI


class GameUI(IGameUI):
    """Class representing a game UI implemented with Terminal"""

    def display_debug_info(self):
        print("<Game runs in DEBUG mode>")
        print(f"language: {self.lang}")
        print(f"ai module: {self.ai.getName()}")

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
        print(f"\n--- {self.msg_json['ui']['status']} ---")
        print(
            f"{self.msg_json['ui']['date']}: {self.current_date} | {self.msg_json['ui']['supply']}: {self.supply} {self.msg_json['ui']['supply_unit']} | {self.msg_json['ui']['traveled']}: {self.ly_traveled} {self.msg_json['ui']['traveled_unit']}")
        self.print_travel_progress()
        print(f"--- {self.msg_json['ui']['party']} ---")
        for member in self.party:
            print(
                f"{member['name']}: {self.msg_json['ui']['health']} - {member['health']}")

    def display_travel_result(self, lys, days):
        print(self.msg_json['ui']['info_traveled'].format(
            lys=lys, days=days))

    def display_rest_result(self, days):
        print(self.msg_json['ui']['info_rested'].format(days=days))

    def display_search_result(self, days, supply):
        print(self.msg_json['ui']['info_searched'].format(
            days=days, supply=supply))

    def get_party_members(self):
        party_size = int(input(self.msg_json['input']['party_number']))
        for i in range(party_size):
            name = input(self.msg_json['input']['member_name'].format(idx=i+1))
            self.party.append(
                {"name": name, "health": const.GAME_DEFAULT_HEALTH_MAX})

    def get_player_choice(self):
        while True:
            print(f"--- {self.msg_json['ui']['choose_action']} ---")
            print(f"1. {self.msg_json['ui']['act_travel']} | 2. {self.msg_json['ui']['act_rest']} | 3. {self.msg_json['ui']['act_search']} | 4. {self.msg_json['ui']['act_status']} | 5. {self.msg_json['ui']['act_quit']}")
            try:
                choice = int(
                    input(f"{self.msg_json['input']['choose_action']}"))
                if 1 <= choice <= 5:
                    return choice
                else:
                    print(f"{self.msg_json['err']['invalid_choice']}")
            except ValueError:
                print(f"{self.msg_json['err']['invalid_input']}")

    def check_game_over(self):
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

    def quit(self):
        print(self.msg_json['ui']['info_quit'])

    def main_loop(self):
        self.get_party_members()
        while True:
            self.display_status()
            choice = self.get_player_choice()
            if choice == 1:
                self.travel()
                self.random_event()
            elif choice == 2:
                self.rest()
            elif choice == 3:
                self.search()
            elif choice == 4:
                pass  # Already displayed status at the beginning of the loop
            elif choice == 5:
                self.quit()
                break
            
            self.remove_dead_members()  # Remove dead members after traveling
            if self.check_game_over():
                break
