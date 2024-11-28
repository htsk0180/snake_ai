from dataclasses import dataclass
from collections import deque
import random
from config.config import GameConfig as cfg

@dataclass
class GameResult:
    new_head: tuple
    reward: float
    done: bool
    info: dict = None

class GameLogic:
    def __init__(self):
        self.collision_checker = CollisionChecker()
        self.reward_calculator = RewardCalculator()
        self.movement_handler = MovementHandler()
        
    def process_move(self, snake: deque, direction: tuple, food: tuple) -> GameResult:
        new_head = self.movement_handler.calculate_new_position(snake[0], direction)
        
        # Çarpışma kontrolü
        if self.collision_checker.is_collision(new_head, snake):
            return GameResult(new_head, -10, True)
            
        # Yiyecek kontrolü
        ate_food = new_head == food
        reward = self.reward_calculator.calculate_reward(snake[0], new_head, food, ate_food)
        
        return GameResult(new_head, reward, False)

class CollisionChecker:
    def is_collision(self, position: tuple, snake: deque) -> bool:
        return (position[0] < 0 or position[0] >= cfg.WIDTH or
                position[1] < 0 or position[1] >= cfg.HEIGHT or
                position in snake)

class MovementHandler:
    def calculate_new_position(self, head: tuple, direction: tuple) -> tuple:
        return (head[0] + direction[0] * cfg.CELL_SIZE,
                head[1] + direction[1] * cfg.CELL_SIZE)

class RewardCalculator:
    def calculate_reward(self, old_head: tuple, new_head: tuple, 
                        food: tuple, ate_food: bool) -> float:
        if ate_food:
            return 10.0
            
        # Yiyeceğe yaklaşma/uzaklaşma ödülü
        old_distance = abs(old_head[0] - food[0]) + abs(old_head[1] - food[1])
        new_distance = abs(new_head[0] - food[0]) + abs(new_head[1] - food[1])
        
        return (old_distance - new_distance) * 0.1 + 0.1  # Hayatta kalma ödülü 