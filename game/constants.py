"""
Game constants for NewDriver
"""

# Window dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Car
CAR_WIDTH = 60
CAR_HEIGHT = 100

# Obstacles
OBSTACLE_WIDTH = 60
OBSTACLE_HEIGHT = 60

# Road layout
LANE_COUNT = 5
ROAD_LEFT = 100
ROAD_RIGHT = SCREEN_WIDTH - 100
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 50)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# YOLO class mapping
CLASS_NAMES = {
    0: "visage_serieux",   # serious face
    1: "livre_droite",     # book right
    2: "livre_milieu",     # book center
    3: "livre_gauche",     # book left
    4: "visage_sourire"    # smiling face
}
