"""
Resource manager for loading all game assets (images, sounds, fonts).
"""

import pygame
import os


class Loads:
    """
    Resource manager that loads and initializes all game assets.
    """
    
    def __init__(self):
        # Get the base directory (parent of this file)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_dir, "assets")
        images_dir = os.path.join(assets_dir, "images")
        sounds_dir = os.path.join(assets_dir, "sounds")
        
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Load images and textures
        self._load_images(images_dir)
        
        # Load sounds
        self._load_sounds(sounds_dir)
        
        # Load fonts (use default pygame font)
        self.game_font1 = pygame.font.Font(None, 36)
        self.game_font_large = pygame.font.Font(None, 75)
        self.game_font_medium = pygame.font.Font(None, 40)
        self.game_font_small = pygame.font.Font(None, 20)
        self.game_font_tiny = pygame.font.Font(None, 15)
        
        # Text surfaces will be created in game_text_config
        self.level_text = None
        self.music_text = None
        self.lose_text = None
        self.restart_text = None
        self.win_text = None
        self.advance_text = None
        self.congrats_text = None
        self.win_game_text = None
        self.play_again_text = None
        
        self.game = None
    
    def _load_images(self, images_dir):
        """Load all image files and create textures with transparency."""
        # Helper function to load image with color key transparency
        def load_image_with_mask(filename):
            path = os.path.join(images_dir, filename)
            if not os.path.exists(path):
                raise FileNotFoundError(f"Image not found: {path}")
            image = pygame.image.load(path).convert_alpha()
            # Set color key to top-left pixel (like SFML CreateMaskFromColor)
            if image.get_width() > 0 and image.get_height() > 0:
                color_key = image.get_at((0, 0))
                image.set_colorkey(color_key)
            return image
        
        # Load all textures
        self.tex_crate = load_image_with_mask("crate.png")
        self.tex_freighter = load_image_with_mask("falcon.png")
        self.tex_freighter_blink = load_image_with_mask("falcon_shield.png")
        self.tex_laser = load_image_with_mask("laser.png")
        self.tex_lg_rock = load_image_with_mask("lg_rock.png")
        self.tex_lg_rock2 = load_image_with_mask("lg_rock_damaged.png")
        self.tex_md_rock = load_image_with_mask("md_rock.png")
        self.tex_sm_rock = load_image_with_mask("sm_rock.png")
        self.tex_lg_explode = load_image_with_mask("lg_explode.png")
        self.tex_sm_explode = load_image_with_mask("sm_explode.png")
        self.tex_lbase = pygame.image.load(os.path.join(images_dir, "lbase.png")).convert_alpha()
        self.tex_rbase = pygame.image.load(os.path.join(images_dir, "rbase.png")).convert_alpha()
        
        # Game icon (for window icon if needed)
        icon_path = os.path.join(images_dir, "..", "icon.png")
        if os.path.exists(icon_path):
            self.img_game_icon = pygame.image.load(icon_path).convert_alpha()
        else:
            # Create a simple icon if not found
            self.img_game_icon = pygame.Surface((32, 32))
            self.img_game_icon.fill((100, 100, 200))
    
    def _load_sounds(self, sounds_dir):
        """Load all sound files."""
        self.boom_buffer = pygame.mixer.Sound(os.path.join(sounds_dir, "boom.wav"))
        self.laser_buffer = pygame.mixer.Sound(os.path.join(sounds_dir, "laser.wav"))
        self.shield_hit_buffer = pygame.mixer.Sound(os.path.join(sounds_dir, "shield_hit.wav"))
        self.collect_crate_buffer = pygame.mixer.Sound(os.path.join(sounds_dir, "crate_collected.wav"))
        self.force_field_buffer = pygame.mixer.Sound(os.path.join(sounds_dir, "zap.wav"))
        self.level_start = pygame.mixer.Sound(os.path.join(sounds_dir, "level_start.wav"))
        
        # Music (streaming)
        music_path = os.path.join(sounds_dir, "music.wav")
        self.techno_beat = music_path  # Store path for pygame.mixer.music
    
    def game_text_config(self, game):
        """Configure all text surfaces based on game window dimensions."""
        self.game = game
        window_width = game.window.get_width()
        window_height = game.window.get_height()
        
        # Level text
        self.level_text = self.game_font_small.render("Zone: 1", True, (255, 255, 255))
        self.level_text_pos = (60, window_height - self.level_text.get_height() - 10)
        
        # Music text
        self.music_text = self.game_font_tiny.render("Music: Playing | F12", True, (255, 255, 255))
        self.music_text_pos = (window_width - self.music_text.get_width() - 60,
                               window_height - self.music_text.get_height() - 10)
        
        # Lose text
        self.lose_text = self.game_font_large.render("You Lose!", True, (255, 255, 255))
        self.lose_text_pos = (window_width // 2 - self.lose_text.get_width() // 2,
                              window_height // 4)
        
        # Restart text
        self.restart_text = self.game_font_medium.render("Press F5 to Restart", True, (255, 255, 255))
        self.restart_text_pos = (window_width // 2 - self.restart_text.get_width() // 2,
                                 self.lose_text_pos[1] + self.lose_text.get_height() + 20)
        
        # Win text
        self.win_text = self.game_font_large.render("You Win!", True, (255, 255, 255))
        self.win_text_pos = (window_width // 2 - self.win_text.get_width() // 2,
                             window_height // 4)
        
        # Advance text
        self.advance_text = self.game_font_medium.render("Press F5 to Advance", True, (255, 255, 255))
        self.advance_text_pos = (window_width // 2 - self.advance_text.get_width() // 2,
                                 self.win_text_pos[1] + self.win_text.get_height() + 20)
        
        # Congrats text
        self.congrats_text = self.game_font_large.render("Congratulations!", True, (255, 255, 255))
        self.congrats_text_pos = (window_width // 2 - self.congrats_text.get_width() // 2,
                                  window_height // 4)
        
        # Win game text
        self.win_game_text = self.game_font_large.render("You Beat the Game!", True, (255, 255, 255))
        self.win_game_text_pos = (window_width // 2 - self.win_game_text.get_width() // 2,
                                   self.congrats_text_pos[1] + self.congrats_text.get_height() + 20)
        
        # Play again text
        self.play_again_text = self.game_font_medium.render("Press F5 to Play Again", True, (255, 255, 255))
        self.play_again_text_pos = (window_width // 2 - self.play_again_text.get_width() // 2,
                                     self.win_game_text_pos[1] + self.win_game_text.get_height() + 20)
    
    def update_level_text(self, level):
        """Update the level text with the current level number."""
        self.level_text = self.game_font_small.render(f"Zone: {level}", True, (255, 255, 255))
    
    def update_music_text(self, playing):
        """Update the music status text."""
        status = "Playing" if playing else "Stopped"
        self.music_text = self.game_font_tiny.render(f"Music: {status} | F12", True, (255, 255, 255))

