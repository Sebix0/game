import pygame

class Scene:
  def __init__(self, sceneManager, stateManager, game):
    self.sceneManager = sceneManager # manages game levels
    self.stateManager = stateManager # manages pause, menu, options...
    self.game = game
    self.main = self.game.main

  def logic(self):
    pass

  def eventHandler(self, event):
    pass

  def render(self, win):
    #draw anything
    pass

  def load(self):
    self.game.transition = -30
    self.game.player.pos = [0, 0]

