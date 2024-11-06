import random
import datetime

def initialize_game():
    """Sets initial game values."""
    global supply, ly_traveled, current_date, party
    supply = 500
    ly_traveled = 0
    current_date = datetime.date(2345, 3, 1)  # Start on March 1st, 2345
    party = []
    party_size = int(input("How many people are in your party? "))
    for i in range(party_size):
        name = input(f"Enter name for person {i+1}: ")
        party.append({"name": name, "health": 5})


def display_status():
    """Displays the current game status."""
    print("\n--- Current Status ---")
    print(f"Date: {current_date}")
    print(f"Supply: {supply} units")
    print(f"Light-years Traveled: {ly_traveled}")
    print("\n--- Party Members ---")
    for member in party:
        print(f"{member['name']}: Health - {member['health']}")


def get_player_choice():
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


def travel():
    """Handles the 'travel' action."""
    global supply, ly_traveled, current_date, party
    days_traveled = random.randint(3, 7)
    lys = random.randint(5, 20)
    # Consume supply based on party size
    supply -= days_traveled * 5 * len(party)
    for member in party:
        # Potential individual health decrease
        member["health"] -= random.randint(0, 1)
    ly_traveled += lys
    current_date += datetime.timedelta(days=days_traveled)
    print(f"Traveled {lys} light-years in {days_traveled} days.")


def rest():
    """Handles the 'rest' action."""
    global current_date, party
    days_rested = random.randint(2, 5)
    for member in party:
        # Increase health, but not beyond the maximum
        member["health"] = min(5, member["health"] + 1)
    current_date += datetime.timedelta(days=days_rested)
    print(f"Rested for {days_rested} days.")


def search():
    """Handles the 'search' action."""
    global supply, current_date
    days_searching = random.randint(2, 5)
    supply += 100 * len(party)  # Increase supply supply based on party size
    current_date += datetime.timedelta(days=days_searching)
    print(f"Searched for {days_searching} days.")


def check_game_over():
    """Checks if game over conditions are met."""
    if ly_traveled >= 580:
        print("\nCongratulations! You reached the Kepler-186f!")
        return True
    elif supply <= 0:
        print("\nGame Over! You ran out of supply.")
        return True
    elif all(member["health"] <= 0 for member in party):  # Check if any member has 0 health
        print("\nGame Over! All party members died.")
        return True
    elif current_date >= datetime.date(2345, 12, 31):
        print("\nGame Over! You didn't reach the Kepler-186f before year ends.")
        return True
    return False


def remove_dead_members():
    """Removes dead members from the party."""
    global party
    # Keep only members with health > 0
    party = [member for member in party if member["health"] > 0]
    if not party:  # If the party is empty
        print("\nGame Over! All party members died.")
        return True
    return False


def random_event():
    """Triggers a random event."""
    global supply, party, current_date

    events = [
        {"text": "A blizzard hits! You lose 3 days and some supply.", "effect": lambda: (globals().update(
            {"supply": supply - 15, "current_date": current_date + datetime.timedelta(days=3)}))},
        {"text": "You find abandoned supplies! Gain 50 units of supply.",
            "effect": lambda: (globals().update({"supply": supply + 50}))},
        {"text": "Oxen wander off! Spend a day searching.", "effect": lambda: (
            globals().update({"current_date": current_date + datetime.timedelta(days=1)}))},
        {"text": "A party member gets sick. Lose some health.", "effect": lambda: random.choice(
            party).update({"health": max(0, random.choice(party)["health"] - 2)})},
        {"text": "You encounter friendly travelers! Gain some health.", "effect": lambda: random.choice(
            party).update({"health": min(5, random.choice(party)["health"] + 1)})},
        {"text": "Bandits attack! You fend them off, but lose some supply and health.", "effect": lambda: (globals().update(
            {"supply": supply - 20}), random.choice(party).update({"health": max(0, random.choice(party)["health"] - 1)}))}
    ]

    event = random.choice(events)
    print(f"\nEvent: {event['text']}")
    event['effect']()  # Execute the effect of the event


# Main game loop
initialize_game()
while True:
    display_status()
    choice = get_player_choice()
    if choice == 1:
        travel()
        if random.random() < 0.3:  # 30% chance of a random event after traveling
            random_event()
        if remove_dead_members():  # Remove dead members after traveling
            break
    elif choice == 2:
        rest()
    elif choice == 3:
        search()
    elif choice == 4:
        pass  # Already displayed status at the beginning of the loop
    elif choice == 5:
        print("Quitting the game.")
        break
    if check_game_over():
        break
