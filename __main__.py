#!/usr/bin/python3
# -*- coding: utf-8 -*-


from yaohaologin import *
import time

if __name__ == '__main__':
    list = [
        {
            "phone": "username_1",
            "pwd": "password_1",
        }, {
            "phone": "username_2",
            "pwd": "password_2",
        },
    ]
    for usr in list:
        userLogin = yaohaologin(usr['phone'], usr['pwd'])
        count = 0
        loginRes = userLogin.login()
        while count < 20 and not loginRes:
            print(usr['phone'] + " login fail, retry")
            count += 1
            time.sleep(1)
            loginRes = userLogin.login()

        if not loginRes:
            print(usr['phone'] + " login fail, stop retrying")
            continue

        print(usr['phone'] + " login success, start renew")

        count = 0
        renewRes = userLogin.renewal()
        while count < 20 and not renewRes:
            print(usr['phone'] + " renewal fail, retry")
            count += 1
            time.sleep(1)
            renewRes = userLogin.renewal()

        if not loginRes:
            print(usr['phone'] + " renewal fail, stop retrying")
            continue

        print(usr['phone'] + " renewal success")
