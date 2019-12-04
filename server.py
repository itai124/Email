import email.utils
import threading
import localmail
from socket import *
import pprint
import imaplib
import mailbox
import email.utils
import smtplib
import redis
import pickle
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

def fetch_mail_msg():
    imap = imaplib.IMAP4(IMAP_IP,IMAP_PORT)
    imap.login('username', 'password')
    imap.select('Inbox')
    tmp, data = imap.search(None, 'ALL')
    for num in data[0].split():
            print "------"
            tmp, data = imap.fetch(num, '(RFC822)')
            print  data
            if tmp != 'OK':
                print "ERROR getting message", num
            print('Message: {0}\n'.format(num))
            pprint.pprint(data[0][1])
    imap.close()


def handler(clientsock,addr):
    while True:
        data = clientsock.recv(Buffsize)
        fixed_data=pickle.loads(data)
        print fixed_data
        if not data:
            break
        if(fixed_data[0]=="S"):
            smtp_mail(fixed_data[3],fixed_data[2],fixed_data[1],addr[0])
            clientsock.send("sent your mail")
        elif(fixed_data[0]=="F"):
            fetch_mail_msg()







# main
SMTP_PORT = 2025
IMAP_PORT = 143
SMTP_IP="172.16.10.157"
IMAP_IP="172.16.10.157"


counter=0
IPAddr = gethostbyname(gethostname())
thread = threading.Thread(
    target=localmail.run,
    args=(SMTP_PORT, IMAP_PORT, 8880, 'localmail.mbox')
)
thread.start()
print "waiting for clients"
Host = 'localhost'
Socket_Port= 50000
Buffsize = 1024 * 9
Addr = (Host, Socket_Port)
servsock = socket(AF_INET, SOCK_STREAM)
servsock.bind(Addr)
servsock.listen(5)

while True:
    print "Im waiting for connection..."
    clientsock, addr = servsock.accept()
    print "yay! connected from: ", addr
    # setting thread and handler for each client
    thread.start_new_thread(handler, (clientsock, addr))

servsock.close()




#localmail.shutdown_thread(thread)
#print "shutdown localmail"