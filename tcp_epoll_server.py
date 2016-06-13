#!/usr/bin/python3
# encoding: utf-8
import select
import socket
import sys
import fcntl
import os

def epoll_loop():
    global epoll_obj
    global server_socket
    
    epoll_obj.register(server_socket, select.EPOLLIN)
    fl = fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL)
    fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, fl | os.O_NONBLOCK)
    epoll_obj.register(sys.stdin, select.EPOLLIN)
    
    while True:
        events = epoll_obj.poll()
        
        for fd, event in events:
            global client_socket
            # 处理客户端连接
            if fd == server_socket.fileno():
                global client_socket
                client_socket, client_addr = server_socket.accept()
                client_socket.setblocking(False)
                epoll_obj.register(client_socket, select.EPOLLIN)
            # 处理用户输入
            elif fd == sys.stdin.fileno():
                msg = sys.stdin.read()
                if client_socket:
                    client_socket.send(msg.encode())
            # 处理客户端发来的消息
            elif fd == client_socket.fileno():
                msg = client_socket.recv(16)
                if len(msg) == 0:
                    client_socket.close()
                    epoll_obj.unregister(fd)
                    client_socket = None
                else:
                    print('recv:', msg.decode())
    
    
if __name__ == '__main__':
    # 创建监听套接字
    server_address = ('127.0.0.1', 5000)
    global server_socket 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(1)
    global client_socket
    client_socket = None

    global epoll_obj
    epoll_obj = select.epoll()
    
    try:
        epoll_loop()
    except KeyboardInterrupt:
        print('你主动退出了程序')
    finally:
        epoll_obj.unregister(server_socket)
        server_socket.close()
        if client_socket:
            epoll_obj.unregister(client_socket)
            client_socket.close()
