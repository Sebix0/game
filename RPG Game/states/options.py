import pygame

from states.stateManager import State

from scripts.utils import Button, getWidth

class Options(State):
  def __init__(self, main, stateManager):
    super().__init__(stateManager)
    self.main = main
    
    self.resolutionButton = Button('Change Res', (50, 100), self.main.assets['button'], True)
    self.fullscreen = Button('Fullscreen', (50, 300), self.main.assets['button'], True)
    self.back = Button('Back', (50, 500), self.main.assets['button'], True)
    self.buttons = {
      'res': self.resolutionButton,
      'fullscreen': self.fullscreen,
      'back': self.back
    }
    self.positions = {
      'res': (50, 100),
      'fullscreen': (50, 300),
      'back': (50, 500)
    }

    self.speed = 3
    self.snapBack = 5
    self.offset = 25

  def logic(self):
    scale = self.main.scale
    for name in self.buttons:
      button = self.buttons[name]
      w, h = button.rect().size # store the width and height
      rect = pygame.Rect(self.positions[name][0] * scale, self.positions[name][1] * scale, w + (button.pos[0] - self.positions[name][0]), h)
      if rect.collidepoint(pygame.mouse.get_pos()):
        button.pos[0] = min(button.pos[0] + self.speed, self.positions[name][0] + self.offset)
      elif button.pos[0] != self.positions[name][0]:
        button.pos[0] = max(self.positions[name][0], button.pos[0] - self.snapBack)
  
  def eventHandler(self, event):
    scale = self.main.scale
    if event.type == pygame.MOUSEBUTTONDOWN:
      for name in self.buttons:
        button = self.buttons[name]
        if button.hover(scale):
          if name == 'back':
            self.stateManager.back()
          if name == 'res':
            self.main.currSize = (self.main.currSize + 1) % len(self.main.size)
          if name == 'fullscreen':
            self.main.fullscreen = not self.main.fullscreen
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        self.stateManager.back()
          

  def render(self, win, offset=(0, 0)):
    win.blit(self.main.assets['background'], (0, 0))

    for name in self.buttons:
      button = self.buttons[name]
      if name == 'res':
        button.text = f"{int(1280 * self.main.scale)} x {int(720 * self.main.scale)}"
      elif name == 'fullscreen':
        button.text = "Fullscreen" if self.main.fullscreen else "Windowed" 
      button.render(win, self.main)