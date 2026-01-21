import socket
import threading

class NetworkServer():
  def __init__(self, host="localhost", port=5000):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind((host,port))
    self.sock.listen()
    self.clients = []
    print("SERVER Up")
    
  def start(self):  
    print("SERVER Waiting for connection")
    while True:
      conn, addr = self.sock.accept()
      print(f"SERVER Client connected: {addr}")
      self.clients.append(conn)
      thread = threading.Thread(
        target=self.handle_client,
        args=(conn, addr),
        daemon=True
      )
      thread.start()

  def handle_client(self, conn, addr):
    try:
      while True:
        data = conn.recv(4096)
        if not data:
          break

        msg = data.decode().strip()
        print(f"[{addr}] {msg}")

        # Beispiel: an alle Clients senden (Broadcast)
        self.broadcast(f"[{addr}] {msg}")
    finally:
      print(f"SERVER Client disconnected: {addr}")
      self.clients.remove(conn)
      conn.close()

  def broadcast(self, msg: str):
    for client in self.clients:
      try:
        client.sendall((msg + "\n").encode())
      except Exception:
        pass
          
  """def send(self, msg: str):
    self.conn.send((msg + "\n").encode())
    print("SERVER Sent: ", str(msg))

  def receive(self):
    #line = self.file.readline()
    #if not line:
    #  raise ConnectionError("SERVER Client disconnected")
    #return line.strip()
    data = self.conn.recv(4096)
    if not data:
      self.close()
      print("SERVER Client disconnected")
    print(data)

  def close(self):
    print("SERVER Closed")
    self.conn.close()
    self.sock.close()"""

if __name__ == "__main__":
  server = NetworkServer()
  server.start()