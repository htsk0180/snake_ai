class GameConfig:
    WIDTH = 640
    HEIGHT = 480
    CELL_SIZE = 20
    FPS = 10
    
    # Renkler
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    SCORE_COLOR = (255, 255, 0)
    BORDER_COLOR = (128, 128, 128)
    
    # UI
    FONT_SIZE = 36
    BORDER_WIDTH = 2

class AIConfig:
    BATCH_SIZE = 32
    MEMORY_SIZE = 2000
    GAMMA = 0.95
    EPSILON_START = 1.0
    EPSILON_MIN = 0.01
    EPSILON_DECAY = 0.995
    LEARNING_RATE = 0.001
    TARGET_UPDATE_FREQ = 100 