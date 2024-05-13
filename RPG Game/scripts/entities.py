import math

import pygame

class PhysicsEntity:
  def __init__(self, main, e_type, pos, size, tilemap):
    self.main = main
    self.type = e_type
    self.pos = list(pos)
    self.size = size
    self.tilemap = tilemap

    self.velocity = [0, 0]

    self.action = ''
    self.setAction('idle')
    self.facing = 'down'
    self.animFacing = 'down'

  def rect(self):
    return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

  def setAction(self, action):
    if self.type == 'door':
      return
    if self.action != action:
      self.action = action
      if self.action == 'walk':
        if self.facing == 'right':
          face = 'left'
        else:
          face = self.facing

        self.animation = self.main.assets[self.type + '/walk/' + face].copy()
      else:
        self.animation = self.main.assets[self.type + '/' + self.action].copy()
        self.facing = 'down'
    elif action == 'walk' and self.facing != self.animFacing:
      self.animFacing = self.facing
      if self.facing == 'right':
        face = 'left'
      else:
        face = self.facing

      self.animation = self.main.assets[self.type + '/walk/' + face].copy()

  def rect(self):
    return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
  
  def update(self, movement=(0, 0)):
    angle = math.atan2(movement[1], movement[0])
    self.velocity[0] = math.cos(angle) * abs(movement[0])
    self.velocity[1] = math.sin(angle) * abs(movement[1])
    
    frame_movement = [(self.velocity[0] + movement[0]) * self.main.dt, (self.velocity[1] + movement[1]) * self.main.dt]


    print(self.tilemap.tilesAround(self.pos))
    self.pos[0] += frame_movement[0]
    entity_rect = self.rect()
    rects = self.tilemap.physicsTilesAround(entity_rect.topleft) # size too big but model too small, makes it look stuck
    for rect in rects:
      if entity_rect.colliderect(rect):
        if frame_movement[0] > 0:
          entity_rect.right = rect.left
        elif frame_movement[0] < 0:
          entity_rect.left = rect.right
    self.pos[0] = entity_rect.x

    self.pos[1] += frame_movement[1]
    entity_rect = self.rect()
    for rect in self.tilemap.physicsTilesAround(entity_rect.topleft):
      if entity_rect.colliderect(rect):
        if frame_movement[1] > 0:
          entity_rect.bottom = rect.top
        if frame_movement[1] < 0:
          entity_rect.top = rect.bottom
    self.pos[1] = entity_rect.y

    if movement[0] > 0:
      self.facing = 'right'
    elif movement[0] < 0:
      self.facing = 'left'
    if movement[1] > 0:
      self.facing = 'down'
    elif movement[1] < 0:
      self.facing = 'up'

    if movement == (0, 0):
      self.setAction('idle')
    else:
      self.setAction('walk')

    self.animation.update()

  def render(self, win, offset=(0, 0)):
    if self.facing == 'right':
      flip = True
    else:
      flip = False
    if self.type == 'door':
      pygame.draw.rect(win, 'red', pygame.Rect(self.pos[0] - offset[0], self.pos[1] - offset[1], self.size[0], self.size[1]))
      return
    win.blit(pygame.transform.flip(self.animation.img(), flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))

class Player(PhysicsEntity):
  def __init__(self, main, pos, size):
    super().__init__(main, 'player', pos, size)
    self.inventory = {}

class StaticEntity:
  def __init__(self, main, e_type, pos, size):
    self.main = main
    self.type = e_type
    self.pos = list(pos)
    self.size = list(size)

  def rect(self):
    return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
  
  def collide(self, obj):
    if type(obj) == pygame.Rect:
      return self.rect().colliderect(obj)
    elif type(obj) == list or type(obj) == tuple:
      return self.rect().collidepoint(obj)
    
  def render(self, win, offset=(0, 0)):
    rect = pygame.Surface(self.size)
    rect.fill('red')
    win.blit(rect, (self.pos[0] - offset[0], self.pos[1] - offset[1]))