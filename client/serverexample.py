import socket

class NetworkServer():
  def __init__(self, host="localhost", port=5000):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind((host,port))
    self.sock.listen(1)
    print("SERVER Up")
    self.conn, self.addr = self.sock.accept()
    self.file = self.conn.makefile("r")
    print(f"SERVER Client connected: {self.addr}")


  def receive(self):
    #line = self.file.readline()
    #if not line:
    #  raise ConnectionError("SERVER Client disconnected")
    #return line.strip()
    data = self.conn.recv()
    if not data:
      self.close()
      print("SERVER Client disconnected")
    print(self.sock.receive())

  def close(self):
    print("SERVER Closed")
    self.conn.close()
    self.sock.close()

server = NetworkServer()
server.close()
