#-*- coding:utf-8 -*-
#/usr/bin/env python
import sys
import pickle
import socket
class ClientArgv(object):
    def __init__(self,argvs):
        self.argvs = argvs
        self.argvs_parser()
        self.handle()
    #处理参数
    def argvs_parser(self):
        argv_list = ['-s','-p']
        if len(self.argvs) < 5:
            self.help()
            sys.exit()
        for i in argv_list:
            if i not in self.argvs:
                sys.exit('Argv is not found please try again !!!')
            try:
                self.host = self.argvs(self.argvs.index('-s')+1)
                self.port = int(self.argvs(self.argvs.index('-p')+1))
            except (ValueError,IndexError) as e:
                self.help()
                sys.exit()
    #定义help信息
    def help(self):
        print '''
        MyFTP Client command argv
        -s      :Server Host Address IP or Domain
        -p      :Server Port
        '''
    #连接服务器端socket
    def connect(self):
        try:
            client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client_socket.connect((self.host,self.port))
        except  socket.error as e:
            sys.exit('connect server filed')
    #用户认证模块
    def auther(self):
        auther_count = 0
        while auther_count < 3:
            user_name = raw_input('Please input username:')
            #if len(user_name) == 0:continue
            user_pass = raw_input('Please input passwd:')
            #if len(user_pass) == 0:continue
            if user_name and user_pass:
                data = pickle.dumps({'user_name':user_name,'user_pass':user_pass})
                socket.send(data)
                server_data = socket.recv(1024)
                if server_data == '200':
                    return True
            auther_count += 1
        else:
            sys.exit('User or Passwd too many mistakes')


    #和服务器进行认证/交互主函数
    def handle(self):
        self.connect()
        if self.auther():
            pass