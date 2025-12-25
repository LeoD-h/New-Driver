"""
Entites du jeu: Voiture et Obstacles
"""

import pygame
import random
from .constants import *


class Car:
    """Voiture du joueur"""
    
    def __init__(self):
        self.x = ROAD_LEFT + ROAD_WIDTH // 2 - CAR_WIDTH // 2
        self.y = SCREEN_HEIGHT - CAR_HEIGHT - 80
        self.speed = 5
        self.max_speed = 12
        self.target_x = self.x
        self.steering_speed = 0.05
        
    def update(self, direction, action):
        """Met a jour la position de la voiture"""
        if direction == "GAUCHE":
            self.target_x = ROAD_LEFT + LANE_WIDTH // 2
        elif direction == "DROITE":
            self.target_x = ROAD_RIGHT - LANE_WIDTH // 2 - CAR_WIDTH // 2
        else:
            self.target_x = ROAD_LEFT + ROAD_WIDTH // 2 - CAR_WIDTH // 2
            
        # Mouvement fluide
        diff = self.target_x - self.x
        self.x += diff * self.steering_speed
        
        # Limites
        self.x = max(ROAD_LEFT + 10, min(self.x, ROAD_RIGHT - CAR_WIDTH - 10))
        
        # Vitesse
        if action == "ACCELERER":
            self.speed = min(self.speed + 0.3, self.max_speed)
        else:
            self.speed = max(self.speed - 0.2, 2)
            
    def draw(self, screen):
        """Dessine la voiture"""
        # Ombre
        pygame.draw.ellipse(screen, (30, 30, 30), 
                           (self.x - 5, self.y + CAR_HEIGHT - 10, CAR_WIDTH + 10, 20))
        # Corps
        pygame.draw.rect(screen, BLUE, 
                        (self.x, self.y, CAR_WIDTH, CAR_HEIGHT), border_radius=12)
        # Toit
        pygame.draw.rect(screen, (40, 80, 200), 
                        (self.x + 8, self.y + 20, CAR_WIDTH - 16, 40), border_radius=8)
        # Pare-brise
        pygame.draw.rect(screen, (100, 150, 255), 
                        (self.x + 10, self.y + 22, CAR_WIDTH - 20, 15), border_radius=4)
        # Phares
        pygame.draw.circle(screen, YELLOW, (int(self.x + 12), int(self.y + 8)), 6)
        pygame.draw.circle(screen, YELLOW, (int(self.x + CAR_WIDTH - 12), int(self.y + 8)), 6)
        # Feux arriere
        pygame.draw.rect(screen, RED, (self.x + 5, self.y + CAR_HEIGHT - 10, 10, 6), border_radius=2)
        pygame.draw.rect(screen, RED, (self.x + CAR_WIDTH - 15, self.y + CAR_HEIGHT - 10, 10, 6), border_radius=2)
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, CAR_WIDTH, CAR_HEIGHT)


class Obstacle:
    """Obstacle a eviter"""
    
    def __init__(self):
        self.x = random.randint(ROAD_LEFT + 20, ROAD_RIGHT - OBSTACLE_WIDTH - 20)
        self.y = -OBSTACLE_HEIGHT - random.randint(0, 200)
        self.type = random.choice(["car", "rock", "cone"])
        
    def update(self, speed):
        """Deplace l'obstacle vers le bas"""
        self.y += speed + 3
        
    def draw(self, screen):
        """Dessine l'obstacle"""
        if self.type == "car":
            pygame.draw.rect(screen, RED, 
                           (self.x, self.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT + 30), border_radius=10)
            pygame.draw.rect(screen, DARK_GRAY, 
                           (self.x + 8, self.y + 15, OBSTACLE_WIDTH - 16, 25), border_radius=6)
        elif self.type == "rock":
            pygame.draw.circle(screen, GRAY, 
                             (int(self.x + OBSTACLE_WIDTH // 2), int(self.y + OBSTACLE_HEIGHT // 2)), 
                             OBSTACLE_WIDTH // 2)
            pygame.draw.circle(screen, (80, 80, 80), 
                             (int(self.x + OBSTACLE_WIDTH // 2 - 5), int(self.y + OBSTACLE_HEIGHT // 2 - 5)), 8)
        else:
            points = [(self.x + OBSTACLE_WIDTH // 2, self.y), 
                     (self.x, self.y + OBSTACLE_HEIGHT), 
                     (self.x + OBSTACLE_WIDTH, self.y + OBSTACLE_HEIGHT)]
            pygame.draw.polygon(screen, ORANGE, points)
            pygame.draw.polygon(screen, WHITE, points, 2)
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
