#Imports + setup
import pygame as pg
import math

import object
import board
import ui
import settings

pg.init()

#Restart var
restart = False
#Creates screen
screen = pg.display.set_mode(settings.size)
pg.display.set_caption("Minesweeper")

#Main function
def main():
  #Board sizes + mine counts (same as google minesweeper)
  board_info = {
    "easy" : (10, 8, 10),
    "medium" : (18, 14, 40),
    "hard" : (24, 20, 99)
  }
  
  #Creates timer and flag counter
  timer = ui.Timer()
  flag_counter = ui.FlagCounter(board_info[settings.difficulty][2])
  #Creates fps counter
  fps_counter = object.Text((0, 0), "FPS 0", 10, layer=1)
  fps_counter.rect.topleft = (2, 2)

  #Creates restart button
  restart_button = object.Image((0, 0), "restart.png", layer=1)
  restart_button.rect.topright = (settings.width - 4, 4)
  #Creates loss and win messages
  loss_text = object.Rectangle((settings.width/2, settings.height/2), (100, 35), text="BOOM!", text_color="red", group=False, layer=1)
  win_text = object.Rectangle((settings.width/2, settings.height/2), (100, 35), text="CLEAR!", text_color="green", group=False, layer=1)

  #Difficulty selector
  diff_select = ui.Difficulty_selector()
  
  #Creates board
  game_board = board.Board(*board_info[settings.difficulty], flag_counter, loss_text, win_text)

  #Vars for loop
  global restart
  clock = pg.time.Clock()
  running = True
  #Game loop
  while running:
    #Max 60 fps
    clock.tick(60)

    
    #Event loop
    for event in pg.event.get():
      #Quit
      if event.type == pg.QUIT:
        running = False
      #Restart game
      if restart_button.rect.collidepoint(pg.mouse.get_pos()):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
          running = False
          restart = True
      #Dev reveal
      if event.type == pg.KEYDOWN and event.key == pg.K_x:
        game_board.dev_reveal()
          
      #Difficulty selector
      for button in diff_select.buttons:
        if button.rect.collidepoint(pg.mouse.get_pos()):
          if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            diff_changed = diff_select.select_difficulty(button)
            if diff_changed:
              running = False
              restart = True

      #Searchs for actions on all squares
      for square in game_board.flat_matrix:
        if square.rect.collidepoint(pg.mouse.get_pos()):
          #If left click
          if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            #Reveal
            square.reveal()
          #If right click
          elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            #Switch flag state
            square.switch_flag_state()
          #If unrevealed (green) square
          elif square.revealed == False:
            #Move hover to correct pos
            game_board.hover.rect.center = square.rect.center

    #Updates ingame clock, flag counter, and fps counter
    timer.update_time()
    flag_counter.update_count()
    fps_counter.update(f"FPS {math.floor(clock.get_fps())}")

    #Reaveals all mines (if game is over)
    game_board.reveal_all_mines()
    
    #Background
    screen.fill("gray60")
    #Draw all game objects
    object.objects.draw(screen)
    #Updates screen
    pg.display.update()

#Runs game
if __name__ == "__main__":
  main()
  #If restarting
  while restart:
    #Cleans up vars
    restart = False
    settings.player_alive = True
    object.objects = pg.sprite.LayeredUpdates()
    settings.dead_time = pg.time.get_ticks()
    #Relaunchs main()
    main()


#Need to add smart reveal for first hit
#Could add some type of flag fall animation + a you clicked this mine and blew up red overlay