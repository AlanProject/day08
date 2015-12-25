#-*- coding:utf-8 -*-
#/usr/bin/env python
with open('MyFTP.conf','rb') as file_read:
    file_read.seek(30)
    for i in file_read:
        print i.strip()
    print file_read.tell()