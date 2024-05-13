
import pygame

from states.stateManager import State

from scripts.utils import Button

class Pause(State):
  def __init__(self, main, stateManager, sceneManager=None):
    super().__init__(stateManager)
    self.main = main
    self.sceneManager = sceneManager
    self.background = pygame.Surface(self.main.display.get_size(), pygame.SRCALPHA)
    self.background.set_alpha(180)

    self.positions = {
      'return': (32, 126),
      'options': (32, 296),
      'quit': (32, 466)
    }

    self.returnButton = Button('Return', (32, 126), self.main.assets['button'], True)
    self.options = Button('Options', (32, 296), self.main.assets['button'], True)
    self.quit = Button('Return to Main Menu', (32, 466), self.main.assets['button'], True)

    self.buttons = {
      'return': self.returnButton,
      'options': self.options,
      'quit': self.quit
    }
  
    self.speed = 3
    self.snapBack = 5
    self.offset = 25

  def eventHandler(self, event):
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        self.stateManager.setState('game')
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        for name in self.buttons:
          button = self.buttons[name]
          if button.hover(self.main.scale):
            if name == 'return':
              self.stateManager.setState('game')
            if name == 'options':
              self.stateManager.setState('options')
            if name == 'quit':
              self.stateManager.setState('mainMenu')

  def logic(self):
    for name in self.buttons:
      button = self.buttons[name]
      w, h = button.rect().size
      scale = self.main.scale
      rect = pygame.Rect(self.positions[name][0] * scale, self.positions[name][1] * scale, w + (button.pos[0] - self.positions[name][0]), h)
      if rect.collidepoint(pygame.mouse.get_pos()):
        button.pos[0] = min(button.pos[0] + self.speed, self.positions[name][0] + self.offset)
      elif button.pos[0] != self.positions[name][0]:
        button.pos[0] = max(self.positions[name][0], button.pos[0] - self.snapBack)
        


  def render(self, win, offset=(0, 0)):
    self.scenes[self.sceneManager.getState()].render(win, offset)
    win.blit(self.main.game.transitionSurface, (0, 0))
    self.background.fill((0, 0, 0))
    win.blit(self.background, (0, 0))
    
    for name in self.buttons:
      self.buttons[name].render(win, self.main, 4 if name!='quit' else 2.5)
    
  def load(self):
    self.scenes = self.main.scenes