"""
Elements d'interface utilisateur
"""

import pygame
from .constants import *


class Button:
    """Bouton clickable"""
    
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.is_active = False
        
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def draw(self, screen, font):
        color = self.hover_color if self.is_hovered else self.color
        if self.is_active:
            color = GREEN
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=8)
        
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


def draw_road(screen, road_offset):
    """Dessine la route"""
    # Fond vert
    screen.fill((34, 139, 34))
    
    # Bande de terre
    pygame.draw.rect(screen, (139, 90, 43), (ROAD_LEFT - 30, 0, 30, SCREEN_HEIGHT))
    pygame.draw.rect(screen, (139, 90, 43), (ROAD_RIGHT, 0, 30, SCREEN_HEIGHT))
    
    # Route
    pygame.draw.rect(screen, DARK_GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))
    
    # Lignes
    for i in range(1, LANE_COUNT):
        x = ROAD_LEFT + i * LANE_WIDTH
        for y in range(-60 + int(road_offset), SCREEN_HEIGHT, 60):
            pygame.draw.rect(screen, WHITE, (x - 3, y, 6, 35))
            
    # Bords
    pygame.draw.rect(screen, WHITE, (ROAD_LEFT - 5, 0, 8, SCREEN_HEIGHT))
    pygame.draw.rect(screen, WHITE, (ROAD_RIGHT - 3, 0, 8, SCREEN_HEIGHT))


def draw_position_indicator(screen, car_x, font):
    """Dessine l'indicateur de position"""
    indicator_y = SCREEN_HEIGHT - 40
    indicator_width = 300
    indicator_x = (SCREEN_WIDTH - indicator_width) // 2
    
    # Zones
    pygame.draw.rect(screen, (100, 50, 50), (indicator_x, indicator_y, indicator_width // 3, 20), border_radius=10)
    pygame.draw.rect(screen, (50, 100, 50), (indicator_x + indicator_width // 3, indicator_y, indicator_width // 3, 20))
    pygame.draw.rect(screen, (50, 50, 100), (indicator_x + 2 * indicator_width // 3, indicator_y, indicator_width // 3, 20), border_radius=10)
    
    # Labels
    labels = ["GAUCHE", "MILIEU", "DROITE"]
    for i, label in enumerate(labels):
        text = font.render(label, True, WHITE)
        text_x = indicator_x + i * (indicator_width // 3) + (indicator_width // 6) - text.get_width() // 2
        screen.blit(text, (text_x, indicator_y + 2))
    
    # Marqueur
    car_center = car_x + CAR_WIDTH // 2
    car_pct = (car_center - ROAD_LEFT) / ROAD_WIDTH
    marker_x = indicator_x + int(car_pct * indicator_width)
    pygame.draw.circle(screen, CYAN, (marker_x, indicator_y + 10), 8)
    pygame.draw.circle(screen, WHITE, (marker_x, indicator_y + 10), 8, 2)


def draw_hud(screen, font, small_font, score, speed, distance, direction, action, detections, test_mode):
    """Dessine l'interface"""
    # Panneau stats
    panel_rect = pygame.Rect(10, 10, 200, 130)
    pygame.draw.rect(screen, (0, 0, 0), panel_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, panel_rect, 2, border_radius=10)
    
    screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 20))
    screen.blit(font.render(f"Vitesse: {int(speed * 10)} km/h", True, WHITE), (20, 50))
    screen.blit(font.render(f"Distance: {int(distance / 10)}m", True, WHITE), (20, 80))
    
    if test_mode:
        screen.blit(font.render("TEST MODE", True, GREEN), (20, 110))
    
    # Panneau detection
    detect_panel = pygame.Rect(SCREEN_WIDTH - 240, 60, 230, 150)
    pygame.draw.rect(screen, (0, 0, 0), detect_panel, border_radius=10)
    pygame.draw.rect(screen, WHITE, detect_panel, 2, border_radius=10)
    
    dir_color = GREEN if direction != "MILIEU" else WHITE
    screen.blit(font.render(f"Dir: {direction}", True, dir_color), (SCREEN_WIDTH - 230, 70))
    
    action_color = GREEN if action == "ACCELERER" else RED
    screen.blit(font.render(f"Act: {action}", True, action_color), (SCREEN_WIDTH - 230, 100))
    
    y_offset = 130
    for det in detections[:3]:
        screen.blit(small_font.render(det, True, YELLOW), (SCREEN_WIDTH - 230, y_offset))
        y_offset += 25


def draw_game_over(screen, font, big_font, score, distance):
    """Affiche game over"""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(180)
    screen.blit(overlay, (0, 0))
    
    go_text = big_font.render("GAME OVER", True, RED)
    screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
    
    score_text = font.render(f"Score final: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    
    dist_text = font.render(f"Distance: {int(distance / 10)}m", True, WHITE)
    screen.blit(dist_text, (SCREEN_WIDTH // 2 - dist_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
    
    restart_text = font.render("ESPACE pour rejouer", True, GREEN)
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
