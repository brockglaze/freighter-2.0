"""
Main Game class - handles game loop, events, and entity management.
"""

import pygame
import random
import config
from loads import Loads
from freighter import Freighter
from crate import Crate
from rock import Rock
from laser import Laser
from boom import Boom
from funcs import rand_int, round_num, bounce_rocks, laser_collide


class Game:
    """
    Main game class that manages the game loop, entities, and game state.
    """
    
    def __init__(self):
        # Window dimensions
        self.sw = config.WINDOW_WIDTH
        self.sh = config.WINDOW_HEIGHT
        self.bits_per_pixel = config.WINDOW_BITS_PER_PIXEL
        
        # Initialize pygame
        pygame.init()
        
        # Try fullscreen, fallback to windowed
        if config.USE_FULLSCREEN:
            try:
                self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            except:
                self.window = pygame.display.set_mode((self.sw, self.sh))
        else:
            self.window = pygame.display.set_mode((self.sw, self.sh))
        
        pygame.display.set_caption("Freighter")
        self.clock = pygame.time.Clock()
        
        # Calculate area modifier
        self.area_mod = round_num((self.window.get_width() + self.window.get_height()) / config.AREA_MODIFIER_DIVISOR)
        
        # Load resources
        self.loads = Loads()
        self.loads.game_text_config(self)
        
        # Create freighter
        self.freighter = Freighter(self)
        
        # Game state
        self.time = 0
        self.ff_blink_time = 0
        self.all_rock_blast_time = 0
        self.last_laser_shot_time = 0
        
        self.level = 1
        self.max_level = config.MAX_LEVEL
        
        # Game state flags
        self.engageable = True
        self.you_lose = False
        self.you_win = False
        self.you_win_game = False
        self.ff_blink_on = False
        
        # Entity containers
        self.cratebox = []
        self.rockbox = []
        self.laserbox = []
        self.boombox = []
        self.soundbox = []  # For managing sound instances
        
        # World shapes (force field, health bars, bases)
        self.force_rect = None
        self.g_hp_bar = None
        self.r_hp_bar = None
        self.lbase_rect = None
        self.rbase_rect = None
        
        # Setup initial level
        self.level_setup()
        
        # Music state
        self.music_playing = False
    
    def get_time(self):
        """Returns the current game time in milliseconds."""
        return self.time
    
    def get_loads(self):
        """Returns the Loads resource manager."""
        return self.loads
    
    def get_freighter(self):
        """Returns the freighter ship."""
        return self.freighter
    
    def ff_set_true(self):
        """Triggers the force field blink effect."""
        self.ff_blink_on = True
        self.ff_blink_time = self.time
    
    def play_sound(self, sound_buffer, volume=1.0):
        """Plays a sound effect."""
        sound_buffer.set_volume(volume)
        sound_buffer.play()
    
    def create_crates(self):
        """Creates the required number of crates for the current level."""
        for _ in range(self.total_crates):
            self.cratebox.append(Crate(self))
    
    def create_rocks(self):
        """Creates the required number of rocks for the current level."""
        from funcs import SMALL, LARGE
        for _ in range(self.total_rocks):
            rock = Rock(self, rand_int(SMALL, LARGE))
            # Rocks created at level start are positioned randomly on screen
            window_width = self.window.get_width()
            window_height = self.window.get_height()
            rock.set_position(
                rand_int(0, window_width - rock.rect.width),
                rand_int(0, window_height - (rock.rect.height + self.freighter.rect.height + 10))
            )
            self.rockbox.append(rock)
    
    def create_world_shapes(self):
        """Creates the force field, health bars, and base images."""
        window_width = self.window.get_width()
        window_height = self.window.get_height()
        freighter_height = self.freighter.rect.height
        
        # Force field rectangle (at bottom, above freighter)
        force_y = window_height - freighter_height - config.FORCE_FIELD_OFFSET
        self.force_rect = pygame.Rect(0, force_y, window_width, 3)
        self.force_color = (0, 0, 0)
        
        # Health bars
        hp_bar_width = self.freighter.rect.width - config.HEALTH_BAR_WIDTH_OFFSET
        self.r_hp_bar = pygame.Rect(0, 0, hp_bar_width, 3)
        self.g_hp_bar = pygame.Rect(0, 0, hp_bar_width, 3)
        
        # Base images
        self.lbase_image = self.loads.tex_lbase
        self.rbase_image = self.loads.tex_rbase
        self.lbase_rect = self.lbase_image.get_rect()
        self.rbase_rect = self.rbase_image.get_rect()
        self.lbase_rect.bottomleft = (0, window_height)
        self.rbase_rect.bottomright = (window_width, window_height)
    
    def destroy_sounds(self):
        """Removes finished sounds from the sound list."""
        # Pygame handles sound cleanup automatically, so this is mostly a placeholder
        # In the original C++ code, this managed sound instances
        pass
    
    def freighter_movement(self):
        """Handles freighter movement based on keyboard input."""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.freighter.x_velocity = -self.freighter.x_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.freighter.x_velocity = self.freighter.x_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.freighter.y_velocity = -self.freighter.y_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.freighter.y_velocity = self.freighter.y_speed
    
    def ff_blink(self):
        """Handles force field blink animation when hit."""
        if self.ff_blink_on:
            self.force_color = (0, 127, 200)
            if self.time - self.ff_blink_time >= config.FORCE_FIELD_BLINK_DURATION:
                self.play_sound(self.loads.force_field_buffer, config.SOUND_FORCE_FIELD_VOLUME)
                self.force_color = (0, 0, 0)
                self.ff_blink_on = False
    
    def level_setup(self):
        """Sets up a new level."""
        self.engageable = True
        self.you_lose = False
        self.you_win = False
        self.you_win_game = False
        self.ff_blink_on = False
        self.last_laser_shot_time = 0  # Reset laser cooldown
        
        self.total_crates = self.level
        self.total_rocks = self.level * self.area_mod
        
        self.cratebox.clear()
        self.rockbox.clear()
        
        self.freighter.alive = True
        self.freighter.hp = self.freighter.max_hp
        window_width = self.window.get_width()
        window_height = self.window.get_height()
        self.freighter.set_position(
            window_width // 2 - self.freighter.rect.width // 2,
            window_height - self.freighter.rect.height
        )
        
        self.create_crates()
        self.create_rocks()
        self.create_world_shapes()
        
        self.loads.update_level_text(self.level)
        
        self.play_sound(self.loads.level_start, config.SOUND_LEVEL_START_VOLUME)
    
    def level_up(self):
        """Advances to the next level."""
        if self.level == self.max_level:
            self.you_win_game = True
        else:
            self.level += 1
    
    def print_bottom_text(self):
        """Draws bottom text (level and music status)."""
        self.window.blit(self.loads.level_text, self.loads.level_text_pos)
        self.window.blit(self.loads.music_text, self.loads.music_text_pos)
    
    def print_top_text(self):
        """Draws top text (win/lose messages)."""
        if self.you_win_game:
            self.window.blit(self.loads.congrats_text, self.loads.congrats_text_pos)
            self.window.blit(self.loads.win_game_text, self.loads.win_game_text_pos)
            self.window.blit(self.loads.play_again_text, self.loads.play_again_text_pos)
        elif self.you_win:
            self.window.blit(self.loads.win_text, self.loads.win_text_pos)
            self.window.blit(self.loads.advance_text, self.loads.advance_text_pos)
        elif self.you_lose:
            self.window.blit(self.loads.lose_text, self.loads.lose_text_pos)
            self.window.blit(self.loads.restart_text, self.loads.restart_text_pos)
    
    def refill_rocks(self):
        """Creates new rocks when they are destroyed."""
        from funcs import SMALL, LARGE
        if not self.you_win and len(self.rockbox) < self.total_rocks:
            self.rockbox.append(Rock(self, rand_int(SMALL, LARGE)))
    
    def run_crates(self):
        """Updates and draws crates, handles collection."""
        for crate in self.cratebox[:]:
            self.window.blit(crate.image, crate.rect)
            
            # Check if freighter collects the crate
            if self.freighter.alive and crate.rect.colliderect(self.freighter.rect):
                if crate.alive:
                    self.play_sound(self.loads.collect_crate_buffer, config.SOUND_COLLECT_CRATE_VOLUME)
                crate.alive = False
            
            if not crate.alive:
                self.cratebox.remove(crate)
                
                # Check win condition
                if len(self.cratebox) == 0 and self.freighter.alive:
                    self.engageable = False
                    self.you_win = True
                    self.level_up()
    
    def run_explosions(self):
        """Updates and draws explosions."""
        for boom in self.boombox[:]:
            boom.update()
            self.window.blit(boom.image, boom.rect)
            
            if not boom.alive:
                self.boombox.remove(boom)
    
    def run_freighter(self):
        """Updates and draws the freighter."""
        self.freighter.update()
        if self.freighter.alive:
            self.window.blit(self.freighter.image, self.freighter.rect)
    
    def run_force_field(self):
        """Updates and draws the force field and bases."""
        self.ff_blink()
        pygame.draw.rect(self.window, self.force_color, self.force_rect)
        self.window.blit(self.lbase_image, self.lbase_rect)
        self.window.blit(self.rbase_image, self.rbase_rect)
    
    def run_lasers(self):
        """Updates and draws lasers, handles collisions."""
        for laser in self.laserbox[:]:
            laser.update()
            self.window.blit(laser.image, laser.rect)
            
            # Check collisions with rocks
            for rock in self.rockbox:
                laser_collide(laser, rock)
            
            if not laser.alive:
                self.laserbox.remove(laser)
    
    def run_rocks(self):
        """Updates and draws rocks, handles collisions."""
        for rock1 in self.rockbox[:]:
            rock1.update()
            self.window.blit(rock1.image, rock1.rect)
            
            # Check collisions with other rocks
            for rock2 in self.rockbox:
                if rock1 != rock2:
                    bounce_rocks(rock1, rock2)
            
            # Check collision with freighter
            if self.engageable and self.freighter.alive and rock1.rect.colliderect(self.freighter.rect):
                if rock1.alive:
                    self.play_sound(self.loads.shield_hit_buffer, config.SOUND_SHIELD_HIT_VOLUME)
                rock1.alive = False
                self.freighter.hp -= rock1.atk
                self.freighter.struck = True
            
            if not rock1.alive:
                self.boombox.append(Boom(self, rock1.size, rock1.rect))
                self.rockbox.remove(rock1)
        
        # Destroy all rocks if level won
        if self.you_win and len(self.rockbox) > 0 and self.time - self.all_rock_blast_time >= config.LEVEL_WIN_ROCK_DESTROY_DELAY:
            if self.rockbox:
                self.rockbox[0].alive = False
            self.all_rock_blast_time = self.time
    
    def set_health_bar(self):
        """Updates and draws the health bar."""
        hp_bar_base_width = self.freighter.rect.width - config.HEALTH_BAR_WIDTH_OFFSET
        self.r_hp_bar.x = self.freighter.rect.x + config.HEALTH_BAR_OFFSET_X
        self.r_hp_bar.y = self.freighter.rect.y + self.freighter.rect.height + config.HEALTH_BAR_OFFSET_Y
        self.r_hp_bar.width = hp_bar_base_width
        
        self.g_hp_bar.x = self.freighter.rect.x + config.HEALTH_BAR_OFFSET_X
        self.g_hp_bar.y = self.freighter.rect.y + self.freighter.rect.height + config.HEALTH_BAR_OFFSET_Y
        # Scale green bar based on HP percentage
        hp_ratio = self.freighter.hp / self.freighter.max_hp if self.freighter.max_hp > 0 else 0
        self.g_hp_bar.width = int(hp_bar_base_width * hp_ratio)
        
        if self.freighter.alive:
            pygame.draw.rect(self.window, (255, 0, 0), self.r_hp_bar)
            pygame.draw.rect(self.window, (0, 255, 0), self.g_hp_bar)
    
    def shoot_laser(self):
        """Creates a new laser projectile."""
        # Check cooldown before allowing shot
        if (self.engageable and self.freighter.alive and 
            self.time - self.last_laser_shot_time >= config.LASER_SHOT_COOLDOWN):
            self.laserbox.append(Laser(self))
            self.last_laser_shot_time = self.time
    
    def run(self):
        """Main game loop."""
        # Start music
        pygame.mixer.music.load(self.loads.techno_beat)
        pygame.mixer.music.set_volume(config.MUSIC_VOLUME)
        pygame.mixer.music.play(-1)  # Loop forever
        self.music_playing = True
        
        running = True
        
        while running:
            # Update time
            self.time = pygame.time.get_ticks()
            
            # Handle freighter movement
            self.freighter_movement()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.shoot_laser()
                    elif event.key == pygame.K_F12:
                        # Toggle music
                        if self.music_playing:
                            pygame.mixer.music.stop()
                            self.music_playing = False
                        else:
                            pygame.mixer.music.play(-1)
                            self.music_playing = True
                        self.loads.update_music_text(self.music_playing)
                    elif event.key == pygame.K_F5:
                        if self.you_win_game or self.you_lose:
                            self.level = 1
                            self.level_setup()
                        elif self.you_win:
                            self.level_setup()
                
                elif event.type == pygame.KEYUP:
                    # Stop movement when keys released
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        self.freighter.x_velocity = 0
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.freighter.x_velocity = 0
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        self.freighter.y_velocity = 0
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.freighter.y_velocity = 0
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.shoot_laser()
            
            # Clear screen
            self.window.fill((0, 0, 0))
            
            # Draw bottom text
            self.print_bottom_text()
            
            # Update and draw game entities
            self.destroy_sounds()
            self.run_force_field()
            self.run_lasers()
            self.run_freighter()
            self.set_health_bar()
            self.run_rocks()
            self.run_crates()
            self.run_explosions()
            self.refill_rocks()
            
            # Draw top text
            self.print_top_text()
            
            # Update display
            pygame.display.flip()
            
            # Cap framerate
            self.clock.tick(config.TARGET_FPS)
        
        pygame.quit()

