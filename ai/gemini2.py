"""This module defines a game AI class implemented with Gemini"""

import os
import json
import jsonschema
from google import genai
from google.genai import types
import const
import base64
import tempfile
import wave

from game import IGameAI


class GameAI(IGameAI):
    """Class representing a game AI implemented with Gemini"""
    __model_name__ = "gemini-2.0-flash-exp"
    __MAX_NUM_OF_TRY__ = 3

    client = None

    def __init__(self, app):
        super().__init__(app, f"{self.__model_name__}")
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

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
                event_string = self.client.models.generate_content(
                    model=self.__model_name__,
                    contents=prompt + " Follow the schema below.\n" + repr(
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
        self.app.display_random_event(
            desc=event['text'], effect=event['effect'])
        
        num_of_try = 0
        while True:
            result = self.generate_image(event['text'])
            if result is True:
                break
            num_of_try += 1
            if num_of_try > self.__MAX_NUM_OF_TRY__:
                print("Too many failure on generating image.")
                break

            print(f"Try again (image) ({num_of_try}/{self.__MAX_NUM_OF_TRY__})")

        num_of_try = 0
        while True:
            result = self.generate_audio(event['text'])
            if result is True:
                break
            num_of_try += 1
            if num_of_try > self.__MAX_NUM_OF_TRY__:
                print("Too many failure on generating audio.")
                break

            print(f"Try again (audio) ({num_of_try}/{self.__MAX_NUM_OF_TRY__})")

        # Execute the effect of the event
        effect = event['effect']
        self.app.update_value(effect.get('supply', None), effect.get(
            'health', None), effect.get('day', None))

    def generate_image(self, description):
        response = self.client.models.generate_content(
            model=self.__model_name__,
            contents="Draw an image, "+description,
            config=types.GenerateContentConfig(response_modalities=['Text', 'Image']))
        if response.candidates[0].content is not None:
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    continue
                elif part.inline_data is not None:
                    self.app.random_event_img = "data:" + part.inline_data.mime_type + \
                        ";base64," + \
                        base64.b64encode(part.inline_data.data).decode('ascii')
                    return True
        
        return False

    def generate_audio(self, description):
        response = self.client.models.generate_content(
            model=self.__model_name__,
            contents="Read the following like a video game narrator. \"" +
            description + "\"",
            config=types.GenerateContentConfig(response_modalities=['Audio'])
        )
        if response.candidates[0].content is not None:
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    continue
                elif part.inline_data is not None:
                    tmp_aud = os.path.join(
                        tempfile._get_default_tempdir(), "temp.wav")
                    rate = int(part.inline_data.mime_type.split('rate=')[-1])
                    with wave.open(tmp_aud, "wb") as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(2)
                        wf.setframerate(rate)
                        wf.writeframes(part.inline_data.data)
                    enc = base64.b64encode(
                        open(tmp_aud, "rb").read()).decode('ascii')
                    self.app.random_event_aud = "data:audio/wav;base64," + enc
                    return True
        
        return False

