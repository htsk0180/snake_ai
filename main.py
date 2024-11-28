import pygame
import sys
from game.game_logic import GameLogic
from ai.agents import DQNAgent
from config.config import GameConfig as cfg, AIConfig as ai_cfg
from game.renderer import GameRenderer
import gym
from collections import deque
import numpy as np

class SnakeGame(gym.Env):
    def __init__(self):
        super(SnakeGame, self).__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
        pygame.display.set_caption("Snake AI")
        
        self.game_logic = GameLogic()
        self.renderer = GameRenderer(self.screen)
        self.snake = deque()
        self.food = None
        self.score = 0
        self.high_score = 0
        
        # Gym spaces
        self.action_space = gym.spaces.Discrete(4)  # UP, DOWN, LEFT, RIGHT
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32
        )
        
        self.reset()
    
    def reset(self):
        start_x = (cfg.WIDTH // cfg.CELL_SIZE // 2) * cfg.CELL_SIZE
        start_y = (cfg.HEIGHT // cfg.CELL_SIZE // 2) * cfg.CELL_SIZE
        self.snake = deque([(start_x, start_y)])
        self.food = self._place_food()
        self.score = 0
        return self._get_state()
    
    def _place_food(self):
        while True:
            x = np.random.randint(0, cfg.WIDTH // cfg.CELL_SIZE) * cfg.CELL_SIZE
            y = np.random.randint(0, cfg.HEIGHT // cfg.CELL_SIZE) * cfg.CELL_SIZE
            if (x, y) not in self.snake:
                return (x, y)
    
    def _get_state(self):
        head = self.snake[0]
        return np.array([
            # Tehlike durumları
            float(self._is_danger((head[0], head[1] - cfg.CELL_SIZE))),  # UP
            float(self._is_danger((head[0], head[1] + cfg.CELL_SIZE))),  # DOWN
            float(self._is_danger((head[0] - cfg.CELL_SIZE, head[1]))),  # LEFT
            float(self._is_danger((head[0] + cfg.CELL_SIZE, head[1]))),  # RIGHT
            # Yiyecek yönü
            (self.food[0] - head[0]) / cfg.WIDTH,
            (self.food[1] - head[1]) / cfg.HEIGHT,
            # Yılan uzunluğu
            len(self.snake) / (cfg.WIDTH * cfg.HEIGHT / (cfg.CELL_SIZE ** 2))
        ], dtype=np.float32)
    
    def _is_danger(self, pos):
        return (pos[0] < 0 or pos[0] >= cfg.WIDTH or
                pos[1] < 0 or pos[1] >= cfg.HEIGHT or
                pos in self.snake)
    
    def step(self, action):
        # Yön belirleme
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # UP, DOWN, LEFT, RIGHT
        direction = directions[action]
        
        # Yeni kafa pozisyonu
        head = self.snake[0]
        new_head = (head[0] + direction[0] * cfg.CELL_SIZE,
                   head[1] + direction[1] * cfg.CELL_SIZE)
        
        # Çarpışma kontrolü
        if self._is_danger(new_head):
            return self._get_state(), -10, True, {}
        
        self.snake.appendleft(new_head)
        reward = 0
        
        # Yemek yeme kontrolü
        if new_head == self.food:
            self.score += 1
            self.high_score = max(self.high_score, self.score)
            self.food = self._place_food()
            reward = 10
        else:
            self.snake.pop()
            reward = -0.1  # Küçük bir ceza
        
        return self._get_state(), reward, False, {}
    
    def render(self, mode='human'):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        game_state = type('GameState', (), {
            'snake': self.snake,
            'food': self.food,
            'score': self.score,
            'high_score': self.high_score
        })
        
        self.renderer.render(game_state)
        pygame.time.Clock().tick(cfg.FPS)

def main():
    env = SnakeGame()
    state_size = 7
    action_size = 4
    agent = DQNAgent(state_size, action_size)
    batch_size = ai_cfg.BATCH_SIZE
    episodes = 1000
    
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        
        while True:
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            
            if len(agent.memory.buffer) > batch_size:
                agent.replay(batch_size)
            
            state = next_state
            total_reward += reward
            
            env.render()
            
            if done:
                break
        
        print(f"Bölüm: {episode + 1}, Skor: {env.score}, Toplam Ödül: {total_reward}")

if __name__ == "__main__":
    main() 