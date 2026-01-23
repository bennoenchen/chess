import pygame

import json
from pathlib import Path

class Game:
  def __init__(self, protocol, settings):
    self.protocol = protocol
    self.settings = settings
    self.bootup()

  def bootup(self):
    self.resolution = self.settings.data["resolution"]
    self.server = self.settings.data["server"]
    self.screen = pygame.display.set_mode((self.resolution["screenwidth"], self.resolution["screenheight"]))
    pygame.display.init()
    self.running = True

  def connect(self):
    self.protocol.connect(self.server)
    self.protocol.hello()
    
  def gameloop(self):
    self.state = "menu"
    self.connected = False
    self.clock = pygame.time.Clock()
    while self.running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT():
          self.running = False

      if self.state == "menu":
        print("main menu")
        setting_button = Button()

      if self.state == "game":
        if not self.connected:
          self.connect()
          self.connected = True
          self.colsize, self.rowsize = self.resolution["screenwidth"] / 8, self.resolution["screenheight"] / 8
        print("in game")

      if self.state == "settings":
        print("settings menu")
        
      pygame.display.flip()
      self.clock.tick(60)

  def board(self, board):
    ifself.state
  
  def boardlayouthandler(self, board):
    if len(board) == 128:
      parts = {}
      for i in range(0,128,2):
        parts[i // 2] = board[i:i+2]
      allpieces = []
      for keys, items in parts.items():
        color = int(items[0])
        piece = int(items[1])
        if not (1 <= color <= 2 and 1 <= piece <= 6):
          continue
        position = keys
        info = {"color":color,"piece":piece,"position":position}
        allpieces.append(info)
    else:
      raise Exception("Invalid board length")
    return allpieces

class ChessFigure:
  def __init__(self, info):
    info["color"], info["piece"], info["position"] = color, piece, position
    row, col = position // 8, position % 8
    x, y = col * self.colsize, row * self.rowsize

class Button:
  def __init__(self):
    return


class Settings:
  def __init__(self, path = "config.json"):
    self.path = Path(path)
    self.data = {}
  
  def load(self):
    if self.path.exists():
      with self.path.open("r", encoding="utf-8") as f:
        self.data = json.load(f)
    else:
      self.setdefaults()
      self.save()

  def save(self):
    with self.path.open("w",encoding="utf-8") as f:
      json.dump(self.data, f, indent=2)
  
  def setdefaults(self):
    self.data = {
      "server": {"username":"Player","host":"localhost", "port":5000},
      "resolution":{"screenwidth":800,"screenheight":800},
      "audio":1.0,

    }

if __name__ == "__main__":
  newgame = Game()
