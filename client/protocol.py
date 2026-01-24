from network import NetworkClient

class ProtocolHandler:
  def __init__(self):
    self.game = None
    self.net = None
    self.server = None

  def set_game(self, game):
    self.game = game
    
  def connect(self, server={"username":"Player","host":"localhost","port":5000}):
    self.server = server
    self.net = NetworkClient(self.on_message, self.server["host"], self.server["port"])

  def on_message(self, msg):
    print(msg)
    

  def hello(self):
    self.net.send("HELLO " + self.server["username"])

  def move(self, pos1, pos2):
    self.net.send("MOVE " + pos1 + " TO " + pos2)