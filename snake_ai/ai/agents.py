from abc import ABC, abstractmethod
import numpy as np
import tensorflow as tf
from ai.memory import PrioritizedReplayBuffer
from ai.networks import create_network
from config.config import AIConfig as cfg

class BaseAgent(ABC):
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = PrioritizedReplayBuffer(cfg.MEMORY_SIZE)
        self.epsilon = cfg.EPSILON_START
        self.model = create_network(state_size, action_size)
        
    @abstractmethod
    def act(self, state):
        pass
        
    @abstractmethod
    def remember(self, state, action, reward, next_state, done):
        pass
        
    @abstractmethod
    def replay(self, batch_size):
        pass

class DQNAgent(BaseAgent):
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.action_size)
        
        state = np.array(state).reshape(1, -1)
        return np.argmax(self.model.predict(state)[0])
        
    def remember(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)
        
    def replay(self, batch_size):
        if len(self.memory.buffer) < batch_size:
            return
            
        samples, indices, weights = self.memory.sample(batch_size)
        
        states = np.array([s[0] for s in samples])
        actions = np.array([s[1] for s in samples])
        rewards = np.array([s[2] for s in samples])
        next_states = np.array([s[3] for s in samples])
        dones = np.array([s[4] for s in samples])
        
        targets = self.model.predict(states)
        next_qs = self.model.predict(next_states)
        
        for i in range(batch_size):
            if dones[i]:
                targets[i][actions[i]] = rewards[i]
            else:
                targets[i][actions[i]] = rewards[i] + cfg.GAMMA * np.amax(next_qs[i])
                
        self.model.fit(states, targets, sample_weight=weights,
                      batch_size=batch_size, epochs=1, verbose=0)
                      
        if self.epsilon > cfg.EPSILON_MIN:
            self.epsilon *= cfg.EPSILON_DECAY 