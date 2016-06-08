#!/usr/bin/python3
# encoding: utf-8

import select
import socket
import sys

# 创建套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接服务端
server_address = ('127.0.0.1', 5000)
client_socket.connect(server_address)

# 监听client_socket
poller = select.poll()
READ_ONLY = (select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR)
poller.register(client_socket, READ_ONLY)

# 将标准输入也加入监听
poller.register(sys.stdin, READ_ONLY)

# 轮询
while True:
    events = poller.poll()
    for fd, flag in events:
        if fd == sys.stdin.fileno():
            # 读取标准输入，然后发送给服务端
            msg = sys.stdin.readline().encode()
            client_socket.send(msg)
        elif fd == client_socket.fileno():
            # 从socket读入
            msg = client_socket.recv(64)
            if len(msg) == 0:
                client_socket.close()
                poller.unregister(client_socket)
                client_socket.close()
                break
            else:
                print('recv:', msg.decode())
                