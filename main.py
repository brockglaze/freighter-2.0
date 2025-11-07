"""
Main entry point for the Freighter game.
"""

import random
from game import Game


def main():
    """Initialize random seed and start the game."""
    random.seed()
    
    # Create and run the game
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

