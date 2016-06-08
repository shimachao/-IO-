# -*- coding:utf-8 -*-

import socket
from select import select

server_address = ('127.0.0.1', 6666)

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.bind(server_address)
listen_socket.listen(1)

sockets_to_read = [listen_socket]
sockets_to_write = []

while True:
    readable_sockets, writable_sockets, exception_sockets = select(sockets_to_read, sockets_to_write, [])

    # 处理可读的socket
    for sock in readable_sockets:
        if sock is listen_socket:
            # 处理新来的连接
            conn_socket, client_address = sock.accept()
            print("收到来自", client_address, "的连接")
            # 将代表连接的socket加入到等待读写列表中
            sockets_to_read.append(conn_socket)
            sockets_to_write.append(conn_socket)
        else:
            # 处理可读的客户socket连接
            data = sock.recv(1024)
            print("收到来自", sock.getpeername(), "的数据:", data.decode())

    # 处理可写的socket
    for socket_ in writable_sockets:
        socket_.send("你好，客户端".encode())
        # 将该socket从等待读写的socket列表中移出
        sockets_to_read.remove(socket_)
        sockets_to_write.remove(socket_)

        socket_.close()
