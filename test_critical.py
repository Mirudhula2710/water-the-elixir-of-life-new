import socket, json
HOST, PORT = '127.0.0.1', 65432
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json.dumps({'zone': 'Hostel Blocks', 'level': -50.0}).encode('utf-8'))
except: pass
