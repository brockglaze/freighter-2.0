"""
Base sprite class for all game entities.
"""

import pygame


class SubSprite:
    """
    Base class for all game sprites.
    Contains common properties and methods for movement, collision, and state.
    """
    
    def __init__(self):
        self.last_move_time = 0
        self.x_speed = 1
        self.y_speed = 1
        self.x_velocity = 0
        self.y_velocity = 0
        self.alive = True
        self.struck = False
        
        # Game entity properties
        self.size = 0
        self.direction = 0
        self.atk = 0.0
        self.hp = 0.0
        self.max_hp = 0.0
        
        # Pygame sprite properties
        self.image = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.game = None
    
    def set_game(self, game):
        """Sets the game reference."""
        self.game = game
    
    def set_rect(self):
        """Updates the collision rectangle to match the sprite's position and size."""
        if self.image:
            self.rect = pygame.Rect(
                self.rect.x,
                self.rect.y,
                self.image.get_width(),
                self.image.get_height()
            )
    
    def get_position(self):
        """Returns the sprite's position as a tuple (x, y)."""
        return (self.rect.x, self.rect.y)
    
    def set_position(self, x, y):
        """Sets the sprite's position."""
        self.rect.x = x
        self.rect.y = y
    
    def get_size(self):
        """Returns the sprite's size as a tuple (width, height)."""
        if self.image:
            return (self.image.get_width(), self.image.get_height())
        return (0, 0)
    
    def move(self, dx, dy):
        """Moves the sprite by the given delta."""
        self.rect.x += dx
        self.rect.y += dy
    
    def set_x(self, x):
        """Sets the x position."""
        self.rect.x = x
    
    def set_y(self, y):
        """Sets the y position."""
        self.rect.y = y

