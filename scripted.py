import random
import datetime

from game import IGameAI


class GameAI(IGameAI):
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
        print(f"\nEvent: {event['text']}")
        # Execute the effect of the event
        effect = event['effect']
        self.app.update_value(effect.get('supply', None), effect.get(
            'health', None), effect.get('day', None))
