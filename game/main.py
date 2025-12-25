#!/usr/bin/env python3
"""
NewDriver - Jeu de Voiture controle par la tete
Point d'entree principal
"""

import pygame
import cv2
import sys
from pathlib import Path

# Ajouter le parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from game.constants import *
from game.entities import Car, Obstacle
from game.tracker import HeadTracker, find_latest_model
from game.ui import Button, draw_road, draw_position_indicator, draw_hud, draw_game_over


class Game:
    """Jeu principal NewDriver"""
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("NewDriver - Jeu de Voiture")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 80)
        
        # Bouton test mode
        self.test_button = Button(SCREEN_WIDTH - 180, 10, 170, 40, "MODE TEST: OFF", GRAY, DARK_GRAY)
        self.test_mode = False
        
        # Trouver le modele
        self.model_path = find_latest_model()
        if not self.model_path:
            print("Erreur: Aucun modele trouve!")
            print("Lancez d'abord l'entrainement: python training/train.py")
            exit(1)
            
        print(f"Modele charge: {self.model_path}")
        
        # Tracker
        self.tracker = HeadTracker(self.model_path)
        
        # Etat du jeu
        self.reset_game()
        
    def reset_game(self):
        """Reinitialise le jeu"""
        self.car = Car()
        self.obstacles = []
        self.score = 0
        self.distance = 0
        self.game_over = False
        self.spawn_timer = 0
        self.road_offset = 0
        self.manual_direction = None
        
    def run(self):
        """Boucle principale"""
        if not self.tracker.start():
            print("Impossible de demarrer la webcam")
            return
            
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            self.test_button.update(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_over:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_t:
                        self.toggle_test_mode()
                    elif event.key == pygame.K_LEFT:
                        self.manual_direction = "GAUCHE"
                    elif event.key == pygame.K_RIGHT:
                        self.manual_direction = "DROITE"
                    elif event.key == pygame.K_UP:
                        self.manual_direction = "MILIEU"
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP]:
                        self.manual_direction = None
                        
                if self.test_button.is_clicked(event):
                    self.toggle_test_mode()
                        
            if not self.game_over:
                self.update()
                
            self.draw()
            self.clock.tick(60)
            
        self.tracker.stop()
        pygame.quit()
        
    def toggle_test_mode(self):
        """Active/desactive le mode test"""
        self.test_mode = not self.test_mode
        self.test_button.is_active = self.test_mode
        self.test_button.text = "MODE TEST: ON" if self.test_mode else "MODE TEST: OFF"
        if self.test_mode:
            self.obstacles.clear()
        
    def update(self):
        """Met a jour le jeu"""
        direction, action, _, _ = self.tracker.get_state()
        
        if self.manual_direction:
            direction = self.manual_direction
        
        self.car.update(direction, action)
        
        if not self.test_mode:
            for obstacle in self.obstacles[:]:
                obstacle.update(self.car.speed)
                
                if self.car.get_rect().colliderect(obstacle.get_rect()):
                    self.game_over = True
                    
                if obstacle.y > SCREEN_HEIGHT:
                    self.obstacles.remove(obstacle)
                    self.score += 10
                    
            self.spawn_timer += 1
            if self.spawn_timer > max(40, 80 - self.car.speed * 3):
                self.spawn_timer = 0
                if len(self.obstacles) < 4:
                    self.obstacles.append(Obstacle())
                
        self.distance += self.car.speed
        self.road_offset = (self.road_offset + self.car.speed) % 60
        
    def draw(self):
        """Dessine le jeu"""
        draw_road(self.screen, self.road_offset)
        
        if not self.test_mode:
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            
        self.car.draw(self.screen)
        
        draw_position_indicator(self.screen, self.car.x, self.small_font)
        
        direction, action, _, detections = self.tracker.get_state()
        draw_hud(self.screen, self.font, self.small_font, 
                self.score, self.car.speed, self.distance,
                direction, action, detections, self.test_mode)
        
        self.test_button.draw(self.screen, self.small_font)
        
        self.draw_webcam()
        
        if self.game_over:
            draw_game_over(self.screen, self.font, self.big_font, self.score, self.distance)
            
        pygame.display.flip()
        
    def draw_webcam(self):
        """Affiche la webcam"""
        frame = self.tracker.get_frame()
        if frame is not None:
            small = cv2.resize(frame, (200, 150))
            small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
            surface = pygame.surfarray.make_surface(small.swapaxes(0, 1))
            self.screen.blit(surface, (10, SCREEN_HEIGHT - 200))
            pygame.draw.rect(self.screen, WHITE, (10, SCREEN_HEIGHT - 200, 200, 150), 3)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
