"""This module defines a game AI class implemented with ollama"""

import os
import json
import jsonschema
import const

from game import IGameAI


class GameAI(IGameAI):
    """Class representing a game AI implemented with ollama"""
    __model_name__ = "gemma2:2b"
    __temp_filename__ = "/tmp/ollama_output.txt"
    __START_TURN_USER__ = "<start_of_turn>user\n"
    __START_TURN_MODEL__ = "<start_of_turn>model\n"
    __END_TURN__ = "<end_of_turn>\n"
    __MAX_NUM_OF_TRY__ = 3

    event_example = const.EVENT_JSON_EXAMPLE_STR

    def __init__(self, app):
        super().__init__(app, f"{self.__model_name__} with Ollama")

    def generate_event(self):
        """Generate and validate event."""
        num_of_try = 0
        prompt = const.EVENT_GENERATION_PROMPT.format(lang="")
        if self.app.lang == "ko":
            prompt = const.EVENT_GENERATION_PROMPT.format(lang=" in Korean")
            self.event_example = const.EVENT_JSON_EXAMPLE_STR_KO
        elif self.app.lang == "ja":
            prompt = const.EVENT_GENERATION_PROMPT.format(lang=" in Japanese")
            self.event_example = const.EVENT_JSON_EXAMPLE_STR_JA

        chat_prompt = f"{self.__START_TURN_USER__}{prompt}\nBelow is an example.\n{self.event_example}\nNo explanation required.{self.__END_TURN__}{self.__START_TURN_MODEL__}"
        while True:
            response = os.popen(
                f"ollama run {self.__model_name__} \"{chat_prompt}\" > {self.__temp_filename__};cat {self.__temp_filename__}").read()
            event_string = response.replace(chat_prompt, "").removeprefix("```json").removesuffix(
                "<end_of_turn>").split("```")[0]  # Extract only the new response
            try:
                event = json.loads(event_string)

                # fix common issues
                if "supply" in event['effect']:
                    event['effect']['supply'] = int(event['effect']['supply'])
                if "health" in event['effect']:
                    event['effect']['health'] = int(event['effect']['health'])
                if "day" in event['effect']:
                    event['effect']['day'] = int(event['effect']['day'])

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
                    return json.loads(self.event_example)
                print(f"Try again ({num_of_try}/{self.__MAX_NUM_OF_TRY__})")

    def random_event(self):
        event = self.generate_event()
        self.app.display_random_event(desc=event['text'], effect=event['effect'])

        # Execute the effect of the event
        effect = event['effect']
        self.app.update_value(effect.get('supply', None), effect.get(
            'health', None), effect.get('day', None))
