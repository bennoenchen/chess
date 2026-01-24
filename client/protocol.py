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

  def on_message(self, msg: str):
    print("PH: " + msg)
    split = msg.split()
    if len(split) > 3:
      print("PH: Message too long")
    if split[0] == "ROLE":
      if split[1] == "WHITE":
        self.game.color = 1
      elif split[1] == "BLACK":
        self.game.color = 2
      else: raise Exception("INVALID COLOR FROM SERVER")
    elif split[0] == "STARTGAME":
      self.game.startgame

    




  def ok(self):
    self.net.send("OK\n")

  def hello(self):
    self.net.send("HELLO " + self.server["username"].strip() + "\n")

  def move(self, pos1, pos2):
    self.net.send("MOVE " + pos1.strip() + " TO " + pos2.strip() + "\n")

  def hold(self):
    self.net.send("HOLD\n")

  def accept(self):
    self.net.send("ACCEPT\n")

  def deny(self):
    self.net.send("DENY\n")

  def draw(self):
    self.net.send("DRAW\n")

  def disconnect(self):
    self.net.send("DISCONNECT\n")