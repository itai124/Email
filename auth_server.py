import socket
import redis
from socket import *
import threading
import  thread
import pickle



def handler(clientsock,addr,rs,port,host):
    data = clientsock.recv(Buffsize)
    if data=="T":
        clientsock.send(data)
        data = clientsock.recv(Buffsize)
        fixed_data=pickle.loads(data)
        username =fixed_data[0]
        password= fixed_data[1]
        rs.set(username,password)
        allow=True
        if allow == True:
            email_Addr = (host, port)
            data = pickle.dumps(email_Addr)
            clientsock.send(data)
    elif data=="L":
        clientsock.send(data)
        data = clientsock.recv(Buffsize)
        fixed_data=pickle.loads(data)
        username =fixed_data[0]
        password= fixed_data[1]
        allow= False
        if allow == True:
            email_Addr = (host, port)
            data = pickle.dumps(email_Addr)
            clientsock.send(data)
        try:
            real_password=rs.get(username)
            if real_password==password:
                allow=True
            if allow == True:
                email_Addr = (host, port)
                data = pickle.dumps(email_Addr)
                clientsock.send(data)
        except:
            allow=False




#creting aut server
rs = redis.Redis(host='localhost', port=6379, db=0)
rs.set('danny','1789')
rs.set('moshe','1234')
rs.set('itai','dhurt')
print "waiting for clients"
IPAddr = gethostbyname(gethostname())
Host = IPAddr
print Host
Socket_Port= 50009
Buffsize = 1024 * 9
Addr = (Host, Socket_Port)
servsock = socket(AF_INET, SOCK_STREAM)
servsock.bind(Addr)
servsock.listen(3)
email_port=50003
email_host= IPAddr
while True:
    print "Im waiting for connection..."
    clientsock, addr = servsock.accept()
    print "yay! connected from: ", addr

    thread.start_new_thread(handler, (clientsock, addr,rs,email_port,email_host))

servsock.close()
