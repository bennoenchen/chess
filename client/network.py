import socket

class NetworkClient():
  def __init__(self, host="localhost", port=5000):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((host, port))
    self.file = self.sock.makefile("r")
    print(f"CLIENT Connected to {host}:{port}")

  def send(self, msg: str):
    self.sock.sendall((msg + "\n").encode())

  def receive(self) -> str:
    #line = self.file.readline()
    #if not line:
    #  raise ConnectionError("CLIENT Server disconnected")
    #return line.strip()
    print(self.sock.receive())

  def close(self):
    print("CLIENT Closed")
    self.sock.close()

client = NetworkClient()
client.close()
