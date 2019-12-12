from socket import *
import threading
import thread
import pickle

def handler(clientsock,addr):
    while 1:
        data = clientsock.recv(BUFSIZ)
        if not data:
            print "ending communication with",addr
            break
        msg = pickle.loads(data)
        print msg
        clientsock.send(data)
        clientsock.close()



BUFSIZ = 1024
HOST = 'localhost'
PORT = 50008
ADDR = (HOST, PORT)
serversock = socket(AF_INET, SOCK_STREAM)
serversock.bind(ADDR)
serversock.listen(3)
while True:
    print 'waiting for connection...'
    clientsock, addr = serversock.accept()
    print '...connected from:', addr
    thread.start_new_thread(handler, (clientsock, addr))

servsock.close()