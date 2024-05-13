import json

import pygame

# create floor autotile when its a little nicer (more assets)
AUTOTILEMAP = {
  'wall': {
    tuple(sorted([(0, 1), (1, 0)])): 0, # could add variant checking but i don't have the time to do that rn. Maybe later. (shiftx, shifty, variant) and do for every type
    tuple(sorted([(-1, 0), (1, 0)])): 1,
    tuple(sorted([(0, 1), (-1, 0)])): 5,
    tuple(sorted([(0, -1), (0, 1)])): 6,
    tuple(sorted([(0, -1), (1, 0)])): 12,
    tuple(sorted([(0, -1), (-1, 0)])): 17
  }
}

NEIGHBOURTILES = (
  (-1, -1), (0, -1), (1, -1),
  (-1, 0), (0, 0), (1, 0),
  (-1, 1), (0, 1), (1, 1)
)

PHYSICSTILES = {'wall'}

class Tilemap:
  def __init__(self, main, tileSize=64):
    self.main = main
    self.tileSize = tileSize
    self.tilemap = {}

  def save(self, path):
    f = open(path, 'w')
    json.dump({'tilemap': self.tilemap, 'tileSize': self.tileSize}, f)
    f.close()

  def load(self, path):
    f = open(path, 'r')
    mapData = json.load(f)
    f.close()

    self.tilemap = mapData['tilemap']
    self.tileSize = mapData['tileSize']

  def autotile(self):
    for loc in self.tilemap:
      tileType = self.tilemap[loc]['type']
      if tileType in AUTOTILEMAP:
        neighbours = set()
        tilePos = self.tilemap[loc]['pos']
        for shift in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
          checkLoc = str(tilePos[0] + shift[0]) + ';' + str(tilePos[1] + shift[1])
          if checkLoc in self.tilemap:
            if self.tilemap[checkLoc]['type'] == tileType:
              neighbours.add(shift)
        neighbours = tuple(sorted(neighbours))
        if neighbours in AUTOTILEMAP[tileType]:
          self.tilemap[loc] = {'type': tileType, 'variant': AUTOTILEMAP[tileType][neighbours], 'pos': tilePos}


  def tilesAround(self, pos):
    tiles = []
    pos = (pos[0] // self.tileSize, pos[1] // self.tileSize)
    for offset in NEIGHBOURTILES:
      neighbour = (pos[0] + offset[0], pos[1] + offset[1])
      if str(neighbour[0]) + ';' + str(neighbour[1]) in self.tilemap:
        tiles.append(neighbour)
    print(tiles)
    return tiles

  def physicsTilesAround(self, pos):
    tiles = self.tilesAround(pos)
    rects = []
    for tile in tiles:
      loc = str(tile[0]) + ';' + str(tile[1])
      if self.tilemap[loc]['type'] in PHYSICSTILES:
        rect = pygame.Rect(tile[0] * self.tileSize, tile[1] * self.tileSize, self.tileSize, self.tileSize)
        rects.append(rect)
    return rects
  
  def render(self, win, offset=(0, 0)):
    xRange = win.get_width()//self.tileSize
    yRange = win.get_height()//self.tileSize
    for loc in self.tilemap:
      tile = self.tilemap[loc]
      # add in checking if in window functionality and the only outputting those in the window
      try:
        win.blit(self.main.assets[str(tile['type'])][tile['variant']], (tile['pos'][0] * self.tileSize - offset[0], tile['pos'][1] * self.tileSize - offset[1]))
      except KeyError:
        print('Asset(s) not found')
      
    