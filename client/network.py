import socket
import threading

class NetworkClient():
  def __init__(self, host="localhost", port=5000):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((host, port))
    self.file = self.sock.makefile("r")
    print(f"CLIENT Connected to {host}:{port}")
    self.running = True
    self.recv_thread = threading.Thread(
      target=self.receive_loop,
      daemon=True
    )

  def receive_loop(self):
    while self.running:
      try:
        data = self.sock.recv(4096)
        if not data:
          break
        print(data.decode().strip())
      except Exception:
        break
      print("CLIENT Server disconnected")
      self.running = False



  def send(self, msg: str):
    self.sock.sendall((msg + "\n").encode())

  """def receive(self) -> str:
    data = self.sock.recv(4096).decode()
    if not data:
      self.close()
      print("SERVER Client disconnected")
    print(data)"""

  def close(self):
    self.sock.close()
    self.running = False
    print("CLIENT Closed")
    

if __name__ == "__main__":
    client = NetworkClient()

    try:
        while True:
            msg = input()
            if msg == "":
                break
            client.send(msg)
    finally:
        client.close()