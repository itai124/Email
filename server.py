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
from threading import Lock, Thread
from email.mime.text import MIMEText

def smtp_mail(txt,subject,dst,Ip):

    msg = MIMEText(txt)
    msg['To'] = email.utils.formataddr(('Recipient-', dst))
    msg['From'] = email.utils.formataddr(('Author-', Ip))
    msg['Subject'] = subject

    server = smtplib.SMTP(SMTP_IP, SMTP_PORT)
    server.login('user', 'password')
    server.set_debuglevel(True)  # show communication with the server
    try:
        server.sendmail(Ip, dst, msg.as_string())
        print "sending email..."
    except:
        print  "no"
    finally:
        server.quit()

def fetch_mail_msg(emails,addr):
    imap = imaplib.IMAP4(IMAP_IP,IMAP_PORT)
    imap.login('username', 'password')
    imap.select('Inbox')
    tmp, data = imap.search(None, 'ALL')
    emails = []
    for num in data[0].split():
            print "------"
            tmp, data = imap.fetch(num, '(RFC822)')
            print  data
            if tmp != 'OK':
                print "ERROR getting message", num
            print('Message: {0}\n'.format(num))
            if addr in data[0][1]:
                emails.append(data[0][1])
                pprint.pprint(data[0][1])
    return emails
    imap.close()


def handler(clientsock,addr,emails):
    while 1:
        data = clientsock.recv(Buffsize)
        fixed_data=pickle.loads(data)
        print fixed_data
        if not data:
            break
        if(fixed_data[0]=="S"):
            lock.acquire()
            smtp_mail(fixed_data[3],fixed_data[2],fixed_data[1],addr[0])
            clientsock.send("sent your mail")
            lock.release()
        elif(fixed_data[0]=="F"):
            lock.acquire()
            pass_emails=fetch_mail_msg(emails,addr[0])
            byted_data = pickle.dumps(pass_emails)
            clientsock.send(byted_data)
            lock.release()







# main
SMTP_PORT = 2025
IMAP_PORT = 143
SMTP_IP="172.16.11.211"
IMAP_IP="172.16.11.211"
lock=Lock()
emails=[]
counter=0
IPAddr = gethostbyname(gethostname())
mail_thread = threading.Thread(
    target=localmail.run,
    args=(SMTP_PORT, IMAP_PORT, 8880, 'localmail.mbox')
)

mail_thread.start()

print "waiting for clients"
Host = IPAddr
print Host
Socket_Port= 50008
Buffsize = 1024 * 9
Addr = (Host, Socket_Port)
servsock = socket(AF_INET, SOCK_STREAM)
#servsock.settimeout(10)
'''https://www.example-code.com/python/ssl_server.asp'''
wrappedSocketServer = ssl.wrap_socket(servsock, ssl_version=ssl.PROTOCOL_TLSv1,server_side=True,certfile="cert.pem",keyfile="cert.pem")
wrappedSocketServer.load_cert_chain(certfile="cert.pem", keyfile="cert.pem")
cipher = ['DHE-RSA-AES128-SHA', 'DHE-RSA-AES256-SHA', 'ECDHE-ECDSA-AES128-GCM-SHA256']
wrappedSocketServer.set_ciphers(cipher)
wrappedSocketServer.bind(Addr)
wrappedSocketServer.listen(3)

while True:
    print "Im waiting for connection..."
    clientsock, addr = wrappedSocketServer.accept()
    print "yay! connected from: ", addr
    thread.start_new_thread(handler, (clientsock, addr, emails))

wrappedSocketServer.close()




#localmail.shutdown_thread(thread)
#print "shutdown localmail"