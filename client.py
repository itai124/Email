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
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key

#defs--------------------------------------------------------
def generate_a_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048*3,
        backend=default_backend())
    return private_key

def generate_key():
    key = Fernet.generate_key()
    return key

def encrypt_a_msg(message, public_key):
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def decrypt_a_msg(encrypted, private_key):
    original = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original

#-----------------------------------------------------
IPAddr = gethostbyname(gethostname())

#logging in to the auth server
Host = IPAddr
Port = 50009
buffsize = 1024*9
Addr = (Host,Port)
TCPclientsock = socket(AF_INET,SOCK_STREAM)
TCPclientsock.connect((Host, Port))
choice = raw_input("welcome to the auth server. if you want to sign up write T and if you want to log in write L: ")
TCPclientsock.send(choice)
data = TCPclientsock.recv(buffsize)
if data=="T":
    name=raw_input("please give me your user name:")
    password = raw_input("please give me your password:")
    choice=[name,password]
    send_auth=pickle.dumps(choice)
    TCPclientsock.send(send_auth)
    auth = TCPclientsock.recv(buffsize)
    Email_Server_addr = pickle.loads(auth)
elif data=="L":
    name=raw_input("please write your username:")
    password = raw_input("please write your password:")
    choice = [name, password]
    send_auth=pickle.dumps(choice)
    TCPclientsock.send(send_auth)
    auth = TCPclientsock.recv(buffsize)
    Email_Server_addr=pickle.loads(auth)
    







#sockets
#packet, reply = "<packet>SOME_DATA</packet>", ""
print Email_Server_addr
Host = Email_Server_addr[0]
Port = Email_Server_addr[1]
buffsize = 1024*9
Addr = (Host,Port)
TCPclientsock = socket(AF_INET,SOCK_STREAM)
#TCPclientsock.settimeout(10)
TCPclientsock.connect((Host, Port))

print "allowed"
private_key = generate_a_keys()  # generates public and private keys
public_key = private_key.public_key()
serialized_public_key=public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.PKCS1)#serialize the key
serialized_public_key=pickle.dumps(serialized_public_key)# pickle the key
TCPclientsock.send(serialized_public_key)# send the key
server_public_key = TCPclientsock.recv(buffsize)#recv key from server
server_public_key=pickle.loads(server_public_key)#load the key
server_public_key= load_pem_public_key(server_public_key, backend=default_backend())#back to the first form
while(True):
    print "-------------------------------"
    check=raw_input("hello client welcome to my server if u want to send mail click S and if you want to check out your emails click F: ")
    if check=="S":
        txt= raw_input("enter the txt you wanna send: ")
        subject= raw_input("enter the subject of your data: ")
        dst= raw_input("enter the ip of your dst client: ")
        data=["S",dst,subject,txt]
        byted_data= pickle.dumps(data)
        encrypted_msg = encrypt_a_msg(byted_data, server_public_key)
        print "encrypted "+encrypted_msg
        TCPclientsock.send(encrypted_msg)
        server_data = TCPclientsock.recv(buffsize)
        decrypted_msg = decrypt_a_msg(server_data,private_key)
        print "after decrypte "+decrypted_msg

    if check=="F":
        data=["F",None,None,None]
        byted_data = pickle.dumps(data)
        encrypted_msg = encrypt_a_msg(byted_data, server_public_key)
        print "encrypted "+encrypted_msg
        TCPclientsock.send(encrypted_msg)
        server_data = TCPclientsock.recv(buffsize)
        decrypted_msg = decrypt_a_msg(server_data,private_key)
        print "after decrypte "+decrypted_msg
        got_emails=pickle.loads(decrypted_msg)
        for email in got_emails:
            pprint.pprint(email)





