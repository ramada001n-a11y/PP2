import json
import os

def load_settings():
    default_settings = {"sound": True, "car_color": "red", "difficulty": "normal"}
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            return json.load(f)
    return default_settings

def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)

def load_leaderboard():
    if os.path.exists("leaderboard.json"):
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    return []

def save_leaderboard(leaderboard):
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:10]
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f, indent=4)