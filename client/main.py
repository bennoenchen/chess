from game import Game
from network import NetworkClient
from protocol import ProtoclHandler

def main():
  addr, port, username = "localhost", 5000, "Player"
  addr = input("Address ('localhost' or IP): ")
  port = input("Port (eg. 5000): ")
  username = input("Username: ")
  
  
  net = NetworkClient(addr, port, username)
  protcol = ProtocolHandler(net)
  game = Game()

if __name__ == "__main__":
  main = main()

