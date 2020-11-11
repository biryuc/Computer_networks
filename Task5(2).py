#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 11:38:19 2019

@author: yana
"""
import sys
import select
import socket
import ipaddress as ip

net1 = ip.IPv4Network('192.168.0.0/255.255.255.0')
#net2 = ip.IPv4Network('192.168.1.0/255.255.255.0')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
s.bind(('',11720)) #привязываем ко всем интерфейсам, к одному порту 

input = [sys.stdin, s]

while True:
    r,w,e = select.select(input, [], [])
    #select.select(rlist, wlist, xlist[, timeout])
    #rlist: wait until ready for reading
    #The return value is a triple of lists of objects that are ready
    for op in r:
        if (op == sys.stdin):
            #print (op.readline().rstrip())
            message = op.readline().rstrip()
            message = message.encode('utf-8')
            s.sendto(message,(str(net1.broadcast_address), 11720))
            #s.sendto(message,((str(net2.broadcast_address), 11720))
        else:
            data, addr = s.recvfrom(1024) #слушаем мы с одного порта в любом случае
            data = data.decode('utf-8')
            if (ip.ip_address(addr[0]) in net1.hosts()):
                s.sendto(message,(str(net1.broadcast_address), 11720))
                
            if (ip.ip_address(addr[0]) in net1.hosts()):
                s.sendto(message,(str(net1.broadcast_address), 11720))
                
            print("received message: " + data + " (from: " + addr[0] + ')')
        
            #если ввели сообщение, то отправляем его всем
            #если пришло сообщение, то смотрим от кого, пересылаем другому и печатаем у себя
            

s.close()
