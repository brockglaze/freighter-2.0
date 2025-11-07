"""
Laser projectile class.
"""

import config
from subsprite import SubSprite


class Laser(SubSprite):
    """
    Laser projectile shot upward from the freighter ship.
    """
    
    def __init__(self, game):
        super().__init__()
        self.set_game(game)
        
        self.atk = config.LASER_DAMAGE
        self.move_delay = config.LASER_MOVE_DELAY
        self.y_speed = config.LASER_Y_SPEED
        self.y_velocity = -self.y_speed  # Negative because moving up
        
        # Set texture
        self.image = game.get_loads().tex_laser
        self.rect = self.image.get_rect()
        
        # Position at freighter's position
        freighter = game.get_freighter()
        self.set_position(
            freighter.rect.x + config.LASER_SPAWN_OFFSET_X,
            freighter.rect.y + config.LASER_SPAWN_OFFSET_Y
        )
        
        # Play laser sound
        sound = game.get_loads().laser_buffer
        sound.set_volume(config.SOUND_LASER_VOLUME)
        sound.play()
    
    def update(self):
        """Update laser position and check if off-screen."""
        # Check if off-screen
        if self.rect.y + self.rect.height < 0:
            self.alive = False
            return
        
        # Move based on time
        current_time = self.game.get_time()
        if current_time - self.last_move_time >= self.move_delay:
            self.move(0, self.y_velocity)
            self.last_move_time = current_time
        
        self.set_rect()

