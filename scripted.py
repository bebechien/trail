"""This module defines a game AI class with a traditional script-based approach"""

import random

from game import IGameAI


class GameAI(IGameAI):
    """Class representing a game AI that uses a traditional script-based approach"""

    def __init__(self, app):
        super().__init__(app, "Traditional Script")

    def random_event(self):
        """Triggers a random event."""
        events = [
            {"text": "You find abandoned supplies! Gain 50 units of supply.",
                "effect": {"supply": 50}},
            {"text": "Lost in space! Spend a day searching.", "effect": {"day": 1}},
            {"text": "A party member gets sick. Lose some health.",
                "effect": {"health": -2}},
            {"text": "You encounter friendly travelers! Gain some health.",
                "effect": {"health": 1}},
            {"text": "Space pirate attack! You fend them off, but lose some supply and health.",
                "effect": {"supply": -20, "health": -1}}
        ]

        event = random.choice(events)
        print(self.app.msg_json['ui']['info_event'].format(desc=event['text'], effect=event['effect']))
        # Execute the effect of the event
        effect = event['effect']
        self.app.update_value(effect.get('supply', None), effect.get(
            'health', None), effect.get('day', None))
