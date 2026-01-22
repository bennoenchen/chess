import pygame

import json
from pathlib import Path

class Game:
  def __init__(self, protocol, settings):
    self.protocol = protocol
    self.settings = settings
    self.bootup()

  def bootup(self):
    data = self.settings.data
    resolution = data["resolution"]
    pygame.display.set_mode((resolution["screenwidth"],resolution["screenheight"]))
    pygame.display.init()

    self.protocol.connect(data["server"])
    self.protocol.hello()



  def gamewindow(width, height):
    pygame.display(width, height)


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
