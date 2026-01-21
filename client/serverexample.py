import socket
import threading

class NetworkServer():
  def __init__(self, host="localhost", port=5000):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind((host,port))
    self.sock.listen()
    self.clients = {}
    self.lock = threading.Lock()
    print("SERVER Up")
    
  def start(self):  
    print("SERVER Waiting for connection")
    threading.Thread(
      target=self.server_input_loop,
      daemon=True
    ).start()
    while True:
      conn, addr = self.sock.accept()
      print(f"SERVER Client connected: {addr}")
      thread = threading.Thread(
        target=self.handle_client,
        args=(conn, addr),
        daemon=True
      )
      thread.start()

  def handle_client(self, conn, addr):
    name = None
    try:
      data = conn.recv(4096)
      if not data:
        return
      
      hello = data.decode().strip().split(maxsplit=1)
      if hello[0] != "HELLO" or len(hello) != 2:
        conn.sendall(b"ERROR Invalid HELLO\n")
        return
      
      requested_name = hello[1]

      with self.lock:
        if requested_name in self.clients:
          conn.sendall(b"ERROR Name already taken\n")
          conn.close()
          return
        name = requested_name
        self.clients[name] = conn

        print(f"SERVER Client '{name}' connected from {addr}")
        self.broadcast(f"SERVER {name} joined")

        while True:
          data = conn.recv(4096)
          if not data:
            break

          msg = data.decode().strip()
          print(f"{name} {msg}")
          
          parts = msg.split(maxsplit=1)
          cmd = parts[0].upper()

          if cmd == "MSG" and len(parts) == 2:
            self.broadcast(f"{name}: {parts[1]}")
          elif cmd == "TO" and len(parts) == 2:
            to_parts = parts[1].split(maxsplit=1)
            if len(to_parts) == 2:
              target, body = to_parts
              self.send_to(target, f"{name} (private): {body}")
            else:
              conn.sendall(b"ERROR TO requires target and message\n")
          elif cmd in ["OK","HELLO","USERNAME","HOLD","MOVE","ACCEPT","DENY","DRAW","DISCONNECT","GAMEEND"]:
            print(f"{name} called {cmd}")
            return cmd, parts[:1]
            

    except ConnectionResetError:
      pass
    finally:
      if name:
        print(f"SERVER Client disconnected: {name}")
        with self.lock:
          self.clients.pop(name, None)
        self.broadcast(f"SERVER {name} left")
      conn.close()

  def server_input_loop(self):
    while True:
      msg = input()
      if msg.startswith("/to "):
        _, name, text = msg.split(maxsplit=2)
        self.send_to(name, text)
      else:
        self.broadcast(msg)

  def broadcast(self, msg: str):
    with self.lock:
      clients = list(self.clients.items())
    for name, client in clients:
      try:
        client.sendall((msg + "\n").encode())
      except Exception:
        self.clients.pop(name, None)
        try:
          client.close()
        except:
          pass
          
  def send_to(self, name: str, msg: str):
    with self.lock:
      client = self.clients.get(name)
      if client:
        try:
          client.sendall((msg + "\n").encode())
        except Exception:
          pass

  def close(self):
    print("SERVER Closed")
    with self.lock:
      items = list(self.clients.values())
      self.clients.clear()
    for c in items:
      try: 
        c.close()
      except: 
        pass
    try: 
      self.sock.close()
    except:
      pass

if __name__ == "__main__":
  server = NetworkServer()
  server.start()