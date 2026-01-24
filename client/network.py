import socket
import threading

class NetworkClient:
  def __init__(self, on_message, host="localhost", port=5000):
    self.on_message = on_message
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((host, port))
    print(f"CLIENT Connected to {host}:{port}")

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
        msg = data.decode().strip()
        self.on_message(msg)
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