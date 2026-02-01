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
    if len(split) >= 3:
      print("PH: Message too long")
    cmd, dat = split[0], split[1]
    if cmd == "ROLE":
      if dat == "WHITE":
        self.game.color = 1
      elif dat == "BLACK":
        self.game.color = 2
      else: raise Exception("INVALID COLOR FROM SERVER")
    elif cmd == "STARTGAME":
      self.game.startgame
    elif cmd == "YOURMOVE":
      self.game.yourmove = True
    elif cmd == "BOARD":
      pieces = self.boardlayouthandler(split[1])
      self.game.pieces = pieces
      

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
        #MAKE IT SO THAT PIECES IS [x,y]
        position = keys
        info = {"color":color,"piece":piece,"position":position}
        allpieces.append(info)
    else:
      raise Exception("Invalid board length")
    return allpieces

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