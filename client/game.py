import pygame
from protocol import ProtocolHandler

class Game:
  def __init__(self):
    protocol = ProtocolHandler()

    gamewidth, gameheight = 800
    gamewindow(gamewidth, gameheight)
    return

  def test(self):
    print("Test successful (game.py)")

  def gamewindow(width, height):
    pygame.display(widht, height)
    

if __name__ == "__main__"
  newgame = Game()
