import pygame

from states.scenes.scene import Scene

class Level(Scene):
  def __init__(self, sceneManager, stateManager, game):
    super().__init__(sceneManager, stateManager, game)
    
  def load(self):
    self.game.tilemap.load('map.json')
    self.game.player.pos = [448, 384]
    self.game.enableMovement()

  def render(self, win, offset=(0, 0)):
    win.fill((37, 19, 26))
    self.game.tilemap.render(win, offset)
    self.game.player.render(win, offset)

