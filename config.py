import pygame

# Screen Settings
WIDTH, HEIGHT = 800, 750
FPS = 30

# Game States
STATE_MENU = "MENU"
STATE_PROFILE = "PROFILE"
STATE_MODE_SELECT = "MODE_SELECT"
STATE_OVERS_SELECT = "OVERS_SELECT"
STATE_TOSS = "TOSS"
STATE_TOSS_ANIM = "TOSS_ANIMATION"
STATE_PLAYING = "PLAYING"
STATE_INNINGS_BREAK = "INNINGS_BREAK"
STATE_GAME_OVER = "GAME_OVER"
STATE_RULES = "RULES"
STATE_WARNING = "WARNING"

# Modes
MODE_STANDARD = "STANDARD"
MODE_HARDCORE = "HARDCORE"

# Colors
BG_COLOR = (30, 30, 30)
PANEL_COLOR = (45, 45, 50)
HOVER_COLOR = (70, 70, 80)
DISABLED_COLOR = (30, 30, 35)
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (255, 215, 0)  # Gold
ALERT_COLOR = (255, 50, 50)   # Red
INFO_COLOR = (50, 150, 255)   # Blue
COIN_COLOR = (255, 223, 0)
COIN_EDGE = (184, 134, 11)

# Hand Colors
SKIN_BASE   = (255, 224, 189)
SKIN_SHADOW = (235, 200, 160)
OUTLINE     = (20, 10, 5)

# Match Presets
MATCH_PRESETS = {
    5:  {"wickets": 2, "bowlers": 2, "limit": 3},
    8:  {"wickets": 3, "bowlers": 3, "limit": 3},
    10: {"wickets": 5, "bowlers": 4, "limit": 4}
}

# Finger Rules
VALID_HANDS = {
    0: [()], 
    1: [(2,), (3,), (4,), (5,)],
    2: [(2, 3), (3, 4), (4, 5)],
    3: [(2, 3, 4), (3, 4, 5)],
    4: [(2, 3, 4, 5)],
    5: [(1, 2, 3, 4, 5)],
    6: [(1,)]
}