#-*- coding:utf-8 -*-
#/usr/bin/env python
import Config_Read
import Server_Socket
class ArgvHandle(object):
    def __init__(self,args):
        self.argv = args
        self.MyFTP_argv()
    def MyFTP_argv(self):
        try:
            argv_frist = self.argv[1]
            if hasattr(self,argv_frist):
                func = getattr(self,argv_frist)
                func()
            else:
               self.MyFTP_help()
        except IndexError,e:
            self.MyFTP_help()
    def MyFTP_help(self):
        print '''
        ----------MyFTP Argv Info---------
        start       :Start Up MyFTP Server
        stop        :Stop MyFTP Server
        ----------------------------------
        '''
    def start(self):
        print 'start .....'
        #获取服务器ipaddress/port信息
        self.host_addr = Config_Read.ConfigRead().server_info()
        server = Server_Socket.SocketServer.ThreadingTCPServer(self.host_addr,Server_Socket.MyFTPSocket)
        server.serve_forever()
if __name__ == '__main__':
    test = ArgvHandle('test')
    test.start()