
import pygame

from states.stateManager import State

from scripts.entities import Player, PhysicsEntity
from scripts.tilemap import Tilemap

class Game(State):
  def __init__(self, main, stateManager, sceneManager):
    super().__init__(stateManager)
    self.main = main
    self.sceneManager = sceneManager
    self.tilemap = Tilemap(self.main)
    self.player = PhysicsEntity(self.main, 'player', (320, 320), (64, 64), self.tilemap)
    self.scenes = {}
    self.cutscene = False

    self.transition = -50
    self.transitionSurface = pygame.Surface(self.main.display.get_size())
    self.transitionSurface.set_colorkey((255, 255, 255))
    self.condition = False
    self.nextScene = ''

    self.playerMove = True

    self.movement = [False, False, False, False]


  def logic(self):
    if self.playerMove:
      self.player.update((self.movement[1] - self.movement[0], self.movement[3] - self.movement[2]))
    self.scenes[self.sceneManager.getState()].logic()
    if self.nextScene != '':
      self.transition += 1
    if self.transition > 50:
      self.sceneManager.setState(self.nextScene)
      self.scenes[self.nextScene].load()
      self.nextScene = ''
      self.transition = -50
    if self.transition < 0:
      self.transition += 1

  def enableMovement(self):
    self.playerMove = True
  
  def disableMovement(self):
    self.playerMove = False

  def playerMovement(self, event):
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a:
        self.movement[0] = True
      if event.key == pygame.K_d:
        self.movement[1] = True
      if event.key == pygame.K_w:
        self.movement[2] = True
      if event.key == pygame.K_s:
        self.movement[3] = True
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_a:
        self.movement[0] = False
      if event.key == pygame.K_d:
        self.movement[1] = False
      if event.key == pygame.K_w:
        self.movement[2] = False
      if event.key == pygame.K_s:
        self.movement[3] = False
    

  def eventHandler(self, event):
    self.scenes[self.sceneManager.getState()].eventHandler(event)
    if self.cutscene:
      self.playerMove = False
    else:
      self.playerMove = True
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        self.stateManager.setState('pause')
    if self.playerMove:
      self.playerMovement(event)
        
  def render(self, win, offset=(0, 0)):
    self.scenes[self.sceneManager.getState()].render(win, offset)
    self.transitionSurface.fill((0, 0, 0))
    if self.transition:
      print(f"radius: {(50 - abs(self.transition)) * 16}")
      pygame.draw.circle(self.transitionSurface, (255, 255, 255), (self.transitionSurface.get_width() // 2, self.transitionSurface.get_height() // 2), (50 - abs(self.transition)) * 16)
      win.blit(self.transitionSurface, (0, 0))
    
  def load(self):
    self.scenes = self.main.scenes