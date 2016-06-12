#!/usr/bin/python3
# encoding: utf-8
import select
import socket
import sys

class Close_exception(Exception):
    def __str__(self):
        return repr('对方关闭了连接')

def epoll_loop():
    global epoll_obj
    global client_socket
    epoll_obj.register(client_socket, select.EPOLLIN)
    epoll_obj.register(sys.stdin, select.EPOLLIN)
    
    while True:
        events = epoll_obj.poll()
        
        for fd, event in events:
            # 处理服务端发送过来的数据
            if fd == client_socket.fileno():
                msg = client_socket.recv(16)
                if len(msg) == 0:
                    raise Close_exception()
                else:
                    print('recv:', msg.decode())
                    msg = ''
            # 处理用户输入
            else:
                msg = sys.stdin.readline()
            if client_socket:
                client_socket.send(msg.encode())
                    

if __name__ == '__main__':
    # 创建监听套接字
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接服务端
    server_address = ('127.0.0.1', 5000)
    client_socket.connect(server_address)
    client_socket.setblocking(False)
    
    global epoll_obj
    epoll_obj = select.epoll()
    
    try:
        epoll_loop()
    except KeyboardInterrupt:
        print('你主动退出了程序')
    except Close_exception:
        print('对方关闭了连接')
    finally:
        epoll_obj.unregister(client_socket)
        client_socket.close()