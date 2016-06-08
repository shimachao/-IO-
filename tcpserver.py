import socket
host = '127.0.0.1'
port = 6666

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))

s.listen(1)

while 1:
    conn, addr = s.accept()
    print('connect by', addr)
    data = conn.recv(1024);
    print(data)
    conn.send(b'hello client!')
    conn.close()
    
