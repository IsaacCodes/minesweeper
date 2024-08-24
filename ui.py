#Imports + setup
import pygame as pg
import math

import object
import settings

pg.init()

class Timer(object.Text):
  #Creates text
  def __init__(self):
    super().__init__((settings.width/2-100, 25), "Time: 000", layer=1)
    
  #Changes time
  def update_time(self):
    #Doesn't update time if game is over
    if not settings.player_alive:
      return
    #Gets new text
    time = math.floor((pg.time.get_ticks() - settings.dead_time)/1000)
    text = f"Time: {str(time).zfill(3)}"
    #Updates object
    self.update(text)


class FlagCounter(object.Text):
  def __init__(self, max_flags):
    #Creates text
    super().__init__((settings.width/2+100, 25), f"Flags: {max_flags}", layer=1)
    self.max_flags = max_flags
    self.placed_flags = 0

    #Flag image
    self.flag_image = object.Image((settings.width/2+35, 25), "flag.png", layer=1)
    
  #Changes count
  def update_count(self):    
    #Gets new text
    text = f"Flags: {self.max_flags - self.placed_flags}"
    #Updates object
    self.update(text)

class Difficulty_selector():
  def __init__(self):
    #X positions for the buttons. Used for button selected placement
    self.x_positions = {
      "easy" : 20,
      "medium" : 40,
      "hard" : 60
    }
    #Circle buttons for difficulty
    self.easy_button = object.Circle((self.x_positions["easy"], 30), 14, color="white", border_size=2, border_color="black", layer=1)
    self.medium_button = object.Circle((self.x_positions["medium"], 30), 14, color="white", border_size=2, border_color="black", layer=1)
    self.hard_button = object.Circle((self.x_positions["hard"], 30), 14, color="white", border_size=2, border_color="black", layer=1)
    #Circle text for the difficulties
    self.easy_text = object.Text((20, 41), "Easy", 10, layer=1)
    self.medium_text = object.Text((40, 18), "Mid", 10, layer=1)
    self.hard_text = object.Text((60, 41), "Hard", 10, layer=1)
    #Button group
    self.buttons = [self.easy_button, self.medium_button, self.hard_button]

    #Button selected
    self.button_selected_circle = object.Circle((self.x_positions[settings.difficulty], 30), 10, color="red", layer=1)
    
  def select_difficulty(self, button):
    #Moves button selected
    self.button_selected_circle.rect.center = button.rect.center
    #Updates difficulty
    old_difficulty = settings.difficulty
    if button == self.easy_button:
      settings.difficulty = "easy"
    elif button == self.medium_button:
      settings.difficulty = "medium"
    else:
      settings.difficulty = "hard"
    #Returns whether difficulty has changed
    if settings.difficulty != old_difficulty:
      return True
    return False