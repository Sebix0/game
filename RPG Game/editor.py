import time

import pygame

# Game scripts
from scripts.utils import load_image, load_images, Font
from scripts.tilemap import Tilemap

class Main:
  def __init__(self):
    pygame.init()
    self.size = (1280, 720)
    self.display = pygame.display.set_mode((1280, 720))
    self.clock = pygame.time.Clock()

    self.last_time = 0
    self.time = 0
    self.dt = 0

    self.fullscreen = False
    self.fullscreened = False

    self.font_dat = {'A':[3],'B':[3],'C':[3],'D':[3],'E':[3],'F':[3],'G':[3],'H':[3],'I':[3],'J':[3],'K':[3],'L':[3],'M':[5],'N':[3],'O':[3],'P':[3],'Q':[3],'R':[3],'S':[3],'T':[3],'U':[3],'V':[3],'W':[5],'X':[3],'Y':[3],'Z':[3],
          'a':[3],'b':[3],'c':[3],'d':[3],'e':[3],'f':[3],'g':[3],'h':[3],'i':[1],'j':[2],'k':[3],'l':[3],'m':[5],'n':[3],'o':[3],'p':[3],'q':[3],'r':[2],'s':[3],'t':[3],'u':[3],'v':[3],'w':[5],'x':[3],'y':[3],'z':[3],
          '.':[1],'-':[3],',':[2],':':[1],'+':[3],'\'':[1],'!':[1],'?':[3],
          '0':[3],'1':[3],'2':[3],'3':[3],'4':[3],'5':[3],'6':[3],'7':[3],'8':[3],'9':[3],
          '(':[2],')':[2],'/':[3],'_':[5],'=':[3],'\\':[3],'[':[2],']':[2],'*':[3],'"':[3],'<':[3],'>':[3],';':[1]}
    self.font = Font('data/font/small_font.png', self.font_dat, 5, 8, (248, 248, 248))

    self.assets = {
      'wall': load_images('wall'),
      'floor': load_images('floor')
    }

    self.tilemap = Tilemap(self)
    try:
      self.tilemap.load('map.json')
    except:
      pass
    self.tileList = list(self.assets)
    self.group = 0
    self.variant = 0

    self.shifting = False
    self.visualise = False

    self.movement = [False, False, False, False] # left right up down
    self.scroll = [0, 0]

  def run(self):
    while True:
      self.time = time.time()
      self.dt = self.time - self.last_time
      self.dt *= 60
      self.last_time = self.time

      self.scroll[0] += (self.movement[1] - self.movement[0]) * self.dt * 5
      self.scroll[1] += (self.movement[3] - self.movement[2]) * self.dt * 5
      render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
      
      if not self.visualise:
        currentTileImage = self.assets[self.tileList[self.group]][self.variant].copy()
        currentTileImage.set_alpha(100)

        self.display.fill((0, 0, 0))

        mpos = pygame.mouse.get_pos()
        pos = [0, 0]
        pos[0] = (mpos[0] + render_scroll[0]) // self.tilemap.tileSize
        pos[1] = (mpos[1] + render_scroll[1]) // self.tilemap.tileSize

        x = pos[0] * self.tilemap.tileSize - render_scroll[0]
        y = pos[1] * self.tilemap.tileSize - render_scroll[1]
        print((x, y))
        self.display.blit(currentTileImage, (10, 10))
        self.display.blit(currentTileImage, (x, y))
      else:
        self.display.fill((37, 19, 26))

      self.tilemap.render(self.display, render_scroll)

      if not self.visualise:
        double = 3
        self.font.render(f'Variant: {self.variant}', 84, 10, 1, 256, self.display, double=double)
        self.font.render(f'Group: {self.tileList[self.group]}', 84, 10*double, 1, 256, self.display, double=double)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          return
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_a:
            self.movement[0] = True
          if event.key == pygame.K_d:
            self.movement[1] = True
          if event.key == pygame.K_w:
            self.movement[2] = True
          if event.key == pygame.K_s:
            self.movement[3] = True
          if event.key == pygame.K_LSHIFT:
            self.shifting = True
          if event.key == pygame.K_t:
            self.tilemap.autotile()
          if event.key == pygame.K_v:
            self.visualise = True
          if event.key == pygame.K_o:
            self.tilemap.save('map.json')
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_a:
            self.movement[0] = False
          if event.key == pygame.K_d:
            self.movement[1] = False
          if event.key == pygame.K_w:
            self.movement[2] = False
          if event.key == pygame.K_s:
            self.movement[3] = False
          if event.key == pygame.K_LSHIFT:
            self.shifting = False
          if event.key == pygame.K_v:
            self.visualise = False

        mousePressed = pygame.mouse.get_pressed(3)
        if mousePressed[0]:
          self.tilemap.tilemap[str(pos[0]) + ';' + str(pos[1])] = {'type': self.tileList[self.group], 'variant': self.variant, 'pos': tuple(pos)}
        elif mousePressed[2]:
          try:
            del self.tilemap.tilemap[str(pos[0]) + ';' + str(pos[1])]
          except:
            pass
        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 2:
            print(self.tilemap.physicsTilesAround(mpos))
          if self.shifting:
            if event.button == 4:
              self.group = (self.group + 1) % len(self.tileList)
              self.variant = 0
            if event.button == 5:
              self.group = (self.group - 1) % len(self.tileList)
              self.variant = 0
          else:
            if event.button == 4:
              self.variant = (self.variant + 1) % len(self.assets[self.tileList[self.group]])
            if event.button == 5:
              self.variant = (self.variant - 1) % len(self.assets[self.tileList[self.group]])
        
      

      pygame.display.update()
      self.clock.tick(60)
  
main = Main()
main.run()
