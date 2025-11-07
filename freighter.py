"""
Freighter player ship class.
"""

import config
from subsprite import SubSprite
from funcs import LARGE
from boom import Boom


class Freighter(SubSprite):
    """
    Player-controlled freighter ship.
    """
    
    def __init__(self, game):
        super().__init__()
        self.set_game(game)
        
        self.hp = config.FREIGHTER_MAX_HP
        self.max_hp = config.FREIGHTER_MAX_HP
        self.move_delay = config.FREIGHTER_MOVE_DELAY
        self.x_speed = config.FREIGHTER_X_SPEED
        self.y_speed = config.FREIGHTER_Y_SPEED
        self.size = LARGE
        self.blink_count = 0
        self.blink_time = 0
        self.shield_blink_on = False
        
        # Set texture
        self.image = game.get_loads().tex_freighter
        self.rect = self.image.get_rect()
        
        # Set initial position (center bottom)
        window_width = game.window.get_width()
        window_height = game.window.get_height()
        self.set_position(
            window_width // 2 - self.rect.width // 2,
            window_height - self.rect.height
        )
    
    def check_struck(self):
        """Handle ship being hit by a rock - check HP and blink shield."""
        if self.struck:
            if self.hp <= 0:
                if self.alive:
                    # Create explosion
                    self.game.boombox.append(Boom(self.game, self.size, self.rect))
                    self.game.you_lose = True
                    self.game.all_rock_blast_time = self.game.get_time()
                self.alive = False
            
            # Handle shield blink animation
            if self.blink_count == 0:
                self.blink_time = self.game.get_time()
                self.blink_count += 1
                self.image = self.game.get_loads().tex_freighter_blink
            elif self.blink_count >= config.FREIGHTER_BLINK_COUNT_MAX:
                self.struck = False
                self.blink_count = 0
                self.image = self.game.get_loads().tex_freighter
            
            # Toggle blink texture
            current_time = self.game.get_time()
            if current_time - self.blink_time >= config.FREIGHTER_BLINK_INTERVAL:
                if not self.shield_blink_on:
                    self.blink_time = current_time
                    self.image = self.game.get_loads().tex_freighter
                    self.shield_blink_on = True
                else:
                    self.blink_time = current_time
                    self.blink_count += 1
                    self.image = self.game.get_loads().tex_freighter_blink
                    self.shield_blink_on = False
    
    def move_me(self):
        """Move the freighter based on velocity and keep it on screen."""
        current_time = self.game.get_time()
        if current_time - self.last_move_time >= self.move_delay:
            self.move(self.x_velocity, self.y_velocity)
            self.last_move_time = current_time
        
        # Keep ship on screen
        window_width = self.game.window.get_width()
        window_height = self.game.window.get_height()
        
        if self.rect.x <= 0:
            self.set_x(0)
        if self.rect.x >= window_width - self.rect.width:
            self.set_x(window_width - self.rect.width)
        if self.rect.y <= 0:
            self.set_y(0)
        if self.rect.y >= window_height - (self.rect.height + config.FREIGHTER_BOTTOM_OFFSET):
            self.set_y(window_height - (self.rect.height + config.FREIGHTER_BOTTOM_OFFSET))
    
    def update(self):
        """Update freighter state and position."""
        self.check_struck()
        if self.alive:
            self.move_me()
            self.set_rect()

