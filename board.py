#Imports + setup
import pygame as pg
import random as r

import object
import settings

pg.init()

#Individual square class
class Square(object.Rectangle):
  def __init__(self, pos, size, color, board, matrix_pos):
    #Creates the square
    super().__init__(pos, (size, size), color)

    #Gives the square a flag (hidden by defualt)
    self.flag = object.Image(pos, "flag.png", group=False)

    #All potential mine colors (green, blue, purple, red, pink, orange, yellow)
    mine_colors = [(0, 135, 68), (72, 133, 237), (182, 72, 242), (197, 45, 49), 
                   (237, 68, 181), (244, 132, 13), (244, 180, 0)]
    #Gives square a mine object (only used when has_mine is true)
    self.mine = object.Circle(pos, size/2, r.choice(mine_colors), group=False)

    #Block states
    self.board = board
    self.has_mine = False
    self.flagged = False
    self.revealed = False
    self.number = 0
    self.matrix_pos = matrix_pos

  #Finds the positions of nearby squares
  def find_near_squares(self):
    #Loops thru pos_diff in x and y
    pos_diff = [-1, 0, 1]
    pos_list = []
    for x in pos_diff:
      for y in pos_diff:
        #Finds the positions of the nearby squares
        new_pos = [x + self.matrix_pos[0], y + self.matrix_pos[1]]

        #Ignores when same pos
        if self.matrix_pos == new_pos:
          continue
        #Prevents index out of range for left and right side squares
        if new_pos[0] == -1 or new_pos[0] == self.board.size[0]:
          continue
        #Prevents index out of range for top and bottom side squares
        if new_pos[1] == -1 or new_pos[1] == self.board.size[1]:
          continue
          
        pos_list.append(new_pos)
        
    return pos_list
  
  #Finds the number of squares nearby (self.number), done after all sqaures created
  def find_number(self):
    for pos in self.find_near_squares():
      #Iterates number based on has_mine for this nearby square
      self.number += self.board.matrix[pos[0]][pos[1]].has_mine


  #Switches flagged
  def switch_flag_state(self, force_off=False):
    #Disabled when revealed or after losing
    if self.revealed or not settings.player_alive:
      return

    #If on
    if self.flagged:
      self.flagged = False
      object.objects.remove(self.flag)
      self.board.flag_counter.placed_flags -= 1
    #If force_off
    elif force_off:
      self.flagged = False
      object.objects.remove(self.flag)
    #If off, turn on
    elif self.board.flag_counter.placed_flags < self.board.flag_counter.max_flags: 
      self.flagged = True
      object.objects.add(self.flag)
      self.board.flag_counter.placed_flags += 1

  #Reveals a square on the board
  def reveal(self):
    #Disabled when flagged, already revealed, or after losing
    if self.flagged or self.revealed or not settings.player_alive:
      return
    
    #If no mine
    if not self.has_mine:
      #Set image to numbered rectangle
      pos = self.rect.centerx, self.rect.centery
      size = self.rect.width, self.rect.height
      #Switches color
      color = (215, 185, 155)
      if self.matrix_pos[0] % 2 == self.matrix_pos[1] % 2:
        color = (230, 195, 160)
      
      #Text colors based on number
      text_colors = {
        0 : color, 1 : (29,119,208), 2 : (72,147,69), 
        3 : (211,50,50), 4 : (123,31,162), 5 : (253,145,7), 
        6 : (0,147,177), 7 : "black", 8 : "gray"
      }
      
      #Replaces image
      super().__init__(pos, size, color, text=str(self.number), text_size=18, text_color=text_colors[self.number])

      #Switches vars
      self.switch_flag_state(True)
      self.revealed = True
      #Hides hover
      self.board.hover.rect.center = (-100, -100) 

      #Searches and reveals nearby squares
      if self.number == 0:
        for pos in self.find_near_squares():
          near_square = self.board.matrix[pos[0]][pos[1]]
          near_square.switch_flag_state(True)
          near_square.reveal()

      #Checks to see if player has won
      self.board.check_win()
      
    #If there is a mine
    else:
      object.objects.add(self.mine)
      object.objects.add(self.board.loss_text)
      settings.player_alive = False


#Board class
class Board():
  def __init__(self, rows: int, columns: int, mine_count: int, flag_counter, loss_text, win_text, square_size = 20, pos = (settings.width/2, settings.height/2)):
    #Board matrix info
    self.matrix = []
    self.size = rows, columns
    self.mine_count = mine_count
    #Refrenced by squares and other functions
    self.flag_counter = flag_counter
    self.loss_text = loss_text
    self.win_text = win_text
    #States used when revealing all squares
    self.last_reveal_time = -1000
    self.reveal_index = 0
    self.done_revealing = False
    
    #Loops thru items for the matrix
    for x in range(rows):
      self.matrix.append([])
      for y in range(columns):
        #Alternates color
        color = (170, 220, 80)
        if x % 2 == y % 2:
          color = (160, 210, 75)
        #Finds position (center + square_size * (row_num - row_count/2 + 0.5 ))
        square_pos = pos[0] + square_size*(x-rows/2+0.5), pos[1] + square_size*(y-columns/2+0.5)
        #Creates square + adds to matrix
        square = Square(square_pos, square_size, color, self, (x, y))
        self.matrix[x].append(square)

    #A square for the on hover effect (offscreen by defualt)
    self.hover = object.Rectangle((-100, -100), (square_size, square_size), color=(255,255,255,80))

    #Creates a flattened matrix
    self.flat_matrix = [square for column in self.matrix for square in column]
    #Assigns mine_count randomly placed squares in the matrix to have mines
    mine_squares = r.sample(self.flat_matrix, mine_count)
    for square in mine_squares:
      square.has_mine = True
    
    #Assigns the squares values
    for square in self.flat_matrix:
      square.find_number()

  #Reveals all mines after game loss, is repeatedly called in main()
  def reveal_all_mines(self):
    #Vars
    current_time = pg.time.get_ticks()
    current_square = self.flat_matrix[self.reveal_index]
    #If off reveal cd and game is over
    if self.last_reveal_time + 75 < current_time and not settings.player_alive and not self.done_revealing:
      #Increments until valid mine found
      while not current_square.has_mine or object.objects.has(current_square.mine):
        #Returns and ends revealing once all mines reavealed
        if self.reveal_index == len(self.flat_matrix) - 1:
          self.done_revealing = True
          return
        #Increment square count
        self.reveal_index += 1
        current_square = self.flat_matrix[self.reveal_index]

      #After finding valid mine, add it, remove potential falgs, then update time
      object.objects.add(current_square.mine)
      if object.objects.has(current_square.flag):
        object.objects.remove(current_square.flag)
      self.last_reveal_time = current_time

  #Checks if you have won
  def check_win(self):
    #Stores revealed square count
    revealed_count = 0
    #Loops and checks for revealed squares
    for square in self.flat_matrix:
      revealed_count += square.revealed

    #Sees if all squares were revealed
    if revealed_count == self.size[0]*self.size[1] - self.mine_count:
      object.objects.add(self.win_text)
      settings.player_alive = False

  #For dev testing, actived by key "x"
  def dev_reveal(self):
    for square in self.flat_matrix:
      if square.has_mine:
        square.switch_flag_state()
      continue
      
      if not square.has_mine:
        flagged = False
        if square.flagged:
          flagged = True
          square.switch_flag_state()
        square.reveal()
        if flagged:
          square.switch_flag_state()