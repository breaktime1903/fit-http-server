#!/usr/bin/python3
import socket,os,sys,time,website_gen,_thread
#用python3编写的HTTP服务器
connected=False
localaddress='192.168.1.13'
port=8080
index_dir='./website'
coding='utf-8'
def log(level,content):
    if level==3:
        warning_level='ERROR'
    elif level==2:
        warning_level='WARNING'
    elif level==1:
        warning_level='IMPORTANT'
    elif level==0:
        warning_level='NOTICE'
    print(f'[{time.asctime( time.localtime(time.time()))}]{warning_level}:{content}')

def handler(client):
    receive_data=client.recv(1024).decode(coding)
    header_lines=receive_data.splitlines()
    log(0,header_lines[0])
    try:
        header_list=header_lines[0].split()
        file=header_list[1]
        
    except:
        log(2,'Header出现错误，退出Handler')
        return
    log(0,f'{file}')
    response_headers='HTTP/1.1 200 OK\r\n'
    response_headers+='\r\n'
    log(0,'读取文件')
    try:
        if os.path.isdir(index_dir+file):
            response_body=website_gen.website_gen(index_dir+file).encode(coding)
        else:
            f=open(index_dir+file,'rb')
            response_body=f.read()
    except:
        log(0,'未找到文件，返回404')
        response_headers='HTTP/1.1 404 ERROR\r\n\r\n'
        response_body='<h1>File Not Found<h1>'.encode(coding)
    log(0,f'发送至远程主机中......')
    client.send(response_headers.encode(coding))
    client.send(response_body)
    client.close()
    log(0,'发送完毕')

def main():
    log(0,f'启动服务器......')
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((localaddress,port))
    server.listen(100)
    log(1,f'服务器启动完毕，启动于{localaddress}:{port}')
    while True:
        client_socket,client_address=server.accept()
        log(0,f'已经与{client_address[0]}:{client_address[1]}连接,启动Handler')
        _thread.start_new_thread(handler,(client_socket,))
        #handler(client_socket)
while True:
    try:
        main()
    except KeyboardInterrupt:
        log(1,'Ctrl-C输入，退出')
        exit(0)
    except OSError as reason:
        log(3,f'出现致命错误:{reason}，退出')
        exit(-1)
    except:
        log(3,'遇到错误，重启服务器中......')


