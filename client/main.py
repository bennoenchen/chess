from game import Game, Settings
from protocol import ProtocolHandler

def main():
  protocol = ProtocolHandler()
  settings = Settings()
  settings.load()
  game = Game(protocol, settings)
  protocol.set_game(game)


if __name__ == "__main__":
  main = main()

