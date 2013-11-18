#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import base64
import select
import socket
import httplib
import os
import sys
#base64.encodestring("das\120xsdada\s")

def usage ():
    print "connect_to_http_proxy %s (lh2008999@gmail.com)"
    print "usage: connect_to_http_proxy <desthost> <destport>"

if len(sys.argv) != 3:
    usage()
    print sys.argv
    sys.exit()

proxy_host="web-proxy-domain.com"
proxy_port="8080"
dest_host=""
dest_port=""
dest_host, dest_port=sys.argv[1:]

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((proxy_host,int(proxy_port)))
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
req="CONNECT "+dest_host+":"+dest_port + " HTTP/1.0\r\n\r\n"
sock.send(req)
resp=sock.recv(100000)
if resp.find("200") < 0:
    print req,resp
    exit(-1)

ep=select.epoll()
ep.register(sock.fileno(),select.EPOLLIN)
ep.register(sys.stdin.fileno(),select.EPOLLIN)
while True:
    events=ep.poll(1,2)
    for fd,event in events:
        if event & select.EPOLLERR:
            sys.exit(0)
        if event & select.EPOLLIN and fd==sock.fileno():
            os.write(sys.stdout.fileno(),sock.recv(1024*100)) 
        if event & select.EPOLLIN and fd==sys.stdin.fileno():
            os.write(sock.fileno(),sys.stdin.read()) 

#conn=httplib.HTTPConnection(proxy_host+":"+proxy_port)
#conn.request("CONNECT",dest_host+":"+dest_port)
#res=conn.getresponse()
#print res.read()
#if res.status != 200:
#    print res.status,res.reason
#    sys.exit()
