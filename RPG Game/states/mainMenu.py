import sys

import pygame

from states.stateManager import State

from scripts.utils import Button

class MainMenu(State):
  def __init__(self, main, stateManager):
    super().__init__(stateManager)
    self.main = main
    self.scale = self.main.scale
    self.selected = None # currently selected option to make it stand out later
    self.positions = { # orginal unchanged positions for all buttons
      'start': (50, 100),
      'options': (50, 300),
      'quit': (50, 500)
    }

    self.start= Button('Start', self.positions['start'], self.main.assets['button'], True)  # actual buttons
    self.options = Button('Options', self.positions['options'], self.main.assets['button'], True)
    self.quit = Button('Quit', self.positions['quit'], self.main.assets['button'], True)
    self.buttons = { # button stored in a list to enable looping through -> less writing
      'start': self.start,
      'options': self.options,
      'quit': self.quit
    }

    self.speed = 3
    self.snapBack = 5
    self.offset = 25

  def eventHandler(self, event):
    self.scale = self.main.scale
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        if self.buttons['quit'].hover(self.scale):
          pygame.quit()
          sys.exit()
        if self.buttons['start'].hover(self.scale):
          self.stateManager.setState('game')
        if self.buttons['options'].hover(self.scale):
          self.stateManager.setState('options')
        
  def logic(self):
    for name in self.buttons:
      button = self.buttons[name]
      w, h = button.rect().size # store the width and height
      rect = pygame.Rect(self.positions[name][0]*self.scale, self.positions[name][1] * self.scale, w + (button.pos[0] - self.positions[name][0]), h)
      if rect.collidepoint(pygame.mouse.get_pos()):
        button.pos[0] = min(button.pos[0] + self.speed, self.positions[name][0] + self.offset)
      elif button.pos[0] != self.positions[name][0]:
        button.pos[0] = max(self.positions[name][0], button.pos[0] - self.snapBack)
        

  def render(self, win, offset=(0,0)):
    win.blit(self.main.assets['background'], (0, 0))

    for name in self.buttons:
      button = self.buttons[name]
      button.render(win, self.main)