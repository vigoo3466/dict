#  coding:utf-8
from socket import *
import os
from pymongo import MongoClient
import signal
import sys
from threading import Thread
import time
import pickle


class DictServer(object):
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 8080
        self.addr = (self.host,self.port)
        self.connect_mongo()
        self.creat_sock()
    #创建数据库连接
    def connect_mongo(self):
        self.client = MongoClient()        
        self.db = self.client['yydict']
        # self.table = self.db.['']

    #创建套接字
    def creat_sock(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sockfd.bind(self.addr)

    #循环接受请求
    def handle(self):
        print('Linsten the port 8080...')
        self.sockfd.listen(5)
        while True:
            try:
                connfd,addr = self.sockfd.accept()
                print("Connect from ",addr)
            except Exception as e:
                print(e)
                continue
            thread = Thread(target = self.do_child,args=(self.db,connfd))
            thread.setDaemon(True)   
            thread.start()

    def do_child(self,db,connfd):
        while True:
            data = connfd.recv(128).decode()
            print(connfd.getpeername(),':',data)
            if not data or data[0] == "E":
                connfd.close()
                sys.exit(0)

            elif data[0] == "L":
                print("登录操作")
                msg = data.split()
                username = msg[1]
                password = msg[2]
                self.do_login(username,password,connfd)

            elif data[0] == "R":
                print("注册操作")
                msg = data.split()
                username = msg[1]
                password = msg[2]
                self.do_register(username,password,connfd)
                
            elif data[0] == "Q":
                print("查询操作")
                msg = data.split()
                word = msg[1]
                username = msg[2]
                print(word,username)
                self.do_query(word,username,connfd)
            
            elif data[0] == "S":
                print("查询记录")
                msg = data.split()
                username = msg[1]
                self.do_hist(username,connfd)


    def do_login(self,username,password,connfd):
        result = self.db['user'].find_one({"username":username},{"_id":0})
        if result['password'] == password:
            connfd.send(b"ok")
        else:
            connfd.send(b"fall")      

        
        
    def do_register(self,username,password,connfd):
        result = self.db['user'].find({"username":username},{"_id":0})
        a = 0
        for i in result:
            a += 1
        if a != 0:
            connfd.send(b'exist')
            return
        try:
            self.db['user'].insert_one({"username":username,"password":password})
            connfd.send(b"ok")
        except:
            connfd.send(b"fall")

    def do_query(self,word,username,connfd):
        self.db["hist"].insert_one({'username':username,'word':word,"time":time.ctime()})
        result = self.db["dict"].find_one({"word":word},{'_id':0})

        if not result:
            connfd.send(b'N')

        else:
            mean = result['mean']
            print(mean)
            connfd.send(mean.encode())

    def do_hist(self,username,connfd):
        print(username)
        a = 0
        result = self.db["hist"].find({'username':username},{'_id':0})
        datas = ""
        for find in result:
            print(find)
            data = find['username'] + ' ' + find['word'] + ' ' + find['time'] + "\n"
            datas += data
            a += 1
        connfd.send(datas.encode())
        if a == 0:
            connfd.send(b'None')
            


    def start(self):
        self.handle()



if __name__ =="__main__":
    dictapp = DictServer()
    dictapp.start()