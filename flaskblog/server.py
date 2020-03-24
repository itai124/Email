import email.utils
import threading
import thread
import localmail
from socket import *
import pprint
import imaplib
import mailbox
import email.utils
import smtplib
import redis
import pickle
import  ssl
import StringIO
from threading import Lock, Thread
from email.mime.text import MIMEText
import sqlite3 as lite
import sys


import base64
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



def smtp_mail(txt,subject,dst,src):

    msg = MIMEText(txt)
    msg['To'] = email.utils.formataddr(('Recipient-', dst))
    msg['From'] = email.utils.formataddr(('Author-', src))
    msg['Subject'] = subject

    server = smtplib.SMTP(SMTP_IP, SMTP_PORT)
    server.login('user', 'password')
    server.set_debuglevel(True)  # show communication with the server
    try:
        server.sendmail(src, dst, msg.as_string())
        print "sending email..."
    except:
        print  "no send"
    finally:
        server.quit()

#https://www.php.net/manual/en/function.imap-search.php
#
def fetch_mail_msg(addr):
    IMAP_IP = "10.100.102.7"
    IMAP_PORT= 143
    imap = imaplib.IMAP4(IMAP_IP,IMAP_PORT)
    imap.login('username', 'password')
    imap.select('Inbox')
    tmp, data = imap.search(None, 'ALL')
    if tmp != 'OK':
        print "ERROR getting messages"
    emails = []
    print "printing type"
    print(data)
    print type(data[0])
    for num in data[0].split():
            print "------"
            tmp, data = imap.fetch(num, '(RFC822)')
            print  data
            if tmp != 'OK':
                print "ERROR getting message", num
            print('Message: {0}\n'.format(num))
            emails.append(data[0][1])
                #pprint.pprint(data[0][1])
    return emails
    imap.close()

#-----------------------------------------------------

def handler(clientsock,addr,emails,keys):
    client_public_key = clientsock.recv(Buffsize)
    send_client_public_key=pickle.loads(client_public_key)
    client_public_key= load_pem_public_key(send_client_public_key, backend=default_backend())
    serialize_public_key=public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.PKCS1)
    send_serialize_public_key=pickle.dumps(serialize_public_key)
    clientsock.send(send_serialize_public_key)
    print "end of public key transformation"
    print "start safe communication>>"
    while 1:
        data = clientsock.recv(Buffsize)
        print "encrypted "+ data
        decrypted_msg = decrypt_a_msg(data, private_key)
        print "decrypted_msg" + decrypted_msg
        fixed_data=pickle.loads(decrypted_msg)
        print fixed_data
        print "end fixed"
        if not fixed_data:
            print "breaking"
            break
        if(fixed_data[0]=="S"):
            lock.acquire()
            print 'lock'
            smtp_mail(fixed_data[4],fixed_data[3],fixed_data[2],fixed_data[1])
            msg= "sent your mail"
            encrypted_msg = encrypt_a_msg(msg, client_public_key)
            clientsock.send(encrypted_msg)
            print "unlock"
            lock.release()
        elif(fixed_data[0]=="F"):
            lock.acquire()
            print "lock"
            pass_emails=fetch_mail_msg(addr[0])
            pprint.pprint(pass_emails)
            byted_data = pickle.dumps(pass_emails)
            encrypted_msg = encrypt_a_msg(byted_data, client_public_key)
            clientsock.send(encrypted_msg)
            print "unlock"
            lock.release()






# main
SMTP_PORT = 2025
IMAP_PORT = 143
Host='10.100.102.7'
SMTP_IP="10.100.102.7"
IMAP_IP="10.100.102.7"
lock=Lock()
emails=[]
counter=0
mail_thread = threading.Thread(
    target=localmail.run,
    args=(SMTP_PORT, IMAP_PORT, 8880, 'localmail.mbox')
)

mail_thread.start()

print "waiting for clients"
private_key = generate_a_keys()#generates public and private keys
public_key = private_key.public_key()
keys=[private_key,public_key]
Socket_Port= 50003
Buffsize = 1024 * 100
Addr = (Host, Socket_Port)
servsock = socket(AF_INET, SOCK_STREAM)
#servsock.settimeout(10)
'''https://www.example-code.com/python/ssl_server.asp'''
servsock.bind(Addr)
servsock.listen(3)

while True:
    print "Im waiting for connection..."
    clientsock, addr = servsock.accept()
    print "yay! connected from: ", addr

    thread.start_new_thread(handler, (clientsock, addr, emails,keys))

servsock.close()




#localmail.shutdown_thread(thread)
#print "shutdown localmail"