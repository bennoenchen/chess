import socket
import threading

class NetworkClient:
  def __init__(self, username, host="localhost", port=5000):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((host, port))
    print(f"CLIENT Connected to {host}:{port}")
    self.sock.sendall(f"HELLO {username}\n".encode())
    print(f"CLIENT Logged in as {username}")

    self.running = True
    self.recv_thread = threading.Thread(
      target=self.receive_loop,
      daemon=True
    )
    self.recv_thread.start()

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

  def close(self):
    self.running = False
    try:
      self.sock.close()
    except:
      pass
    print("CLIENT Closed")

if __name__ == "__main__":
  username = input("Username: ")
  client = NetworkClient(username)

  try:
    while True:
      msg = input()
      if msg == "":
        break
      client.send(msg)
  finally:
    client.close()