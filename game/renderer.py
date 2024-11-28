import pygame
import math
import time
from config.config import GameConfig as cfg

class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.snake_renderer = SnakeRenderer(screen)
        self.food_renderer = FoodRenderer(screen)
        self.ui_renderer = UIRenderer(screen)
        
    def render(self, game_state):
        self.screen.fill(cfg.BLACK)
        self.snake_renderer.render(game_state.snake)
        self.food_renderer.render(game_state.food)
        self.ui_renderer.render(game_state.score, game_state.high_score)
        pygame.display.flip()

class SnakeRenderer:
    def __init__(self, screen):
        self.screen = screen
        
    def render(self, snake):
        for i, segment in enumerate(snake):
            color_intensity = max(50, 255 - (i * 5))
            pygame.draw.rect(self.screen, (0, color_intensity, 0),
                           (*segment, cfg.CELL_SIZE-1, cfg.CELL_SIZE-1))
            pygame.draw.rect(self.screen, (0, min(color_intensity + 50, 255), 0),
                           (*segment, cfg.CELL_SIZE-1, cfg.CELL_SIZE-1), 1)

class FoodRenderer:
    def __init__(self, screen):
        self.screen = screen
        
    def render(self, food):
        food_intensity = abs(math.sin(time.time() * 5)) * 155 + 100
        pygame.draw.rect(self.screen, (food_intensity, 0, 0),
                        (*food, cfg.CELL_SIZE-1, cfg.CELL_SIZE-1))
        pygame.draw.rect(self.screen, cfg.RED,
                        (*food, cfg.CELL_SIZE-1, cfg.CELL_SIZE-1), 1)

class UIRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, cfg.FONT_SIZE)
        
    def render(self, score, high_score):
        score_text = self.font.render(f'Skor: {score}', True, cfg.SCORE_COLOR)
        high_score_text = self.font.render(f'En Yüksek: {high_score}', True, cfg.SCORE_COLOR)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (cfg.WIDTH - 200, 10)) 