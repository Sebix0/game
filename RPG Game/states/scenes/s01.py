
import pygame

from states.scenes.scene import Scene

from scripts.entities import StaticEntity
from scripts.utils import TextBox

class Level(Scene):
  def __init__(self, sceneManager, stateManager, game):
    super().__init__(sceneManager, stateManager, game)
    self.cutsceneRange = 200

    self.caveEntrance = StaticEntity(self.main, 'door', (576, 100), (64, 64))

    self.textBox = TextBox(['A cave', 'Imma explore'], self.main.font)
    self.nextText = False

  def eventHandler(self, event):
    self.game.playerMovement(event)
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        self.nextText = True

  def logic(self):
    self.textBox.update(self.nextText)
    if self.nextText:
      self.nextText = False

    dx = self.game.player.rect().centerx - self.caveEntrance.rect().centerx
    dy = self.game.player.rect().centery - self.caveEntrance.rect().centery
    dist = (dx*dx) + (dy*dy)
    if dist <= self.cutsceneRange*self.cutsceneRange and not self.textBox.done:
      self.game.cutscene = True
      self.textBox.active = True
    
    if self.textBox.done:
      self.game.cutscene = False
      self.textBox.active = False

    if self.caveEntrance.collide(self.game.player.rect()):
      self.game.nextScene = 'caveHub'
      self.game.disableMovement()

  def render(self, win, offset):
    win.fill((32, 180, 59))
    self.game.player.render(win, offset)
    self.caveEntrance.render(win, offset)
    if self.textBox.active:
      self.textBox.render(win)

  def freeze(self):
    self.movement = [False, False, False, False]

