#Imports + setup
import pygame as pg

import settings

pg.init()


#List of all game objects
objects = pg.sprite.LayeredUpdates()

#Basic object class
class Object(pg.sprite.Sprite):
  def __init__(self, pos: "tuple[int, int]", group: bool, layer: int):
    #Sprite class parent
    super().__init__()
    #Converts image type + alpha
    self.image = self.image.convert_alpha()
    #Creates a rect from the surface
    self.rect = self.image.get_rect(center=pos)

    #Assigns layer and adds player to objects list
    self._layer = layer
    if group:
      objects.add(self)

#Text class
class Text(Object):
  def __init__(self, pos=(0, 0), text="", text_size=24, text_color="black", group=True, layer=0):
    #Creates font image
    self.image = settings.font(text_size).render(text, True, text_color)
    #Stores vars
    self.text = text
    self.text_size = text_size
    self.text_color = text_color

    #Object parent
    super().__init__(pos, group, layer)

  def update(self, new_text):
    #If text is changing
    if new_text != self.text:
      #Store and updates the text
      self.text = new_text
      self.image = settings.font(self.text_size).render(new_text, True, self.text_color)
  

#Rectangle class
class Rectangle(Object):
  def __init__(self, pos=(0, 0), size=(25, 25), color="black", border_size=0, border_color="black", corner_rounding=0, text="", text_size=24, text_color="black", group=True, layer=0):
    #Creates the base rectangle
    self.image = pg.Surface(size, pg.SRCALPHA)
    pg.draw.rect(self.image, color, pg.Rect(0, 0, size[0], size[1]), 0, corner_rounding)
    #If there is a border
    if border_size != 0:
      #Draw a border onto the rectangle
      pg.draw.rect(self.image, border_color, pg.Rect(0, 0, size[0], size[1]), border_size, corner_rounding)

    #Object parent (done before adding text so self.rect may be used)
    super().__init__(pos, group, layer)

    #Creates text and adds its image
    if text != "":
      self.text = Text(pos, text, text_size, text_color, group=False, layer=layer)
      #Finds upper left position where text is blitted
      blit_pos = (self.text.rect.left - self.rect.left, self.text.rect.top - self.rect.top)
      self.image.blit(self.text.image, blit_pos)

  #Updates text
  def update_text(self, new_text):
    self.text.update(new_text)
    blit_pos = (self.text.rect.left - self.rect.left, self.text.rect.top - self.rect.top)
    self.image.blit(self.text.image, blit_pos)

#Circle class
class Circle(Object):
  def __init__(self, pos=(0, 0), diameter=1, color="black", border_size=0, border_color="black", group=True, layer=0):    
    #Alpha compatible image + draw circle on it
    self.image = pg.Surface((diameter, diameter), pg.SRCALPHA)
    image_center = self.image.get_rect().center
    pg.draw.circle(self.image, color, image_center, diameter/2-border_size)
    #Draw interior circle when there is a border
    if border_size != 0:
      pg.draw.circle(self.image, border_color, image_center, diameter/2, width=border_size)

    #Object parent
    super().__init__(pos, group, layer)

#Custom image class
class Image(Object):
  def __init__(self, pos=(0, 0), file="flag.png", size=(0, 0), group=True, layer=0):
    #Loads image
    self.image = pg.image.load(f"{settings.dir}//images//{file}")
      
    #Changes the size
    if size != (0, 0):
      self.image = pg.transform.smoothscale(self.image, size)

    #Object parent
    super().__init__(pos, group, layer)