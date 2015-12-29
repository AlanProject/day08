#-*- coding:utf-8 -*-
#/usr/bin/env python
import SocketServer
import pickle,os,time
import Auth_User
from Config_Read import ConfigRead
class MyFTPSocket(SocketServer.BaseRequestHandler):
    staus_coding = {
        'auth_success':'200',
        'auth_filed':'201',
        'isfile':'202',
        'unfile':'203',
        'trans_ok':'300'
    }
    def handle(self):
        self.conn = self.request
        self.conn.send('Welcome to Alan FTP Server !!!')
        self.user_auth()
        self.comm_argv()
    #用户认证
    def user_auth(self):
        auth_count = 0
        while auth_count < 3:
            #从客户端接收用户名和密码
            user_info = pickle.loads(self.conn.recv(1024))
            self.user_name = user_info.get('user_name')
            self.user_pass = user_info.get('user_pass')
            #对用户密码进行验证 如果成功
            if Auth_User.auth_user(self.user_name,self.user_pass):
                self.conn.send(self.staus_coding.get('auth_success'))
                return True
            else:
                self.conn.send(self.staus_coding.get('auth_filed'))
                auth_count += 1
    def comm_argv(self):
        while True:
            self.command=self.conn.recv(1024).split()
            if hasattr(self,self.command[0]):
                func = getattr(self,self.command[0])
                func()
    def ls(self):
        self.base_path = ConfigRead().user_dir(self.user_name)
        file_name = os.listdir(self.base_path)
        file_number = str(len(os.listdir(self.base_path)))
        self.conn.send(file_number)
        self.conn.recv(1024)
        for i in file_name:
            file = os.path.join(self.base_path,i)
            create_time = time.localtime(os.stat(file).st_ctime)
            date = '%d/%d/%d %d:%d'%(create_time.tm_year,create_time.tm_mon,create_time.tm_mday,create_time.tm_hour,create_time.tm_min)
            string = '%s\t%d\t%s'%(i,os.path.getsize(file),date)
            self.conn.recv(1024)
            self.conn.send(string)
    def get(self):
        file_name = os.path.join(self.base_path,self.command[1])
        if not os.path.isfile(file_name):
            self.conn.send(self.staus_coding.get('unfile'))
        else:
            self.conn.send(self.staus_coding.get('isfile'))
            self.conn.recv(100)
            file_size = str(os.path.getsize(file_name))
            self.conn.send(file_size)
            self.conn.recv(100)
            file_data = 0
            with open(file_name,'rb') as file_read:
                while file_data != int(file_size):
                    data = file_read.read(2048)
                    file_data += len(data)
                    self.conn.sendall(data)
            self.conn.recv(1024)
    def put(self):
        file_name = os.path.join(self.base_path,os.path.basename(self.command[1]))
        self.conn.send('start')
        file_size = int(self.conn.recv(1024))
        self.conn.send('ok')
        file_data = 0
        with open(file_name,'wb') as file_write:
            while file_data != file_size:
                data = self.conn.recv(2048)
                file_write.write(data)
                file_data += len(data)
        self.conn.send('ok')
    def rm(self):
        file_name = os.path.join(self.base_path,os.path.basename(self.command[1]))
        os.remove(file_name)
        self.conn.send('remove %s ok'%os.path.basename(self.command[1]))
if __name__ == '__main__':
    test = MyFTPSocket()
    print test.list_dir()