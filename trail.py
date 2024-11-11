"""This runs the game application."""

import os

# default language = English
# Use "ko" for Korean and "ja" for Japanese
LANG = "en"
# default GameAI = "gemini"
AI_TARGET = "gemini"
# default GameUI = "terminal"
GAME_UI = "terminal"

DEBUG = False
if "GAME_LANG" in os.environ:
    LANG = os.environ.get("GAME_LANG")
if "GAME_DEBUG" in os.environ:
    if os.environ.get("GAME_DEBUG") == "True":
        DEBUG = True
if "GAME_AI" in os.environ:
    AI_TARGET = os.environ.get("GAME_AI")
if "GAME_UI" in os.environ:
    GAME_UI = os.environ.get("GAME_UI")

match AI_TARGET:
    case "gemma":
        from gemma import GameAI

    case "gemma_ollama":
        from gemma_ollama import GameAI

    case "gemini":
        from gemini import GameAI

    case _:
        from scripted import GameAI

match GAME_UI:
    case "gradio":
        from game_gradio import GameUI

    case "flask":
        from game_flask import GameUI

    case "gui":
        from game_gui import GameUI

    case _:
        from game_tty import GameUI

trail = GameUI(LANG, DEBUG)
game_ai = GameAI(trail)
trail.set_game_ai(game_ai)

# Main game loop
trail.main_loop()
