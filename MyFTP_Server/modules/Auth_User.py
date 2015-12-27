#-*- coding:utf-8 -*-
#/usr/bin/env python
import os,sys
import pickle
import hashlib
def auth_user(user_name,user_passwd):
    hash_passwd = hashlib.md5()
    hash_passwd.update(user_passwd)
    user_passwd = hash_passwd.hexdigest()
    user_file=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/config/user.db'
    if not os.path.isfile(user_file):
        sys.exit('User config is not found please run bin/Create_User.py')
    with open(user_file,'r') as file_read:
        user_data = pickle.load(file_read)
    if user_data.has_key(user_name):
        if user_passwd == user_data.get(user_name):
            return True
    return False

if __name__ == '__main__':
   print  auth_user('Ala','rot')