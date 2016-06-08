# -*-coding:utf-8-*-

import socket
from select import select

server_address = ('127.0.0.1', 6666)


def main():
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.connect(server_address)

    _socket.send('你好，服务端！'.encode())

    readable_sockets, w, e = select([_socket], [], [])

    for sock in readable_sockets:
        data = sock.recv(100)
        print("收到来自", sock.getpeername(), "的数据:", data.decode())

if __name__ == '__main__':
    main()
