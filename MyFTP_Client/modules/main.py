#-*- coding:utf-8 -*-
#/usr/bin/env python
import sys,os
import pickle
import socket
class ClientArgv(object):
    def __init__(self,argvs):
        self.argvs = argvs
        self.argvs_parser()
        self.handle()
    def handle(self):
        self.connect()
        #接收打印欢迎信息
        server_data = self.client_socket.recv(1024)
        print server_data
        if self.auther():
            self.comm_argv()
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
                self.host = self.argvs[self.argvs.index('-s')+1]
                self.port = int(self.argvs[self.argvs.index('-p')+1])
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
    def comm_help(self):
        print '''
        get [file]    :Download file
        put [file]    :Upload file
        cd [path]     :change dir path
        rm [path]     :delete file
        exit          :exit Ftp system
        '''
    #连接服务器端socket
    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.client_socket.connect((self.host,self.port))
        except  socket.error as e:
            sys.exit('connect server filed')
    #用户认证模块
    def auther(self):
        auther_count = 0
        while auther_count < 3:
            user_name = raw_input('Please input username:')
            if len(user_name) == 0:continue
            user_pass = raw_input('Please input passwd:')
            if len(user_pass) == 0:continue
            data = pickle.dumps({'user_name':user_name,'user_pass':user_pass})
            self.client_socket.send(data)
            server_data = self.client_socket.recv(1024)
            if server_data == '200':
                return True
            else:
                print '%s user name or password error please try agin'%server_data
                auther_count += 1
        else:
            sys.exit('User or Passwd too many mistakes')
    #命令调度
    def comm_argv(self):
        while True:
            self.command = raw_input('>>>')
            if len(self.command.split()) == 0:continue
            if hasattr(self,self.command.split()[0]):
                func = getattr(self,self.command.split()[0])
                func()
            else:
                self.comm_help()
    #下载文件
    def get(self):
        comm_list = self.command.split()
        if len(comm_list) < 2:
            self.comm_help()
            sys.exit()
        self.client_socket.send(self.command)
        status_coding = self.client_socket.recv(1024)
        if status_coding == '203':
            print 'file is not found'
        else:
            self.client_socket.send('start')
            file_size = int(self.client_socket.recv(1024))
            self.client_socket.send('ok')
            file_data = 0
            with open(comm_list[1],'wb') as file_write:
                while file_data != file_size:
                    data = self.client_socket.recv(2048)
                    file_write.write(data)
                    file_data += len(data)
            print '%s Transfer ok'%comm_list[1]
            self.client_socket.send('ok')
    #上传文件
    def put(self):
        comm_list = self.command.split()
        if len(comm_list) < 2:
            self.comm_help()
            sys.exit()
        #发送命令
        self.client_socket.send(self.command)
        #接受服务器确认收到命令的消息
        self.client_socket.recv(1024)
        if not os.path.isfile(comm_list[1]):
            print 'File is not found'
        else:
            file_size = str(os.path.getsize(comm_list[1]))
            self.client_socket.send(file_size)
            self.client_socket.recv(100)
            file_data = 0
            with open(comm_list[1],'rb') as file_read:
                while file_data != int(file_size):
                    data = file_read.read(2048)
                    file_data += len(data)
                    self.client_socket.sendall(data)
            self.client_socket.recv(1024)
    #列出文件目录
    def ls(self):
        self.client_socket.send(self.command)
        file_number = int(self.client_socket.recv(1024))
        self.client_socket.send('OK')
        for i in range(file_number):
            self.client_socket.send('ok')
            file_name = self.client_socket.recv(1024)
            print file_name
    def rm(self):
        self.client_socket.send(self.command)
        rm_data = self.client_socket.recv(1024)
        print rm_data
    #切换文件目录
    def cd(self):
        comm_list = self.command.split()
        if len(comm_list) < 2:
            self.comm_help()
            sys.exit()

    #退出FTP客户端
    def exit(self):
        sys.exit('Exiting')
