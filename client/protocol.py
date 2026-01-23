from network import NetworkClient

class ProtocolHandler:
  def __init__(self):
    return

  def set_game(self, game):
    self.game = game
    
  def connect(self, server={"username":"Player","host":"localhost","port":5000}):
    self.server = server
    self.net = NetworkClient(self.server["username"], self.server["host"], self.server["port"])
    

  def hello(self):
    self.net.send("HELLO " + self.server["username"])

  def move(self, pos1, pos2):
    self.net.send("MOVE " + pos1 + " TO " + pos2)

if __name__ == "__main__":
  protocol = ProtocolHandler({"server": {"host": "localhost","port": 5000}})
