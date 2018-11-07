from socket import *
import sys
import getpass




class DictClient(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.address = (host,port)
        self.sockfd = socket()
        self.sockfd.connect(self.address)

    def main(self):
        while True:
            print('''
            ============Welcome============
            |                             |
            --1.注册     2.登陆    3.退出--
            |                             |
            ===============================

            ''') 
            try :
                cmd = int(input("请输入"))

            except Exception as e:
                print("命令错误")
                continue
            
            if cmd not in [1,2,3]:
                print("命令错误")
                continue
            elif cmd == 1:
                self.do_register()
            
            elif cmd == 2:
                self.do_login()

            elif cmd ==3:
                self.do_exit()

    def do_register(self):
        while True:
            name = input("请输入用户名:")
            password = getpass.getpass("请输入密码:")
            password2 = getpass.getpass("请再次输入密码:")
            if (" " in name) or (" "in password):
                print("用户名和密码不能有空格")
                continue
            elif password != password2:
                print("两次输入的密码不同,请重新输入!")
                continue
            msg = 'R {} {}'.format(name,password)
            self.sockfd.send(msg.encode())
            data = self.sockfd.recv(128).decode()
            if data == 'ok':
                print("注册成功")
                
            elif data == 'exist':
                print("用户名已存在")
            else :
                print("注册失败")
            break

    def do_login(self):
        while True:
            name = input("请输入用户名:")
            password = getpass.getpass("请输入密码:")
            self.sockfd.send
            msg = 'L {} {}'.format(name,password)
            self.sockfd.send(msg.encode())
            if (" " in name) or (" " in password):
                print("用户名和密码不能有空格")
                continue
            data = self.sockfd.recv(128).decode()
            if data == "ok":
                print("登录成功")
                self.login(name)

            else:
                print("登陆失败")
            break
        
    def login(self,name):
        while True:
            print('''
            ============查询界面============
            |                              |
            --1.查询    2.查询记录   3.退出--
            |                              |
            ===============================
            ''')
            try:
                cmd = int(input("请输入>>"))
            except Exception as e:
                print("命令错误",e)
                continue
            
            if cmd not in [1,2,3]:
                print("命令错误")
                
                continue
            elif cmd == 1:
                self.do_query(name)
            elif cmd == 2:
                self.do_hist(name)
            elif cmd ==3:
                return

    def do_query(self,name):
        word = input("请输入要查询的单词:")
        msg = 'Q {} {}'.format(word.strip(),name)
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(1024).decode()
        if data == "N":
            print("对不起,您查询的单词不存在")
        else:
            print(word,':',data)

    def do_hist(self,name):
        msg = "S {}".format(name)
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(1024).decode()
        print(data)

    def do_exit(self):
        self.sockfd.send(b'E')









if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('address error')
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
    clientapp = DictClient(host,port)
    clientapp.main()
















