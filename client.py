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
from email.mime.text import MIMEText


    



rs = redis.Redis(host='localhost', port=6379, db=0)
rs.set('1','172.16.11.211')
rs.set('2','172.16.10.154')
IPAddr = gethostbyname(gethostname())
#sockets
Host = 'localhost'
Port = 50007
buffsize = 1024*9
Addr = (Host,Port)
TCPclientsock = socket(AF_INET,SOCK_STREAM)
TCPclientsock.connect(Addr)
while(True):
    print "-------------------------------"
    check=raw_input("hello client welcome to my server if u want to send mail click S and if you want to check out your mails click F: ")
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



