#Imports + setup
import pygame as pg
import os

pg.init()

#Set screen size
size = width, height = 540, 500

#Finds current directory
dir = os.path.dirname(os.path.realpath(__file__))

#Game font
def font(size: int):
  font = pg.font.Font('freesansbold.ttf', size)
  return font

#Dead time that is removed from the clock between main() cycles
dead_time = 0

#Game board difficulty, hard by defualt
difficulty = "hard"

#Whether or not the game has ended
player_alive = True