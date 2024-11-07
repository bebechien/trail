"""This module defines a game AI class implemented with Gemma"""

import keras_nlp
import const

from game import IGameAI


class GameAI(IGameAI):
    """Class representing a game AI implemented with Gemma"""
    __model_name__ = "gemma2_instruct_2b_en"
    __START_TURN_USER__ = "<start_of_turn>user\n"
    __START_TURN_MODEL__ = "<start_of_turn>model\n"
    __END_TURN__ = "<end_of_turn>\n"

    model = None

    def __init__(self, app):
        super().__init__(app)
        self.model = keras_nlp.models.GemmaCausalLM.from_preset(
            self.__model_name__)

    def generate_event(self):
        """Generate and validate event."""
        while True:
            event_string = self.model.generate_content(self.__START_TURN_USER__ + const.EVENT_GENERATION_PROMPT + repr(
                const.EVENT_JSON_SCHEMA) + self.__END_TURN__ + self.__START_TURN_MODEL__)
            print(event_string)

    def random_event(self):
        self.generate_event()
