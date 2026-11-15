import sys, json, socket
port = int(sys.argv[1]); cmds = json.loads(sys.stdin.read())
s = socket.socket(); s.connect(('127.0.0.1', port)); s.sendall(json.dumps(cmds).encode() + b'\n\n'); s.shutdown(socket.SHUT_WR)
d = b''
while True:
    x = s.recv(65536)
    if not x: break
    d += x
for r in json.loads(d.decode()): print(json.dumps(r)[:int(sys.argv[2]) if len(sys.argv) > 2 else 3000])
