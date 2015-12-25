#-*- coding:utf-8 -*-
#/usr/bin/env python
import pickle
def user_data_init():
    user_data = {'Alan':'admin',
                 'Lisa':'root'
                 }
    with open('user.db','w') as user_file:
        pickle.dump(user_data,user_file)

if __name__ == '__main__':
    user_data_init()