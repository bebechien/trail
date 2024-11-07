"""This module defines a game AI class implemented with Gemma"""

import json
import jsonschema
import keras
import keras_nlp
import const

from game import IGameAI


# Run at half precision to save memory
keras.config.set_floatx("bfloat16")

class GameAI(IGameAI):
    """Class representing a game AI implemented with Gemma"""
    __model_name__ = "gemma2_instruct_2b_en"
    __START_TURN_USER__ = "<start_of_turn>user\n"
    __START_TURN_MODEL__ = "<start_of_turn>model\n"
    __END_TURN__ = "<end_of_turn>\n"
    __MAX_NUM_OF_TRY__ = 3

    model = None

    def __init__(self, app):
        super().__init__(app)
        self.model = keras_nlp.models.GemmaCausalLM.from_preset(
            self.__model_name__)
        self.model.compile(sampler="top_k")

    def generate_event(self):
        """Generate and validate event."""
        num_of_try = 0
        prompt = f"{self.__START_TURN_USER__}{const.EVENT_GENERATION_PROMPT}{const.EVENT_JSON_EXAMPLE_STR}\nNo explanation required.{self.__END_TURN__}{self.__START_TURN_MODEL__}"
        while True:
            response = self.model.generate(prompt, max_length=1024)
            event_string = response.replace(prompt, "").removeprefix("```json").removesuffix("<end_of_turn>").split("```")[0]  # Extract only the new response
            try:
                event = json.loads(event_string)
                jsonschema.validate(instance=event, schema=const.EVENT_JSON_SCHEMA)
                return event

            except (jsonschema.exceptions.ValidationError, json.decoder.JSONDecodeError) as e:
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
        print(f"\nEvent: {event['text']}\n `-> Effect: {event['effect']}")
        # Execute the effect of the event
        effect = event['effect']
        self.app.update_value(effect.get('supply', None), effect.get(
            'health', None), effect.get('day', None))
