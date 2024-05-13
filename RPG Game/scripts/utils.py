import os
from copy import deepcopy

import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
  img = pygame.image.load(BASE_IMG_PATH + path).convert()
  img.set_colorkey((0, 0, 0))
  return img

def load_images(path):
  imgs = []
  for img in os.listdir(BASE_IMG_PATH + path):
    imgs.append(load_image(path + '/' + img))
  return imgs

def getWidth(game, string):
  total = 0
  for c in string:
    if c == ' ':
      total += 3
    else:
      total += game.font_dat[c][0]
  return total

def blur(surface, radius):
  scaled_surface = pygame.transform.smoothscale(surface, (surface.get_width() // radius, surface.get_height() // radius))
  scaled_surface = pygame.transform.smoothscale(scaled_surface, (surface.get_width(), surface.get_height()))
  return scaled_surface

class Button:
  def __init__(self, text, pos, img, drawText=False):
    self.text = text
    self.pos = list(pos)
    self.img = img
    self.drawText = drawText

  def rect(self):
    return pygame.Rect(self.pos[0], self.pos[1], self.img.get_width(), self.img.get_height())
  
  def hover(self, scale):
    mpos = list(pygame.mouse.get_pos())
    mpos[0] = mpos[0] // scale
    mpos[1] = mpos[1] // scale
    return self.rect().collidepoint(mpos)
  
  def render(self, win, game, double=4):
    win.blit(self.img, self.pos) # draw the image to screen
    if self.drawText:
      game.font.render(self.text,  self.pos[0] + 110 - (getWidth(game, self.text) * double) // 2, self.pos[1] + 64 - 2*double, 1, 256, win, double=double)

class TextBox:
  def __init__(self, texts, font, pos=[20, 450], size=[1240, 180]):
    self.texts = list(texts)
    self.font = font
    self.currText = ""
    self.currIndex = 0
    self.currTextIndex = 0
    self.nextLetter = 0
    self.writingSpeed = 5 # the lower the quicker

    self.pos = list(pos)
    self.size = list(size)

    self.box = pygame.Surface((self.size), pygame.SRCALPHA)
    self.box.set_alpha(127)
    self.box.fill((0, 0, 0))

    self.active = False
    self.done = False
    
  def update(self, nextText=False):
    if not self.active or self.done:
      return
    if nextText:
      self.currText = ""
      self.currIndex += 1
      self.currTextIndex = 0
      if self.currIndex >= len(self.texts):
        self.done = True
        return

    if self.nextLetter%(self.writingSpeed) == 0 and self.currTextIndex < len(self.texts[self.currIndex]):
      self.currText += self.texts[self.currIndex][self.currTextIndex]
      self.currTextIndex += 1
    self.nextLetter =  (self.nextLetter + 1) % (self.writingSpeed)

  def render(self, win):
    if not self.active or self.done:
      return
    win.blit(self.box, self.pos)
    double = 4
    self.font.render(self.currText, self.pos[0] + 20, self.pos[1] + 20, 1, 1200, win, double=double)
    

class Animation:
  def __init__(self, images, img_dur=10, loop=True):
    self.images = images
    self.loop = loop
    self.img_duration = img_dur
    self.done = False
    self.frame = 0
  
  def copy(self):
    return Animation(self.images, self.img_duration, self.loop)
  
  def update(self):
    if self.loop:
      self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
    else:
      self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
      if self.frame >= self.img_duration * len(self.images) - 1:
        self.done = True

  def img(self):
    return self.images[int(self.frame / self.img_duration)]

class Font:
  def __init__(self, FontImage, FontSpacingMain, TileSize, TileSizeY, color):
    FontSpacing = deepcopy(FontSpacingMain)
    FontOrder = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.-,:+\'!?0123456789()/_=\\[]*"<>;')
    FontImage = pygame.image.load(FontImage).convert()
    NewSurf = pygame.Surface((FontImage.get_width(), FontImage.get_height())).convert()
    NewSurf.fill(color)
    FontImage.set_colorkey((0, 0, 0))
    NewSurf.blit(FontImage, (0, 0))
    FontImage = NewSurf.copy()
    FontImage.set_colorkey((255, 255, 255))
    num = 0
    for char in FontOrder:
      rect = pygame.Rect(((TileSize+1)*num), 0, TileSize, TileSizeY)
      FontImage.set_clip(rect)
      clip = FontImage.get_clip()
      CharacterImage = FontImage.subsurface(clip)
      FontSpacing[char].append(CharacterImage)
      num += 1
    FontSpacing['Height'] = TileSizeY
    self.font = FontSpacing
  
  def render(self, Text, X, Y, Spacing, WidthLimit, surface, double=1, overflow='normal'):
    Font = self.font
    Text += ' '
    if double != 1:
      X = int(X/double)
      Y = int(Y/double)
    OriginalX = X
    OriginalY = Y
    CurrentWord = ''
    if overflow == 'normal':
      for char in Text:
        if char not in [' ', '\n']:
          try:
            Image = Font[str(char)][1]
            CurrentWord += str(char)
          except KeyError:
            pass
        else:
          WordTotal = 0
          for char2 in CurrentWord:
            WordTotal += Font[char2][0]
            WordTotal += Spacing
          if WordTotal+X-OriginalX > WidthLimit:
            X = OriginalX
            Y += Font['Height']
          for char2 in CurrentWord:
            Image = Font[str(char2)][1]
            surface.blit(pygame.transform.scale(Image, (Image.get_width()*double, Image.get_height()*double)), (X*double, Y*double))
            X += Font[char2][0]
            X += Spacing
          if char == ' ':
            X += Font['A'][0]
            X += Spacing
          else:
            X = OriginalX
            Y += Font['Height']
          CurrentWord = ''
        if X-OriginalX > WidthLimit:
          X = OriginalX
          Y += Font['Height']
      return X, Y
    if overflow == 'cut all':
      for char in Text:
        if char not in [' ', '\n']:
          try:
            Image = Font[str(char)][1]
            surface.blit(pygame.transform.scale(Image, (Image.get_width()*double, Image.get_height()*double)), (X*double, Y*double))
            X += Font[str(char)][0]
            X += Spacing
          except KeyError:
            pass
        else:
          if char == ' ':
            X += Font['A'][0]
            X += Spacing
          if char == '\n':
            X = OriginalX
            Y += Font['Height']
          CurrentWord = ''
        if X-OriginalX > WidthLimit:
          X = OriginalX
          Y += Font['Height']
      return X, Y