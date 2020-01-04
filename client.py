import pprint
import imaplib
import mailbox
import email.utils
import threading
import localmail
import smtplib
import socket
from socket import *
import redis
import  pickle
import ssl
from email.mime.text import MIMEText


    



rs = redis.Redis(host='localhost', port=6379, db=0)
rs.set('1','172.16.11.211')
rs.set('2','169.254.153.36')
rs.set('3','10.100.102.6')

IPAddr = gethostbyname(gethostname())
allow=False
#sockets
#packet, reply = "<packet>SOME_DATA</packet>", ""
Host = IPAddr
Port = 50008
buffsize = 1024*9
Addr = (Host,Port)
TCPclientsock = socket(AF_INET,SOCK_STREAM)
#TCPclientsock.settimeout(10)
TCPclientsock.connect((Host, Port))

for i in range(1, 4):
    check_user=rs.get(i)
    print "check"+check_user
    print "my ip"+IPAddr
    print (check_user==IPAddr)
    if(check_user==IPAddr):
        allow=True
if allow:
    print "allowed"
    while(True):
        print "-------------------------------"
        check=raw_input("hello client welcome to my server if u want to send mail click S and if you want to check out your emails click F: ")
        if check=="S":
            txt= raw_input("enter the txt you wanna send: ")
            subject= raw_input("enter the subject of your data: ")
            dst= raw_input("enter the ip of your dst client: ")
            data=["S",dst,subject,txt]
            byted_data= pickle.dumps(data)
            TCPclientsock.send(byted_data)
            server_data = TCPclientsock.recv(buffsize)
            print server_data

        if check=="F":
            data=["F",None,None,None]
            byted_data = pickle.dumps(data)
            TCPclientsock.send(byted_data)
            server_data = TCPclientsock.recv(buffsize)
            got_emails=pickle.loads(server_data)
            for email in got_emails:
                pprint.pprint(email)
else:
    print "you are not allowed to use this email server. bye bye "



