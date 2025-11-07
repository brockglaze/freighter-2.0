"""
Utility functions for the Freighter game.
"""

import random
import math


# Direction and size constants
NONE = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
DOWNLEFT = 5
DOWNRIGHT = 6
UPLEFT = 7
UPRIGHT = 8
SMALL = 9
MEDIUM = 10
LARGE = 11


def rand_int(a, b):
    """Generates a random integer between a and b (inclusive)."""
    return random.randint(a, b)


def round_num(n):
    """Rounds a float to the nearest integer."""
    return round(n)


def bounce_rocks(rock1, rock2):
    """
    Checks if two rocks collide and bounces the smaller one accordingly.
    Changes the direction of rock1 if it collides with rock2 and rock1 is smaller or equal size.
    """
    if rock1.rect.colliderect(rock2.rect):
        # Check collision from top
        if (rock1.rect.top <= rock2.rect.bottom and 
            rock1.rect.bottom >= rock2.rect.bottom and 
            rock1.size <= rock2.size):
            if rock1.direction == UPRIGHT:
                rock1.direction = DOWNRIGHT
            elif rock1.direction == UPLEFT:
                rock1.direction = DOWNLEFT
        
        # Check collision from bottom
        if (rock1.rect.bottom >= rock2.rect.top and 
            rock1.rect.top <= rock2.rect.top and 
            rock1.size <= rock2.size):
            if rock1.direction == DOWNRIGHT:
                rock1.direction = UPRIGHT
            elif rock1.direction == DOWNLEFT:
                rock1.direction = UPLEFT
        
        # Check collision from right
        if (rock1.rect.right >= rock2.rect.left and 
            rock1.rect.left <= rock2.rect.left and 
            rock1.size <= rock2.size):
            if rock1.direction == DOWNRIGHT:
                rock1.direction = DOWNLEFT
            elif rock1.direction == UPRIGHT:
                rock1.direction = UPLEFT
        
        # Check collision from left
        if (rock1.rect.left <= rock2.rect.right and 
            rock1.rect.right >= rock2.rect.right and 
            rock1.size <= rock2.size):
            if rock1.direction == DOWNLEFT:
                rock1.direction = DOWNRIGHT
            elif rock1.direction == UPLEFT:
                rock1.direction = UPRIGHT


def laser_collide(laser, rock):
    """
    Checks if a laser collides with a rock.
    If so, damages the rock and destroys the laser.
    """
    if laser.rect.colliderect(rock.rect):
        rock.hp -= laser.atk
        laser.alive = False

