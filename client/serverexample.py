import socket
import threading

class NetworkServer:
  def __init__(self, host="localhost", port=5000):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind((host, port))
    self.sock.listen(5)
    self.clients = {}  # name -> socket
    self.lock = threading.Lock()
    print("SERVER Up")

  def start(self):
    print("SERVER Waiting for connection")
    threading.Thread(target=self.server_input_loop, daemon=True).start()
    try:
      while True:
        conn, addr = self.sock.accept()
        print(f"SERVER Client connected: {addr}")
        thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
        thread.start()
    except KeyboardInterrupt:
      print("SERVER KeyboardInterrupt, closing")
      self.close()

  def handle_client(self, conn, addr):
    name = None
    try:
      data = conn.recv(4096)
      if not data:
        conn.close()
        return

      hello = data.decode(errors="replace").strip().split(maxsplit=1)
      if len(hello) < 2 or hello[0] != "HELLO":
        conn.sendall(b"ERROR Invalid HELLO\n")
        conn.close()
        return

      requested_name = hello[1]

      with self.lock:
        if requested_name in self.clients:
          conn.sendall(b"ERROR Name already taken\n")
          conn.close()
          return
        self.clients[requested_name] = conn
        name = requested_name

      print(f"SERVER Client '{name}' connected from {addr}")
      self.broadcast(f"SERVER {name} joined")

      while True:
        data = conn.recv(4096)
        if not data:
          break

        msg = data.decode(errors="replace").strip()
        if not msg:
          continue

        print(f"{name}: {msg}")

        parts = msg.split(maxsplit=1)
        cmd = parts[0].upper()

        if cmd == "MSG":
          if len(parts) == 2:
            self.broadcast(f"{name}: {parts[1]}")
          else:
            conn.sendall(b"ERROR MSG requires a message\n")
        elif cmd == "TO":
          if len(parts) == 2:
            to_parts = parts[1].split(maxsplit=1)
            if len(to_parts) == 2:
                target, body = to_parts[0], to_parts[1]
                self.send_to(target, f"{name} (private): {body}")
            else:
                conn.sendall(b"ERROR TO requires target and message\n")
          else:
            conn.sendall(b"ERROR TO requires target and message\n")
        else:
          conn.sendall(b"ERROR Unknown command\n")

    except ConnectionResetError:
      pass
    except Exception as e:
      print("SERVER handle_client exception:", e)
    finally:
      if name:
        print(f"SERVER Client disconnected: {name}")
        with self.lock:
          self.clients.pop(name, None)
        self.broadcast(f"SERVER {name} left")
      try:
        conn.close()
      except Exception:
        pass

  def server_input_loop(self):
    while True:
      try:
        msg = input()
      except EOFError:
        break
      if not msg:
        continue
      if msg.startswith("/to "):
        parts = msg.split(maxsplit=2)
        if len(parts) == 3:
          _, name, text = parts
          self.send_to(name, f"SERVER (to {name}): {text}")
        else:
          print("Usage: /to <name> <message>")
      else:
        self.broadcast(f"SERVER: {msg}")

  def broadcast(self, msg: str):
    with self.lock:
      items = list(self.clients.items())  # [(name, sock), ...]
    for name, client in items:
      try:
        client.sendall((msg + "\n").encode())
      except Exception:
        with self.lock:
          removed = self.clients.pop(name, None)
          if removed:
            try:
              removed.close()
            except Exception:
              pass

  def send_to(self, name: str, msg: str):
    with self.lock:
      client = self.clients.get(name)
    if client:
      try:
        client.sendall((msg + "\n").encode())
      except Exception:
        with self.lock:
          self.clients.pop(name, None)
        try:
          client.close()
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
      except Exception:
        pass
    try:
      self.sock.close()
    except Exception:
      pass


if __name__ == "__main__":
  server = NetworkServer()
  server.start()
