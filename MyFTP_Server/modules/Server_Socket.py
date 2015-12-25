#-*- coding:utf-8 -*-
#/usr/bin/env python
import SocketServer
class MyFTPSocket(SocketServer.BaseRequestHandler):
    def handle(self):
        conn = self.request
        conn.sendall('Welcome to Alan FTP Server !!!')