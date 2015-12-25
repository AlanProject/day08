#-*- coding:utf-8 -*-
#/usr/bin/env python
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import main

if __name__ == '__main__':
    EntryPort = main.ArgvHandle(sys.argv)