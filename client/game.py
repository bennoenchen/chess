import pygame

import json
from pathlib import Path

class Game:
  def __init__(self, protocol, settings):
    self.protocol = protocol
    self.settings = settings
    self.bootup()

  def bootup(self):
    pygame.init()
    self.resolution = self.settings.data["resolution"]
    self.server = self.settings.data["server"]
    self.screen = pygame.display.set_mode((self.resolution["screenwidth"], self.resolution["screenheight"]))
    pygame.display.init()
    pygame.display.set_caption('chess')
    icon_image = pygame.image.load('icon.png')
    pygame.display.set_icon(icon_image)
    pygame.mixer.init()
    self.clock = pygame.time.Clock()
    self.running = True
    self.mainloop()

  def connect(self):
    self.protocol.connect(self.server)
    self.protocol.hello()
    

  def mainloop(self):
    self.state = "menu"
    self.connected = False
    self.state_change = True
    self.menu_music_start = True
    self.clr = None

    while self.running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
          self.game_started = False
        
        if self.state == "menu":
          if self.state_change == True:
            self.screen.fill((0, 0, 0))
            self.connected = False
            background = pygame.image.load("background.jpg").convert()
            background = pygame.transform.scale(background, self.screen.get_size())
            play_img = pygame.image.load("play.png").convert_alpha()
            options_img = pygame.image.load("options.png").convert_alpha()
            button_size = self.screen.get_height() / 5
            play_img = pygame.transform.scale(play_img, (button_size * 2, button_size))
            options_img = pygame.transform.scale(options_img, (button_size * 2, button_size))
            play_rect = play_img.get_rect()
            options_rect = options_img.get_rect()
            play_rect.center = (self.screen.get_width() / 2, self.screen.get_height() / 2 - 90)
            options_rect.center = (self.screen.get_width() / 2, self.screen.get_height() / 2 + 90)

            self.state_change = False

          if event.type == pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
              self.state = "game"
              self.state_change = True
            if options_rect.collidepoint(event.pos):
              self.state = "options"
              self.state_change = True

          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
              self.running = False

          self.screen.blit(background, (0,0))
          self.screen.blit(play_img, play_rect)
          self.screen.blit(options_img, options_rect)

        if self.state == "game":
          if self.state_change == True:
            self.screen.fill((0, 0, 0))
            if not self.connected:
              self.connect()
              self.connected = True
            pygame.mixer.stop()
            pygame.mixer.music.load('game.mp3')
            pygame.mixer.music.play(-1)
            board = pygame.image.load("board.png").convert()
            board = pygame.transform.scale(board, self.screen.get_size())
            self.colsize, self.rowsize = self.resolution["screenwidth"] / 8, self.resolution["screenheight"] / 8
            self.state_change = False
          self.screen.blit(board, (0,0))

          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
              self.connected = False
              self.state = "menu"
              self.state_change = True
              self.menu_music_start = True
              self.game_started = False


        if self.state == "options":
          if self.state_change == True:
            self.screen.fill((0, 0, 0))
            background = pygame.image.load("background.jpg").convert()
            background = pygame.transform.scale(background, self.screen.get_size())
            back_img = pygame.image.load("back.png").convert_alpha()
            button_size = self.screen.get_height() / 8
            back_img = pygame.transform.scale(back_img, (button_size, button_size))
            back_rect = back_img.get_rect()
            back_rect.center = (self.screen.get_width() / 8, self.screen.get_height() / 8 * 7)
            self.state_change = False

          if event.type == pygame.MOUSEBUTTONDOWN:
            if back_rect.collidepoint(event.pos):
              self.state = "menu"
              self.state_change = True

          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
              self.connected = False
              self.state = "menu"
              self.state_change = True
          
          self.screen.blit(background, (0,0))
          self.screen.blit(back_img, back_rect)

        if self.state == "menu" or self.state == "options":
          if self.menu_music_start == True:
            pygame.mixer.stop()
            pygame.mixer.music.load('menu.mp3')
            pygame.mixer.music.play(-1)
            self.menu_music_start = False

          

      pygame.display.flip()
      self.clock.tick(60)


  def board(self, board):
    if self.state == "game":
      return
  
  def boardlayouthandler(self, board: str):
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
    color, piece, position = info["color"], info["piece"], info["position"]
    row, col = position // 8, position % 8
    x, y = col * self.colsize, row * self.rowsize

    pygame.display.blit()


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
