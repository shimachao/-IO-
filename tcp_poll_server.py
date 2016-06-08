#!/usr/bin/python3
# encoding: utf-8
import select
import socket
import sys

# 创建监听套接字
server_address = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(1)

# 利用poll监听server_socket
# poll监听5种事件
# POLLIN:输入准备好
# POLLPRI:带外数据可读
# POLLOUT:准备好接受数据
# POLLERR:有错误发生
# POLLHUP:通道关闭
# POLLVAL:通道未打开
READ_ONLY = (select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR)
poller = select.poll()
poller.register(server_socket, READ_ONLY)
poller.register(sys.stdin, READ_ONLY)

client_socket = None

fd_to_sokcet = {server_socket.fileno(): server_socket}
while True:
    # 轮询
    events = poller.poll()
    for fd, flag in events:
        if fd == server_socket.fileno() and (flag & READ_ONLY):
            # 处理新来的连接
            client_socket , client_address = server_socket.accept()
            print('收到来自', client_address, '的连接')
            # 将新创建的客户端连接socket加入到监听中
            poller.register(client_socket, READ_ONLY)
            
        elif fd == sys.stdin.fileno() and (flag & READ_ONLY):
            # 接收控制台输入
            msg_to_send = sys.stdin.readline().encode()
            # 发送给对方
            client_socket.send(msg_to_send)
            
        else:
            # 处理连接上的可读
            if flag & READ_ONLY:
                msg = client_socket.recv(64)
                if len(msg) == 0:
                    poller.unregister(client_socket)
                    client_socket.close()
                    client_socket = None
                else:
                    print("收到:", msg.decode())
