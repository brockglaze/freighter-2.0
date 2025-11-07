"""
Rock enemy class.
"""

import config
from subsprite import SubSprite
from funcs import rand_int, SMALL, MEDIUM, LARGE, DOWNLEFT, DOWNRIGHT, UPLEFT, UPRIGHT


class Rock(SubSprite):
    """
    Enemy rock that moves diagonally and bounces off walls and other rocks.
    """
    
    def __init__(self, game, size):
        super().__init__()
        self.set_game(game)
        
        self.size = size
        self.direction = rand_int(DOWNLEFT, DOWNRIGHT)
        
        # Set stats based on size
        if size == SMALL:
            self.hp = config.ROCK_SMALL_HP
            self.max_hp = config.ROCK_SMALL_HP
            self.atk = self.max_hp
            self.move_speed = rand_int(config.ROCK_SMALL_MOVE_SPEED_MIN, config.ROCK_SMALL_MOVE_SPEED_MAX)
            self.x_speed = rand_int(config.ROCK_SMALL_X_SPEED_MIN, config.ROCK_SMALL_X_SPEED_MAX)
            self.y_speed = rand_int(config.ROCK_SMALL_Y_SPEED_MIN, config.ROCK_SMALL_Y_SPEED_MAX)
            self.image = game.get_loads().tex_sm_rock
        elif size == MEDIUM:
            self.hp = config.ROCK_MEDIUM_HP
            self.max_hp = config.ROCK_MEDIUM_HP
            self.atk = self.max_hp
            self.move_speed = rand_int(config.ROCK_MEDIUM_MOVE_SPEED_MIN, config.ROCK_MEDIUM_MOVE_SPEED_MAX)
            self.x_speed = rand_int(config.ROCK_MEDIUM_X_SPEED_MIN, config.ROCK_MEDIUM_X_SPEED_MAX)
            self.y_speed = rand_int(config.ROCK_MEDIUM_Y_SPEED_MIN, config.ROCK_MEDIUM_Y_SPEED_MAX)
            self.image = game.get_loads().tex_md_rock
        elif size == LARGE:
            self.hp = config.ROCK_LARGE_HP
            self.max_hp = config.ROCK_LARGE_HP
            self.atk = self.max_hp
            self.move_speed = rand_int(config.ROCK_LARGE_MOVE_SPEED_MIN, config.ROCK_LARGE_MOVE_SPEED_MAX)
            self.x_speed = config.ROCK_LARGE_X_SPEED
            self.y_speed = config.ROCK_LARGE_Y_SPEED
            self.image = game.get_loads().tex_lg_rock
        
        self.rect = self.image.get_rect()
        
        # Set initial position (off-screen at top)
        window_width = game.window.get_width()
        self.set_position(
            rand_int(0, window_width - self.rect.width),
            config.ROCK_SPAWN_OFFSET_Y - self.rect.height
        )
    
    def move_me(self):
        """Move the rock based on its direction and handle wall bouncing."""
        # Set velocity based on direction
        if self.direction == DOWNLEFT:
            self.x_velocity = -self.x_speed
            self.y_velocity = self.y_speed
        elif self.direction == DOWNRIGHT:
            self.x_velocity = self.x_speed
            self.y_velocity = self.y_speed
        elif self.direction == UPLEFT:
            self.x_velocity = -self.x_speed
            self.y_velocity = -self.y_speed
        elif self.direction == UPRIGHT:
            self.x_velocity = self.x_speed
            self.y_velocity = -self.y_speed
        
        # Move based on time
        current_time = self.game.get_time()
        move_interval = config.ROCK_MOVE_BASE // self.move_speed if self.move_speed > 0 else config.ROCK_MOVE_BASE
        if current_time - self.last_move_time >= move_interval:
            self.move(self.x_velocity, self.y_velocity)
            self.last_move_time = current_time
        
        # Bounce off left wall
        if self.rect.x <= 0:
            if self.direction == DOWNLEFT:
                self.direction = DOWNRIGHT
            elif self.direction == UPLEFT:
                self.direction = UPRIGHT
        
        # Bounce off right wall
        window_width = self.game.window.get_width()
        if self.rect.x >= window_width - self.rect.width:
            if self.direction == DOWNRIGHT:
                self.direction = DOWNLEFT
            elif self.direction == UPRIGHT:
                self.direction = UPLEFT
        
        # Bounce off top wall
        if self.rect.y <= 0:
            if self.direction == UPRIGHT:
                self.direction = DOWNRIGHT
            elif self.direction == UPLEFT:
                self.direction = DOWNLEFT
        
        # Bounce off bottom (force field)
        window_height = self.game.window.get_height()
        freighter_height = self.game.get_freighter().rect.height
        bottom_boundary = window_height - (self.rect.height + freighter_height + config.FORCE_FIELD_OFFSET)
        if self.rect.y >= bottom_boundary:
            if self.direction == DOWNRIGHT:
                self.direction = UPRIGHT
            elif self.direction == DOWNLEFT:
                self.direction = UPLEFT
            
            # Trigger force field blink
            self.game.ff_set_true()
    
    def rock_blasted(self):
        """Check if rock is destroyed or damaged and update texture."""
        if self.hp <= 0:
            self.alive = False
        elif self.hp < self.max_hp and self.alive:
            if self.size == LARGE:
                self.image = self.game.get_loads().tex_lg_rock2
    
    def update(self):
        """Update rock state and position."""
        self.rock_blasted()
        if self.alive:
            self.move_me()
            self.set_rect()

