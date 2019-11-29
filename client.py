import pprint
import imaplib
import mailbox
import email.utils
import threading
import localmail
import smtplib
import socket
import redis
from email.mime.text import MIMEText

def smtp_mail(txt,subject,dst,rs):
    for x in range(1,2):
        t=False
        redis_user=rs.get(x)
        if(redis_user==IPAddr):
            t=True

    if(t==False):
        return
    msg = MIMEText(txt)
    msg['To'] = email.utils.formataddr(('Recipient-', dst))
    msg['From'] = email.utils.formataddr(('Author-', IPAddr))
    msg['Subject'] = subject

    server = smtplib.SMTP(SMTP_IP, SMTP_PORT)
    server.login('user', 'password')
    server.set_debuglevel(True)  # show communication with the server
    try:
        server.sendmail(IPAddr, dst, msg.as_string())
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


SMTP_PORT = 2025
IMAP_PORT = 143
SMTP_IP="172.16.10.157"
IMAP_IP="172.16.10.157"
rs = redis.Redis(host='localhost', port=6379, db=0)
rs.set('1','172.16.10.184')
rs.set('2','172.16.10.154')
IPAddr = socket.gethostbyname( socket.gethostname())
while(True):
    print "-------------------------------"
    check=raw_input("hello client welcome to my server if u want to send mail click S and if you want to check out your mails click F: ")
    if check=="S":
        txt= raw_input("enter the txt you wanna send: ")
        subject= raw_input("enter the subject of your data: ")
        dst= raw_input("enter the ip of your dst client: ")
        smtp_mail(txt, subject, dst,rs)
    if check=="F":
        fetch_mail_msg()
        print "thank you"



