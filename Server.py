
'''
重写了整个HTTP服务器，使用面向对象的方法编写
'''

import socket,re,json,_thread
class HTTPServer():
    address=('',80)
    listen_count=10
    def __init__(self):
        self.serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def serve_forever(self):
        self.serversocket.bind(self.address)
        self.serversocket.listen(self.listen_count)
        self.serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        while True:
            client,client_addr=self.serversocket.accept()
            self.Main_Handler(client,client_addr)
    def Main_Handler(self,client,addr):
        client_header=client.recv(8192).decode('utf-8')
        client_header_list=client_header.splitlines()
        print(f'{addr}Connected:{client_header_list[0]}')
        request_list=client_header_list[0].split()
        if request_list[0]=='GET':
            try:
                if request_list[1]=='/':
                    content=self.GET_Handler('./website/index.html')
                    header='HTTP/1.1 200 OK\nServer: FIT\n\n\n'
                else:
                    content=self.GET_Handler(request_list[1])
                    header='HTTP/1.1 200 OK\nServer: FIT\n\n\n'
            except:
                content=self.Code404Handler()
                header='HTTP/1.1 404 Not Found\n\n\n'
        client.send(header.encode('utf-8'))
        client.send(content.encode('utf-8'))
        client.close()
    def GET_Handler(self,filename):
        f=open(f'./website{filename}','rb')
        return f.read()
    def Code404Handler(self):
        try:
            f=open('404.html','rb')
            return f.read()
        except:
            return '404 Not Found'

    
server=HTTPServer()
server.address=('127.0.0.1',8080)
server.serve_forever()

    