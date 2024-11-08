"""This module defines project-level constants."""

import datetime

GAME_DEFAULT_SUPPLY = 500
GAME_DEFAULT_SUPPLY_SEARCH = 100
GAME_DEFAULT_CONSUME_TRAVEL = 5
GAME_DEFAULT_CONSUME_REST = 1
GAME_DEFAULT_HEALTH_MAX = 5
GAME_DEFAULT_START_DATE = datetime.date(2345, 3, 1)  # Start on March 1st, 2345
GAME_DEFAULT_END_DATE = datetime.date(2345, 12, 31)  # End on December 31st, 2345
GAME_DESTINATION_DISTANCE = 580
GAME_DEFAULT_TRAVEL_SPEED = 7

GAME_UI_PROGRESS_BAR_LENGTH = 50

EVENT_GENERATION_PROMPT = """You are in-game AI for "The Kepler Trail", the game inspired by "The Oregon Trail" but traveling in space.
Write a random event in json format{lang}."""

EVENT_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "effect": {
            "type": "object",
            "properties": {
                "supply": {"type": "integer", "minimum": -50, "maximum": 50},
                "health": {"type": "integer", "minimum": -2, "maximum": 2},
                "day": {"type": "integer", "minimum": 0, "maximum": 2},
            }
        }
    }
}
EVENT_JSON_EXAMPLE_STR = """{"text": "Signal disruption! You spend a day to fix the equipment.", "effect": {"supply": -10, "health": 0, "day": 1}}"""
EVENT_JSON_EXAMPLE_STR_KO = """{"text": "신호 장애 발생! 장비를 수리하는 데 하루를 소모합니다.", "effect": {"supply": -10, "health": 0, "day": 1}}"""
EVENT_JSON_EXAMPLE_STR_JA = """{"text": "信号が途絶！ 機器の修理に1日を費やします。", "effect": {"supply": -10, "health": 0, "day": 1}}"""
