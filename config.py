"""
Game configuration file.
Edit these values to customize game behavior and difficulty.
"""

# ============================================================================
# WINDOW SETTINGS
# ============================================================================

# Window dimensions (used as fallback if fullscreen fails)
WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 900
WINDOW_BITS_PER_PIXEL = 32

# Try fullscreen mode (True) or use windowed mode (False)
USE_FULLSCREEN = True


# ============================================================================
# FREIGHTER (PLAYER SHIP) SETTINGS
# ============================================================================

# Ship health
FREIGHTER_MAX_HP = 40.0

# Movement delay/throttle (lower = faster movement)
# This is the delay in milliseconds between movement updates
# Lower values make the ship move more frequently (smoother but more CPU-intensive)
FREIGHTER_MOVE_DELAY = 3  # Reduced from 5 for faster movement

# Movement distance per update (pixels)
FREIGHTER_X_SPEED = 5  # Increased from 2 for faster horizontal movement
FREIGHTER_Y_SPEED = 5  # Increased from 2 for faster vertical movement

# Shield blink timing (milliseconds)
FREIGHTER_BLINK_INTERVAL = 80
FREIGHTER_BLINK_COUNT_MAX = 4


# ============================================================================
# LASER SETTINGS
# ============================================================================

# Laser damage
LASER_DAMAGE = 18.0

# Movement delay/throttle (lower = faster movement)
# This is the delay in milliseconds between movement updates
# Lower values make the laser move more frequently (smoother but more CPU-intensive)
LASER_MOVE_DELAY = 1  # Reduced from 2 for faster laser movement

# Movement distance per update (pixels, moving upward)
LASER_Y_SPEED = 10  # Increased from 4 for faster laser speed

# Cooldown between shots (milliseconds)
# Higher values = slower fire rate (more delay between shots)
LASER_SHOT_COOLDOWN = 150  # Milliseconds between allowed shots

# Laser spawn offset from freighter (pixels)
LASER_SPAWN_OFFSET_X = 24
LASER_SPAWN_OFFSET_Y = -30


# ============================================================================
# ROCK SETTINGS
# ============================================================================

# Small rock stats
ROCK_SMALL_HP = 11.0
ROCK_SMALL_MOVE_SPEED_MIN = 18
ROCK_SMALL_MOVE_SPEED_MAX = 24
ROCK_SMALL_X_SPEED_MIN = 1
ROCK_SMALL_X_SPEED_MAX = 2
ROCK_SMALL_Y_SPEED_MIN = 1
ROCK_SMALL_Y_SPEED_MAX = 2

# Medium rock stats
ROCK_MEDIUM_HP = 18.0
ROCK_MEDIUM_MOVE_SPEED_MIN = 13
ROCK_MEDIUM_MOVE_SPEED_MAX = 17
ROCK_MEDIUM_X_SPEED_MIN = 1
ROCK_MEDIUM_X_SPEED_MAX = 2
ROCK_MEDIUM_Y_SPEED_MIN = 1
ROCK_MEDIUM_Y_SPEED_MAX = 2

# Large rock stats
ROCK_LARGE_HP = 30.0
ROCK_LARGE_MOVE_SPEED_MIN = 6
ROCK_LARGE_MOVE_SPEED_MAX = 12
ROCK_LARGE_X_SPEED = 1
ROCK_LARGE_Y_SPEED = 1

# Rock movement calculation base (used in move_interval calculation)
ROCK_MOVE_BASE = 300


# ============================================================================
# EXPLOSION SETTINGS
# ============================================================================

# Explosion duration (milliseconds)
EXPLOSION_DURATION = 150


# ============================================================================
# FORCE FIELD SETTINGS
# ============================================================================

# Force field blink duration (milliseconds)
FORCE_FIELD_BLINK_DURATION = 25


# ============================================================================
# LEVEL PROGRESSION SETTINGS
# ============================================================================

# Maximum level
MAX_LEVEL = 10

# Area modifier for calculating rock count per level
# Formula: total_rocks = level * AREA_MODIFIER_DIVISOR
# The actual divisor is calculated as: (window_width + window_height) / AREA_MODIFIER_DIVISOR
AREA_MODIFIER_DIVISOR = 250.0

# Rock destruction delay when level is won (milliseconds)
LEVEL_WIN_ROCK_DESTROY_DELAY = 100


# ============================================================================
# AUDIO SETTINGS
# ============================================================================

# Music volume (0.0 to 1.0)
MUSIC_VOLUME = 0.75

# Sound effect volumes (0.0 to 1.0)
SOUND_LASER_VOLUME = 1.0
SOUND_BOOM_VOLUME = 0.4
SOUND_SHIELD_HIT_VOLUME = 0.75
SOUND_COLLECT_CRATE_VOLUME = 1.0
SOUND_FORCE_FIELD_VOLUME = 0.3
SOUND_LEVEL_START_VOLUME = 1.0


# ============================================================================
# GAME TIMING SETTINGS
# ============================================================================

# Target FPS
TARGET_FPS = 60

# Rock spawn offset from top of screen (pixels)
ROCK_SPAWN_OFFSET_Y = -40

# Freighter boundary offset from bottom (pixels)
FREIGHTER_BOTTOM_OFFSET = 7

# Force field position offset from bottom (pixels)
FORCE_FIELD_OFFSET = 18

# Health bar offset from freighter (pixels)
HEALTH_BAR_OFFSET_X = 9
HEALTH_BAR_OFFSET_Y = 4
HEALTH_BAR_WIDTH_OFFSET = 18

