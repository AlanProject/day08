#-*- coding:utf-8 -*-
#/usr/bin/env python
import os
import hashlib
def auth_user(user_name,user_passwd):
    base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/config/'

