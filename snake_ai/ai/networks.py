import tensorflow as tf
from config.config import AIConfig as cfg

def create_network(state_size, action_size):
    """Neural network oluşturur."""
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, input_dim=state_size),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.Dense(64),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.Dense(action_size, activation='linear')
    ])
    
    model.compile(
        loss='mse',
        optimizer=tf.keras.optimizers.Adam(learning_rate=cfg.LEARNING_RATE)
    )
    
    return model 