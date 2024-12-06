import pygame
import game

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
GRID_WIDTH = 10
GRID_HEIGHT = 10
CELL_MARGIN = 0

if __name__ == "__main__":
    game.loop(pygame,
              WINDOW_WIDTH,
              WINDOW_HEIGHT,
              GRID_WIDTH,
              GRID_HEIGHT,
              CELL_MARGIN
              )
