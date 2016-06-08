import socket
host = '127.0.0.1'
port = 6666

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((host, port))

sock.send('你好，服务端！'.encode())

print(sock.recv(1024).decode())

sock.close()
