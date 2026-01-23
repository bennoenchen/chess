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

    self.running = True

  def connect(self):
    self.protocol.connect(self.server["server"])
    self.protocol.hello()
    
  def gameloop(self):
    self.state = "menu"
    self.connected = False
    while self.running:
      for event in pygame.event.get():
        if event == pygame.QUIT():
          self.running = False

      if state == "menu":
        print("main menu")
        setting_button = Button(

      if state == "game":
        if not self.connected:
          self.connect()
          self.connected = True
        print("in game")

      if state == "settings":
        print("settings menu")
        
      screen.flip()
      clock.tick(60)


class ChessFigure:
  def __init__(self, type, position):
    print(type, position)

class Button:
  def __init__(self, 


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
