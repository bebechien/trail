import os
import json
import jsonschema
import google.generativeai as genai

from game import IGameAI

__system_prompt__ = "You are in-game AI for \"The Kepler Trail\", the game inspired by \"The Oregon Trail\" but traveling in space."
__event_json_schema__ = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "effect": {
            "type": "object",
            "properties": {
                "supply": {"type": "integer"},
                "health": {"type": "integer", "minimum": -2, "maximum": 2},
                "day": {"type": "integer", "minimum": 0, "maximum": 2},
            }
        }
    }
}


class GameAI(IGameAI):
    """Class representing a game AI implemented with Gemini"""
    model = None

    def __init__(self, app):
        super().__init__(app)
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_event(self):
        """Generate and validate event."""
        while True:
            event_string = self.model.generate_content(__system_prompt__ + "\nWrite a random event in json format, follow the schema below. The event may affect supply, a party member's health or time.\n" +
                                                       repr(__event_json_schema__)).text.removeprefix("```json").split("```")[0]
            try:
                event = json.loads(event_string)
                try:
                    jsonschema.validate(
                        instance=event, schema=__event_json_schema__)
                    return event
                except jsonschema.exceptions.ValidationError:
                    print(event_string)
                    print("-"*80)
                    print("Invalid format. Try again")

            except json.decoder.JSONDecodeError:
                print(event_string)
                print("-"*80)
                print("Invalid format. Try again")

    def random_event(self):
        """Triggers a random event."""
        event = self.generate_event()

        print(f"\nEvent: {event['text']}")
        print(f"\nEffect: {event['effect']}")
        # Execute the effect of the event
        effect = event['effect']
        self.app.update_value(effect.get('supply', None), effect.get(
            'health', None), effect.get('day', None))
