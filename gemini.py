"""This module defines a game AI class implemented with Gemini"""

import os
import json
import jsonschema
import google.generativeai as genai
import const

from game import IGameAI


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
            event_string = self.model.generate_content(const.EVENT_GENERATION_PROMPT + repr(
                const.EVENT_JSON_SCHEMA)).text.removeprefix("```json").split("```")[0]
            try:
                event = json.loads(event_string)
                try:
                    jsonschema.validate(
                        instance=event, schema=const.EVENT_JSON_SCHEMA)
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
        event = self.generate_event()
        print(f"\nEvent: {event['text']}\n `-> Effect: {event['effect']}")
        # Execute the effect of the event
        effect = event['effect']
        self.app.update_value(effect.get('supply', None), effect.get(
            'health', None), effect.get('day', None))
