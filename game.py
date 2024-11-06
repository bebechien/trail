import random
import datetime


class IGameAI:
    app = None

    def __init__(self, app):
        self.app = app

    def random_event(self):
        pass


class GameApp:
    supply = 500
    ly_traveled = 0
    current_date = datetime.date(2345, 3, 1)  # Start on March 1st, 2345
    party = []
    ai = None

    def initialize_game(self, ai):
        """Sets initial game values."""
        self.ai = ai

        party_size = int(input("How many people are in your party? "))
        for i in range(party_size):
            name = input(f"Enter name for person {i+1}: ")
            self.party.append({"name": name, "health": 5})

    def display_status(self):
        """Displays the current game status."""
        print("\n--- Current Status ---")
        print(f"Date: {self.current_date}")
        print(f"Supply: {self.supply} units")
        print(f"Light-years Traveled: {self.ly_traveled}")
        print("\n--- Party Members ---")
        for member in self.party:
            print(f"{member['name']}: Health - {member['health']}")

    def get_player_choice(self):
        """Gets and validates player input."""
        while True:
            print("\n--- Choose an action ---")
            print("1. Travel")
            print("2. Rest")
            print("3. Search")
            print("4. Status")
            print("5. Quit")
            try:
                choice = int(input("Enter your choice (1-5): "))
                if 1 <= choice <= 5:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def travel(self):
        """Handles the 'travel' action."""
        days_traveled = random.randint(3, 7)
        lys = random.randint(5, 20)
        # Consume supply based on party size
        self.supply -= days_traveled * 5 * len(self.party)
        for member in self.party:
            # Potential individual health decrease
            member["health"] -= random.randint(0, 1)
        self.ly_traveled += lys
        self.current_date += datetime.timedelta(days=days_traveled)
        print(f"Traveled {lys} light-years in {days_traveled} days.")

    def rest(self):
        """Handles the 'rest' action."""
        days_rested = random.randint(2, 5)
        # Consume supply based on party size
        self.supply -= days_rested * 1 * len(self.party)
        for member in self.party:
            # Increase health, but not beyond the maximum
            member["health"] = min(5, member["health"] + 1)
        self.current_date += datetime.timedelta(days=days_rested)
        print(f"Rested for {days_rested} days.")

    def search(self):
        """Handles the 'search' action."""
        days_searching = random.randint(2, 5)
        # Increase supply supply based on party size
        self.supply += 100 * len(self.party)
        for member in self.party:
            # Potential individual health decrease
            member["health"] -= random.randint(0, 1)
        self.current_date += datetime.timedelta(days=days_searching)
        print(f"Searched for {days_searching} days.")

    def check_game_over(self):
        """Checks if game over conditions are met."""
        if self.ly_traveled >= 580:
            print("\nCongratulations! You reached the Kepler-186f!")
            return True
        elif self.supply <= 0:
            print("\nGame Over! You ran out of supply.")
            return True
        # Check if any member has 0 health
        elif all(member["health"] <= 0 for member in self.party):
            print("\nGame Over! All party members died.")
            return True
        elif self.current_date >= datetime.date(2345, 12, 31):
            print("\nGame Over! You didn't reach the Kepler-186f before year ends.")
            return True
        return False

    def remove_dead_members(self):
        """Removes dead members from the party."""
        # Keep only members with health > 0
        self.party = [member for member in self.party if member["health"] > 0]
        if not self.party:  # If the party is empty
            print("\nGame Over! All party members died.")
            return True
        return False

    def random_event(self):
        self.ai.random_event()

    def update_value(self, supply, health, day):
        if supply is not None:
            self.supply += supply

        if health is not None:
            target = random.choice(self.party)
            target['health'] = min(5, target['health'] + health)

        if day is not None:
            self.current_date += datetime.timedelta(days=day)
