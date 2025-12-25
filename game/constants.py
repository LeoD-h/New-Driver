"""
Constantes du jeu NewDriver
"""

# Dimensions de la fenetre
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Voiture
CAR_WIDTH = 60
CAR_HEIGHT = 100

# Obstacles
OBSTACLE_WIDTH = 60
OBSTACLE_HEIGHT = 60

# Route
LANE_COUNT = 5
ROAD_LEFT = 100
ROAD_RIGHT = SCREEN_WIDTH - 100
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT

# Couleurs
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

# Mapping des classes YOLO
CLASS_NAMES = {
    0: "visage_serieux",
    1: "livre_droite",
    2: "livre_milieu", 
    3: "livre_gauche",
    4: "visage_sourire"
}
