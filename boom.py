"""
Explosion animation class.
"""

import config
from subsprite import SubSprite
from funcs import LARGE


class Boom(SubSprite):
    """
    Explosion animation that appears when rocks or the ship are destroyed.
    """
    
    def __init__(self, game, size, sprite_rect):
        super().__init__()
        self.set_game(game)
        
        self.boom_time = game.get_time()
        self.size = size
        
        # Set texture based on size
        if size == LARGE:
            self.image = game.get_loads().tex_lg_explode
        else:
            self.image = game.get_loads().tex_sm_explode
        
        self.rect = self.image.get_rect()
        
        # Position at center of destroyed sprite
        sprite_center_x = sprite_rect.x + sprite_rect.width // 2
        sprite_center_y = sprite_rect.y + sprite_rect.height // 2
        self.set_position(
            sprite_center_x - self.rect.width // 2,
            sprite_center_y - self.rect.height // 2
        )
        
        # Play explosion sound
        sound = game.get_loads().boom_buffer
        sound.set_volume(config.SOUND_BOOM_VOLUME)
        sound.play()
    
    def update(self):
        """Update explosion animation and remove when finished."""
        current_time = self.game.get_time()
        if current_time - self.boom_time >= config.EXPLOSION_DURATION:
            self.alive = False

