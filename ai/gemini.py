"""This module defines a game AI class implemented with Gemini"""

import os
import json
import jsonschema
import google.generativeai as genai
import const

from game import IGameAI


class GameAI(IGameAI):
    """Class representing a game AI implemented with Gemini"""
    __model_name__ = "gemini-1.5-flash"
    __MAX_NUM_OF_TRY__ = 3

    model = None

    def __init__(self, app):
        super().__init__(app, self.__model_name__)
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel(self.__model_name__)

    def generate_event(self):
        """Generate and validate event."""
        num_of_try = 0
        prompt = const.EVENT_GENERATION_PROMPT.format(lang="")
        if self.app.lang == "ko":
            prompt = const.EVENT_GENERATION_PROMPT.format(lang=" in Korean")
        elif self.app.lang == "ja":
            prompt = const.EVENT_GENERATION_PROMPT.format(lang=" in Japanese")

        while True:
            try:
                event_string = self.model.generate_content(prompt + " Follow the schema below.\n" + repr(
                    const.EVENT_JSON_SCHEMA)).text.removeprefix("```json").split("```")[0]
                event = json.loads(event_string)
                jsonschema.validate(
                    instance=event, schema=const.EVENT_JSON_SCHEMA)
                return event

            except (KeyError, jsonschema.exceptions.ValidationError, json.decoder.JSONDecodeError) as e:
                print(e)
                print(event_string)
                print("-"*80)
                num_of_try += 1
                if num_of_try > self.__MAX_NUM_OF_TRY__:
                    print("Too many failure. Use example json instead.")
                    return json.loads(const.EVENT_JSON_EXAMPLE_STR)
                print(f"Try again ({num_of_try}/{self.__MAX_NUM_OF_TRY__})")

    def random_event(self):
        event = self.generate_event()
        self.app.display_random_event(desc=event['text'], effect=event['effect'])

        # Execute the effect of the event
        effect = event['effect']
        self.app.update_value(effect.get('supply', None), effect.get(
            'health', None), effect.get('day', None))
