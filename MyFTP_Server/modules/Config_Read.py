#-*- coding:utf-8 -*-
#/usr/bin/env python
import os,sys
import ConfigParser
class ConfigRead(object):
    def __init__(self):
        self.base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/config/'
        self.config_file = self.base_dir+'MyFTP.conf'
        self.config = ConfigParser.ConfigParser()
    def server_info(self):
        self.config.read(self.config_file)
        self.server_address=self.config.get('server','server_address')
        self.server_port = self.config.get('server','server_port')
        self.MyFTP_address = (self.server_address,int(self.server_port))
        return self.MyFTP_address
if __name__ == '__main__':
    test = ConfigRead()
    print test.server_info()