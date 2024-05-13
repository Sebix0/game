import os
import time

import pygame

# Game states and manager
from states.stateManager import StateManager
from states.mainMenu import MainMenu
from states.game import Game
from states.options import Options
from states.pause import Pause

# Game levels
import states.scenes.s01 as s01
import states.scenes.caveHub as caveHub

# Game scripts
from scripts.utils import load_image, load_images, Animation, Font

class Main:
  def __init__(self):
    pygame.init()
    self.size = [(1920, 1080), (1600, 900), (1280, 720), (1024, 576)]
    self.currSize = 2
    self.rawW, self.rawH = self.size[self.currSize]
    self.scale = self.size[self.currSize][0] / 1280
    self.screen = pygame.display.set_mode((self.rawW, self.rawH))
    self.display = pygame.Surface((1280, 720))
    self.clock = pygame.time.Clock()

    self.last_time = 0
    self.time = 0
    self.dt = 0

    self.fullscreen = False
    self.fullscreened = False

    self.assets = {
      'button': load_image('menu/button.png'),
      'background': load_image('menu/background.png'),
      'pause/background': load_image('pause/background.png'),
      'player/idle': Animation(load_images('player/idle')),
      'player/walk/left': Animation(load_images('player/walk/left')),
      'player/walk/up': Animation(load_images('player/walk/up')),
      'player/walk/down': Animation(load_images('player/walk/down')),
      'wall': load_images('wall'),
      'floor': load_images('floor'),
    }
    
    #just ignore this rq
    self.font_dat = {'A':[3],'B':[3],'C':[3],'D':[3],'E':[3],'F':[3],'G':[3],'H':[3],'I':[3],'J':[3],'K':[3],'L':[3],'M':[5],'N':[3],'O':[3],'P':[3],'Q':[3],'R':[3],'S':[3],'T':[3],'U':[3],'V':[3],'W':[5],'X':[3],'Y':[3],'Z':[3],
          'a':[3],'b':[3],'c':[3],'d':[3],'e':[3],'f':[3],'g':[3],'h':[3],'i':[1],'j':[2],'k':[3],'l':[3],'m':[5],'n':[3],'o':[3],'p':[3],'q':[3],'r':[2],'s':[3],'t':[3],'u':[3],'v':[3],'w':[5],'x':[3],'y':[3],'z':[3],
          '.':[1],'-':[3],',':[2],':':[1],'+':[3],'\'':[1],'!':[1],'?':[3],
          '0':[3],'1':[3],'2':[3],'3':[3],'4':[3],'5':[3],'6':[3],'7':[3],'8':[3],'9':[3],
          '(':[2],')':[2],'/':[3],'_':[5],'=':[3],'\\':[3],'[':[2],']':[2],'*':[3],'"':[3],'<':[3],'>':[3],';':[1]}
    self.font = Font('data/font/small_font.png', self.font_dat, 5, 8, (248, 248, 248))

    self.stateManager = StateManager('mainMenu')
    self.sceneManager = StateManager('01')
    
    self.mainMenu = MainMenu(self, self.stateManager)
    self.game = Game(self, self.stateManager, self.sceneManager)
    self.options = Options(self, self.stateManager)
    self.pause = Pause(self, self.stateManager, self.sceneManager)

    self.states = {
      'mainMenu': self.mainMenu,
      'game': self.game,
      'options': self.options,
      'pause': self.pause
    }

    self.s01 = s01.Level(self.sceneManager, self.stateManager, self.game)
    self.caveHub = caveHub.Level(self.sceneManager, self.stateManager, self.game)
  
    self.scenes = {
      '01': self.s01,
      'caveHub': self.caveHub
    }

    for state in self.states:
      self.states[state].load()

    self.scroll = [0, 0]

  def run(self):
    while True:
      self.time = time.time()
      self.dt = self.time - self.last_time
      self.dt *= 60
      self.last_time = self.time

      focus = list(self.game.player.rect().center)
      self.scroll[0] += (focus[0] - self.display.get_width()/2 - self.scroll[0]) / 30
      self.scroll[1] += (focus[1] - self.display.get_height()/2 - self.scroll[1]) / 30
      render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

      self.display.fill((0, 0, 0))

      self.scale = self.screen.get_width() / 1280

      if self.fullscreen and self.stateManager.getState() == 'game':
        pygame.mouse.set_pos((self.rawW // 2, self.rawH // 2))
        pygame.mouse.set_visible(False)
      else:
        pygame.mouse.set_visible(True)

      self.states[self.stateManager.getState()].logic()
      self.states[self.stateManager.getState()].render(self.display, render_scroll)

      #temp = self.dt / 60
      #self.font.render(f"{int(1/temp)}FPS", 10, 10, 1, 256, self.display, 4)


      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          return

        self.states[self.stateManager.getState()].eventHandler(event)
      
      if self.fullscreen != self.fullscreened:
        if self.fullscreen:
          pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
          self.fullscreened = self.fullscreen
        else:
          pygame.display.set_mode(self.size[self.currSize])
          self.fullscreened = self.fullscreen
      else:
        if self.screen.get_size() != self.size[self.currSize] and not self.fullscreen:
          pygame.display.set_mode(self.size[self.currSize])
        
      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
      pygame.display.update()
      self.clock.tick(60)
  
main = Main()
main.run()

'''
TODO:
finish autotiling / assets so it looks cleaner and autotiles better
create level saving feature
then start working on interacting with chests...
create hud
create an inventory (json)

when entering the cave create the transition window
when entering the cave change scene and load in the next one
create an unloading function or something maybe to allow passage between?
or maybe not bc no escape...

'''