from game import Game
from network import NetworkClient

class ProtocolHandler:
  def __init__(self, net):
    net.receive()

if __name__ == "__main__":
  net = NetworkClient("localhost", 5000, "Player")
  protocol = ProtocolHandler(net)
