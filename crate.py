"""
Crate collectible class.
"""

from subsprite import SubSprite
from funcs import rand_int


class Crate(SubSprite):
    """
    Collectible crate that spawns randomly in the upper third of the screen.
    """
    
    def __init__(self, game):
        super().__init__()
        self.set_game(game)
        
        # Set texture
        self.image = game.get_loads().tex_crate
        self.rect = self.image.get_rect()
        
        # Set random position in upper third of screen
        window_width = game.window.get_width()
        window_height = game.window.get_height()
        self.set_position(
            rand_int(0, window_width - self.rect.width),
            rand_int(0, window_height // 3 - self.rect.height)
        )
        
        self.set_rect()

