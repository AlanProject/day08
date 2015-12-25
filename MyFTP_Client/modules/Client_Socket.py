#-*- coding:utf-8 -*-
#/usr/bin/env python
import socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = ('127.0.0.1',8080)
client_socket.connect(host)
welcome_info = client_socket.recv(1024)
print welcome_info
